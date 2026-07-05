---
name: find-exemplar
description: "Use before building or refactoring anything with design freedom (new page, endpoint, CLI verb, background job, provider, chapter), and IMMEDIATELY when the user rejects an approach as hacky/wrong-layer/not-how-the-system-works. Finds the concrete sibling implementation to mirror instead of inventing a pattern or iterating on abstract feedback."
---

# Find Exemplar — mirror a sibling, don't invent

The strongest single finding in the transcript analysis: **naming a concrete existing
implementation converged design disputes that abstract feedback could not.** Sagas of 5–6
rejected attempts ("this is hacky", "wrong layer", "that's not right") each ended the moment
a sibling was named ("trace how the other fields get rewritten and follow that pattern";
"it's structurally the same as the existing built-in — go find it in the registry").
Conversely, prompts that named the exemplar up front ("follow claude code's model for
project directories", "see how the last provider was added") shipped in one pass.

## Rails — when starting work with design freedom

1. **Search for the sibling first.** Before designing anything, find how the codebase already
   does the nearest-neighbor thing: the adjacent list/detail page, the last provider added,
   how the sibling field's rewrite path works, the previous chapter's structure, the same
   feature in a sibling repo or a well-known external tool's convention.
2. **Name it in your plan**: "mirroring how <sibling> is handled end-to-end" — this gives
   the user a one-glance check that you're on the right rails, and gives you an objective
   done-condition ("matches the exemplar") instead of taste.
3. **If no exemplar exists**, say so explicitly and either propose the closest analog or ask
   the user for one — they usually have a specific reference in mind, and inferring it wrong
   was the corpus's #1 cause of interrupt-and-redirect.
4. **Deviations are decisions.** Where you must diverge from the exemplar, list the divergence
   and why — don't silently improvise.

## Rails — when the user rejects your architecture

- After **one** rejection: re-read their words for the implied exemplar ("we have plenty of
  message creation routines — reuse what we have" means *go find those routines*).
- After **two** rejections on the same code: stop producing variants. Trace how the
  established sibling handles the equivalent problem and restructure to match it exactly.
  Ask "which existing implementation should this mirror?" if you can't find one — that
  question is cheaper than a third wrong attempt.

## Parity loops

For match-the-reference work (mock HTML, design spec, prior harness), structure it as:
compare → fix ONE inconsistency → commit → repeat, with an explicit stopping condition
("until every distinctive element of the mock renders"). This shape ran 14 unattended
iterations to pixel parity and self-terminated correctly.

## Caveat

An exemplar is a hypothesis, not ground truth — one user-supplied analogy in the corpus was
a wrong lead ("ignore my last comment"). If the exemplar's mechanism visibly doesn't match
the observed behavior, say so with evidence rather than force-fitting it.
