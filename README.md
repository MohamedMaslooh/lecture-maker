# Lecture Maker

A skill for Claude by **Dr. Mohamed Maslooh** ([maslooh.com](https://maslooh.com)), version 1.1.0.

It makes a lecture or presentation **with** you, the same way his AI lecture series was made. You
talk; it asks what it needs (each question with a suggested answer), agrees the outline with you,
checks every fact against a source it opened, builds the slides with a team of agents and a fresh
reviewer, and gives you back **one HTML file** that works offline in any browser, animated one
click at a time, with a slide navigator at the right edge. Every rule in it comes from a correction
the lecturer once had to make, so you do not have to make it again.

## Install in the Claude app (desktop or claude.ai)

1. Go to **Customize > Plugins**.
2. Press **Add marketplace** and paste:
   `https://github.com/MohamedMaslooh/lecture-maker`
3. Find **Lecture Maker** in the list and press **Install**.
4. Leave **Sync automatically** on, so new versions arrive by themselves.

Menus in the app move from time to time. If yours look different, look for "Plugins" under
Customize or Settings.

## Install in Claude Code

```
claude plugin marketplace add https://github.com/MohamedMaslooh/lecture-maker
claude plugin install lecture-maker@maslooh
```

Start a new session afterwards. To update later:

```
claude plugin marketplace update maslooh
claude plugin update lecture-maker@maslooh
```

## No plugins? Upload the ZIP

Works on the Free plan too. Download `lecture-maker.zip` from
[maslooh.com/skills/lecture-maker/](https://maslooh.com/skills/lecture-maker/) (do not unzip it).

1. Go to **Settings > Capabilities** and turn on **Code execution and file creation**.
2. Go to **Customize > Skills**, press **+ > Create skill > Upload a skill**, and choose
   `lecture-maker.zip`.
3. Make sure the skill is switched on.

Claude Code without the plugin: unzip and copy the `lecture-maker` folder into `~/.claude/skills/`.

## Start a lecture

Open a new chat and just talk, for example:

> Make me a lecture on how to present a paper at journal club, about twenty minutes, next
> Wednesday. I want them to leave knowing what to look for first...

Messy is fine; more is better. Nothing is built until you say **"go"**. Say **"update the skill"**
at any time to check for a newer version.

## What is inside

```
.claude-plugin/marketplace.json        the "maslooh" marketplace
plugins/lecture-maker/
  .claude-plugin/plugin.json           the plugin
  skills/lecture-maker/                the skill
    SKILL.md                           the method: Day 0 to Day 3, when to stop and ask, how to update
    references/  assets/  scripts/  examples/
```

A finished 4-slide example is in
`plugins/lecture-maker/skills/lecture-maker/examples/why-is-the-sky-blue/why-is-the-sky-blue.html`.

## Good to know

- **Facts:** it uses only sources it actually opened and says when it could not check something.
  Still read the sources line on each slide before you present.
- **Privacy:** never upload patient details, names or faces to any AI tool.
- **Usage:** a lecture with agents uses a good share of a plan's weekly usage.

## Licence

MIT (see `LICENSE`). Includes the animated-html-deck engine (MIT). Fonts: Space Grotesk, Inter and
IBM Plex Mono, SIL Open Font License.

Made by Dr. Mohamed Maslooh · [maslooh.com](https://maslooh.com)
