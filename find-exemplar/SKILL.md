---
name: find-exemplar
description: "Use before building or refactoring anything with design freedom (a page, endpoint, CLI verb, background job, tool, provider, chapter), before an operational step such as a deploy, release or key rotation, when a brief says 'reuse what exists', 'see how X works', 'like the existing Y' or 'don't build a new one', and IMMEDIATELY when the user rejects an approach as hacky, wrong-layer or overfitted. First checks whether the requested behavior already exists, then finds the sibling to call, extract from or mirror, and reports the exemplar and every deviation from it."
---

# Find Exemplar — reuse a sibling, don't invent

Naming a concrete existing implementation settles a design dispute that abstract feedback
("this is hacky", "wrong layer") cannot. Work that names its exemplar up front tends to ship
in one pass.

## Rails — when starting work with design freedom

1. **Check whether the thing itself already exists.** Search for the requested behavior
   before searching for its neighbors. If it exists, the task is "why did it not fire" or
   "why is it not enough", not "build it". Look beyond the current repo with a keyword code search over
   the organization's other repos you can list; another team's tool may already own the
   mechanism.
2. **Then find the sibling.** How does the codebase already do the nearest thing: the
   adjacent list and detail page, the last provider added, the rewrite path of the sibling
   field, the previous chapter's structure, the same feature in a sibling repo, a well-known
   external tool's convention.
   - For an operational step (a deploy, a release, a rotation, a publish), the exemplar is
     the last time it was done: past workflow runs, the git log, the runbook. Find that
     before proposing a manual path.
3. **Check the exemplar's layer.** It must sit at the layer the new code belongs in. A
   product-specific sibling is not a pattern for shared or platform code, and shared code
   must not learn one caller's names.
4. **Reuse before you mirror.** In order of preference:
   1. Call the exemplar's own entry point.
   2. If it needs to change to serve both callers, extract the shared piece, moving the code
      verbatim, so both call sites use it.
   3. Only when neither works, write new code in the exemplar's shape.

   A second copy is a deviation and needs a reason.
5. **Name it in the plan and in the final report.** Both carry:
   - `Exemplar: <path or function>`
   - `Deviations:` each one with its reason, or "none"

   This gives the user a one-glance check and gives you an objective done-condition
   ("matches the exemplar") in place of taste.
6. **If no exemplar exists**, say so and either propose the closest analog or ask the user
   for one. They usually have a specific reference in mind, and guessing it wrong is a
   leading cause of being interrupted and redirected.
7. **When you move or reorganize an existing surface, list every existing action and where
   it now lives.** A table of "was here → is here" shows nothing was dropped.

## Rails — when the user rejects your design

- After **one** rejection: re-read their words for the implied exemplar. "We have plenty of
  message creation routines, reuse what we have" means go find those routines. "You are
  hard-coding" or "you are overfitting" means the design lists special cases; find the
  general rule a sibling already uses.
- After **two** rejections on the same code: stop producing variants. Trace how the
  established sibling handles the equivalent problem and restructure to match it. If you
  cannot find one, ask "which existing implementation should this mirror?" That question
  costs less than a third wrong attempt.

## What it sounds like

- Plan: *"Exemplar: the integrations page (list → detail, same table primitives, same
  registration in nav.ts). Deviations: no bulk actions, because webhooks are singletons."*
- Finding it already exists: *"The rerun-on-infrastructure-failure behavior you asked for is
  already in reruns.go. It did not fire because it requires every failed job to be an
  infrastructure failure and one was a test failure. So this is a fix to that rule, not a
  new feature."*
- After a rejection: *"Before I produce another variant: should this mirror how the sibling
  reference fields get rewritten, or how the installer handles it? I will trace whichever
  and match it."*

## Caveat

An exemplar is a hypothesis. If its mechanism visibly does not match the observed behavior,
or it is itself a pattern the codebase is moving away from, say so with evidence instead of
force-fitting it.

## Footnote: parity loops

For match-the-reference work (a mock, a design spec, a prior harness), run it as: compare →
fix ONE inconsistency → commit → repeat, with an explicit stop ("until every distinctive
element of the mock renders"). See the `loop-author` skill for the full loop contract.
