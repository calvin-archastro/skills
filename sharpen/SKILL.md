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

Given the rough ask, build a working spec with these eight elements. Fill in what you can
from the repo and conversation yourself first — do not offload research to the user.

1. **Goal** — one sentence, outcome-shaped ("settings page shows bulk upgrades grouped by
   package"), not activity-shaped ("work on the upgrades page").
2. **Exemplar** — the existing implementation, sibling feature, prior PR, mock, or external
   reference this should mirror. Search the codebase for one (the sibling module, the
   adjacent page, how the last refactor of this area was done). This is the single
   highest-value element: "it's structurally the same as X, look at Y" repeatedly beat
   paragraphs of description.
3. **Scope bounds** — what NOT to touch, and the PR shape. One feature is one PR and
   independent concerns get their own ("the queue change in one pr, the sweeper fix in
   another"); do not offer to split a coherent change. State back-compat expectations
   explicitly ("no back compat — nothing uses this yet" vs "must not break existing
   callers"). The smallest change that solves the stated problem is the default; each new
   table, endpoint or flag needs a reason it is needed now.
   - **Authority, asked once.** Settle at the start how far the task runs: "Ship as I go
     (commit, push, open the PR, watch CI to green)?" A yes is standing approval for
     every such step in this task, so no later turn ends with "say commit and I'll push".
     Merges, live infrastructure and hard-to-reverse cleanup are still asked for by name.
   - **Prior work.** Search recently merged PRs and other sessions' work for the same
     symptom or file before starting. Build on what exists; do not redo it.
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
   - Prove it on the surface the user named, not a stand-in. A static code read is not an
     audit of the running pages; an SPA tested without its APIs is not tested.
   - A UI change is shown, not described: run the app and capture screenshots with real
     data (light, dark and narrow where they apply) before offering to commit. If the user
     gave mocks, the bar is each mock side by side with the build, every mismatch listed.
     A mock uses the live components and the existing data model.
   - Name the end state the plan reaches: merged, released, deployed, or observed working.
     "Done" means the last one unless the user said otherwise.
   - Say the command and its expected duration before any local check over about five
     minutes. Prefer focused tests and let CI run the long suites.
7. **Method hints** — only if the task is investigation-shaped: which logs/metrics/tools to use.
   Plan to gather that evidence yourself with the access you have. A step goes to the user
   only when it needs a person (a passkey, a payment, an approval).
8. **Parallelism** — if the spec has two or more independent parts, say which run as
   separate subagents in separate worktrees. Do not wait to be told to fan out.

## Then

- Present the spec compactly (a few lines per element, skip elements that are genuinely N/A).
- If one or two elements are load-bearing and unknowable (e.g. which of two existing flows
  the ask means), ask **once, batched** — never serially. Use concrete options, not open
  questions.
- On approval (or if nothing needed asking), execute against the spec. Treat the acceptance
  criteria as your own exit checklist and report against them at the end.

## Worked example

Rough ask: *"add an upgrades page to the dashboard"*

```
GOAL: dashboard page listing installed packages with pending upgrades, bulk-upgrade per group.
EXEMPLAR: mirror the integrations list page (same table primitives, filters, row actions).
  The existing per-item upgrade card already computes the version diff — reuse its logic,
  do not reimplement the comparison.
SCOPE: UI + one list endpoint. Don't touch the upgrade executor. One PR.
ACCEPTANCE: url /dashboard/upgrades; rows grouped by package; bulk button per group;
  seeded fixtures with 2 packages → 2 groups shown.
BANNED: no parallel version-diff implementation; no back-compat shims (nothing links here yet).
VERIFICATION: e2e test on the seeded fixtures + light, dark and narrow screenshots of
  the running page. End state: PR green and mergeable.
AUTHORITY: ship as I go? (commit, push, open the PR, watch CI) — merge stays yours.
PARALLEL: none; one coherent change.
```

Two sentences of ask became eight checkable lines — and the exemplar line alone is what
prevents the wrong-feature build observed in the transcripts.

## Anti-patterns this replaces

- Long prose specs with no exemplar → wrong build despite the detail volume; fixed only by
  a pointer to an existing UI element that already had the intended semantics.
- Discovering scope bounds via interrupt ("rip this out — the only thing you should have
  addressed was X").
- The user firing corrective addenda one at a time because the spec was never made explicit.
