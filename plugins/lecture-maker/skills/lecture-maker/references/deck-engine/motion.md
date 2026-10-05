# Motion

Everything here is already in `assets/deck-template.html`. This file is the explanation,
so you know which class to reach for and why.

## How a slide is built

```html
<section class="slide">          <!-- one slide -->
  <div class="kick">1966 · the first chatbot</div>
  <h2>ELIZA had no idea<br>what you were <em>saying.</em></h2>
  <p class="say new" data-step="1">One line, on the first click.</p>
  <div class="cite">Weizenbaum, CACM 9(1), January 1966.</div>
  <div class="pnum"></div>
</section>
```

`data-step="1"` is the first click, `data-step="2"` the second, and so on. Anything without
a `data-step` is on the screen the moment the slide opens. The engine counts the beats per
slide by itself; you never write a total anywhere.

## The reveals

| class | what it does | when to use it |
|---|---|---|
| `r` | fades and rises into space already reserved, so nothing else moves | **the default for any row or grid of cards**: numbers, posts, price tags, quotes side by side. Also a caption under a fixed picture |
| `new` | takes up no room until it arrives, so everything else moves over | content that stacks, or a fixed-width card arriving beside another fixed-width card. This is the morph |
| `rise` | the same, from 30px | a heavier arrival, one per slide at most |
| `grow` | scales up from 92% | a shape, a ring, a badge. Not text |
| `wipe` | uncovers left to right | a quotation, a headline on a document, a title being written |
| `side` | comes in from the right | a list item that must not push the others |
| `strk` | draws a line through the word | an idea being cancelled in front of the room |

Add the class and a `data-step`, and that is the whole mechanism:

```html
<div class="pt new" data-step="2">…</div>
<span class="strk" data-step="1">written out by hand</span>
```

## An arrival never resizes what is already there

This is the rule people get wrong, and it is what separates a deck that looks
deliberate from one that looks like a template filling itself in.

When something arrives on a slide, everything already on screen may **move**. Nothing may
**grow or shrink**. A card that will be one of three is the width of one of three from the
moment it appears, so the first card slides left when the second arrives instead of
collapsing from full width down to a third. In practice that means:

- Cards in a row are a fixed width (`.card` already is), never `flex:1`, if they arrive with
  `.new`. Set `--cw` on a card if you need a different width.
- A row of flexible cards (`flex:1`, which is what a number row or a row of posts usually
  is) must never use `.new`. With `.new` the first card starts full width and shrinks as
  each neighbour arrives, and the room sees it as a cut that slices the card in half. Give
  every card in the row `class="r"` so its space is reserved from the start and it fades up
  in place.
- A lone box stretched across the whole board is dead space with a border around it. If one
  card is alone on screen for a beat, it sits at its own width, centred.
- The same goes for the two act stage: `duo-a` never resizes when `duo-b` arrives, it only
  slides over.
- Text blocks get a `max-width` so a paragraph does not reflow when something appears
  beside it.

## The morph, in one paragraph

Before every click the engine measures every block on the slide, changes what is shown,
measures again, and plays the difference back as one movement. So when a second card
arrives, the first card **travels** to its new position over 640ms rather than appearing
somewhere else. Nested blocks travel by the difference only, so a caption inside a moving
card is never carried twice. You get this for free by using `.new`. You lose it if you
reveal something with `.r` inside a fixed-height box, because then nothing had to move.

## The two act stage

For a slide where you say the sentence first and show the evidence second:

```html
<section class="slide" data-act1="1">
  <div class="duo">
    <div class="duo-a"> the sentence, centred on the board </div>
    <div class="duo-b"> the chart, the number, the picture </div>
  </div>
</section>
```

On the click, `duo-a` slides left and `duo-b` arrives beside it. Use it when the claim
should land on its own before the proof shows up. Two or three of these in a deck, no more.

## Timings

Do not change these. They are the reason two decks made a year apart feel like the same
deck.

| | |
|---|---|
| easing, everything | `cubic-bezier(.2,.9,.25,1)` |
| slide change | 420ms fade, 620ms drift |
| the morph | 640ms |
| a reveal | 500 to 680ms |
| a wipe | 750ms |
| a bar growing | 950ms |
| a line drawing itself | 1250ms |
| a number counting | 1100ms |

## Never

- A transition between slides other than the built-in one. No flip, no cube, no push, no
  zoom, no page curl.
- Anything that loops while the speaker is talking. Everything plays once and stops.
- Text animating letter by letter, unless the point of the slide is that something is being
  typed.
- Two things moving at once.
- A beat that reveals a whole finished slide in one go. That is not a beat, that is a cut
  with extra steps.
- Anything that grows or shrinks because something else arrived.
- `.new` on a card in a row of flexible cards. Use `.r`.
- Motion on a chapter cover. It is a breath, not an event.
- More than five beats on a slide. Split it.

## Keys, for the person presenting

Click, `→`, or space moves on. Click the left quarter of the board, `←`, or backspace goes
back. `F` is full screen. `Home` and `End` jump to the ends. On a phone, tap right or swipe.

## Replace in place

When the next click answers what is already on screen, the answer takes its place instead
of getting a new slide. Five spending figures arrive one by one, then on the next click they
fade out and the quote that explains them fades in, in exactly the same area. Stepping back
brings the figures back.

The engine toggles `.show` on every `[data-step]` whose step is at or below the current one,
so this needs no script. Put both layers in one grid cell, the replacing layer first in the
markup, and hide the old layer with a sibling selector:

```html
<div class="swapstage">
  <div class="swapb r" data-step="6"> the quote that explains the numbers </div>
  <div class="swapa"> the numbers, each with its own data-step 1 to 5 </div>
</div>
```

```css
.swapstage{display:grid}
.swapstage > .swapa, .swapstage > .swapb{grid-area:1/1}
.swapa{transition:opacity .55s var(--e),transform .6s var(--e)}
.swapb{z-index:2;align-self:center}
.swapb.show + .swapa{opacity:0;transform:translateY(-12px) scale(.985);pointer-events:none}
```

The same idea moves a diagram aside. The circles sit alone in the middle while you explain
them, then the list arrives on the right and the diagram shrinks and slides left:

```css
.stage{position:relative;height:470px}
.stage .diagram{position:absolute;left:50%;width:500px;transform:translateX(-50%);
  transition:left .85s var(--e),transform .85s var(--e),width .85s var(--e)}
.stage .list{position:absolute;left:430px;right:0;opacity:0;transform:translateX(28px);
  transition:opacity .6s var(--e) .28s,transform .7s var(--e) .28s}
.stage .list.show{opacity:1;transform:none}
.stage .list.show ~ .diagram{left:0;transform:none;width:392px}
```

Put the list before the diagram in the markup so the `~` selector can reach it. Always step
forwards and back through a replacement before delivering.
