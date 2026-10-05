# The making of "Why is the sky blue?"

The example that ships with the Lecture Maker skill, made with the skill's own method on a neutral,
non-medical topic. Newest step at the bottom.

---

## Day 0 · Design system

One question: "Use the house look?" Yes. The series uses the Maslooh house look as it ships
(`../design-system/theme.css`: indigo, amber, Space Grotesk and Inter, fonts embedded). No design
session was needed; the sheet (`../design-system/design-system.html`) was built only to show it.

## Day 1 · Brief, questions, outline

Brief (paraphrase): a four-slide example on a neutral topic that shows every part of the method.
Questions answered with their suggested answers: audience (curious adults), length (~4 minutes),
spoken in Egyptian Arabic, one real photo for the sunset, the rest drawn. Outline agreed, then the go.

## Day 2 · Fact-check and build

The research step opened NASA Space Place and Wikipedia's "Rayleigh scattering" and filled
`sources.md`. One catch: neither page gives a "blue vs red" multiplier, so the ~5.9x on slide 3 is
labelled "our calculation" with its inputs. "Why not violet?" was dropped: not in the sources
opened. The sunset photo is CC0 on Wikimedia Commons (licence read on the file page), credited in
slide 4's source line; on click 1 it shrinks aside for the drawn explanation. Four slides built,
every click screenshot and checked. The blue wave and bar on slide 3 use a real sky blue, not the
indigo accent, so the drawing matches the thing it names.

## Day 3 · Finish

Deck built (one file, 0.70 MB, fonts and photo inside); `check_deck.py` clean; console clean in
every screenshot; the slide navigator opens at the right edge and jumps to any slide.
