# Building the deck

The finished deck is one HTML file made by `scripts/build.py` from a lecture folder. Never edit the
built file by hand; build.py overwrites it. The engine is the animated-html-deck engine
(`assets/engine/deck-template.html`): nobody edits it.

## The folders

```
<series>/
  house-rules.md                 the speaker's rules (grows with every correction)
  design-system/theme.css        the approved look (Day 0). Lead only.
  design-system/design-system.html   the approval sheet (build.py --sheet)
  <lecture>/
    lecture.json                 {"title": "...", "file": "<slug>", "theme": "../design-system/theme.css"}
    trail.md  outline.md  sources.md
    source/slides/NN-name.html   ONE <section> per file. Owned by that slide's builder.
    source/css/NN-name.css       that slide's CSS. Same owner.
    source/js/NN-name.js         optional scene for that slide. Same owner.
    assets/img/                  pictures, I<id>-what.jpg
    <slug>.html                  the deck (built)
```

Make it with `python scripts/new_lecture.py <series> <slug> --title "..."`.

## Commands

```
python scripts/build.py <lecture>                                # the whole deck
python scripts/build.py <lecture> --only 03-05 --out <scratch>/p.html   # a range, as a preview
python scripts/build.py <lecture> --sheet                        # the design-system sheet
python scripts/check_deck.py <lecture>/<slug>.html               # one file? em dashes? layouts?
python scripts/shoot.py <deck.html> <outdir> [--from 3 --to 5]   # a PNG of every click (Playwright)
```

Partial builds always need `--out`, so the real deck is never overwritten by a subset.

## A slide

```html
<section class="slide s04" data-s="s04" data-topic="Sunset">
  <div class="kick">Same sun, same air, longer road</div>
  <h2>Why are sunsets <em>red?</em></h2>
  ... the visual ...
  <div class="cite">NASA Space Place, "Why Is the Sky Blue?" · checked 5 Oct 2026 · <a href="https://...">link</a></div>
  <div class="pnum"></div>
</section>
```

- `class="slide sNN"` and `data-s="sNN"` with the file's number. Optional extras on the section:
  `top`, `center`, `dark`, `pad0` (no padding, for full-bleed pictures).
- `data-topic="..."`: the slide's topic for the strip along the top. Slides with no topic (title,
  close) have no strip. Topics appear in the strip in the order of their first slide.
- One `.kick` (small line above the title), one plain title: `h1` on the title slide, `h2` (`.sm`,
  `.big`) elsewhere, with one lit word in `<em>` (`<em class="wa">` for the second colour).
- `<div class="cite">` is the last element before `<div class="pnum"></div>`. Keep the pnum exactly.
- Every class you invent starts with `sNN-`, and every selector in your CSS starts with `.sNN`.
- No notes, comments meant for the room, narration, or labels that tell the room nothing.

## Beats (clicks)

- The engine counts `data-step="1"`, `"2"` … on any element; each number is one click.
  `.r` fades in place (space reserved: use for rows and grids), `.new` takes no room until it
  arrives so the rest moves over (use for stacking), `.rise`, `.grow`, `.wipe`, `.side`, `.strk`.
  Full list and timings: `deck-engine/motion.md`.
- **One click per group:** put `class="grp" data-step="1"` on the group; its children fade up
  together, staggered.
- **Past steps shrink:** `data-shrink-at="2"` with `--shrink:.55; --origin:left top; --sx/--sy`
  on the element. **Replace in place:** `data-out="2"` on the old thing, `class="r" data-step="2"`
  on the new one, in the same grid cell (`data-gone="2"` also stops it being clicked or hovered).
  The example's slide 4 shows a real photo that shrinks aside on click 1. If the last beat is only a shrink or an out, add
  `<i data-step="N" hidden></i>`.
- Every slide gets `.b1 .b2 …` and `data-beat` as you click, so slide CSS can say
  `.s04.b1 .s04-ray{…}`.
- Never put a state transform on a **direct child** of the section (the entrance cascade pins it):
  wrap it in a div.
- JavaScript only if CSS cannot do it: `LM.scene('s05', (slide, step) => { … })` in `source/js/05-*.js`.
  It must draw the state of `step` whichever way you arrived. No loops, no timers that outlive the slide.

## Parts from the engine and the kit

Engine (see `deck-engine/*.md`): `.split/.words/.art`, `.cols`, `.card`, `.quote`, `.stat` with
`data-count`, `.bars/.bar/.bf` (`.bf.out` for a short bar's label outside it), `.lc` + `path.draw`,
`.steps/.stp`, `.win/.wbar/.wbody` (a drawn window), `.term`, `.hero` (full-bleed picture),
`.duo` with `data-act1` (centred, then makes room).

Kit (`assets/kit/lecture-kit.css`): topic strip, one-line sources with hover, tags
(`<span class="tag ours">our calculation</span>`, `.mine` my experience, `.self` their own test,
`.plan` a plan name, plain `.tag` estimate), `.grp`, shrink and out, `.frame` + `.caption` for real
pictures (`.frame.contain` to show all of it, `.frame.bare` for no border).

## The slide navigator

build.py puts it in every deck (`assets/kit/deck-nav.css|js`, the same navigator as the lecture
site, maslooh.com; it replaces the engine's older built-in copy). It is hidden during the talk:
move the mouse to the right edge and a ladder of ticks appears (one per slide); hover it and a panel
of slide thumbnails slides in; hover a thumbnail to see it large; click one to jump to that slide at
its first beat. **G** opens it and keeps it open (G, Esc or a click outside closes it); while open,
Up/Down and a typed number plus Enter also jump. On a tablet, a touch shows the ladder. The
thumbnails are copies of the slides themselves, made in the page, so they work offline and need no
pictures of their own. Nothing to add per slide; it only needs every slide to be a
`<section class="slide">` (build.py does that).

## Pictures

`<img src="@@IMG:I03-prism.jpg@@" alt="...">` with the file in `assets/img/`. build.py inlines it.

## Before handing back (every builder, then the reviewer)

Look at every screenshot (1920x1080, one per click) and fix: text overflow or too small to read
from the back, a void under the content, edges that do not line up, a box much bigger than its
words, anything that cuts or pops, two neighbouring slides with the same layout, console errors,
build warnings, em dashes, dot pills, numbers far bigger than the title. The example in
`examples/why-is-the-sky-blue/` is the quality floor.
