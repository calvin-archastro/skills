# SDLC playbook

The loop observed in every session:

```
research -> numbered options -> "do 1" -> plan or task graph -> "build it"
  -> proof -> review gate -> "commit and push a pr" -> "watch ci" -> "ci failed" -> fix
  -> user merges -> "merged" -> next step on a new branch -> release/deploy -> verify live
```

Each phase: how the user opens it, what to send back, the skill, the bar for done.

## 1. Research

1. Opens: "go look at / go research X and give me options".
2. Do: read the code first, find the sibling implementation, compare with named
   outside systems. Fan out 3 or 4 read-only agents, one per subsystem, when it
   spans several.
3. Send back: findings the user can check (`file:line`), numbered options, one
   recommendation. No code.
4. Skills: `find-exemplar`; `sharpen` when the ask is rough and the build large.
5. Ask clarifying questions only for greenfield work. Otherwise decide and say
   what you decided.

## 2. Design and options

1. Opens: "give me options", "quick design", "let's talk about the shape first",
   "is this the idiomatic way?".
2. Send back: three or four options at most, tradeoffs, one pick. Tables for
   comparisons. A page the user can open when they must scan it; mockups before
   a non-trivial UI build.
3. Skill: `design-options`. Stop after the memo.
4. Rapid "why / what if" questions are an interrogation. Answer each; edit nothing.
5. Objections to pre-empt:
   1. A new mechanism where an existing table, route or helper fits.
   2. Heuristics, arbitrary timeouts or extra heartbeats around work whose owner
      can report its own result.
   3. Product-specific logic placed in a shared platform layer.
   4. Two sources of truth.
   5. A general tool overfitted to one codebase.
   6. Shims, fallbacks and back-compat for things that have not shipped.

## 3. Task breakdown

1. Opens: "turn this into tasks", "break it into smaller tasks".
2. Every task: solution notes, implementation plan, risk, the planned
   end-to-end verification. Verifiable locally. One PR per task, linked to it.
3. Decisions that belong to the user are listed separately with system state,
   problem and tradeoff. Do not pick for them there.
4. Cold-read check on request: one cheap-model agent per task, given only that
   task, returns missing information. One round.
5. The user reviews the plan where it is published and says "i submitted
   feedback". Read it there, revise, republish. Never approve on their behalf.
6. Keep the review URL; it gets asked for again.
7. Hygiene: close tasks whose PRs merged, dedupe, attach new evidence to the
   existing task instead of filing a twin.

## 4. Implementation

1. Opens: "great, build it", "do step 12", "merged, do the next one".
2. Where: the session that owns the context, or a subagent in its own worktree
   for an independent piece.
3. What draws corrections most often:
   1. Not mirroring the existing sibling. Say which one you mirrored.
   2. More change than the problem needs.
   3. Logic in the wrong layer.
   4. Escalating privileges to get past an authorization error instead of
      fixing the rule.
   5. Untyped maps where a schema belongs.
   6. Catch-all error handling, matching on error strings, suppressed checks.
   7. Deleting tests or features to get green.
4. Bug fixes are test-first: failing repro, then the fix.
5. Stepwise plans: one step, one PR. Follow-ups after a merge go in a new PR.

## 5. Testing and proof

1. Ladder: unit tests per new module, focused end-to-end, contract tests, a
   manual run against the worktree's own stack, a browser pass with screenshots
   for UI.
2. Every feature names one canonical end-to-end proof: file, test name, the
   real boundary it crosses.
3. Tests wait on events, never on sleeps. A test failing at its timeout has not
   shown the timeout is too small.
4. New API: a caller-and-owner matrix as table-driven tests.
5. Run what the commit hook will run before declaring done.
6. Benchmarks and evals model what a real user does, and a script aggregates
   the results.

## 6. Review

1. Self review on "review the code": numbered findings, "address", review
   again. Usually two to four rounds.
2. Independent review before a PR on anything non-trivial: a fresh subagent,
   template T2 in `briefs.md`.
3. Adversarial and persona reviewers for design, copy, UX and visuals, looped
   until the stated bar passes; ask for a before/after table.
4. Third-party review comments are wrong until proven. Reply to the unproven
   ones. Do not resolve threads yourself.
5. Third round still finding new issues: say the design is wrong, bring options.

## 7. Commit and PR

1. Only on the user's words. See the git table in `decoder.md`.
2. Before pushing: is this branch's PR already merged? Then new branch, new PR.
3. Description: the problem as a concrete story first, then before and after
   mechanics, scope, risk, user impact, how it was tested, follow-ups. Refresh
   it after every later push.
4. Follow the repo's draft and label conventions; "ready" means ready for the
   user's review.

## 8. CI

1. After any push, someone watches the run to completion.
2. Red: read the failed log, classify real bug, test race or environment, fix
   the cause. No retries, skips or timeout bumps.
3. A flake not caused by the change gets its own branch, subagent and PR.
4. Conflicts: rebase onto the remote default branch, resolve, force-with-lease.
5. Report "green" with the head sha and link, and say what CI did not cover.
6. CI speed is a project of its own: measure runs first, sort fixes by payoff,
   one PR per fix, in parallel.

## 9. Merge, release, deploy

1. The user merges. After "merged": rebase siblings, close the task, start the
   next step.
2. Releases and staging deploys go through CI on the user's word; watch them.
   Merged is not released: check the fix commit is in the release.
3. Production promotion needs the user's word each time.
4. Done means deployed and seen working in logs or monitoring.

## 10. Production, incidents, RCA

1. Opens: a screenshot, an alert, a pasted trace, "figure out why prod ...".
2. Skill: `rca`. Look at the environment the user named.
3. Evidence before theory. If the logs cannot show the mechanism, add logging
   and say so.
4. Numbered findings with evidence; the user answers by number.
5. One fix per branch with a regression test. Each incident class ends with a
   detection (alert, metric or lint), then log evidence that it stopped.
6. Reads are free. Mutations are the user's: give exact commands.

## 11. Long unattended work

1. Skill: `loop-author` before any loop or goal.
2. The prompt carries: one unit per iteration, one commit or PR per unit, a
   test per unit, a gate, a journal file, rebase each iteration, what must not
   happen between iterations, and the exit condition last.
3. A goal names the end state and the invariant: existing tests stay green and
   are not edited.

## 12. Docs, copy, design

1. Mock first, build, screenshot, persona review, then expect several rounds of
   redlines.
2. Analyses and explainers go to a page with a summary on top.

## 13. Context and cleanup

1. Before a session clears or compacts: `handoff` skill.
2. Resume by reading the previous transcript, not by re-deriving.
3. Leftover staged files in a worktree: check against the default branch; if
   merged, reset; if not, report.
4. Remove dead worktrees and build output you verified are unused. List what
   you left and why.
