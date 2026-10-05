# Pictures

Three kinds of picture earn a place in a deck like this: a real photograph when the
photograph is the evidence, a drawn interface when you are showing how something behaves,
and a full bleed image on a chapter cover. Everything else is decoration and makes the
deck look like a template.

## Drawn, not screenshotted

Draw the thing in the slide. It stays sharp on any projector, it takes the deck's own
colours, it weighs nothing, and you can reveal one part of it on its own click. A
screenshot cannot do any of that.

A window:

```html
<div class="win">
  <div class="wbar"><i></i><i></i><i></i><span>what this window is</span></div>
  <div class="wbody">
    <div class="line w90"></div><div class="line w70"></div>
    <div class="r" data-step="1">the line that answers, on its own click</div>
  </div>
</div>
```

A terminal, for anything that was typed:

```html
<div class="term">
  <span class="u">&gt; what the person typed</span><br>
  the machine's answer<span class="caret"></span>
</div>
```

`.line` bars stand in for text you do not want anyone reading. `.w90`, `.w80`, `.w70`,
`.w60`, `.w40` set the widths. Vary them or it looks like a barcode.

A sheet of paper, a phone, a machine, a door, a chessboard: all of these are a handful of
divs with a border radius. Build the one the story needs. Keep it to flat shapes, one or
two colours from the theme, and no more detail than the point requires.

## Photographs

Use one when the photograph itself is the fact: the person who did the thing, the room it
happened in, the four pictures you are asking the room to name. Not as a mood image behind
a heading.

```html
<div class="shot">
  <img src="img/whoever.jpg" alt="">
  <div class="cap">Who or what this is, and the year.</div>
</div>
```

A row of four, named after the room has guessed:

```html
<div class="figs">
  <div class="fig"><div class="ph"><img src="img/first.jpg" alt=""></div>
    <b class="r" data-step="1">Its name</b><span class="r" data-step="1">what it is</span></div>
  …
</div>
```

## Getting the pictures into a single file

The deck is one file, so every picture ends up as a `data:` URI inside it. Do not write
base64 by hand and do not paste it into the slides while you work. The way round it:

1. **Get the photographs.** Ask the person for them, or use the ones they attached to the
   conversation. If they have none, say so and offer to draw the thing instead, or leave
   the chapter cover as a plain dark slide. Never go and take pictures off the web without
   checking what you are allowed to use, and never present a stock photograph as if it were
   the real thing being discussed.
2. **Put them in a folder beside the deck**, `img/`, and point at them normally while you
   build: `<img src="img/dartmouth.jpg" alt="">`.
3. **Fold them in at the end**, once:

   ```bash
   python3 scripts/inline-images.py yourdeck.html
   ```

   Every local `src` and every `url(…)` is resized, re-encoded and replaced with a data
   URI, in place. `--max-width` defaults to 1600, which is more than a 1280 wide board ever
   needs, and `--quality` defaults to 78. It prints the size of every picture and the size
   of the finished file, and it fails loudly if a picture is missing.
4. **Check the deck opens with the `img/` folder moved away.** If anything is still
   pointing at a file on disk, it will be blank in the lecture hall.

Sizes worth knowing: a full bleed cover wants about 1600px wide, a picture in the art
column about 900px, a tile in a row of four about 420px. Keep the whole deck under about
15MB. Six or seven good photographs fit in that easily, and if it is getting heavy the
pictures are too large rather than too many.

Say where each photograph came from in the `.cite` line, and only use images you are
allowed to use.

## Chapter covers

A dark slide with a photograph behind it at the start of each chapter. The photograph is a
real generated image (Gemini's image model works well for this), never hand-drawn SVG art,
which reads as cheap on a projector. Describe a cinematic, dark, 16:9 scene with empty
space on the left third for the title, and no text, letters or logos in the image. The
title slide follows the series house style every time, with its own photograph.

Chapters are marked by these covers. Do not also run a progress bar or timeline across the
top of every slide; keep that only for a talk that is one chronological story. Do not add a
cover that restates the title slide.

```html
<section class="slide dark pad0">
  <div class="hero"><img src="img/chapter-two.jpg" alt=""></div>
  <div class="hx">
    <div class="kick">Chapter two</div>
    <h2 class="big">The line that names<br>what <em>changes</em> here.</h2>
  </div>
</section>
```

The scrim over the photograph is already there, so text stays readable over anything. Leave
the cover still: no beats, no reveals. It is a breath between sections.

No subtitle sentence under the title. If there is no photograph yet, drop the `<img>` and
keep the `.hero` div, then generate one before delivering.

## Icons and logos

Draw simple marks inline as SVG. Do not load an icon font, do not link to an icon CDN, do
not scatter emoji through a deck for a professional room.

A company logo goes in when the slide is about that company, as inline SVG or an embedded
image. Use the official mark in its real colours: Google is the four-colour G, not a
single-colour one. Monochrome icon sets such as simple-icons are fine for single-colour
brands, but check each brand's real colours and take the multi-colour marks from their
official source. Keep them in a shared `logos/` folder for the whole series.

On a number tile the logo sits in the empty top-right corner at about 44px, and the number
keeps its own space:

```css
.num{position:relative}
.num .lg{position:absolute;right:24px;top:22px;height:44px}
.num .lg svg,.num .lg img{height:44px;width:auto;display:block}
.num b{padding-right:64px}
```

Never squeeze a small logo above the number.

## Faces

Every quoted person sits beside their portrait. Never put a known person's words on a slide
without their face. Use a real photograph of the person, not their social media avatar when
that avatar is a logo: some people use their company mark (the OpenAI mark, the X mark) and
a room reads it as the company talking. Wikipedia's lead images are a reliable source for
public figures. Crop them square from the upper middle, save them at 256px in a shared
`faces/` folder, and reuse them in every talk. Check each face is the right person before
it goes in.

A row of names with faces is a row of rounded rectangles, radius about 14px, the face
beside the name. Not ovals, not pills, not the face stacked above the name.

```css
.sig{display:flex;flex-direction:row;align-items:center;gap:12px;padding:12px 20px 12px 12px;
  border-radius:14px;background:var(--paper);border:1px solid var(--hair)}
.sig img{width:44px;height:44px;border-radius:50%;object-fit:cover}
```

## Posts and quotes

Match the card to where the words came from.

- **A post** is shown as the post, in the look of the platform it came from. Retyped into
  the deck's own quote card, it reads as boring and invented. Build it in HTML so it stays
  sharp on a projector, and make it look like that app.
- **Something said out loud**, in an interview, a speech, a podcast or on stage, is a plain
  quote card with the speaker's face. It was never a post, so it never gets a platform's
  frame.

Take the exact words, date and counts from the real source. Posts in a row share one height
and arrive with `.r`.

**X.** A dark card, the round avatar, the name with the blue verified tick, the handle, the
post text at the app's size, and a footer row with the date and the view count.

```css
.xp{background:#15181C;border:1px solid #2F3336;border-radius:18px;padding:18px 20px 16px;
  display:flex;flex-direction:column}
.xp .xn{font:700 15.5px var(--sans);color:#E7E9EA}   /* name, then the tick svg */
.xp .xu{font:400 14px var(--sans);color:#71767B}     /* @handle */
.xp .xt{margin-top:13px;font:400 19px/1.44 var(--sans);color:#E7E9EA}
.xp .xf{margin-top:auto;padding-top:13px;border-top:1px solid #2F3336;
  font:400 13px var(--mono);color:#71767B}             /* date, views */
```

**LinkedIn.** A white card with a light grey border and a small radius (about 8px). The
round avatar, the name in bold, one line of their job title under it in grey, then the time
and a small globe. The post text in dark grey, and a footer with the reaction icons, the
reaction count, and the comment and repost counts, over a thin divider.

**Facebook.** A white card, round avatar, the name in bold, the date and a small globe under
it, the post text, and a footer with the reaction icons and count on the left and the
comment and share counts on the right.

**Any other platform.** Copy its card the same way: its background, its avatar shape, where
it puts the name, the date and the counts. If you do not know how the platform looks, open a
real post and match it rather than guessing.

## Video

Never leave an empty video well. Each video is a poster with a play mark that loads the
platform's embedded player only when clicked, so the rest of the deck works with no
internet and the room never sees an empty black box:

```html
<div class="clip"><div class="ph play" data-yt="VIDEO_ID" role="button" tabindex="0">
  <div class="pl"></div><b>what the clip shows</b><span>click to play</span></div></div>
```

A click replaces the poster with a `youtube-nocookie.com` embed. Check the clip is
embeddable and still online before delivering. Show other people's videos only through
the platform's own player. Never download and re-host a video the speaker does not own, and
check the licence before hosting anything: a standard YouTube licence does not allow it.
Video the speaker owns, such as his own recordings, can be hosted wherever he likes.
