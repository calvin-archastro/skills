---
name: handoff
description: "Use at both ends of a context switch. Writing: the user says 'summarize the problem and plan', 'so I can clear context', 'summarize what you did here', or a long session is about to move to a fresh session or worktree. Resuming: the user says 'pick up where you left off', 'look at the last session', 'continue from the last session', or 'where are we' in a session with no context. Produces a paste-ready handoff block, or rebuilds one from the previous session's transcript and continues from it."
---

# Handoff — carry state across a context switch

Two modes. **Write** a block before the context goes away. **Resume** from one after.

What this prevents: the next session re-deriving state, losing standing rules and half-made
decisions, or opening with a menu of guesses about what to do.

## Write mode — the block

Produce ONE fenced markdown block (so it copies clean) containing, in order:

1. **Problem** — what we are solving and why, one short paragraph. Include the original
   symptom or error verbatim if the task started from one.
2. **Root cause / key findings** — the mechanism, with file:line pointers. Facts, not the
   story of how you found them.
3. **Decisions made** — settled choices the next session must not reopen (label it
   AGREED DECISIONS). Include each rejected alternative with its one-line reason.
4. **Standing rules invoked** — constraints the user stated this session ("never amend",
   "no back compat", "one PR per concern", scope bans) and any standing approval they gave
   ("ship as you go", "don't block on me").
5. **Current state** — one line per item, each with its state and one proof:
   - branch, and what is committed versus only in the working tree;
   - each PR: link, CI status, and whether it is merged, released, deployed, or observed
     working (these are four different states);
   - which tests exist and pass;
   - anything still running: subagents, watchers, dev servers, and where their output goes;
   - questions asked of the user and not yet answered.
6. **Next steps** — ordered, with the first step concrete enough to start on immediately
   ("NOW DO: …" with the exact file and pattern pointers), not "continue the work".
7. **Key files** — the 5–10 paths that matter, each with a phrase on why.

Write the block unprompted when you can see the switch coming: the user says they will
clear, the session is about to be compacted, or the work is moving to another worktree. A
compaction summary is not a handoff; it drops standing rules and unanswered questions.

### Example block

````
```
PROBLEM: bulk export 500s for non-admin members. Original error:
`PermissionError: CanRead violated for Export (member m_412)` from POST /api/exports.
ROOT CAUSE: export controller checks the *requester* against the org policy, but the rows
are fetched with the *job owner's* scope (export_controller.ts:88 vs job_runner.ts:203).
AGREED DECISIONS: fix at the controller (single enforcement point); rejected widening the
job runner's scope (would grant more than the requester is entitled to).
STANDING RULES: no privilege escalation to make reads pass; one PR per concern;
standing approval to push and watch CI on this branch.
STATE:
- branch fix/export-authz; controller change uncommitted in the working tree
- PR #412 open, not merged; CI green except the new repro test (failing on purpose)
- background: CI watcher on #412, output in /tmp/ci-412.log
- unanswered: asked whether admins should also be re-scoped — no reply yet
NEXT: 1) make the repro green by threading requester scope into the fetch (list_exports
does it — same pattern), 2) e2e test for member versus admin, 3) push, re-request review.
KEY FILES: export_controller.ts (enforcement), job_runner.ts:203 (scope bug),
exports.e2e.ts (add case here), policies/export.ts (policy definitions).
```
````

## Resume mode — rebuild the block, then continue

When asked to resume and no block was pasted:

1. **Read the previous session, not only git.** Open the newest earlier transcript for this
   working directory (for Claude Code: `~/.claude/projects/<cwd-slug>/*.jsonl`, excluding
   the current session). Read its tail: the last user asks, the last assistant report, any
   running subagents and unanswered questions. `git status` alone misses decisions, standing
   rules and work in flight elsewhere.
   - If the user named a topic ("the session that was researching X"), grep the transcripts
     for it; the newest session is not always the right one.
   - Say which session you chose in one line: its date and its first ask. A wrong pick is
     then caught before any work starts.
   - List every remaining slice of the work, not only the one the last message mentions.
2. **Re-check what the transcript claims.** A PR it called open may have merged; CI it
   called running has finished. Re-read each PR and CI status now.
3. **Reply with the rebuilt block** in the DONE / IN FLIGHT / NEXT shape, 8 lines or fewer.
4. **Start NEXT without waiting**, unless it needs a merge, a deploy, a force-push, a
   change to live infrastructure, a new PR, hard-to-reverse cleanup, or a decision.
   An approval recorded in an earlier session ("standing approval to push") is listed
   for the user to confirm; it is not acted on until they do.
5. **Do not offer a menu** of what you could do. Ask only when two earlier sessions
   conflict, and then ask about that conflict.

Before starting NEXT, check that another session has not already done it: search recently
merged PRs and sibling worktrees' sessions for the same symptom or file.

## Answering "where are we"

A status answer is the Current state section on its own:

- a numbered list, 8 lines or fewer, grouped as done, in flight, blocked, needs you;
- each item has one proof: a PR link, a CI run, a deployed version, a command's output;
- each in-flight item says when you expect it and what will wake you;
- the first time an internal name appears, add a 3–6 word gloss.

## Rules

- Write for a reader with zero context. No session-local shorthand ("option B", "the second
  approach") without saying what it means.
- Facts over prose. The block compresses; target 60 lines or fewer.
- Prefer flat lists over nested structures, and never put load-bearing detail in a table.
  The block gets pasted into places that mangle both.
- In write mode, the reply is the block and nothing else.
