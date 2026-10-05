# What it cost: a short, honest check

Speakers on a subscription pay a flat price, so the honest bill is **a share of their plan**, not
API dollars (API prices make the same work look far more expensive than what they paid).

## The method that works everywhere

1. Before the work starts (Day 1, before the go), ask the speaker to open **Settings > Usage** in
   the Claude app and note the session and weekly percentages. (Other tools have similar pages.)
2. At the end, read them again. The difference is the real share of their plan this lecture used.
   If the work crossed a reset, add the readings of each stretch.
3. Write two or three lines in `trail.md` and tell the speaker, for example:
   "This lecture used ~5% of one week of your plan (Settings > Usage, before and after)."

If no reading was taken at the start, say so and give only what is known; never back-fill a number.

## If the session files exist (Claude Code, or the desktop app's Code tab)

`python scripts/tally_tokens.py ~/.claude/projects/<project-folder> [--since 2026-10-01]` counts the
tokens by model and how many were cheap cache reads. Providers do not publish how many tokens a
plan includes, so any "share of the plan" from tokens is an estimate from community measurements:
label it "estimate" and name the source and its date.

## What to say about where it went

Usually: most tokens are the same context re-read on every turn; agents are most of the total;
the biggest model costs the most per turn. That is the case for one task per chat, small models
for small jobs, and stopping agents when their output is no longer needed.
