# skills

Skills distilled from an analysis of ~252 real Claude Code sessions / ~2,700 prompts
(two months of daily engineering work: a large production monorepo worked across many
git worktrees, two technical book projects, and assorted side projects). Each skill puts
one empirically successful prompting technique on rails.

They are revised from use. The November 2026 pass re-read three more weeks of sessions
(238 sessions, about 3,000 prompts) for two things: what the user still had to correct
after a skill ran, and what the user kept typing by hand that a skill should have covered.

## The skills

| Skill | One-liner |
|---|---|
| **`sharpen`** | The entry point. Upgrades a rough ask into the high-success shape before any code is written: exemplar anchor, scope bounds, authority asked once ("ship as I go?"), acceptance criteria, banned shortcuts, a verification plan on the real surface, and what runs in parallel. |
| **`loop-author`** | Writes the contract for an autonomous run (/loop, /goal, "keep going until") as a file, launched by a one-line pointer: work unit, spec and journal, gates, ship authority, standing rules, blocked rule, housekeeping, exit. Short forms for count targets ("till 250") and conditional chains ("once X, do Y"). |
| **`rca`** | Diagnose-before-fix rails: start from current state, inventory the failures, mechanism with primary evidence, bug versus by-design, a repro that fails before the fix and passes after, flake / PR-caused / broken-on-main triage, alert triage, banned band-aids, and a report that covers onset, path to live and the detection gap. |
| **`design-options`** | Bounded, numbered decision memos: what exists today, options at more than one layer (smallest change, deeper model change, new surface), one recommendation (combinations allowed), rejected options, and open decisions with defaults so the answer is one line. |
| **`find-exemplar`** | Check whether the requested behavior already exists, then find the sibling to call, extract from or mirror, at the right layer. Reports `Exemplar:` and `Deviations:`. Switches to exemplar-hunting the moment an approach is rejected as hacky, wrong-layer or overfitted. |
| **`handoff`** | Both ends of a context switch. Write: a paste-ready block (problem, root cause, decisions, standing rules, state with proof, next steps, key files). Resume: rebuild that block from the previous session's transcript, re-check it, and continue without offering a menu. Also the shape of a "where are we" answer. |
| **`persist-rule`** | Converts repeated corrections, repeated requests and "always/never" preferences into durable artifacts: an existing linter extended > test > CLAUDE.md > skill > loop standing rules. The check is shown failing on the offence before it is trusted. |
| **`tweet-reply-review`** | Review a draft or convert notes/essays into a tweet or thread in the author's live voice. Ranks internally, prints a plain-language call + the post. |
| **`beautify-page`** | Marketing/landing pages with anti-AI-slop craft: token plan, distinctive type/color, one signature, purposeful motion. Build, polish, or meta-prompt modes + paste-ready prompt pack. |
| **`visualize-data`** | Data → claim → chart → designed self-contained HTML. Newsroom / visual-essay / scale-poster / explainer registers, FT chart lookup, anti-dashboard slop. Research + paste prompts included. |
| **`omarchy-plugin`** | Author/review/publish Omarchy Quickshell plugins: clone-a-builtin, `qs.Ui` contract, QML untrusted-content (AutoText remote images), Process/argv secrets, marketplace listing. |
| **`overseer`** | One session runs the others: decode terse prompts, route them to the owning worktree session (Herdr) or a subagent, attach the standing rules to every brief, inspect the repo for its default branch, agent harness and standing worktrees, open or recycle a worktree session per feature, hold the proof and review bar, and report back in one numbered screen. Includes a prompt decoder, per-phase SDLC playbook, brief templates, and a read-only fleet snapshot script. |
| **`pr-to-green`** | A pushed change is not a finished one. Arms a background CI watch after every push, classifies each failure (this change, already red on the default branch, flake), fixes at the cause, and reports once with proof. On request, follows release and deploy through to observed working. Does not merge unless asked. |
| **`bug-bash`** | Use the real product as a signed-in user, write a bug list with evidence, fix each bug in its own worktree and PR in parallel, re-test after the fixes deploy, clean up the test data. |
| **`product-video`** | A recorded video of a product journey, made in the [Splice](https://github.com/ArchAstro/splice) editor, of one of four types: product demo, friction log, tutorial, or release clip (60 s or less). Scenario and beat budget storyboarded in Splice, a screen take with anchor lines and checks, then a separate narration take read from a full numbered transcript and cut line by line onto the beats — intro, face in frame, click zooms, callouts, fades and persona handoffs. Files live in the project's `docs/videos/<type>/` and run on local or staging. Includes templates, Splice recipes and validated scene files. |

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
npx skills add calvin-archastro/skills -s sharpen -s loop-author -s pr-to-green -a claude-code
npx skills add calvin-archastro/skills -s '*' -a codex -a cursor
```

The CLI installs to whichever harnesses it detects — Claude Code, Codex, Cursor, opencode,
Gemini CLI, Amp, Cline, Roo, Windsurf, Zed, Goose, Droid, and others. Use `--copy` if you
prefer real files over symlinks.

### Manual (Claude Code, no npx)

```bash
git clone https://github.com/calvin-archastro/skills ~/projects/skills
for s in sharpen loop-author rca design-options find-exemplar handoff persist-rule tweet-reply-review beautify-page visualize-data omarchy-plugin overseer product-video pr-to-green bug-bash; do
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
| **Anti-slop design rails** — ban defaults (Inter/purple), plan tokens before code, one signature + orchestrated motion | Opus-era frontend aesthetics cookbook + community landing prompts; distinctive landings without generic SaaS template. | `beautify-page` |
| **Claim-first data pages** — quoteable sentence before SVG; chart type from a vocabulary; newsroom anatomy not dashboard chrome | Year-end viz lists + FT Visual Vocabulary + Datawrapper/OWID/Pudding craft; stops Chart.js KPI-card slop. | `visualize-data` |

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
