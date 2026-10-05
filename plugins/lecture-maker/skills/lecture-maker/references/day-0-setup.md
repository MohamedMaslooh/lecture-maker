# Day 0 · The project and the design system

Day 0 happens once per series, not once per lecture. Its job is that from Day 1 on, a short messy
message is enough, because everything else is already known and the look is already decided.

## 1. Which mode of the app

When the speaker opens the Claude desktop app they may see Chat, Cowork and Code.

- **Chat** answers questions. Fine for Day 1 talk, but it cannot run agents, and its files stay in
  that chat (see "Save your files" in `review-loop.md`).
- **Cowork** does multi-step jobs with a folder of files: the right place for this skill on a paid
  plan. By default it asks before acting; recommend keeping that default at first, and keeping a
  copy of any folder they give it.
- **Code** is for software. The same agent, with a terminal. Not needed for this.

Cowork is being folded into the main Claude app (announced for 6 Oct 2026; new Pro and Max tasks
then run in the cloud). If the speaker sees no Cowork, they already have the new Claude: same thing,
give it a folder. On a free plan the skill works in a normal chat with "Code execution and file
creation" turned on, playing the agent roles one after another; keep each chat to ~8 to 10 slides.
App menus change often; if the speaker's screen differs, follow what they see.

## 2. The project

A project holds everything about one job: files, instructions, and its chats. One project per job
(the lecture series is one job).

Ask in ONE message, each question with your suggested answer, so they can reply "yes" or change one:
- who the speaker is and where they teach · suggested: from anything they already said
- who the audience is (role, what they already know) · suggested: from the brief
- the language of the slides and of the talk · suggested: slides in English, the talk in their language
- usual length and room · suggested: ~20 minutes, a projector
- past lectures (files), the series plan if any, any lecture the audience already heard on the
  same subject (so you do not repeat it) · suggested: "none yet" is fine
- the look: "Use the Maslooh house look? Suggested: yes" (section 3)

Write the answers into `assets/project/project-instructions.md` (filled), and tell the speaker where
to paste it: Claude: the project's instructions; ChatGPT: Project > instructions; Google: an
Antigravity project (a folder with its own chats), or a Gem's instructions for standing
instructions only. Then copy `house-rules.md` into the project files.

A project can hold any rules the speaker wants. Do not suggest which rules to add beyond the house
rules; the speaker knows their own field and audience better than you.

## 3. The look: the house look by default

Why first: a plain "make me slides" has no look to follow, so every slide drifts. Agreeing the look
once means every later slide, from every agent, comes out the same without asking again.

The skill ships an approved look: Dr. Maslooh's house look from his AI lecture series
(`assets/design-system/theme.css`): indigo accent `#4F46E5`, amber second voice `#B45309`, a cool
grey board, Space Grotesk titles, Inter text and IBM Plex Mono numbers, all three fonts embedded so
the deck looks the same on every computer and needs no internet.

1. **Ask one question** (in the Day 0 message): "Use the house look (indigo, Space Grotesk and
   Inter)? Suggested: yes." If they want to see it first, show the example
   (`examples/why-is-the-sky-blue/why-is-the-sky-blue.html`) or its screenshots.
2. **On yes:** make the series folder, `python scripts/new_lecture.py <series>`, which copies the
   house `theme.css` and `house-rules.md`. That is the whole design step. Write "house look,
   approved <date>" at the top of the series' theme.css.
3. **Only if they want changes** (their institution's colours, a logo colour, a dark room):
   edit only the tokens in the series' `design-system/theme.css` (board, ink, accent, `--warm`,
   alert; fonts only if they ask). Keep the embedded fonts unless they want others; a new font must
   also be embedded as base64 `@font-face`, never linked. Check contrast: body text on the board,
   white on the accent. Build the sheet (`python scripts/build.py <lecture> --sheet`, after the
   first lecture folder exists, or show one test slide), show it, and change it until they say it
   is approved. Write "approved on <date>" at the top of theme.css.

After approval, nobody changes the theme inside a lecture. A wish for a new look is a new Day 0.

## 4. What Day 0 hands to Day 1

- project instructions in place, house rules in the project files
- `design-system/theme.css` approved (the house look, or their changes)
- in a normal chat: the speaker has downloaded `theme.css` and `house-rules.md` into their Project
- the speaker knows that from now on they can just talk
