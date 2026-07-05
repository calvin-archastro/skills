---
name: sharpen
description: "Use when starting a nontrivial build/refactor task from a rough or underspecified ask, or when the user invokes /sharpen with a draft prompt. Upgrades the ask into the high-success shape (exemplar anchor, scope bounds, acceptance criteria, banned shortcuts, verification plan) before any code is written. Do NOT use for closers (commit/push/rebase), quick questions, or asks that already name an exemplar and scope."
---

# Sharpen — upgrade a rough ask before executing it

Transcript analysis showed that failed sessions almost never failed from missing effort —
they failed because the model had to *infer* something the user already knew: which existing
pattern to mirror, where the scope boundary was, or which shortcut was off-limits.
This skill front-loads that naming.

## Procedure

Given the rough ask, build a working spec with these seven elements. Fill in what you can
from the repo and conversation yourself first — do not offload research to the user.

1. **Goal** — one sentence, outcome-shaped ("settings page shows bulk upgrades grouped by
   package"), not activity-shaped ("work on the upgrades page").
2. **Exemplar** — the existing implementation, sibling feature, prior PR, mock, or external
   reference this should mirror. Search the codebase for one (the sibling module, the
   adjacent page, how the last refactor of this area was done). This is the single
   highest-value element: "it's structurally the same as X, look at Y" repeatedly beat
   paragraphs of description.
3. **Scope bounds** — what NOT to touch, and the PR shape (one PR per concern; "the queue
   change in one pr, the sweeper fix in another"). State back-compat expectations explicitly
   ("no back compat — nothing uses this yet" vs "must not break existing callers").
4. **Acceptance criteria** — checkable, ideally numeric or structural ("times cut in half",
   "two instances configured → two rows shown", "the page lives at /settings/upgrades").
   If the user gave none, derive them and state them so they can veto.
5. **Banned shortcuts** — the failure modes this task invites. Standing bans observed to
   matter: no suppressing or exception-listing static-analysis/type errors; never fix an
   authorization failure by escalating the acting principal's privileges; no branching on
   error-message strings (use error codes); never amend a pushed/merged commit; no parallel
   implementations of pipelines that already exist (reuse/refactor instead); no test-file
   edits to make checks pass.
6. **Verification plan** — how you'll prove it works beyond unit tests: live run, e2e test,
   smoke via the relevant project skill, screenshot comparison. "Did you actually run it
   live?" surfaced real gaps ~100% of the time — pre-empt the question.
7. **Method hints** — only if the task is investigation-shaped: which logs/metrics/tools to use.

## Then

- Present the spec compactly (a few lines per element, skip elements that are genuinely N/A).
- If one or two elements are load-bearing and unknowable (e.g. which of two existing flows
  the ask means), ask **once, batched** — never serially. Use concrete options, not open
  questions.
- On approval (or if nothing needed asking), execute against the spec. Treat the acceptance
  criteria as your own exit checklist and report against them at the end.

## Anti-patterns this replaces

- Long prose specs with no exemplar → wrong build despite the detail volume; fixed only by
  a pointer to an existing UI element that already had the intended semantics.
- Discovering scope bounds via interrupt ("rip this out — the only thing you should have
  addressed was X").
- The user firing corrective addenda one at a time because the spec was never made explicit.
