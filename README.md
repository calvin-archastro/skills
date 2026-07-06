# skills

Skills distilled from an analysis of ~252 real Claude Code sessions / ~2,700 prompts
(two months of daily engineering work: a large production monorepo worked across many
git worktrees, two technical book projects, and assorted side projects). Each skill puts
one empirically successful prompting technique on rails.

## The skills

| Skill | One-liner |
|---|---|
| **`sharpen`** | The entry point. Upgrades a rough ask into the high-success shape — exemplar anchor, scope bounds, acceptance criteria, banned shortcuts, verification plan — before any code is written. |
| **`loop-author`** | Hardens an autonomous run (/loop, /goal, "keep going until") with the nine-part anatomy: work-unit discipline, spec + journal files, exit criteria, quality gates, standing rules, pacing. Includes a full template. |
| **`rca`** | Diagnose-before-fix rails: mechanism + primary evidence + repro test, go/no-go before implementing, banned band-aid fixes, and method-switching when stuck. |
| **`design-options`** | Bounded, numbered decision memos (default top 3 + why + recommendation) instead of open-ended exploration or premature code. |
| **`find-exemplar`** | Find the sibling implementation to mirror before designing anything; switch to exemplar-hunting immediately when an approach gets rejected as hacky/wrong-layer. |
| **`handoff`** | A paste-ready block (problem, root cause, decisions, standing rules, state, next steps, key files) so a fresh session resumes with zero scope loss. |
| **`persist-rule`** | Converts repeated corrections and "always/never" preferences into durable artifacts — lint rule > test > CLAUDE.md > skill > loop standing-rules — instead of session memories. |

## Install

The repo is [`npx skills`](https://skills.sh)-compatible: each skill is a top-level
directory with a `SKILL.md`.

```bash
# interactive: pick skills and detected harnesses
npx skills add calvin-archastro/skills

# everything, into every detected harness, no prompts
npx skills add calvin-archastro/skills --all

# user-level (global) instead of project-level
npx skills add calvin-archastro/skills --all -g

# specific skills / specific harnesses
npx skills add calvin-archastro/skills -s sharpen -s loop-author -a claude-code
npx skills add calvin-archastro/skills -s '*' -a codex -a cursor
```

The CLI installs to whichever harnesses it detects — Claude Code, Codex, Cursor, opencode,
Gemini CLI, Amp, Cline, Roo, Windsurf, Zed, Goose, Droid, and others. Use `--copy` if you
prefer real files over symlinks.

### Manual (Claude Code, no npx)

```bash
git clone https://github.com/calvin-archastro/skills ~/projects/skills
for s in sharpen loop-author rca design-options find-exemplar handoff persist-rule; do
  ln -sfn ~/projects/skills/$s ~/.claude/skills/$s
done
```

For project-scoped installs, symlink into `.claude/skills/` inside the repo instead.

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
