---
name: loop-author
description: "Use when the user is about to start an autonomous run — /loop, /goal, 'keep going until', 'work through these tasks', overnight/unattended work — or asks to write/fix a loop prompt. Produces a hardened loop prompt with work-unit discipline, durable state files, exit criteria, and quality gates. Also use when an existing loop is drifting, pacing badly, or shipping violations."
---

# Loop Author — harden an autonomous run before launching it

Loops are the highest-output workflow in the analyzed transcripts (a ~130-task burndown
shipped as a 133-commit PR; a 14-iteration mock-parity loop; 28 bugs fixed in 25 commits).
The evidence is unambiguous: **under-specified loop prompts get interrupted and re-issued;
fully-specified ones run 20+ iterations clean.** Every element below earned its place by
being the thing whose absence broke a real loop.

## The anatomy — build the loop prompt from these parts

1. **Work-unit discipline.** Exactly one unit per iteration, and name the unit's shipping
   shape: "one task per loop", "one PR per issue", "one commit per fix". This is what makes
   iterations auditable and interruption-safe.
2. **Durable state, not context memory.**
   - A **spec file** the loop consumes (`docs/specs/*.csv` or `.md` task list) — check items
     off in the file as they complete.
   - A **journal file** (`docs/journals/<topic>.md`) — per-iteration: what was done, decisions
     made, how to use the feature, RCA notes. Loops without journals lost state; loops with
     them survived restarts and context clears.
   - If resuming: embed a **DONE/NOW recap** in the prompt itself ("DONE: T01..T11, T13 —
     ONLY T12 REMAINS. DO T12 = ...") with pointers to the exact files/patterns the next
     task needs.
3. **Exit criteria** — compound and checkable: "exit when all units are merged-ready and
   verified, or pause if blocked on a user decision". Loops with explicit exits
   self-terminated correctly ("complete — stopping"); vague ones over- or under-ran.
4. **Quality gates per iteration** — name them all: build/typecheck, lint, focused tests,
   e2e or blackbox test for the feature, smoke via the relevant project skill, and for
   risky work an unbiased subagent review or critic with "no blocking findings" as the bar.
5. **Design values up front.** The values users otherwise inject via interrupt:
   "most problems are due to incomplete abstractions, poor architecture, or missing edge
   cases", "elegance and great code design are key", reuse existing pipelines rather than
   standing up parallel paths, keep files under the size cap.
6. **Standing rules section.** A named, amendable block of hard bans (never fix an
   authorization failure by escalating the caller's privileges; no error-string matching;
   no test-file edits; no amending pushed commits; don't relitigate AGREED DECISIONS).
   Mid-flight corrections should be folded into this block so they persist across
   iterations — that mechanism demonstrably held.
7. **AGREED DECISIONS block** — settled design choices, so iterations don't reopen them.
8. **Pacing directive.** Loops defaulted too conservative ("don't wait so long — you need to
   run the loop faster" was a real correction). State it: work continuously through the
   backlog; only sleep when genuinely blocked on external events, and say what interval.
9. **Named skills/tools** — which project skill to use for fixes, which logs/metrics
   sources, whether subagents should be dispatched for parallel issues.

## Procedure

1. Ask yourself which parts are already settled in context; draft the plan/spec/journal files
   first if they don't exist (plan-to-file-then-loop produced the cleanest large build observed).
2. Write the loop prompt containing all nine parts. Length is fine — completeness beats brevity
   here, the opposite of interactive prompting.
3. Show it to the user for launch, or launch it if they've already said to.

## Known failure modes to design against

- **No journal → amnesia** between iterations and after /clear.
- **No exit criteria → babysitting**: dozens of no-op ticks until the user kills it.
- **Missing standing rules → systematic violations at scale** (a loop shipped multiple
  privilege-escalating "fixes" before the ban was added; every PR needed re-auditing).
- **Stray background processes**: have the loop verify it cleaned up watchers/processes
  each iteration ("looks like you may have an infinite loop" was caught by the user, not
  the loop).
