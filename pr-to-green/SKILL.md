---
name: pr-to-green
description: "Use after pushing a branch or opening a pull request, and when the user says 'ci failed', 'still failing', 'watch ci', 'keep going until green', 'get these PRs out', 'make sure this goes out', 'watch the deploy' or 'tell me when prod goes out'. Carries a change from pushed to green and mergeable, and on request through release and deploy to observed working: arms a background watch, classifies each failure, fixes it at the cause, and reports once with proof. Does not merge unless the user asks."
---

# PR to Green — a pushed change is not a finished one

The most repeated message in real sessions is "ci failed", typed by the user at an agent
that ended its turn on "CI is running". Opening the PR starts this job.

## The states

A change is in exactly one of these. Say which one, with the proof.

| State | Proof |
|---|---|
| pushed | the commit on the remote branch |
| green | the CI run on the pushed head, linked |
| mergeable | the repo's own merge method reports it can merge (a clean merge check does not prove a rebase or squash will apply) |
| merged | the merge commit on the default branch |
| released | the version or artifact that contains it |
| deployed | the version the target environment reports it is running |
| observed working | the behavior seen in that environment: a log line, a screenshot, a query |

"Done" is the last state the user asked for. If they did not say, it is green and
mergeable for a PR, and observed working for a fix to something broken in an environment.

## Loop

1. **Arm a watch after every push.** Use the harness's background or monitor mechanism so
   the run's result wakes you. End a turn only with a watcher armed that will wake you;
   never end on "CI is running" with nothing armed, and do not poll in the foreground.
2. **On red, read the failing job's log before anything else.** Then classify each failure,
   with evidence:
   1. Caused by this change → fix it on this branch.
   2. Already red on the default branch → find the merge that broke it; fix it on its own
      branch and PR.
   3. Flake (red, then green on a rerun of the same commit; or the same test failing on
      unrelated branches) → find the shared state or race; fix it on its own branch and PR.

   "Unrelated" needs that test's history on the default branch as evidence, and it does not
   end the work: the PR is still red. Classes 2 and 3 go to a separate subagent and
   worktree so this branch keeps moving. That fix is pushed to its own branch; it becomes
   a PR if the user approved opening PRs for this work, and is otherwise reported as a
   branch waiting for them.
3. **Fix at the cause.** Not allowed as a way to get green:
   - raising a timeout or a retry count;
   - skipping, quarantining or deleting the failing test;
   - editing a test's assertion to match wrong behavior;
   - rerunning until it passes without knowing why it failed.

   One rerun is fine as a diagnostic for class 3. Use the `rca` skill when the mechanism is
   not obvious from the log.
4. **Verify locally with the focused check, then push.** Run the failing test or lint, not
   the whole suite. CI runs the long suites.
5. **Re-check after every push:** the head CI ran on is the head you pushed, the branch
   still applies by the repo's merge method, the PR description still matches the diff,
   and new review comments have been read. Resolve a conflict against the remote default
   branch, not a stale local copy.
6. **Repeat until green and mergeable, or blocked.** Three rounds that each surface a new
   failure mean the change or the test design is wrong. Stop, name the fault, bring options.

## Through release and deploy

When the ask reaches past the PR ("make sure this goes out", "watch the deploys"):

1. Follow each pipeline stage in order. One background watcher per gate.
2. Report each gate as it passes, with the run link.
3. On a failed stage, find the cause and fix it in code, through a PR. Rerun only the
   failed stage, not the whole chain. Rerunning a deploy or promotion stage is asked for
   by name unless the user asked you to carry out that deploy.
4. For "once X is done, do Y, then Z", arm the watcher for X and act when it fires. Stop
   and report on any red gate.
5. Finish at observed working: name the version the environment runs and the evidence
   that the behavior is right there.

## Authority

- A push to the PR's own branch, a rerun, and a reply on a review thread are in scope once
  the user asked for the PR or for green.
- Ask by name before: opening a new PR the user has not approved, a merge, a force-push,
  a deploy or promotion, changing live infrastructure, skipping a gate, or closing
  someone else's PR.
- Follow the repository's own rules where they are stricter than this skill.

## Report

One report, when the state changes, not a running commentary:

```
PR #412 "Scope exports to the requester" — green, mergeable.
1. CI: <run link> on 4e1f9ab (the pushed head).
2. Fixed on the way: export e2e failed because the fixture user had no org (this change).
3. Split out: flaky `retry_queue_test` → PR #415 (race on a shared temp dir), green.
4. Not verified: not deployed; staging still runs 2.14.0, which predates this.
Needs you: merge #412 and #415.
```

When blocked, the report is the blocker: what failed, the evidence, what you tried, and
the one decision or action that unblocks it.

## Clean up

Stop the watchers you armed and delete the build output you created. List the worktrees
and branches you created for split-out fixes so the user can have them removed once
their PRs merge; remove them yourself only if that was approved. Say what you left
running.
