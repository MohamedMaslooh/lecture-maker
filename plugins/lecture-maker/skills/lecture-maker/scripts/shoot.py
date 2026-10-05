# -*- coding: utf-8 -*-
"""Screenshot every beat of a built deck, forwards, in a real browser (Playwright). Optional:
use it where Python can drive a browser (your own computer, Claude Code). Elsewhere, open the
file and click through it yourself.

    python shoot.py <deck.html> <outdir> [--from 2] [--to 5] [--settle 1600] [--width 1920]
        -> <outdir>/s02-b0.png, s02-b1.png ... and the console errors, if any

--from/--to are slide positions in the built file. --settle: ms to wait after each click (moves take
~0.7 s; raise it for long staggers or count-ups).
Needs: pip install playwright. Uses the installed Chrome (channel='chrome'); if that fails it tries
Playwright's own Chromium (python -m playwright install chromium).
"""
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import sys, os, pathlib


def arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


if len(sys.argv) < 3:
    sys.exit(__doc__)
html, out = sys.argv[1], sys.argv[2]
a, b = int(arg('--from', 1)), int(arg('--to', 999))
settle = int(arg('--settle', 1600))
w = int(arg('--width', 1920))
os.makedirs(out, exist_ok=True)

from playwright.sync_api import sync_playwright
STATE = """(()=>{const ss=[...document.querySelectorAll('#deck .slide')];const k=ss.findIndex(s=>s.classList.contains('on'));
const s=ss[k];return [k+1,+(s.dataset.beat||0),Math.max(0,...[...s.querySelectorAll('[data-step]')].map(e=>+e.dataset.step||0),+(s.dataset.act1||0)),ss.length]})()"""
with sync_playwright() as p:
    try:
        br = p.chromium.launch(channel='chrome')
    except Exception:
        br = p.chromium.launch()
    pg = br.new_page(viewport={'width': w, 'height': round(w * 9 / 16)})
    errs = []
    pg.on('console', lambda m: errs.append(m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    pg.goto(pathlib.Path(html).resolve().as_uri())
    pg.mouse.move(1, 1)
    pg.wait_for_timeout(6500)            # fonts, and the help / full-screen chrome fade out
    shots = 0
    for _ in range(800):
        idx, beat, top, total = pg.evaluate(STATE)
        if idx > b:
            break
        if idx >= a:
            pg.wait_for_timeout(settle)
            pg.screenshot(path=os.path.join(out, 's%02d-b%d.png' % (idx, beat)))
            shots += 1
        if idx == total and beat >= top:
            break
        pg.keyboard.press('ArrowRight')
        pg.wait_for_timeout(80)
    print('%d screenshots in %s' % (shots, out))
    print('\n'.join(errs) or 'console clean')
    br.close()
