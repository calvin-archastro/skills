---
name: rca
description: "Use when investigating any failure — 'figure out why', 'ci failed', production/staging errors, flakes, alerts, 'still broken', synthetic test failures, or a pasted stack trace/log. Enforces mechanism-before-patch, primary evidence, and a repro test; bans band-aid fixes. Also use when a debugging exchange has gone 2+ rounds without converging."
---

# RCA — diagnose before fixing, with primary evidence

Transcript analysis: "figure out why X" followed by a user go/no-go was the default debugging
rhythm and almost never produced friction. What *did* produce friction: plausible-sounding
diagnoses without primary evidence, band-aid fixes, and re-describing symptoms instead of
changing the investigation method.

## Rails

1. **Name the mechanism before touching code.** The deliverable of the first pass is a causal
   chain ("X calls Y which assumes Z, but Z rotated"), not a patch. Present it and get a
   go/no-go before implementing — the user catches wrong theories cheaply at this stage.
2. **Primary evidence beats inference.** When a diagnosis rests on reasoning alone, go get the
   ground truth *before* asserting it: cloud logs, metrics dashboards, query insights,
   `ps` output, git blame, the actual failing URL. Disputed diagnoses in the transcripts were
   settled by "pull the metrics", never by re-arguing.
3. **Repro test with exact parameters.** Encode the hypothesis as a failing test with the
   precise fixture the user cares about ("a plain member with no ownership overrides — it
   should still 500"). Twice, the repro test *overturned* the working hypothesis — that is
   the point.
4. **Escalate to an experiment when words stall.** If the user rejects your diagnosis twice,
   or you've rejected your own twice, design a control: a no-op PR to see what CI does, a
   throwaway database with the exact unprivileged role, a second screenshot under changed
   conditions. A control PR broke a three-round stalemate that verbal correction couldn't.
5. **Change the instrument, not the phrasing, when stuck.** After two failed fix attempts on
   the same symptom, stop patching and switch method: introspect the running process, drive
   the app in your own PTY, add keypress/state logging, capture the actual bytes. Every hard
   bug in the corpus (input hang, terminal rendering race) was cracked by a method change,
   never by attempt N+1 of the same approach.
6. **Honest verification claim.** Distinguish "tests pass" from "I ran it live". If you did
   not exercise the real flow (real TTY, real deploy, real API), say so unprompted — the
   user *will* ask "did you actually run it?", and the honest gap-admission was always
   better received than an overclaim.

## Banned fixes (standing rules that earned their place)

- Suppressing, exception-listing, or ignoring static-analysis/type errors ("no analyzer
  exception lists — actually figure out what's wrong").
- Fixing authorization/privacy errors by escalating the acting principal's privileges —
  almost always the wrong solution.
- Branching on error *strings*; use error codes from the backend.
- Patching the symptom at the wrong layer when the mechanism points deeper.
- Editing test files to make a check pass.

## Output shape

Root cause (mechanism + evidence) → repro (test or experiment) → proposed fix with layer
justification → what verification will prove it. Then wait for go/no-go unless the user
already said to fix it — and even then, lead the final report with the mechanism.
