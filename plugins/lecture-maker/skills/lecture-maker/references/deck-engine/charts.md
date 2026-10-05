# Charts

Every chart is drawn in the slide, in the deck's own colours, and animates once when it is
revealed. No screenshots, no chart libraries, no images of graphs.

## The rules before the markup

- **One chart answers one question.** If the reader has to work out what to look at, the
  chart is doing two jobs.
- **Direct labels.** Put the value on the mark it belongs to. Never a number on every point,
  never a table of numbers under the chart.
- **A legend whenever there are two or more series**, above the chart, not floating beside it.
- **Two series, two colours that survive a bad projector**: `--accent` and `--warm` in the
  template are far enough apart in hue and in lightness that they still read in greyscale
  and for a colour-blind viewer. If you add a third series, check the same two things.
- **The axis carries the two ends, not every tick.** 1950 and 2026, not eight years.
- **Every chart carries its source and date** in `.cnote` or the slide's `.cite` line, with
  a link where one exists.
- **Never invent a number.** If you cannot cite it, the chart does not go in. If a figure is
  there to show a shape rather than a measurement, say so on the slide.

## Bars, for a comparison

```html
<div class="chart">
  <div class="ct">What each of them scored</div>
  <div class="cs">One line saying what to look at.</div>
  <div class="leg"><span><i></i>The machine</span><span><i class="w"></i>The people</span></div>
  <div class="bars">
    <div class="bar"><div class="bl">The machine</div>
      <div class="bt"><div class="bf" style="--w:86%">86%</div></div></div>
    <div class="bar w"><div class="bl">The people<small>five of them</small></div>
      <div class="bt"><div class="bf" style="--w:64%">64%</div></div></div>
  </div>
  <div class="cnote">Author, journal, year. <a href="…">link</a></div>
</div>
```

`--w` is the length. `.bar.w` colours that row warm. The bars grow from zero when the
slide opens, or when the step that holds them is revealed. If a value is small, put
`class="bf out"` on the fill so the label sits outside the bar instead of inside it.
Set `--lw` on `.bar` to widen the label column.

## A line, for a change over time

```html
<svg class="lc" viewBox="0 0 560 300" preserveAspectRatio="xMidYMid meet">
  <line class="grid" x1="46" y1="40"  x2="540" y2="40"/>
  <line class="axis" x1="46" y1="255" x2="540" y2="255"/>
  <path class="draw" d="M56,244 C…" fill="none" stroke="var(--accent)"
        stroke-width="3.2" stroke-linecap="round"/>
  <circle class="dot" cx="528" cy="36" r="5.5" fill="var(--accent)"/>
  <text class="lab" x="470" y="24" fill="var(--accent)">today</text>
  <text x="46" y="278">1950</text><text x="500" y="278">2026</text>
</svg>
```

`class="draw"` makes the path draw itself once. The engine measures the path and sets the
dash length itself, so you never hardcode one. `class="dot"` on the end marker fades in
after the line arrives. Two lines on one chart is the maximum.

## Nested sets, for one thing inside another

```html
<div class="rings">
  <div class="ring r1" data-step="1">The whole field</div>
  <div class="ring r2" data-step="2">A part of it</div>
  <div class="ring r3" data-step="3">A part of that</div>
  <div class="ring r4" data-step="4">The bit<br>they know</div>
</div>
```

Outermost first, one click each, ending on the small solid one, which is usually the thing
the room already had a name for. Four rings is the limit.

Labels only. A caption line under each ring title crowds the figure and makes it look
strange. If the innermost ring needs its families (for example LLM, images, video, audio
inside generative AI), put them in as small chips on their own click. Give the circles the
slide to themselves while you explain them; if a list follows, move the diagram aside with
the step-aside pattern in `motion.md` rather than starting a new slide.

## Stages, for a sequence

```html
<div class="steps">
  <div class="stp" data-step="1"><b>First</b><span>one line</span></div>
  <div class="stp" data-step="2"><b>Second</b><span>one line</span></div>
</div>
```

Each lights as you reach it and stays lit. Nothing goes dark behind you. Four is the limit
before the text is too small to read from the back of the room.

## One big number

```html
<div class="stat">
  <b data-count="1000000" data-comma>0</b>
  <div class="lab">people, in five days</div>
</div>
```

`data-count` is the target, `data-comma` groups the thousands, `data-suf="%"` adds a small
suffix, `data-dec="1"` keeps one decimal. It counts once, over about a second, then stops.
Pair it with the two act stage: the number lands alone, then the sentence explaining why it
is big arrives beside it. Let the count finish before speaking.

## Number tiles

A row of big numbers is the deck's main voice when a slide is about money or scale. Two
rows at most, the first with two wide tiles and the second with three. Each tile holds a
number, a unit in small type, and one short label saying what it counts; nothing else. The
company's logo sits in the tile's empty corner (see `visuals.md`). Every tile in a row
arrives with `.r`, so the row never resizes.

## Diagrams in general

- No node, pill or label may sit on top of the line or ring it belongs to.
- The diagram and whatever sits beside it are balanced: no void under the diagram, no list
  squeezed into a narrow column.
- Every label is true for the whole talk. If a recap says "every model we named", check
  that no video or image model was named too.

## What not to do

- Pie charts. Two slices is a sentence, more than two is unreadable from row six.
- 3D anything, drop shadows on data, gradients inside bars.
- A y axis that does not start at zero on a bar chart.
- Gridlines darker than the data.
- More than about six bars on one slide. Group them or split the slide.
