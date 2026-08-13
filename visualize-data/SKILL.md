---
name: visualize-data
description: >
  Turn data into a designed, self-contained HTML page — sentence-titled
  charts, honest encodings, no dashboard slop. Use when the user wants a
  chart, infographic, data viz, visual explainer, or "make this data
  beautiful," pastes a CSV/table, or runs /visualize-data. Triggers:
  visualize this, chart this, infographic, data visualization, turn this
  into a graphic, beautiful charts from data, visual essay from a dataset.
---

# Visualize Data

One job: ship a **self-contained HTML page** (or a single figure) that is
true to the data and designed for *this* dataset — not a Chart.js dashboard
and not a Visual Capitalist costume.

Marketing landings use `beautify-page`. This skill owns **data → claim →
chart → page**. Evidence and exemplars live in
[references/research.md](references/research.md). Paste prompts live in
[references/prompts.md](references/prompts.md). Load research when picking
a register or an unusual chart; do not dump it into the reply.

## Operating order (non-negotiable)

1. **Ground** — source, grain, units, what a row is, what the data cannot say
2. **Claim** — one quoteable sentence the data actually supports
3. **Chart** — lookup, not flourish (FT vocabulary)
4. **Register** — newsroom | visual-essay | scale-poster | explainer
5. **Tokens** — color / type / layout / one signature (before code)
6. **Build** — HTML + SVG, chart-object anatomy
7. **Critique** — not-generic pass, Chanel, mobile, source check

A pretty chart of the wrong comparison is a failed job. Claim first.

## Mode selection

| User intent | Mode |
| --- | --- |
| Data + "make a page / viz / infographic" | **Build** |
| Existing chart/page looks default or lying | **Polish** |
| "Give me a prompt for v0 / Claude / Gemini" | **Meta-prompt** |
| "Which chart should this be?" | **Chart-pick** (stop after step 3) |

Default to **Build** when data is present. If data is missing, ask once for
the table/CSV/source — do not invent numbers.

---

## 1. Ground the data

State explicitly (named assumption if unknown):

- **Source** — file, URL, or "user-pasted table"
- **Grain** — one row equals what
- **Unit / window** — people? %, 2019–2025?
- **Audience** — who has to get it in 10 seconds
- **Forbidden claims** — what this table cannot support

Drop any number you cannot point at in the source. If the ask is a
dashboard of "all the columns," refuse the dashboard: pick the one
comparison that matters, offer extras as later figures.

## 2. Write the claim

One sentence a reader could quote. It must contain a comparison
(more / less / faster / unlike / almost-all / vs a baseline).

Bad: "Revenue overview."
Good: "Enterprise overtook self-serve in 2024 and never gave it back."

That sentence **is the title**. If you cannot write it, you do not have a
chart yet — go back to the data, don't pick a pie.

## 3. Pick the chart

Match the **statement**, not the file shape. Full table:
[research.md §3](references/research.md). Pocket version:

| Statement is… | Default mark | Reach for only if needed |
| --- | --- | --- |
| Change over time | Line (1–4 series); small-multiple lines if spaghetti | Slope / arrow if only start→end; columns if ≤6 dates |
| Rank / size | Horizontal **sorted** bars | Lollipop; ISOTYPE for whole counts |
| Part-to-whole | Bars or waffle; stacked bars for Likert | Pie only if ≤5 slices and the point *is* "this is a %" |
| Relationship | Scatter | Bubble (area, not radius); hexbin if overplotting |
| vs a target / zero | Diverging bars; surplus/deficit area | |
| Flow / stages | Sankey / alluvial, tiny flows deleted | Chord only with a reading guide |
| Location **is** the claim | Choropleth (rates) or symbols (counts) | Map otherwise → don't |

Hard rules:

1. Bars compare. Lines time. Scatter relates. Maps only for geography.
2. Sort categorical bars. No 45° labels — flip to horizontal.
3. Bar axes include 0. Line axes may not, and then the dek says so.
4. No dual axis. No 3D. No comparing two pies.
5. Rainbow never encodes a quantity.
6. Mobile: bars, not 20 squeezed columns.
7. Direct-label ≤4 series; legends are a last resort.
8. One claim per chart. Escalate: simple figure first, scatter second.

If the interesting visual is a **custom encoding** (Pudding / Bremer), you
still ship a boring chart that proves the same sentence — then the custom
form. Custom-only is allowed in visual-essay when the encoding *is* the
argument and you include a "how to read this" before the swarm.

## 4. Choose a register

| Register | When | Page |
| --- | --- | --- |
| **Newsroom** (default) | One claim, a table, a briefing | Proof column: hed + one figure + short notes |
| **Visual essay** | A process, a mood, a reconstruction | Scrolly or stepped; custom encoding; no-JS stack fallback |
| **Scale poster** | Hidden scale, shareable frame | One composition at 1080×1350 (+ desktop sibling) |
| **Explainer** | Teach a mechanism | One new idea per step; encoding taught in step 1 |

Do not hybridize (no poster-in-a-dashboard, no NYT chrome on a 12-row CSV).

## 5. Plan tokens, then stop

Output the sheet, uniqueness-check it, **then** write HTML.

| Token | Required |
| --- | --- |
| **Color** | 4–6 named hex (bg, surface, ink, muted, accent, optional warn). Marks ≥3:1 on bg, colorblind-distinct, equal weight unless one series is the point. Hue from the **subject**. |
| **Type** | Display (page hed only) + body + **tabular/grotesk** for ticks/labels. Load real fonts + fallbacks. |
| **Layout** | One sentence + ASCII wireframe. Prose ~65ch; chart `min(100%, 1120px)`. Full-bleed only if the encoding needs the horizon. |
| **Signature** | One memorable thing: a custom encoding, a subject metaphor, or a single annotation — not a gradient. |

**Uniqueness check:** if the sheet would fit any other recap, revise.

### Default looks to refuse (unless the brief names them)

1. Chart.js / Recharts / Observable default blues + 4 KPI cards + doughnut
2. Playfair Display + Lato (OWID costume)
3. Dark navy + gold isometric (Visual Capitalist costume)
4. Cream `#F4F1EA` + terracotta serif, or black + acid green (frontend-design slop trio)
5. Inter / Roboto / Arial / system-ui / Open Sans / Lato / Space Grotesk

Also banned: glassmorphism, neon, purple-on-white, word clouds, radar-for-fun.

## 6. Build

### Chart-object anatomy (every figure)

```
kicker
TITLE AS THE CLAIM SENTENCE
dek: unit, window, definition
marks + direct labels
annotation sentence on the interesting mark
Source: …  ·  Note: …  ·  data link if any
```

Imitate the HTML skeleton in [prompts.md](references/prompts.md) — change
tokens and marks, not the object model.

### Technical floor

- One self-contained `.html` file (inlined CSS/JS/data). No build step
  unless the repo already has one.
- **SVG marks.** Library only if it does not dictate the look. Restyle
  every default. Prefer vanilla SVG for ≤3 charts.
- CSS variables for every color. Tabular lining figures on numbers.
- Hover = extra detail. The thesis is visible with hover disabled.
- `prefers-reduced-motion`: opacity/color only; scrolly becomes stacked figures.
- Visible focus. Contrast. A table or `aria` on the figure when the
  encoding is custom.
- Real source line. If there isn't one, say "User-provided table" and
  the date you built it.

### Page architecture by register

**Newsroom** — first viewport is the statement. One primary figure.
Optional 1–2 support figures. No filter bar above the fold. No sidebar.

**Visual essay** — hide chrome during the read. Narrow prose, full-bleed
viz. Scroll adds marks. Teach the encoding before the swarm. Ship a
mobile-specific drawing when the desktop swarm dies (Pudding's dual SVG).

**Scale poster** — the frame *is* the page. One metaphor, giant comparison,
source still on the frame.

**Explainer** — stepper or scrolly. Never a new color and a new mark in
the same beat.

## 7. Polish mode

1. Read the page. Write the current implied claim. Is it true?
2. Fix lying encodings first (truncated bars, dual axis, rainbow sequential).
3. Then anti-slop (checklist below).
4. Then one signature + quieter chrome.
5. Not-generic pass from [prompts.md §10](references/prompts.md).

## 8. Meta-prompt / Chart-pick modes

**Chart-pick:** ground → claim → type table. Stop. No HTML unless asked.

**Meta-prompt:** fill [prompts.md §12](references/prompts.md). Three
paragraphs, no brand names, append the constraint line.

---

## Ship checklist

- [ ] Every number is in the source; unsourced deleted
- [ ] Title is the claim sentence; claim is a comparison
- [ ] Chart type matches the statement (not a pie-of-habit)
- [ ] Token sheet followed; not costumes 1–5
- [ ] Anatomy: title, dek, direct labels, annotation, source
- [ ] Sorted bars; 0-baseline on bars; no dual axis / 3D
- [ ] Mobile readable; reduced-motion respected
- [ ] Hover optional to the finding
- [ ] Chanel: removed one accessory

## Anti-slop hard floor

| Rule | Detail |
| --- | --- |
| No invented data | Missing → omit or ask |
| No dashboard reflex | Filters after the thesis, if at all |
| Tokens only | Subject-derived accent; no library defaults |
| Real fonts | Not the refuse list |
| Labels > legends | Direct-label ≤4 series |
| Source on the figure | Not a graveyard footer only |
| One signature | Rest quiet |

## Output shape when reporting

1. **Claim** — the sentence
2. **Type + register** — one line
3. **Token sheet** — Build / first Polish
4. **File** — path to the HTML
5. **Risks** — 0–3 (encoding, source, residual generic)

Do not lecture visualization theory. Ship the page.

## Related skills (load if present)

- **beautify-page** — marketing/landing chrome. Don't restate it.
- **frontend-design** / **interaction-design** — identity and motion craft.
- **find-exemplar** — if a sibling figure already exists in the repo, mirror it.
