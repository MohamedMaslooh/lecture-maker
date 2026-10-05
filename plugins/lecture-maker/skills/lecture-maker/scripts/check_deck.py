# -*- coding: utf-8 -*-
"""Quick checks on a built deck that need no browser.

    python check_deck.py <deck.html>

Checks: one file (no picture, script or style pointing at a file or the internet), no leftover @@ tokens,
no em dashes, no bullet characters (possible dot pills), every slide has a page number, every
<section> carries data-s, sources are one-liners, neighbouring slides do not share the same layout,
and it prints slides, clicks and size. Exit code 1 if something must be fixed.
A browser check (shoot.py, or opening the file) is still needed for overflow and motion.
"""
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import re, sys, html

if len(sys.argv) < 2:
    sys.exit(__doc__)
doc = open(sys.argv[1], encoding='utf-8').read()
m1 = doc.find('SLIDES START')
m2 = doc.find('SLIDES END')
content = doc[m1:m2] if m1 > 0 and m2 > m1 else doc
must, should = [], []

for m in re.finditer(r'<(img|script|link|source|video|iframe)\b[^>]*\b(src|href)="([^"]+)"', content):
    url = m.group(3)
    if not url.startswith(('data:', '#')):
        must.append('<%s %s="%s"> points outside the file: inline it (inline-images.py or @@IMG@@)' % (m.group(1), m.group(2), url[:60]))
for m in re.finditer(r'url\(\s*[\'"]?((?!data:|#)[^\'")]+)', content):
    must.append('url(%s) points outside the file' % m.group(1)[:60])
if re.search(r'@@[A-Z]+:[^@]*@@', doc):
    must.append('leftover @@ tokens: build with build.py')
text_only = re.sub(r'<(script|style)\b.*?</\1>', '', content, flags=re.S)
if '\u2014' in text_only:
    must.append('%d em dash(es) on the slides' % text_only.count('\u2014'))
if re.search('[•●◦]', text_only):
    should.append('a bullet character on a slide: make sure it is not a dot beside text in a pill')

secs = list(re.finditer(r'<section\b([^>]*)>(.*?)</section>', content, flags=re.S))
clicks, shapes = 0, []
for k, m in enumerate(secs, 1):
    attrs, body = m.group(1), m.group(2)
    sid = (re.search(r'data-s="([^"]+)"', attrs) or [None, 's?%d' % k])[1]
    if 'data-s=' not in attrs:
        should.append('slide %d: no data-s (scenes and beat classes need it)' % k)
    if 'class="pnum"' not in body:
        should.append('%s: no page number (<div class="pnum"></div>)' % sid)
    steps = [int(x) for x in re.findall(r'data-step="(\d+)"', body)]
    act = re.search(r'data-act1="(\d+)"', attrs)
    clicks += max(steps + ([int(act.group(1))] if act else []) or [0])
    for c in re.findall(r'<div class="cite[^"]*"[^>]*>(.*?)</div>', body, flags=re.S):
        words = len(html.unescape(re.sub(r'<[^>]+>', ' ', c)).split())
        if words > 60:
            should.append('%s: the source line has %d words; keep the visible part to one line (hover shows the rest)' % (sid, words))
    # layout signature: the classes of the slide's first big block after the title
    blocks = re.findall(r'^\s{2}<div class="([^"]+)"', body, flags=re.M)
    sig = ' '.join(b.split()[0] for b in blocks if b.split()[0] not in ('kick', 'cite', 'pnum', 'say'))[:40]
    shapes.append((sid, sig))
for (a, sa), (b, sb) in zip(shapes, shapes[1:]):
    if sa and sa == sb:
        should.append('%s and %s look like the same layout (%s): vary the shape' % (a, b, sa))

print('%s: %d slides, %d clicks, %.2f MB' % (sys.argv[1], len(secs), clicks, len(doc.encode('utf-8')) / 1e6))
for x in must:
    print('MUST FIX  ', x)
for x in should:
    print('CHECK     ', x)
if not must and not should:
    print('all checks passed')
sys.exit(1 if must else 0)
