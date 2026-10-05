# Pictures

"Pictures, pictures." A slide of text boxes with no picture reads as boring. But a picture only
helps if the room gets the idea at once.

## Order of preference

1. **The speaker's own pictures** (their photos, screenshots of their real work). Ask what they have.
2. **Real pictures of the real thing:** the actual page, the actual object, the person's photo.
   Use pictures the speaker may use: their own, public-domain, openly licensed, or official press
   material; put the credit in the source line.
3. **Draw it** in the slide (HTML/SVG in the deck's colours): diagrams, interfaces, charts, simple
   scenes. Drawn things stay sharp on any projector. See `deck-engine/visuals.md` and `charts.md`.
4. **Generate it** only when nothing real exists and drawing cannot show it. Claude itself does not
   make photographs or illustrations; use an image tool the speaker has (for example an image model
   opened through the browser tool, or a local image model), and say on the slide or in the caption
   that it was generated where that matters.

## Permission

Downloads and generated images need the speaker's OK on the exact list (file name, source, what it
shows). Ask once, briefly, in the same message as the draft, not one by one. Do not upload faces
of other people, patients or anything private to an AI service.

## What makes a picture fail

- it shows the thing in a state that hides the point (a rolled scroll when the story is that it was read)
- raw artifacts the room cannot read: code, an author list, a tiny chart
- a metaphor from the audience's own profession forced onto the subject (instrument trays for model
  sizes, a conductor for orchestration): use a plain diagram
- private details: names, faces, patient data, internal documents. Black them out or redraw.
- a drawing that does not match the real thing it introduces (a drawn tool, screen or organ that
  looks different from the real one the room will meet). Draw it from the real picture, or show the real one.
- a label or caption that tells the room nothing ("Figure 1", "Example", the slide title again)

## Into the file

Save pictures to `assets/img/` as `I<id>-what.jpg` and use `@@IMG:I<id>-what.jpg@@` as the `src`.
build.py folds them into the HTML (big ones are scaled to 1920 px), so the deck stays one file.
For a hand-written deck, `scripts/inline-images.py deck.html` does the same. Never leave a `src`
pointing at a file or a web address; `check_deck.py` catches it.
