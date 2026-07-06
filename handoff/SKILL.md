---
name: handoff
description: "Use when the user says 'summarize the problem and plan', 'so I can clear context', 'summarize what you did here', or when a long session is about to move to a fresh session/worktree. Produces a paste-ready handoff block that a context-free session can resume from without scope loss."
---

# Handoff — a paste-ready block for the next session

Observed pattern: the user asks for a summary, runs /clear (or opens another worktree), and
pastes the summary verbatim as the first message of the next session. Every observed handoff
resumed cleanly. The failure mode it prevents: the next session re-deriving state, or losing
standing rules and half-made decisions.

Also observed working: pasting Claude's own analysis into a fresh session with just
"implement this" or "solve this" prepended — write the block so it works that way.

## The block

Produce ONE fenced markdown block (so it copies clean) containing, in order:

1. **Problem** — what we're solving and why, one short paragraph. Include the original
   symptom/error verbatim if the task started from one.
2. **Root cause / key findings** — the mechanism, with file:line pointers. Facts, not
   narrative of how you found them.
3. **Decisions made** — settled choices the next session must not reopen (label it
   AGREED DECISIONS). Include rejected alternatives with the one-line reason.
4. **Standing rules invoked** — any constraints the user stated this session ("never amend",
   "no back compat", "one PR per concern", scope bans).
5. **Current state** — branch, PR URL + CI status, what's committed vs working-tree,
   which tests exist and pass, anything running in the background.
6. **Next steps** — ordered, first step concrete enough to start on immediately
   ("NOW DO: …" with the exact file/pattern pointers), not "continue the work".
7. **Key files** — the 5–10 paths that matter, each with a phrase on why.

## Example block

````
```
PROBLEM: bulk export 500s for non-admin members. Original error:
`PermissionError: CanRead violated for Export (member m_412)` from POST /api/exports.
ROOT CAUSE: export controller checks the *requester* against the org policy, but the rows
are fetched with the *job owner's* scope (export_controller.ts:88 vs job_runner.ts:203).
AGREED DECISIONS: fix at the controller (single enforcement point); rejected widening the
job runner's scope (would grant more than the requester is entitled to).
STANDING RULES: no privilege escalation to make reads pass; one PR per concern.
STATE: branch fix/export-authz, PR #412 open, CI green except the new repro test
(intentionally failing); controller change uncommitted in working tree.
NEXT: 1) make repro green by threading requester scope into fetch (see how list_exports
does it — same pattern), 2) e2e test for member-vs-admin, 3) push, re-request review.
KEY FILES: export_controller.ts (enforcement), job_runner.ts:203 (scope bug),
exports.e2e.ts (add case here), policies/export.ts (policy definitions).
```
````

## Rules

- Write for a reader with zero context — no session-local shorthand ("option B", "the second
  approach") without expanding what it means.
- Facts over prose; the block should compress, not pad. Target ≤60 lines.
- If formatting matters (the user once had to ask "resummarize — formatting got messed up"),
  prefer flat lists over nested structures and never rely on tables for load-bearing detail.
- Offer nothing else in the reply — the block is the deliverable.
