---
name: design-options
description: "Use when the user asks for options, recommendations, strategies, a design or design review, 'what's the best way', 'how can we better…', 'let's talk about better ways', 'is there a better way', 'how should we improve this UX', or wants the shape discussed before code, including after an incident. Produces a bounded, numbered decision memo: what exists today, options at more than one layer, one recommendation (a combination is allowed), and open decisions with defaults, so the user can answer in one line."
---

# Design Options — bounded menu, then a one-line go

A numbered, bounded memo gets a one-line pick and little rework. An unbounded "do a full
design review" sends the agent into setup and exploration with nothing delivered.

## Rails

1. **Deliver the memo before touching anything.** No dev servers, no refactoring
   experiments, no "let me first fix the build". Read what you need, then write. If
   exploration is required, timebox it and say what you are checking.
2. **Open with "What exists today".** 3–5 bullets with file references: the mechanism that
   already covers part of this, the precedent, the gap. This often changes the question
   ("the mechanism exists; nothing enforces it"). Before proposing a new mechanism, search
   the organization's other repos that you can list (a code search by keyword, a few
   minutes) for one that already does it, and name it or say none was found.
3. **For an incident-driven ask, open with the failure chain.** Number it: trigger → each
   check that missed → symptom. Map each option to the links it breaks.
4. **Bounded count.** Default to 3 options unless the user named a number. An unbounded list
   is a dodge.
5. **Span the layers.** A menu of three fixes at the same layer gets thrown out and reframed.
   - Option 1 is the smallest change that solves the stated problem.
   - At least one option changes the underlying model, ownership or root cause, not only
     the feature on top of it.
   - For a UX ask, one option is a new surface or a change to the navigation, not polish
     of the existing screen.
   - If you reject the structural option, say why in one line.
6. **Number every option** so the user can answer "do 2" or "1 and 2".
7. **Each option is 3–5 bullets:** what it is, the files or modules it touches, then
   `Tradeoff:` and `Cost:` on their own lines. Mirror an existing pattern where one exists.
8. **Justify every new part.** For each new table, endpoint, flag, service or PR split in an
   option, give a one-line reason it is needed now. Cut it if the reason is speculative.
   An option that lists special cases (tool names, repo names, job types, paths) is
   probably wrong: restate it as a rule over a general property, or say why that is
   impossible.
9. **Recommend one, and say why in a sentence.** The recommendation can be a single option
   or a sequence ("2 now, 3 later"). Mark which options combine and which exclude each
   other; "do 1 and 2" is a common answer. Never present a neutral menu.
10. **Name what you rejected.** `Rejected:` one line each, for the options a reader would
    expect to see. When the user scopes to "for now", design that version and name the seam
    that keeps the later path open. Do not analyze the later path in full.
11. **Draw it when options act at different stages.** A few lines of ASCII flow with each
    option marked where it acts. For a UI question, offer or produce a quick mock of the
    recommended option; a screen is judged faster than a description.
12. **End with open decisions and your defaults**, numbered, so "go" accepts all of them and
    one line overrides any. Each question:
    - names its object in plain words (the PR's number and title, not a bare ID or an
      internal label);
    - defines any term it introduces;
    - says what the user will see differently under each answer.
13. **Stop after the memo.** Implementation starts when the user picks. A constraint added
    with the pick ("do 1, and make sure tests reproduce this first") becomes an acceptance
    criterion. If the caller already authorized building (a brief that says "design, then
    implement if small"), still write the memo first, in 10 lines or fewer, then proceed.
    The memo is the record of the choice.
14. **After the pick, update what depends on it** in the same turn: the spec, the task
    briefs, the agreed-decisions list, open PR descriptions. List each one you edited. A
    later correction that changes a decision gets the same sweep.

## Template

```
<Topic> — 3 options

What exists today
- <mechanism or precedent, file ref>
- <the gap>

<ASCII flow, options marked, when they act at different stages>

1. <Smallest change>
   - <what it is; files touched>
   - Tradeoff: <the one that matters>
   - Cost: <rough>
2. <Deeper-layer change>
   - …
3. <New surface, or the other structural choice>
   - …

Combine: 1+2 stack. 3 replaces 1.
Recommendation: <N, or "N now, M later"> — <one sentence why>.
Rejected: <option> — <one line>.

Open decisions (my default in brackets):
1. <plain-words question; what changes for the user> [<default>]
2. …
```

## Example memo

```
Realtime sync for the settings panel — 3 options

What exists today
- sync/poller.ts polls every 30s; it is the only path that updates the panel.
- bus/consumer.ts already delivers audit events with retries, but carries only mutations.
- Nothing pushes settings changes today, so every option below adds a path.

  edit ─▶ API ─▶ DB ─▶ [poller 30s] ─▶ panel
                  │        ▲ option 1 shortens this
                  └─▶ bus ─────────────▶ panel   ◀ option 2 adds this

1. Shorten the poller interval
   - One constant in sync/poller.ts; one code path stays.
   - Tradeoff: still polling; load grows with open panels.
   - Cost: ~0.5 day.
2. Push over the existing event bus
   - New topic in bus/consumer.ts; panel subscribes; poller stays as the fallback.
   - Tradeoff: needs a backfill on reconnect.
   - Cost: ~2 days.
3. Dedicated webhook receiver
   - New service surface for third parties as well as the panel.
   - Tradeoff: a new surface to secure and deploy; duplicates what the bus gives us.
   - Cost: ~4 days.

Combine: 1+2 stack (1 is the fallback for 2). 3 replaces 2.
Recommendation: 2 — realtime without a new surface.
Rejected: client-side long polling — same load problem as 1, more code.

Open decisions (my default in brackets):
1. Should the panel show a "live" indicator when the push connection is up? You would see
   a small dot beside the title. [no — add it only if users report stale data]
2. On reconnect, backfill the last 5 minutes or everything since the last seen event?
   The second never misses a change but costs a query per reconnect. [since last seen]
```
