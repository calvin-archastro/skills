# skills

Skills distilled from an analysis of ~252 real Claude Code sessions / ~2,700 prompts
(two months of daily engineering work: a large production monorepo worked across many
git worktrees, two technical book projects, and assorted side projects). Each skill puts
one empirically successful prompting technique on rails.

## Install

```bash
npx skills add calvin-archastro/skills
```

Or symlink the ones you want into your personal skills directory:

```bash
for s in sharpen loop-author rca design-options find-exemplar handoff persist-rule; do
  ln -sfn "$(pwd)/$s" ~/.claude/skills/$s
done
```

## What the transcript analysis found

### Techniques that consistently worked

| Technique | Evidence | Skill |
|---|---|---|
| **Exemplar anchoring** — "look at how X does it", "it's structurally the same as Y", mock-file parity | The single most reliable ambiguity-collapser. Multiple golden episodes where 5–6 abstract corrections failed and one concrete reference converged in one turn. | `find-exemplar` |
| **Diagnose-before-fix** — "figure out why X", then approve the fix | Dozens of successes. Demanding primary evidence ("pull the metrics", "pull query insights") and control experiments broke stalemates that verbal correction couldn't. | `rca` |
| **Hardened autonomous loops** — spec/CSV + journal + one unit per iteration + exit criteria + quality gates | The highest-output workflow observed (a ~130-task burndown shipped as a 133-commit PR; a 14-iteration mock-parity loop; 28 bugs fixed in 25 commits). Under-specified loop prompts got interrupted; the fuller re-issue ran 20+ clean iterations. | `loop-author` |
| **Options-before-implementation** — "top 3 + why", then "do 2" | Bounded option menus led to clean one-word acceptance and near-zero rework. Unbounded "do a full review" with no format constraint led to an exploration tangent and an interrupt. | `design-options` |
| **Skeptical verification** — "did you actually run it live?", "did you edit any test files?" | ~100% hit rate at surfacing real gaps the model had glossed over. | folded into `rca`, `loop-author` |
| **Rule persistence** — turn a correction into a lint rule / style-guide entry / standing loop rule | A file-size lint rule and a privilege-escalation ban folded into a loop prompt held across all later sessions with zero re-litigation. | `persist-rule` |
| **Context handoff** — "summarize the problem and plan so i can clear context", paste into next session | Every observed handoff resumed cleanly with no scope loss. | `handoff` |
| **Pasting raw evidence verbatim** — CI logs, stack traces, review comments with file:line, URLs | Uniformly successful; one pasted URL overturned a wrong in-progress fix. | folded into `sharpen`, `rca` |
| **Tiny imperative closers** — "commit and push a pr", "ci failed" | Near-100% success — but *only* as closers on settled context. | no skill needed |

### Anti-patterns that consistently caused friction

1. **Urgency retries with no new information** — "go", "do it all like i said": three consecutive
   interrupts; broken only by a specific, answerable question.
2. **Abstract architecture complaints** — "this is hacky", "wrong layer" repeated across turns:
   churn until a sibling implementation was named.
3. **Unbounded review/recommendation asks** — no scope or output format → exploration tangent → interrupt.
4. **Rapid-fire sequential addenda** — three corrections sent as separate interrupting messages;
   none landed until batched into one.
5. **Symptom re-description on hard bugs** — "still broken" cycles; broken only by prescribing the
   debugging *method* (own PTY, process introspection) or pasting diagnostics.
6. **Detail volume without semantic anchoring** — a long spec + screenshot still built the wrong
   feature; one pointer to an existing UI element that already did the right thing fixed it.

### The meta-lesson

Terse prompts are fine when the referent is unambiguous (closers, option picks, "ci failed").
Friction appears exactly where the model must *infer an approach you already have in mind* —
and the fix is always the same: name the exemplar, the constraint, the banned shortcut, or the
method. These skills exist to make that naming happen up front instead of via interrupt.
