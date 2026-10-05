# The review loop, and corrections that become rules

## The reviewer

A fresh agent that wrote none of the slides. A builder cannot see the problems in its own work;
a separate reader can. (Research has measured models improving when they critique and revise their
own drafts, and also that a model tends to rate its own writing higher; using a different reviewer
is our practice, not something those studies tested.)

The reviewer gets: the built deck, `outline.md`, `sources.md`, `house-rules.md`, and screenshots
of every click (or makes them with `shoot.py`). It checks, slide by slide, click by click:

1. **Sources:** every fact on screen is in `sources.md` in the true or attributed bin; the source
   line matches what is on that slide; attributed claims say who said them; nothing dropped crept
   back in. It spot-opens a few sources itself.
2. **The outline:** every agreed slide is there, in order, with the agreed clicks.
3. **House rules:** plain titles, visuals over text, no repeated neighbouring layouts, one click per
   group, past steps shrink, topic strip on top, one-line sources, no em dashes, no dot pills, no
   forced analogies, no preachy closing lines, no filler labels or captions, drawings that match the
   real thing, numbers in proportion, nothing private visible.
4. **Craft:** overflow, voids, misaligned edges, text too small for the back row, motion that cuts
   or pops, console errors.

It writes `REVIEW-<n>.md`: totals ("28 slides, 47 clicks, 31 fixes, 5 must-fix"), then one line per
item: slide, click, what is wrong, the fix, **must-fix** or **nice-to-have**.

## Another round?

The reviewer decides, by this rule: any must-fix item (a wrong or unsourced fact, a broken click,
something unreadable, a house-rule break) means another round. Must-fix items go back to the
builder who owns that slide; the reviewer re-checks only those slides. Nice-to-have items are
listed for the speaker, not done automatically. Stop after two rounds and show the speaker what is
left; endless polishing costs the speaker's usage.

## The speaker checks

Show the result as soon as the must-fix items are done: the deck, and a short list of what the
reviewer changed and what is still open. The speaker's reaction is the real review.

## Corrections become rules

Whenever the speaker corrects you (content, design, or how you work):
1. Fix it where it occurred, and check the other slides for the same problem.
2. Add a rule to `house-rules.md`, under "My own rules", in this shape:
   `27. **Short rule.** What to do. Why: what happened (date).`
   Generalise it just enough to apply next time ("plain titles", not "change slide 7's title").
3. If the platform has memory or project instructions, save it there too, or tell the speaker
   exactly what to paste.
4. Add one line to `trail.md`: the correction, paraphrased, and the rule it became.
5. Tell the speaker in one line that it is saved, so they never need to say it twice.

A correction to a single slide that will never recur is just a fix, not a rule; ask if unsure.

## Save your files (normal chat and the free plan)

In a normal chat nothing carries over: the series folder, `house-rules.md` and `theme.css` live
only in that chat. Without saving them, the next chat starts from the house defaults again and
forgets every correction. So:

1. **At the end of every session,** give the speaker these to download: the deck, `house-rules.md`
   and `design-system/theme.css` (and `outline.md` if the lecture is not finished). Then say:
   "In Claude, open **Projects**, make one for your lectures (or open it), and add these files to
   its **Project knowledge**. Replace the old copies. Start your next lecture chat inside that
   project."
2. **At the start of a session,** look for those files in the project and restore the series from
   them before anything else (copy them into the working folder). Tell the speaker in one line
   that you did.
3. Where the work happens in a real folder (the desktop app with a folder, Claude Code), the files
   are already saved; skip this, but still say where they are.
