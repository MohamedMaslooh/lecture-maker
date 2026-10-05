# Day 2 · Orchestrating a team of agents

You are the lead. You plan the work, brief the agents, review what they bring back and do the
final build. You do not do every part yourself, and you do not launch anything before the go.

## Why a team

Each agent starts on a clean page and sees only its own job, so its context stays focused. Jobs
that do not depend on each other run side by side. A reviewer that wrote nothing sees what the
builders cannot see in their own work. Agents cost usage: a team uses several times the tokens of
one chat, so size the team to the job and stop agents as soon as their output is no longer needed.

## Roles, and which model for each

Use the platform's model names. The rule: the stronger the model, the slower it is and the faster
it uses the speaker's limit, so give each job the smallest model that does it well.

| Role | Job | Model |
|---|---|---|
| Lead (you) | plan, brief, review, final build | the strongest available (Opus) |
| Researcher / fact-checker | open every source, fill `sources.md`, sort claims | middle (Sonnet) |
| Picture finder | find real pictures, or drive an image tool through the browser | middle (Sonnet) |
| Architect (big decks only) | shared pieces first: theme parts, kit additions, first 3-4 slides as the reference | strongest (Opus) |
| Slide builders | own a range of slides each; layout, motion, drawing | strongest (Opus) |
| Reviewer | fresh eyes on the whole build, every click, every source | strongest (Opus) |
| Quick lookups, one-line mechanical edits | a date, a rename | smallest (Haiku) |

The strongest reasoning model (for example Fable, where the plan includes it) is for a genuinely
hard problem, not for routine slides. On plans without a model choice, use what is there and say so.

## Order

1. Research and fact-check first (others depend on it). Pictures can start in parallel once the
   outline names them.
2. Architect, if the deck is big (15+ slides) or needs shared pieces. Builders wait for it.
3. Builders in parallel, each on its own slide range. Two to four builders is plenty.
4. Reviewer after the builders, on the full build.
5. Fix round (only the must-fix items), then the speaker checks.

## File ownership: nobody overwrites anybody

- Builder A owns `source/slides/01-*` to `05-*`, the same numbers in `source/css/` and `source/js/`,
  and the pictures it adds to `assets/img/` (named `I<id>-what.jpg`). Nothing else.
- Shared files (`design-system/theme.css`, the kit) belong to the lead or the architect. A builder
  that needs a shared change asks the lead.
- Each builder previews only its own range: `python scripts/build.py <lecture> --only 01-05 --out <scratch>/a.html`
  (always with `--out`, so the real deck is never overwritten by a subset), then
  `python scripts/shoot.py <scratch>/a.html <scratch>/a-shots`.
- `trail.md`: every agent appends one short step at the bottom (what it did, how long, what it
  found), never edits earlier steps.

## The brief (every agent gets all of this)

```
Job: <one sentence>
Read first: house-rules.md, outline.md (your slides: NN-NN), sources.md (verified facts only),
  references/build.md (for builders), design-system/theme.css (do not edit)
You own: <exact files>. Do not touch anything else.
Facts you may use: <from sources.md, with their bins>. Nothing else; if you need a fact, ask.
Done means: <what to hand back>, checked by <build preview + screenshots of every click>,
  console clean, no em dashes, no dot pills, plain titles.
Hand back: a short report (what you made, anything you could not do, open questions).
```

## Reviewing what comes back

Read the report, look at the screenshots, and check against the outline and house rules before
anything goes into the real build. Agents are confident when they are wrong; a catch from the lead
belongs in the trail too (e.g. "the drawn form invented a hospital name; blacked out").

## Without sub-agents

If the platform cannot launch agents (normal chat, free plan), play the roles in the same order,
one at a time, and keep them apart: finish `sources.md` before writing slides; build in slide
ranges; then review as a separate pass that re-reads the built file and the sources, as if someone
else wrote them. Tell the speaker this is the one-person version of the same method.

## While the speaker is away

"Go ahead, I'm going to sleep" is a go for the agreed plan. Keep working, route around blockers
(a blocked web page: try opening it in the browser tool; a missing picture: a placeholder and a
note), never sign in, buy, download outside the agreed list, or publish. Collect every open
question into one list for the morning.
