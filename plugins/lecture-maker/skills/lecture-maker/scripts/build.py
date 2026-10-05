# -*- coding: utf-8 -*-
"""Lecture builder: assembles a lecture folder into ONE self-contained HTML file that works offline.

    python build.py <lecture>                      -> <lecture>/<file>.html (the deck)
    python build.py <lecture> --out preview.html   -> a preview copy; the real deck is left alone
    python build.py <lecture> --only 03-05 --out p.html   -> only slides 03 to 05 (lists and ranges mix: 01-02,07)
    python build.py <lecture> --sheet              -> design-system.html next to the theme (Day 0 approval sheet)

<lecture> is a folder made by new_lecture.py:
    lecture.json             {"title": "...", "file": "my-lecture", "theme": "design-system/theme.css"}
    source/slides/NN-name.html   ONE <section class="slide sNN" data-s="sNN"> per file, sorted by number
    source/css/NN-name.css       that slide's CSS (every selector starts with .sNN)
    source/js/NN-name.js         optional scene for that slide: LM.scene('sNN', (slide, step) => {...})
    assets/img/                  pictures, used as @@IMG:file.jpg@@

What goes in, in this order:
    the engine (assets/engine/deck-template.html, the animated-html-deck engine, never edited),
    the series theme (design system), the lecture kit (assets/kit), the slides' CSS, the slides,
    the kit's runtime, the slides' scripts, then the engine's script, then the slide navigator
    (assets/kit/deck-nav.css|js: ticks at the right edge, thumbnails of every slide, click to jump;
    it replaces the engine's older built-in copy, so a deck never carries two).

Tokens a slide may use (replaced at build time, so the output never points at a file):
    @@IMG:<file>@@   assets/img/<file> as a data: URI. Big JPG/PNG are scaled to 1920 px and re-encoded
                     when Pillow is installed (without it they go in at full size).
"""
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import os, re, sys, glob, json, base64, io

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
TEMPLATE = os.path.join(SKILL, 'assets', 'engine', 'deck-template.html')
KIT_CSS = os.path.join(SKILL, 'assets', 'kit', 'lecture-kit.css')
KIT_JS = os.path.join(SKILL, 'assets', 'kit', 'lecture-kit.js')
SHEET = os.path.join(SKILL, 'assets', 'design-system', 'design-sheet.html')
NAV_CSS = os.path.join(SKILL, 'assets', 'kit', 'deck-nav.css')
NAV_JS = os.path.join(SKILL, 'assets', 'kit', 'deck-nav.js')


def read(p):
    return open(p, encoding='utf-8').read()


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


if len(sys.argv) < 2 or sys.argv[1].startswith('--'):
    sys.exit(__doc__)
LEC = os.path.abspath(sys.argv[1])
cfg_path = os.path.join(LEC, 'lecture.json')
if not os.path.exists(cfg_path):
    sys.exit('build.py: no lecture.json in ' + LEC + ' (make the folder with new_lecture.py)')
cfg = json.load(open(cfg_path, encoding='utf-8'))
TITLE = cfg.get('title', 'Lecture')
THEME = os.path.normpath(os.path.join(LEC, cfg.get('theme', 'design-system/theme.css')))
if not os.path.exists(THEME):
    sys.exit('build.py: theme not found: ' + THEME)
SRC = os.path.join(LEC, 'source')
IMG = os.path.join(LEC, 'assets', 'img')
CACHE = os.path.join(LEC, 'assets', '.cache')
sheet_mode = '--sheet' in sys.argv

if arg('--out'):
    OUT = os.path.abspath(arg('--out'))
elif sheet_mode:
    OUT = os.path.join(os.path.dirname(THEME), 'design-system.html')
elif arg('--only'):
    sys.exit('build.py: a partial build needs --out <file>, so the real deck is never overwritten by a subset')
else:
    OUT = os.path.join(LEC, cfg.get('file', 'lecture') + '.html')

# ---------- the engine, split around the slides ----------
tpl = read(TEMPLATE)
# the slide navigator: the kit's version replaces the engine's older built-in copy (the engine file stays untouched)
tpl = re.sub(r'<style id="dnav-css">.*?</style>\n?', '', tpl, count=1, flags=re.S)
tpl = re.sub(r'<script id="dnav-js">.*?</script>\n?', '', tpl, count=1, flags=re.S)
m1 = re.search(r'<!-- ═+ SLIDES START ═+ -->', tpl)
m2 = re.search(r'<!-- ═+ SLIDES END ═+ -->', tpl)
if not (m1 and m2):
    sys.exit('build.py: the engine template has no SLIDES START / SLIDES END markers')
head, tail = tpl[:m1.end()], tpl[m2.start():]
head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % TITLE.replace('<', '&lt;'), head, count=1)
if head.count('</head>') != 1:
    sys.exit('build.py: the engine template changed (no single </head>)')
head = head.replace('</head>', '<style id="lm-theme">\n/* ---- theme: %s ---- */\n%s\n/* ---- lecture kit ---- */\n%s\n</style>\n'
                    '<style id="dnav-css">\n%s\n</style>\n</head>'
                    % (os.path.basename(THEME), read(THEME), read(KIT_CSS), read(NAV_CSS)), 1)
if tail.count('</body>') != 1:
    sys.exit('build.py: the engine template changed (no single </body>)')
tail = tail.replace('</body>', '<script id="dnav-js">\n%s\n</script>\n</body>' % read(NAV_JS), 1)


# ---------- images ----------
MIME = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.gif': 'image/gif',
        '.svg': 'image/svg+xml', '.webp': 'image/webp'}
_cache = {}


def img_uri(name):
    if name in _cache:
        return _cache[name]
    p = os.path.join(IMG, name)
    if not os.path.exists(p):
        sys.exit('build.py: missing picture assets/img/' + name)
    ext = os.path.splitext(name)[1].lower()
    raw, mime = open(p, 'rb').read(), MIME.get(ext, 'application/octet-stream')
    if ext in ('.jpg', '.jpeg', '.png') and len(raw) > 450_000:
        try:
            from PIL import Image
            im = Image.open(io.BytesIO(raw))
            alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
            im.thumbnail((1920, 1920), Image.LANCZOS)
            buf = io.BytesIO()
            if alpha:
                im.save(buf, 'PNG', optimize=True); mime = 'image/png'
            else:
                im.convert('RGB').save(buf, 'JPEG', quality=84, optimize=True, progressive=True); mime = 'image/jpeg'
            raw = buf.getvalue()
        except ImportError:
            print('note: Pillow not installed, %s goes in at full size' % name)
    _cache[name] = 'data:%s;base64,%s' % (mime, base64.b64encode(raw).decode())
    return _cache[name]


def tokens(s):
    return re.sub(r'@@IMG:([^@]+)@@', lambda m: img_uri(m.group(1)), s)


# ---------- which slides ----------
def key(num):
    m = re.match(r'(\d+)([a-z]?)$', num)
    return (int(m.group(1)), m.group(2))


def wanted(num):
    only, skip = arg('--only'), arg('--skip')
    if skip and num in skip.split(','):
        return False
    if not only:
        return True
    n = key(num)[0]
    for part in only.split(','):
        if '-' in part:
            a, b = part.split('-')
            if int(a) <= n <= int(b):
                return True
        elif part and int(re.match(r'\d+', part).group(0)) == n:
            return True
    return False


warnings = []
if sheet_mode:
    content = read(SHEET) + '\n<script>\n' + read(KIT_JS) + '\n</script>\n'
    chosen = ['design sheet']
else:
    files = []
    for f in glob.glob(os.path.join(SRC, 'slides', '*.html')):
        mm = re.match(r'(\d+[a-z]?)-([\w-]+)\.html$', os.path.basename(f))
        if not mm:
            sys.exit('build.py: slide file not named NN-name.html: ' + f)
        files.append((key(mm.group(1)), mm.group(1), f))
    files.sort()
    nums = [x[1] for x in files]
    if len(nums) != len(set(nums)):
        sys.exit('build.py: two slide files share a number')
    chosen = [x for x in files if wanted(x[1])]
    if not chosen:
        sys.exit('build.py: no slides match')
    keep = {x[1] for x in chosen}

    def per_slide(folder, ext):
        out = []
        for f in sorted(glob.glob(os.path.join(SRC, folder, '*.' + ext))):
            mm = re.match(r'(\d+[a-z]?)-', os.path.basename(f))
            if not mm or mm.group(1) in keep or mm.group(1) not in nums:
                out.append(f)
        return out

    body = []
    for _, num, f in chosen:
        src = read(f)
        if len(re.findall(r'<section\b[^>]*class="slide\b', src)) != 1:
            sys.exit('build.py: %s must hold exactly one <section class="slide ...">' % os.path.basename(f))
        tag = re.search(r'<section\b[^>]*>', src).group(0)
        if 'data-s="s%s"' % num not in tag:
            warnings.append('%s: the section should carry data-s="s%s"' % (num, num))
        steps = [int(x) for x in re.findall(r'data-step="(\d+)"', src)]
        later = [int(x) for x in re.findall(r'data-(?:out|gone|shrink-at)="(\d+)"', src)]
        if later and max(later) > max(steps or [0]):
            warnings.append('%s: a beat-%d out/shrink has no data-step="%d" to give it a click (add <i data-step="%d" hidden></i>)'
                            % (num, max(later), max(later), max(later)))
        if '<div class="pnum"></div>' not in src:
            warnings.append('%s: keep <div class="pnum"></div> as the last element (page number)' % num)
        body.append('<!-- ═════════ %s · %s ═════════ -->\n%s' % (num, os.path.basename(f), src.strip()))

    css = '\n'.join('/* ---- %s ---- */\n%s' % (os.path.basename(p), read(p)) for p in per_slide('css', 'css'))
    js = ''.join('\n<script>\n/* ---- %s ---- */\n%s\n</script>' % (os.path.basename(p), read(p)) for p in per_slide('js', 'js'))
    content = ('\n<style>\n' + css + '\n</style>\n\n' + '\n\n'.join(body) +
               '\n<script>\n/* ---- lecture kit ---- */\n' + read(KIT_JS) + '\n</script>' + js + '\n')


content = tokens(content)


# every source link opens in its own tab
def newtab(m):
    return re.sub(r'<a href="(https?://[^"]+)"(?![^>]*\btarget=)', r'<a href="\1" target="_blank" rel="noopener"', m.group(0))


content = re.sub(r'<div class="cite(?: [^"]*)?"[^>]*>.*?</div>', newtab, content, flags=re.S)
out = head + '\n' + content + tail
if '\u2014' in content:
    warnings.append('em dash in the slides (house style: none)')
if '•' in content or '●' in content:
    warnings.append('a bullet character in the slides: check it is not a dot pill')
left = set(re.findall(r'@@[A-Z]+:[^@]*@@', out))
if left:
    warnings.append('leftover tokens: %s' % left)

os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
open(OUT, 'w', encoding='utf-8', newline='\n').write(out)
print('wrote', OUT)
print('slides', len(chosen), ':', ' '.join(c if isinstance(c, str) else c[1] for c in chosen))
print('size %.2f MB' % (len(out.encode('utf-8')) / 1e6))
for w in warnings:
    print('WARNING', w)
