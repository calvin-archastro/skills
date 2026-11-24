---
name: bug-bash
description: "Use when the user asks to 'bug bash', 'bug hunt', 'dogfood', 'test staging end to end', 'try everything that landed recently', 'test it and fix what you find', or to keep testing and fixing an environment overnight. Drives the real product as a signed-in user, writes a bug list with evidence, fixes each bug in its own worktree and pull request in parallel, re-tests after the fixes deploy, and cleans up what it created."
---

# Bug Bash — use it for real, list what breaks, fix in parallel, re-test

The user otherwise drives this by hand with four prompts in a row: "go test staging end to
end", "spawn subagents to fix the bugs", "keep merging and re-testing", "clean up after
yourself". This is that sequence as one procedure.

## 0. Scope, settled once at the start

State these back in a few lines. Ask only for the ones you cannot find yourself.

1. **Environment** — local stack, staging, or production (read-only unless told otherwise).
2. **What to exercise** — a named feature, or everything merged in a window ("last 48
   hours": list the merged PRs and derive the journeys from them).
3. **Authority** — may you open fix PRs as you find bugs? A yes is standing approval for
   every fix PR in this bash. Without it, each fix stops at a pushed branch. Merging and
   deploying stay the user's unless they name them.
4. **Stop condition** — the bug list is empty after a re-test, or a time or round limit.

## 1. Exercise the product the way a user does

1. Sign in as a real user through the real UI or CLI. No API shortcuts around the surface
   under test, and no mocked backends: an app tested without its APIs is not tested.
2. Walk each journey start to finish, including the unglamorous parts: first run, empty
   states, errors, sign-out and back in, a second user or tab where sharing matters.
3. Capture evidence as you go: a screenshot per step that matters, console and network
   errors, the server log lines for each failure.
4. Tag everything you create (a `bugbash-<date>` prefix) so it can be found and removed.
5. Pause any recording or capture during long waits. Unattended captures fill the disk.

## 2. Write the bug list before fixing anything

`bugs.md` in the working directory, one entry per distinct bug:

```
B3 — Invite link 404s for a user who is already in another org   [severity: high]
Repro: 1) sign in as a member of org A  2) open an invite link for org B  3) 404
Expected: the join screen for org B.
Evidence: screenshot b3-404.png; server log `route not found /invites/…` at 14:02:11 UTC.
Status: open
```

- **Bug, by design, or friction?** A deliberate guard is not a bug. A flow that works but
  costs the user effort goes in a separate friction list, with the same evidence.
- **Dedupe by mechanism.** Two symptoms with one cause are one entry.
- **Check it is still open.** Search open and recently merged PRs before listing it.
- Show the list to the user when it is first complete; continue to step 3 without waiting
  if authority was given in step 0.

## 3. Fix in parallel

1. One bug → one subagent → its own worktree and branch off the remote default branch →
   one PR. Bugs that share a cause share a PR.
2. Each brief is self-contained: the entry from `bugs.md`, the evidence, the suspected
   area, the focused test command, and the bar (a test that fails without the fix).
3. Cap concurrency to what the machine can build at once, and check free disk first.
4. Each fix follows mechanism before patch (the `rca` skill) and is watched to green (the
   `pr-to-green` skill).
5. Update each entry's status as it moves: open → PR #N → green → merged → deployed →
   verified.

## 4. Re-test

After the fixes reach the environment:

1. Re-run every failing journey, not only the step that failed. Confirm the version the
   environment runs includes the fix before judging it.
2. Mark an entry verified only when the original repro now passes there.
3. A new bug found in the re-test is a new entry. Go back to step 3.
4. Stop at the condition from step 0. If the same area keeps producing new bugs for three
   rounds, stop fixing: the design is wrong there. Name the fault and bring options.

## 5. Clean up and report

1. Delete the test data you tagged and created, stop the servers and watchers you
   started, and delete your own build output. List the worktrees and branches you
   created; remove them only if the user approved that. In production, list the test
   data and ask before deleting. Say what you left and why.
2. Report in one screen:

```
Bug bash — staging, features merged Nov 18–20 — 2 rounds
1. Found 7 bugs, 3 friction items. bugs.md and friction.md attached.
2. Verified fixed on staging: B1, B2, B3, B5 (PRs #501–#504).
3. Green, waiting on merge: B4 (#505), B7 (#507).
4. Open: B6 — needs a product decision: should archived threads be searchable?
5. Not exercised: billing flows (no test card in this environment).
6. Cleaned up: 12 `bugbash-1120` threads deleted; 4 worktrees removed.
```
