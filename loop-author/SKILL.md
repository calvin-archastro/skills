---
name: loop-author
description: "Use before starting, or when writing, any autonomous run: /loop, /goal (including a count target such as 'keep going till 250' or 'do another 100 rounds'), 'plan it then run a goal', 'keep going until', 'keep testing and fixing', 'repeat till it gets done', 'work on this all night', 'once X is done do Y then Z'. Also use when writing or reviewing a skill that will be run under /loop, and when a running loop is drifting, pacing badly, re-reporting the same block, or shipping violations. Writes a loop-contract file (work unit, journal, gates, ship authority, standing rules, exit) and a one-line /loop pointer to it."
---

# Loop Author — write the contract before the run starts

An under-specified loop gets interrupted and re-issued. A loop with a written contract runs
dozens of iterations clean. Every part below is here because its absence broke a real loop.

## Three shapes of run

| Shape | The user types | What to write |
|---|---|---|
| **Contract file** (default) | "plan this and loop on it", a task list, overnight work | a loop-contract file, then `/loop Read and follow <path> exactly` |
| **Skill as contract** | `/loop /some-skill` | nothing new: check the skill has the parts marked † below, and fix the skill if not |
| **Count or chain** | `/goal keep going till 250`, "once X deploys, do Y, then Z" | the short forms at the end of this file |

A slash command runs at once, so this skill is used at authoring time: when the plan is
being written, before the user types `/loop`. If a loop is already running without a
contract and is drifting, stop and write one.

## The contract file

Write `docs/specs/<topic>-loop.md` (or the project's equivalent), commit it if the user
has approved commits, and launch with a one-line pointer:

```
/loop Read and follow docs/specs/<topic>-loop.md exactly. Resume from the first unchecked
task in the spec and the latest journal entry.
```

A contract in a file survives context clears, can be amended mid-run, and is the same on
every iteration. A contract pasted into the prompt drifts as it is re-issued.

The file has these parts:

1. **Work unit.** † Exactly one unit per iteration, with its shipping shape: "one task per
   iteration", "one PR per issue", "one commit per fix". This is what makes iterations
   auditable and safe to interrupt.
2. **Durable state.**
   - A **spec file** the loop consumes (a task list); check items off in the file.
   - A **journal file** with one entry per iteration: what was done, decisions made, how to
     use the result, what was ruled out. Number the entries.
   - On resume, the first unchecked task plus the latest journal entry are the state. Do
     not rely on context memory.
3. **Scope partitions.** If the work spans areas (languages, services, test suites), list
   them and say how the loop rotates through them. A loop without this stays in the area
   it started in.
4. **Quality gates per iteration.** † Name them: build and typecheck, lint, the focused
   tests, one end-to-end proof of the unit, and for risky work a review by a fresh
   subagent with "no blocking findings" as the bar.
5. **Ship authority.** † Say exactly which of these the loop may do without asking, and
   where: commit, push, open a PR, mark it ready, merge (and by which method), tag or
   release, deploy, change live infrastructure, touch other repositories. A loop with no
   authority line either holds every commit waiting for a "yes" that never comes, or
   guesses. Anything not listed is asked for once, by name. List only what the user
   actually granted, and where the repository's own rules are stricter, they win.
6. **Standing rules.** † A named, amendable block of hard bans. Start from:
   - the user's own global rules, copied in verbatim (a loop that cannot see them breaks
     them: for example, it converts PRs to draft when the user's rule says never to);
   - never fix an authorization failure by escalating the caller's privileges;
   - no matching on error strings; no test edits to make a check pass;
   - no amending or force-pushing pushed commits;
   - do not reopen an agreed decision.

   Fold each mid-run correction into this block the moment it is given, so it holds on
   every later iteration.
7. **Agreed decisions.** Settled design choices, each with the rejected alternative in a
   line, so iterations do not reopen them.
8. **Design values.** The values the user otherwise injects by interrupting: fix the
   abstraction and not the call sites, reuse existing pipelines, no special cases in
   shared code, keep files under the size cap.
9. **Pacing.** † Work continuously. Sleep only when blocked on an external event, and say
   on what and for how long. Once the focused tests pass, push and let CI run the long
   suites; do not wait on a full local run.
10. **Blocked.** † When one unit needs the user: ask once, with the exact decision, then
    move to the next independent unit. Do not repeat the same block on every tick, and do
    not pile further work on top of the blocked unit.
11. **Housekeeping each iteration.** † Stop the watchers, servers and processes the
    iteration started; delete the build output it created; check free disk before a
    build. Removing worktrees or branches is in the contract only if the user granted
    it. A loop that leaks processes or fills the disk stalls every session
    on the machine.
12. **Exit.** † Compound and checkable: "every task checked off, all gates green on the
    final commit, the journal has a closing summary; or stop and report if blocked on a
    decision with no independent unit left". If the real units run out before a numeric
    target, stop and report the shortfall with the remaining candidates. Do not pad, and
    do not ship early and call it done.
13. **Named skills and tools.** Which project skill handles fixes, which log and metric
    sources to use, when to dispatch subagents.

## Procedure

1. Note which parts are already settled in the conversation. Draft the spec and journal
   files if they do not exist.
2. Write the contract file with every part. Length is fine here: completeness beats
   brevity, the opposite of an interactive prompt.
3. Ask for ship authority once if the user has not given it. This is the only question
   worth interrupting for before launch.
4. Show the user the contract and the one-line pointer, or launch if they already said to.

## Template

```
# Export pipeline — loop contract

WORK UNIT: one task from docs/specs/export-pipeline-tasks.md per iteration, in order.
One commit per task. Check the task off in the spec when its gates pass.

STATE: journal each iteration to docs/journals/export-pipeline.md as a numbered entry
(what you did, decisions, how to use it, gotchas). Resume from the first unchecked task
and the latest entry.

SCOPE: rotate api → worker → cli; do not do two tasks in a row in the same area while
another area has open tasks.

GATES per iteration: build and typecheck green; lint clean; the task's focused tests; one
end-to-end test that exercises the task; for schema or concurrency changes, a fresh
subagent review with no blocking findings.

SHIP AUTHORITY: commit and push to feat/export-pipeline; keep PR #812 ready for review and
its description current. Do not merge, tag, or touch other repositories.

STANDING RULES (fold my corrections in here):
- <the user's global rules, verbatim>
- never fix an authorization failure by escalating the caller's privileges
- no error-string matching; no test edits to make checks pass; never amend pushed commits

AGREED DECISIONS (do not reopen): storage is JSONL, not sqlite (revisit past 1M rows);
the CLI verb is `export`, not `dump`.

DESIGN VALUES: reuse existing pipelines; fix the abstraction, not the call sites; no
special cases in shared code.

PACING: no sleeping between tasks. After focused tests pass, push and let CI run the rest.

BLOCKED: ask once with the exact decision, then take the next independent task. Do not
repeat the block each tick.

HOUSEKEEPING: stop what you started; remove build output of finished work; check free disk
before building.

EXIT: every task checked off, gates green on the final commit, closing journal summary.
Or: no independent task left and a decision is pending — stop and report.
```

## Short forms

**Count target** (`/goal keep going till 250`, "do another 100 rounds"):

```
Number each unit in <log file> (one entry per unit: what, why, evidence). EXIT at entry N.
If real candidates run out first, stop at the last real one and report the shortfall and
what remains. One unit per commit. <ship authority line>. <standing rules>.
```

The numbered log is what makes "till 250" checkable and "another 100" resumable.

**Conditional chain** ("once staging deploys, deploy prod, then the CLI"):

```
Gate 1: <event> — watcher: <how you will know>. Then do: <action>.
Gate 2: <event> — watcher: … Then do: …
Report each gate as it passes, with its link. On a red gate: stop, report, do not
continue the chain and do not restart it. <which actions need a yes by name>.
```

A deploy or promotion in the chain runs only because the user named it in the ask. One
background watcher per gate. End a turn between gates only with the next watcher armed;
do not poll in the foreground.

**Until-green or until-fixed** ("keep going until CI is green", "keep testing and
fixing"): this is a loop with a one-line contract. Write the exit, the authority and the
blocked rule, at least. For CI, the `pr-to-green` skill is that contract.

## Failure modes this prevents

- **No journal → amnesia** between iterations and after a context clear.
- **No exit → babysitting**: dozens of empty ticks until the user kills it.
- **No ship authority → a stalled loop** holding commits and asking the same question.
- **Missing standing rules → the same violation at scale**: one loop shipped several
  privilege-escalating "fixes" before the ban was added, and every PR needed re-auditing.
- **Stopping short of a numeric target** and opening the PR anyway.
- **Stray background processes and a full disk**, noticed by the user and not the loop.
