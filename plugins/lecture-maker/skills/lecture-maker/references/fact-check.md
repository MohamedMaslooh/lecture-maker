# Fact-check: only verified claims reach a slide

AI models state wrong things confidently, including invented sources that look real. So nothing
goes on a slide as a fact unless someone opened its source and read it.

## The researcher's job

For every claim in the outline (numbers, dates, names, quotes, "studies show", product facts):
1. Find the primary source: the study, the organisation's own page, the official help page. A
   news article about a study is a pointer to the study, not the source.
2. **Open it and read the part that matters.** Copy a short exact quote into `sources.md`. If the
   page will not open for the fetch tool, try a real browser tool if there is one. If it still will
   not open, the claim is unverified.
3. Write the checked date (the day it was opened). Things about software, prices and plans change
   monthly: recheck those close to the talk.
4. Sort it into a bin.

| Bin | Means | On the slide |
|---|---|---|
| **true** | the source says it, and the source is the right one | yes, with its one-line source |
| **attributed** | true that they said it, but self-reported, unaudited, or one study | only with who said it ("their own test", "one 2023 study"); ask the speaker first |
| **dropped** | false, unsourced, the page would not open, or the source says something else | never, not even to debunk it |

Replace a dropped claim with the verified fact next to it, stated on its own. No "myth vs reality"
slides.

## Who said what

- A sentence that is half theirs and half ours is split on the slide: their part with their name,
  our part tagged "our addition" (a real case: a line was put under a company's name, but only its
  first half was on their page).
- Our own calculations get "our calculation" and show the inputs (e.g. (700/450)^4 ≈ 5.9).
- The speaker's own experience gets "my experience"; an estimate gets "estimate"; a company's
  measurement of its own product gets "their own test".
- Quotes from people are exact and sourced; conversations and messages are paraphrased.

## Never

- invent a source, a URL, a DOI, an author, a quote, a page title, a number or a date
- cite a source you did not open, or cite the search snippet instead of the page
- round a number into something the source did not say ("about half" for 38%)
- keep a fact because it is good for the story

When you cannot verify something important, say so plainly to the speaker and suggest dropping it
or asking a colleague who knows.

## The source line on the slide

One line at the bottom left: `Author or organisation, "Title," year · checked 5 Oct 2026` with a
real link where one exists. If it is longer, it is cut with "…" and the whole of it shows on hover
(the kit does this). Each source matches what is on that slide: nothing on screen without a
source, no source for something not on screen. A well-known saying needs no source.
