---
name: lecture-maker
description: Lecture Maker, by Dr. Mohamed Maslooh (maslooh.com). Makes a whole lecture or presentation with the speaker, the way his AI lecture series was made - set up the project and the house look (indigo, Space Grotesk and Inter, offline), take a messy spoken brief, ask the questions it needs (each with a suggested answer), agree the outline in chat, then research and fact-check every claim, build the slides with a team of agents and a fresh reviewer, and deliver ONE offline animated HTML file with a slide navigator. Use it whenever someone asks for a lecture, talk, presentation, teaching session, journal club, grand round, seminar, conference talk, slide deck or slides on any topic ("make me a lecture on...", "I'm giving a talk next week about...", "help me prepare slides"), even if they do not name the skill; when they want to continue, fix or review a deck made this way; and when they say "update the skill" or "do an update".
---

# Lecture Maker

By **Dr. Mohamed Maslooh** · [maslooh.com](https://maslooh.com) · version in `VERSION`.

This skill makes a lecture **with** a speaker, not for them. It is the method Dr. Maslooh used to
build his AI lecture series, saved as steps. Every rule in it comes from a correction he once had
to make. The result is one HTML file that opens offline in any browser, in his house look, with a
slide navigator at the right edge. It makes presentations only: no speaker notes, no presenter
copy, no script.

The method runs over four "days" (stages of work, not calendar days). Each day ends at a gate
where you stop and wait for the speaker.

| Day | What happens | Gate |
|---|---|---|
| 0 | Project with everything about the speaker; the house look, or their own | one yes/no on the look |
| 1 | The messy brief; read what you already know; questions with suggested answers; outline in chat | the speaker says **go** |
| 2 | Research and fact-check, pictures, builders, a fresh reviewer; corrections saved as rules | the speaker checks the draft |
| 3 | The one HTML file, a browser check, a "what it cost" note, "save your files" | hand over |

## The rules that matter most

These are the lessons, not decoration. Read `assets/project/house-rules.md` for the full list; the
speaker's own copy lives in their project as `house-rules.md` and grows with every correction.

1. **Ask before acting.** Discuss, recommend one option, then wait. Launch agents, build files,
   download pictures or publish anything only after a clear go: "go", "start", "build it".
2. **Liking an idea is not a go.** "That sounds great" and answering your questions mean the
   speaker is still thinking. Keep it in chat. Dr. Maslooh once had three agents launched on "the
   idea is very appealing" and had to stop them; that is why this rule exists.
3. **Facts are verified or they are out.** Every claim is checked against a source you actually
   opened. Never invent a source, quote, number, name or date. If you could not open it, say so.
   A false claim is dropped, never shown "to debunk it".
4. **Every question comes with your suggested answer,** so the speaker can reply "yes" or change one.
5. **Every correction becomes a rule.** When the speaker corrects you, fix it, then add a dated rule
   with the reason to their `house-rules.md` (and memory, if the platform has it), so it never
   needs saying twice.
6. **Show the result as soon as it exists.** Offer extras in one line; make them only on a yes.
   The speaker is paying for usage.
7. **No em dashes, no dot pills** (a decorative dot beside text inside an oval), **plain titles**,
   **visuals over text**, **no filler labels or captions**, **pictures that match the real thing.**

## Where you are running, and what changes

Check what you can do before Day 0, and tell the speaker in one line what that means.

- **Claude with files and code (the desktop app with a folder, Claude Code, claude.ai with "Code
  execution and file creation" on):** the full method. Use the scripts in `scripts/`. Cowork is being
  folded into the main Claude app (announced for 6 Oct 2026; new Pro and Max tasks then run in the
  cloud). If the speaker sees no Cowork, they already have the new Claude: same thing, give it a folder.
- **Sub-agents available** (desktop app tasks, Claude Code): orchestrate as in
  `references/orchestration.md`, choosing the model per job.
- **No sub-agents** (normal chat, free plan): play each role yourself, one after another, and keep
  them separate: finish the research and its sources table before writing any slide; review as a
  fresh pass that re-reads the built file, not your memory of it. Say that a paid plan would run
  these in parallel; do not pretend it did.
- **Free plan:** usage is small and there is no Opus, so the strongest model offered leads. Keep a
  deck to ~8 to 10 slides per chat, or build a longer one in slide ranges over several chats
  (save the files between them, below). Say this before Day 2, not after the limit is hit.
- **Normal chat, nothing carries over.** A chat's files live in that chat only. At the start, if
  the speaker has a Project, restore the series from its files (`house-rules.md`,
  `design-system/theme.css`, the last outline). At the end of every session, give them those files
  to download and say how to add them to their Project (see "Save your files" in
  `references/review-loop.md`). Without this, "every lecture keeps the look" and "corrections
  become rules" are not true.
- **No code execution:** you cannot run the build. Write the slides into a copy of
  `assets/engine/deck-template.html` by hand (THEME block, then the slides between the markers),
  and give the speaker the file.
- **No browser tool** for checking: run `scripts/check_deck.py`, then ask the speaker to open the
  file and click through it once before the talk.

## Day 0 · Set up the project and the look

Read `references/day-0-setup.md`. In short:

1. **One message of questions about the speaker,** each with a suggested answer: who they are,
   where they teach, the audience, the slide language, the usual length. Fill
   `assets/project/project-instructions.md` from the answers and say where to paste it.
2. **The look, as one yes/no question.** "Use the Maslooh house look (indigo accent, Space
   Grotesk titles, Inter text, fonts built in so it looks the same on every computer)? Suggested:
   yes." On yes, `assets/design-system/theme.css` is used as it is: no design session, no sheet
   unless they want to see it. Only if they want changes (their institution's colours, a dark
   room), edit the tokens in `theme.css`, build the sheet (`python scripts/build.py <lecture>
   --sheet`) and change it until they approve. After approval every slide follows it; a new look is
   a new Day 0.
3. **The series folder:** `python scripts/new_lecture.py <series>` (house rules and theme; the
   first lecture's folder is made after the go on Day 1).

If the speaker already has a project and an approved look, say so and skip to Day 1.

## Day 1 · The brief, the questions, the outline

Read `references/interview.md` and `references/outline.md`.

1. **Take the brief as it comes.** A long dictated voice message with no order is ideal: more
   context, not less. Do not ask them to restructure it.
2. **Read before replying,** without being asked: the project instructions, `house-rules.md`,
   memory, the series plan, the last lecture's outline and trail. Tell the speaker in one line what
   you read.
3. **Answer with one idea and a recommendation, not a menu,** then ask what is missing: each
   question with your suggested answer (see the question bank). Usually five to eight questions.
4. **Draft the outline in the chat,** slide by slide (title, what each click shows, source needed,
   pictures needed). Discuss and change it there. Mark facts not yet checked as `[CHECK]`.
5. **Wait for the go.** Then run `python scripts/new_lecture.py <series> <slug> --title "..."`,
   save the agreed outline to `outline.md`, and start `trail.md`: the story of this lecture, one
   step per stage, corrections included, newest at the bottom.

## Day 2 · Build it with a team

Read `references/orchestration.md` first, then the reference for each job as you brief it.

1. **Research and fact-check** (`references/fact-check.md`): one agent opens every source, fills
   `sources.md`, sorts each claim into true / attributed / dropped. Nothing goes on a slide from
   memory. Dropped claims are removed from the outline before building.
2. **Pictures** (`references/pictures.md`): real pictures first, found and downloaded only with the
   speaker's OK on the exact list; generated pictures only when nothing real exists, through
   whatever image tool the platform gives you. A drawing must match the real thing it introduces.
3. **Builders** (`references/build.md`): each owns separate slide files (`source/slides/NN-*`, its
   CSS and JS), so no two agents ever edit the same file. Each checks its own slides with a
   preview build and screenshots before handing back.
4. **A fresh reviewer** (`references/review-loop.md`) that wrote nothing: steps through every click,
   checks every source against its slide, checks the house rules, and decides whether another
   round is needed. Must-fix items go back to the builder who owns that slide.
5. **The speaker checks the draft.** Every correction is fixed and saved as a rule
   (`references/review-loop.md`, "Corrections become rules").

If the speaker said "carry on, I'm away", keep going with your best judgment, route around
blockers, never sign in, buy or publish, and give one list of open questions at the end.

## Day 3 · Finish and hand over

1. **The one file:** `python scripts/build.py <lecture>` writes `<file>.html`. Every picture and
   font is inside it; it works with no internet. Run `python scripts/check_deck.py <file>.html`.
2. **Check it in a browser:** `python scripts/shoot.py <file>.html <outdir>` (where Playwright
   exists) and look at every screenshot, or click through it yourself, forwards and back.
3. **What it cost** (`references/cost-check.md`): a short honest note, as a share of the speaker's
   plan, labelled as an estimate.
4. **Save your files** (normal chat, free plan): the deck, `house-rules.md` and
   `design-system/theme.css` to download, and where to add them in their Project.
5. **Hand over** the file with three lines: open in a browser, F for full screen, arrows or click
   to move, and the mouse at the right edge (or G) shows every slide; click one to jump.
   Then stop. Offer extras in one line.

## Updating the skill

When the speaker says "update the skill", "Claude, do an update" or similar:

1. Read this skill's `VERSION` (for example `1.1.0`).
2. Open `https://maslooh.com/skills/lecture-maker/version.txt` (web fetch, browser or code,
   whatever you have). The latest ZIP is at
   `https://maslooh.com/skills/lecture-maker/lecture-maker.zip`.
3. **If the address does not answer** (not found, no internet, no web tool): say it plainly: "The
   update page maslooh.com/skills/lecture-maker/ is not live yet, or I cannot reach it
   from here. You have version X." Do not guess a version and do not look elsewhere.
4. **If it is the same or older:** "You have the latest version (X)."
5. **If it is newer:** say how to get it, depending on how they installed it.
   - **As a plugin** (from the `maslooh` marketplace): with "Sync automatically" on, the Claude app
     updates it by itself; otherwise sync the marketplace in **Customize > Plugins**. Claude Code:
     `claude plugin marketplace update maslooh`, then `claude plugin update lecture-maker@maslooh`.
   - **As a ZIP** (desktop app or claude.ai): download the ZIP (do not unzip it), go to
     **Customize > Skills**, remove or turn off the old Lecture Maker, press **+ > Upload a skill**,
     choose the new ZIP, switch it on, and start a new chat. Claude Code without the plugin: unzip
     it and replace the `lecture-maker` folder in `~/.claude/skills/`.
   Their own files (house rules, theme, lectures) live in their project and are not touched.

Never install, upload or replace anything yourself; the speaker does the upload.

## Files in this skill

- `VERSION` · the version number, compared on update
- `references/day-0-setup.md` · project, the house look, which app mode
- `references/interview.md` · what to read first, the question bank with suggested answers
- `references/outline.md` · the outline format and the gate
- `references/orchestration.md` · roles, model per job, briefs, file ownership, no-agent fallback
- `references/fact-check.md` · the three bins, sources, tags, what never to do
- `references/pictures.md` · real first, permissions, generated pictures, inlining
- `references/build.md` · lecture folder, slide conventions, beats, tokens, the kit, the navigator
- `references/review-loop.md` · the reviewer, rounds, corrections become rules, save your files
- `references/cost-check.md` · the "what it cost" check
- `references/deck-engine/motion.md`, `charts.md`, `visuals.md` · the animated-html-deck engine's
  own pattern references (reveals, charts, pictures)
- `assets/engine/deck-template.html` · the animated-html-deck engine (MIT), never edited
- `assets/kit/lecture-kit.css|js` · topic strip, one-line sources, tags, groups, shrink, scenes
- `assets/kit/deck-nav.css|js` · the slide navigator (from the lecture site), added to every deck by build.py
- `assets/design-system/theme.css` · the Maslooh house look (colours and 8 embedded fonts, OFL)
- `assets/design-system/design-sheet.html` · the sheet shown only if the look is changed
- `assets/project/*` · house rules, project instructions, trail, outline and sources templates
- `scripts/new_lecture.py`, `build.py`, `check_deck.py`, `shoot.py`, `inline-images.py`,
  `tally_tokens.py`
- `examples/` · a finished 4-slide example ("Why is the sky blue?") in the house look, with a real
  photo that shrinks aside, its outline, sources and trail. Open it to see the target.

## How this relates to the animated-html-deck skill

The deck engine is bundled (`assets/engine/deck-template.html`, from animated-html-deck 1.2), so
this skill works on its own after a single ZIP upload. If animated-html-deck is also installed,
both share the same engine and motion rules; for lectures, this skill leads and its house rules win
where they differ (for example: sources are one line with hover, and nothing but the slides goes in
the deck).
