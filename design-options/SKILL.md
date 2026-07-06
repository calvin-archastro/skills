---
name: design-options
description: "Use when the user asks for recommendations, design options, strategies, a design review, 'is there a better way', or 'let's discuss the shape first' — any request for judgment before implementation. Produces a bounded, numbered decision memo instead of open-ended exploration or premature code."
---

# Design Options — bounded menu, then a one-word go

The evidence: "give me the top 3 and why" and "let's discuss the cli shape first" produced
clean decision→implementation pipelines with near-zero rework (the shape-first CLI port ran
dozens of turns with no design corrections). The failure case: an unbounded "do a full pass
design review and come up with recommendations" sent Claude into environment setup and
exploration until the user killed it with nothing delivered.

## Rails

1. **Deliver the memo before touching anything.** No dev servers, no big refactoring
   experiments, no "let me first fix the build" detours. Read what you need, then write.
   If exploration is genuinely required, timebox it and say what you're checking.
2. **Bounded count.** Default to 3 options unless the user named a number. Prioritize —
   an unbounded list is a dodge.
3. **Number or letter every option** so the user can answer "do 2" or "A". Terse picks off
   an enumerated menu were ~100% reliable; terse picks against un-enumerated prose were not.
4. **Each option carries:** what it is (2–4 sentences), the tradeoff that actually matters,
   and rough cost. Ground options in the real codebase — name the files/modules affected,
   mirror existing patterns where one exists.
5. **Recommend one, and say why** in a sentence. The user usually accepts the recommendation
   or picks the adjacent one; never present a neutral menu with no opinion.
6. **Anticipate the follow-ups**: "what problem does this solve?" and "doesn't X already do
   this?" killed redundant abstractions twice in the corpus. For each option, check whether
   an existing mechanism already provides it — if yes, say so instead of listing it.
7. **Stop after the memo.** Implementation starts when the user picks. If they picked with
   an added constraint ("do 1 — make sure tests repro this scenario first"), that constraint
   becomes part of the acceptance criteria.

## Example memo

```
Realtime sync for the settings panel — 3 options:

1. Extend the existing poller (sync/poller.ts) — smallest change, one code path stays.
   Tradeoff: latency stays at the 30s interval. ~0.5 day.
2. Push over the event bus we already run for audit events (bus/consumer.ts) — realtime,
   reuses delivery guarantees we've already hardened. Tradeoff: new topic + a backfill
   story for reconnects. ~2 days.
3. Dedicated webhook receiver — most flexible for third parties later. Tradeoff: a new
   surface to secure and deploy, and it duplicates what the bus already gives us. ~4 days.

Recommendation: 2 — realtime without a new surface; 3 is 1 mostly re-solved by existing infra.
(Checked: nothing existing already pushes settings changes — the audit topic carries only
mutations, not reads, so option 2 needs the new topic either way.)
```

The last parenthetical matters: it pre-answers "doesn't X already do this?" — the question
that killed redundant designs twice in the transcripts.

## Contrast pair from the transcripts

- Worked: "suggest 3 things we could do to really improve the language/debugging experience…
  suggest the top 3 and why" → structured, scoped memo, clean pick.
- Failed: "Do a full pass design review on the UX and the features and come up with a set of
  recommendations" → exploration tangent, interrupted, zero output.

The difference is the bound and the required justification — enforce them even when the
user's ask has neither.
