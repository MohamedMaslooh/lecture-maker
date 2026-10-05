# -*- coding: utf-8 -*-
"""Make the folders for a new lecture (and, the first time, for the series).

    python new_lecture.py <series-folder>                                  (Day 0: the series only)
    python new_lecture.py <series-folder> <lecture-slug> --title "Why is the sky blue?"   (after the go)

Creates, without overwriting anything that already exists:
    <series>/house-rules.md             the speaker's standing rules (starts from the house rules; every
                                        correction the speaker makes is added here as a new rule)
    <series>/design-system/theme.css    the look of the series: the house look unless the speaker changed it on Day 0
    <series>/<slug>/lecture.json        title, output file name, path to the theme
    <series>/<slug>/trail.md            the story of this lecture and every correction, newest at the bottom
    <series>/<slug>/outline.md          slide by slide, agreed in chat before any slide is built
    <series>/<slug>/sources.md          every claim, its source, and its bin (true / attributed / dropped)
    <series>/<slug>/source/slides/01-title.html, css/, js/
    <series>/<slug>/assets/img/
"""
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import os, sys, json, shutil, re

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(os.path.dirname(HERE), 'assets')


def arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


if len(sys.argv) < 2 or sys.argv[1].startswith('--'):
    sys.exit(__doc__)
series = os.path.abspath(sys.argv[1])
slug = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
if slug and not re.match(r'^[a-z0-9][a-z0-9-]*$', slug):
    sys.exit('new_lecture.py: the slug is lower case words joined by hyphens, e.g. why-is-the-sky-blue')
title = arg('--title', (slug or '').replace('-', ' ').capitalize())
lec = os.path.join(series, slug) if slug else None
made = []


def put(dst, src=None, text=None):
    if os.path.exists(dst):
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if src:
        shutil.copyfile(src, dst)
    else:
        open(dst, 'w', encoding='utf-8', newline='\n').write(text)
    made.append(os.path.relpath(dst, series))


put(os.path.join(series, 'house-rules.md'), os.path.join(A, 'project', 'house-rules.md'))
put(os.path.join(series, 'design-system', 'theme.css'), os.path.join(A, 'design-system', 'theme.css'))
if not slug:
    print('series :', series)
    print('made   :', ', '.join(made) if made else 'nothing new (everything was already there)')
    sys.exit(0)
put(os.path.join(lec, 'lecture.json'), text=json.dumps(
    {'title': title, 'file': slug, 'theme': '../design-system/theme.css'}, indent=2) + '\n')
for name in ('trail.md', 'outline.md', 'sources.md'):
    t = open(os.path.join(A, 'project', name), encoding='utf-8').read().replace('{{TITLE}}', title)
    put(os.path.join(lec, name), text=t)
put(os.path.join(lec, 'source', 'slides', '01-title.html'), text='''<section class="slide s01 center" data-s="s01">
  <div class="kick">{kick}</div>
  <h1>{title}</h1>
  <div class="pnum"></div>
</section>
'''.format(kick='Speaker name &nbsp;·&nbsp; date', title=title.replace('<', '&lt;')))
put(os.path.join(lec, 'source', 'css', '01-title.css'), text='/* slide 01: every selector starts with .s01 */\n')
os.makedirs(os.path.join(lec, 'source', 'js'), exist_ok=True)
os.makedirs(os.path.join(lec, 'assets', 'img'), exist_ok=True)

print('series :', series)
print('lecture:', lec)
print('made   :', ', '.join(made) if made else 'nothing new (everything was already there)')
