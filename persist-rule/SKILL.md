---
name: persist-rule
description: "Use when the user corrects the same thing a second time, states a standing preference ('never amend', 'always look up by the stable id', 'keep files under 500 lines'), or says 'update your instructions' / 'encapsulate this rule somewhere'. Converts the correction into the most durable enforceable artifact instead of a memory that dies with the session."
---

# Persist Rule — corrections become artifacts, not memories

The most durable wins in the transcript analysis came from converting a one-off correction
into a machine-checked or document-anchored rule: a 500-line-cap lint rule that every later
session self-enforced; "gloss the term as you introduce it" added to a style guide and never
violated again; "never fix an authorization error by escalating privileges" folded into a
standing loop rule that held across ~30 unattended iterations. The failure mode it prevents
is real: "i thought i told you to always do lookups by the id" — a rule stated verbally in a
prior session, regressed silently later.

## Procedure

1. **Recognize the trigger.** A second correction of the same class, an "always/never" from
   the user, or visible frustration at a repeat offense — treat all three as "this rule wants
   to be persisted", and propose it proactively; don't wait to be told.
   - The repeat may have happened in another session. "I thought we fixed this" and "I
     thought I told you" mean it did. Search recent sessions and merged PRs for the earlier
     instance, then persist the rule this time.
   - A recurring *request* counts too. If the user types the same instruction at the start
     of the same kind of task every time ("use my voice skill when writing as me", "watch CI
     after you push"), it belongs in the skill or the project instructions for that task.
2. **Pick the most durable home that can hold it.** In descending order of preference:
   - **Lint rule / CI check** — for anything mechanically checkable (file size caps, banned
     APIs, no test-file edits, import layering). Strongest: self-enforcing forever.
     Extend the linter the toolchain already runs (a clippy lint, an ESLint rule, a
     credo check) so the command people already run finds it. Write a new standalone
     script only when no existing linter can host the rule, and wire it to an automatic
     caller (CI, a hook) in the same change; otherwise nothing runs it.
   - **Test** — for behavioral invariants ("a resource provisioned on behalf of a member is
     owned by that member").
   - **CLAUDE.md** (project or user level) — for judgment rules a machine can't check
     ("prefer tool X's conventions, fall back to Y"; "never amend pushed commits"; "reuse
     existing pipelines, no parallel paths").
   - **The relevant skill** — if the rule belongs to a workflow a skill already governs
     (style rules → the writing skill's style guide; TUI rules → the TUI dev skill).
   - **Standing-rules block of the active loop prompt** — for rules scoped to a running
     autonomous campaign; restate the amended block so it appears in every future iteration.
3. **Implement it now**, in the same turn as the fix it accompanies — a rule proposed but not
   written is a memory, not an artifact.
   - Prove the check bites: show it failing on the offending code and passing on the fix.
   - A check that only tests format or ritual, and blocks work without catching the
     behavior, is worse than no check. Tie the rule to the failure it prevents.
4. **Audit backwards when the rule invalidates prior work.** When a rule is born from a
   systematic mistake, sweep what already shipped under the old behavior (one new ban
   required re-auditing every PR an autonomous loop had produced). Offer this explicitly.
5. **Cite the rule when it binds.** In later work, name the constraint you're honoring
   ("keeping this under the 500-line cap → splitting the module") so drift is visible.

## Worked example

User (after a violation): *"why did you amend?? never amend"*

Same turn, alongside the apology/fix:

1. Home: CLAUDE.md (judgment rule — not mechanically checkable).
2. Write it:
   ```
   ## Git
   - Never amend or force-push a commit that has been pushed. Add follow-up commits;
     rebase only when explicitly asked. (Amending rewrites history reviewers have seen.)
   ```
3. Sweep backwards: check whether any open PR already contains an amended pushed commit.
4. Later sessions cite it: "adding a follow-up commit rather than amending, per CLAUDE.md."

## Wording the rule

State it as ban + correct alternative + one-line why — the form that worked in practice:
"don't condition error handling on strings — use codes sent from the backend (strings are
locale/format-fragile)". A ban without an alternative invites the next-nearest workaround.
