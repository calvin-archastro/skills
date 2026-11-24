---
name: rca
description: "Use when investigating any failure or unexplained behavior: 'figure out why', 'what's going on', 'dig into', 'ci failed', 'X failed, fix', staging or production broken, an alert (pasted or 'active alerts'), a flaky PR, a CI or test slowdown, a performance regression, CI running lanes nobody expected, a deploy or release failure, a synthetic test failure, or a screenshot, pasted log or stack trace. Enforces a current-state check, mechanism before patch, primary evidence, flake-versus-regression triage, and a repro that fails before the fix and passes after; bans band-aid fixes. Also use when a debugging exchange has gone 2+ rounds without converging."
---

# RCA — diagnose before fixing, with primary evidence

What produces friction in real debugging sessions: a plausible diagnosis with no primary
evidence, a band-aid fix, a report built on stale state, and calling something a bug that is
working as designed.

## Rails

1. **Start from current state.** Before diagnosing, and again before every status report and
   every push, re-read:
   - the PR head and its CI status (the head may have moved since the failure was reported);
   - the default branch since the failure (someone may have landed the same fix);
   - open PRs, recently merged PRs and other sessions' work on the same symptom or file.
     If someone already fixed or investigated it, verify and build on that. Do not redo it.

   Never repeat a status you have not re-read in this turn.
2. **Inventory the failures.** List every distinct failure first: symptom, onset, owner. One
   mechanism per row. A report that stops at the first root cause leaves the second failure
   for the user to find.
3. **Name the mechanism before touching code.** The deliverable of the first pass is a causal
   chain ("X calls Y which assumes Z, but Z rotated"), not a patch. Present it and get a
   go/no-go before implementing, unless the ask already said to fix it (see "When to
   wait"). A wrong theory is cheap to catch at this stage.
4. **Primary evidence beats inference.** When a diagnosis rests on reasoning alone, get the
   ground truth before asserting it: cloud logs, metrics, query plans, `ps` output, git blame,
   the actual failing URL. A disputed diagnosis is settled by pulling the metrics, not by
   arguing it again.
   - **Get it yourself.** Use the CLIs, logs, browser and remote shells you already have
     access to before asking the user to run something. Hand over a step only when it needs
     a person (a passkey, a password prompt, an approval), and then give one exact command.
   - **Pin what the evidence is about** before reasoning from it: the environment or
     namespace, the instance, pod or host that acted, the exact resource ID (copy it, do not
     retype it), and the units and timezone of every timestamp.
   - **Find which hop emitted each error.** For an HTTP status, check the load balancer, the
     gateway and the app. The hop that reports an error is often not the one that caused it.
   - **A deploy in the same window is a lead, not a cause.** Count the failures per hour
     or day for a period before and after it, and count how many deploys had no such
     failures. Blame the deploy only if the rate changes at its time. Backtest a changed
     alert or threshold against a week or more of historical data.
5. **Bug, by design, or someone else's action?** Before calling a finding a bug, check
   whether it is documented intent (a code comment, a commit message, a deliberate guard) and
   whether another legitimate actor caused it (another daemon, host, deploy or user). Report
   a working-as-designed finding as that. The fix may belong in the test or the alert, not
   the product.
6. **Repro that fails before the fix and passes after.** Encode the hypothesis as a failing
   test with the exact fixture the user cares about ("a plain member with no ownership
   overrides should still get a 500"). Then show red on the old code and green on the new:
   revert only the fix and rerun. A repro that passes either way proves nothing, and a repro
   that overturns the hypothesis has done its job.
   - For a performance or rate problem, measure the fix against the baseline and say what
     share of the regression it explains. "The fix is real but covers 9% of the slowdown" is
     a finding; the rest is still open.
7. **Escalate to an experiment when words stall.** If the user rejects your diagnosis twice,
   or you have rejected your own twice, design a control: a no-op PR to see what CI does, a
   throwaway database with the exact unprivileged role, a second screenshot under changed
   conditions.
8. **Change the instrument, not the phrasing, when stuck.** After two failed fix attempts on
   the same symptom, stop patching and switch method: introspect the running process, drive
   the app in your own PTY, add keypress or state logging, capture the actual bytes. If the
   logs cannot show the mechanism, adding that logging is a valid first deliverable.
9. **Label every claim.** Mark each one **observed** (cite the run, log line or query) or
   **hypothesis**. If the mechanism is unproven, say so and make no product patch.
10. **Honest verification claim.** Report a fix as exactly one of: merged, released,
    deployed, or observed working. Name the version the target environment runs and the
    evidence (log line, screenshot, query). Do not say "fixed" below "observed working",
    and do not say CI is fixed before the run on the pushed head is green. Say unprompted
    what is not proven yet and which run will prove it.

## Flake, PR-caused, or broken on the default branch

Classify a CI failure before fixing it. The three classes have different fixes.

1. The same failure appears on unrelated branches or on the default branch → broken there.
   Find the merge that did it.
2. Red, then green on a rerun of the same commit → flake. Find the shared state or the race.
   Do not retry it or stretch its timeout.
3. Fails only on this PR and reproduces → PR-caused.
4. Before blaming the runner or the environment, list what merged in that area since the
   last green run.
5. When a test fails locally, run it on a clean checkout of the default branch to separate
   pre-existing failures from yours.
6. "Unrelated" and "flaky" are claims that need evidence: that test's history on the default
   branch. Neither one ends the work. The PR is still red, so fix the flake or the broken
   default branch on its own branch and PR.

## Alert triage

For "check alerts" or several alerts at once:

1. List every open alert.
2. Label each one: real, noise, or outside our control (a customer-side or provider-side
   condition). Say what evidence decided it.
3. Real → mechanism and fix, as below. Noise → propose retuning or deleting the alert,
   since an alert with no action attached trains people to ignore the real ones.
4. Fix the clear-cut ones in one pass, through the repository's alert config or
   infrastructure code. A change made directly to a live system is asked for by name.
   Ask about the ones that need a product call.

## Banned fixes

- Suppressing, exception-listing or ignoring static-analysis or type errors.
- Fixing an authorization or privacy error by escalating the acting principal's privileges.
- Branching on error strings. Use error codes from the backend.
- Patching the symptom at the wrong layer when the mechanism points deeper.
- Editing a test so that wrong behavior passes. Changing a test that asserts the wrong
  thing is allowed when you show evidence of the intended behavior (rail 5).
- Raising a timeout or adding a retry for a failure that is not transient. A retry is right
  only for a proven transient error from a dependency you do not control (an external API's
  5xx), and the report says what proved it transient.
- Satisfying a check that tests format or ritual and not behavior. Propose removing or
  demoting it.
- Teaching a shared or platform layer one caller's names, fields or special cases. On the
  third special case of the same kind, stop and design the general rule, then show it
  covers every case found so far.

## Output shape

Lead with a one-line verdict in bold. Then, numbered, in this order:

1. **Root cause** — the mechanism, each claim marked observed or hypothesis, with evidence.
2. **Onset** — when it started and what changed then (a merge, a deploy, an external
   provider, traffic). Give a short timeline in UTC when ordering matters.
3. **Ruled out** — what you checked and eliminated, one line each.
4. **Repro** — the test or experiment, red before and green after.
5. **Fix** — the proposed change and why that layer.
6. **Path to live** — what makes the fix take effect (merge, deploy, config apply, image
   build), the first real-world run that will prove it, and any records already damaged
   that the fix will not repair.
7. **Detection gap** — why CI, alerts or logs did not surface it, and the change that would.

**When to wait.** If the ask was only "figure out why", stop here for a go/no-go. If the ask
already says to fix it ("and fix", "fix it", "make it work"), the go is given: implement,
verify, then report in this shape with the mechanism first. Still stop before a change to
live infrastructure, a merge, a force-push or a product choice. Do not ask again for a kind
of step the user already approved in this session; that never covers those four, which are
approved one at a time.

### Example

```
**Retries duplicate jobs; the fix is at enqueue, and 3 jobs need manual cleanup.**

1. ROOT CAUSE (observed): the worker's dedupe key includes the enqueue timestamp, so every
   retry looks new and the original is never cancelled (worker.ts:141).
   Evidence: 3 active rows for job 8123 in staging (query attached).
2. ONSET: 14:02 UTC Tuesday, the deploy that added `enqueued_at` to the key (commit 4e1f).
3. RULED OUT: queue redelivery (broker shows one delivery per message); clock skew.
4. REPRO: test added — enqueue, fail once, retry → asserts one active row.
   Red on main (2 rows), green with the fix, red again with the fix reverted.
5. FIX (proposed): dedupe on (queue, payload_hash) at the enqueue layer. A cleanup sweep
   would patch the wrong layer: duplicates would still race before each sweep.
6. PATH TO LIVE: merge + worker deploy. Proof: next retry in staging leaves one active row.
   Jobs 8123, 8130, 8141 already have duplicates and need a one-off cancel.
7. DETECTION GAP: no alert on active rows per job. Propose one at > 1.
Go/no-go?
```
