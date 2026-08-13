# Paste-ready prompts

Use with Build / Polish / Meta-prompt modes. Fill brackets. Never leave placeholders in shipped copy. Never invent numbers — if a value is missing, omit it or ask.

Evidence and exemplars: [research.md](research.md).

---

## 1. Source extraction (run before any visual)

```text
You are extracting structured facts for a visualization. Use only the
material below. Do not add outside knowledge. Flag anything ambiguous.

SOURCE MATERIAL:
[paste table / CSV / notes / URLs / quotes]

Extract:

1. CORE CONCEPT — one sentence
2. GRAIN — what is a row? what is a unit? what is the time window?
3. KEY DATA POINTS — each as {value, unit, date, source line}
4. COMPARISONS THE DATA CAN SUPPORT — time / rank / part / relation / place
5. COMPARISONS THE DATA CANNOT SUPPORT — and why
6. CAVEATS — definitions, missing years, selection bias

Output as tight bullets. If a number has no source, drop it.
```

---

## 2. Force the statement

```text
Write the one sentence a reader should be able to quote after 10 seconds.
It must contain a comparison (more/less/faster/unlike/almost-all).

Then:
- Audience: [who]
- Decision or belief this changes: [one verb]
- Register: newsroom | visual-essay | scale-poster | explainer
- Why the other three registers are wrong for this dataset
```

---

## 3. Chart pick (FT vocabulary)

```text
Statement: [sentence]
Data grain: [rows, fields, n]
Comparison: time | rank | part | relation | place | deviation | flow

Pick ONE primary chart from the FT Visual Vocabulary in that category.
Name 5 common charts you are ignoring and why.
If the statement needs a second chart, say so — do not combine claims.

Mobile: if the pick is columns with >8 categories, switch to bars.
```

---

## 4. Token sheet (plan before code)

```text
Dataset/subject: [concrete, not "dashboard"]
Register: [newsroom | visual-essay | scale-poster | explainer]
Statement: [sentence]

Plan, then stop:

1. Color — 4–6 named hex (bg, surface, ink, muted, accent, optional warn).
   Marks must be ≥3:1 on bg, distinct from each other and for deuteranopia,
   equal visual weight unless one series is the point.
   Derive hue from the subject. No purple-on-white. No rainbow sequential.
2. Type — display (page hed only) + body + tabular/grotesk for chart chrome.
   No Inter, Roboto, Arial, system-ui, Open Sans, Lato, Space Grotesk.
3. Layout — one sentence + ASCII wireframe. Prose ~65ch; chart min(100%, 1120px).
4. Signature — the one memorable thing (encoding, metaphor, annotation, not a gradient).

Uniqueness check: if this sheet would fit any other recap/dashboard, revise.
```

---

## 5. Full agent kit (Build)

```text
You are a news-graphics designer shipping a self-contained HTML page.

DATA: [paste or path]
STATEMENT: [quoteable sentence]
AUDIENCE: [specific]
REGISTER: [newsroom | visual-essay | scale-poster | explainer]

Operating order (do not skip):
1. Extract facts from the data only. Drop unsourced numbers.
2. Confirm the statement is actually in the data. Rewrite if not.
3. Pick the chart from FT vocabulary (time=line/cols; rank=sorted bars;
   part=bars/waffle not 12-slice pie; relation=scatter; place=map only
   if location is the claim). Escalate: simple chart first, fancy second.
4. Token sheet (color / type / layout / signature). Then build.

Page anatomy:
- First viewport = the statement, not filters
- Chart object: kicker → sentence title → dek (units/window) → marks
  with direct labels → annotation on the interesting mark → source/note
- 3–5 sections max if it is an essay; one figure if it is newsroom
- Mobile: horizontal bars; do not squeeze 20 columns
- Hover = detail; thesis visible with hover disabled
- prefers-reduced-motion: no parallax / scroll-jack
- Inlined data. Self-contained HTML. SVG marks. CSS variables.

Anti-slop:
- No Chart.js / Recharts / Observable default theme
- No 4 KPI cards + doughnut
- No Inter/Roboto/purple/neon/glass
- No dual axis, no 3D, no legend for ≤4 series, no unsorted bars
- No Playfair+Lato OWID costume, no navy-gold Visual Capitalist costume
  unless the brief asks for that publication

Ship the HTML file. Do not lecture theory.
```

---

## 6. Chart-object only (embed)

```text
Build a single figure, not a page. Width 700–800px, self-contained HTML.

Title is a sentence. Direct-label the series. Source + note in the footer.
[chart type]. Data: [paste].

Hairline grid or none. Tabular figures. Accent only on the series
the sentence is about; others gray. No tooltip-only insight.
```

---

## 7. Visual essay

```text
Build a scrollytelling HTML essay.

The scroll is the argument: each step adds or transforms marks.
Do not introduce a new encoding and a new idea in the same step.
Step 1 teaches the encoding with 3 rows.

No-JS / reduced-motion fallback = the same figures stacked, titles intact.
Hover is optional. Click is not required to get the finding.

Custom encoding must come from the subject ([subject materials]),
not a force-layout or a spiral-for-its-own-sake.
```

---

## 8. Scale poster

```text
One frame, 1080×1350 (and a 1600×2000 sibling).
The comparison must survive a 200px thumbnail.

One subject-metaphor, then stop. Giant number or giant overlay.
Source line still required. No 12-hue legend. No 3D pie.
```

---

## 9. Color spec

```text
Give [n] categorical colors for a chart on [bg hex].
Equal visual importance. Distinguishable at 8px stroke and at 12px type.
≥3:1 against the background. Colorblind-safe (no same-lightness red/green).
Subject vibe: [one adjective], used only after the constraints.
Bind each hex to a named series. Return hex + why.
```

---

## 10. Not-generic second pass

```text
Look at the page you just built.

1. Where does this match a Chart.js dashboard, an OWID clone,
   or a Visual Capitalist poster that isn't this data?
2. Name 3 generic elements. Replace each with something that
   could only belong to [this dataset / this subject].
3. Is the quoteable sentence still the title? If not, fix it.
4. Delete one accessory (Chanel).

Then implement.
```

---

## 11. Cut copy

```text
Reduce page copy 30% without losing a number or a source.
One takeaway per section. Titles stay sentences.
If a paragraph restates the chart, delete the paragraph.
```

---

## 12. Meta-prompt (for v0 / Claude Design / Gemini)

Emit exactly three paragraphs, then stop:

```text
Paragraph 1 — register + statement + what the first viewport feels like.
Paragraph 2 — type / color / marks as sensation, not brand names.
Paragraph 3 — abstract references (a reconstruction, a proof column,
a shareable scale-frame) — no publication names.

Constraints to append:
self-contained HTML, SVG, sentence title, source on figure,
no dashboard chrome, no default chart-library theme.
```

---

## HTML skeleton to imitate

Agents imitate examples harder than rules. Start from this anatomy; change tokens and marks, not the object model.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>STATEMENT AS TITLE</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <style>
    :root {
      --bg: #f7f4ef;
      --ink: #1a1814;
      --muted: #6b6560;
      --rule: #d9d2c8;
      --accent: #c44b1c;
      --mark: #2c4a6e;
      --mark-2: #c47a2c;
    }
    body { background: var(--bg); color: var(--ink); }
    .hed { /* display face, sentence case */ }
    .dek { color: var(--muted); }
    figure.chart { max-width: 72rem; }
    figcaption.source { color: var(--muted); font-size: .8rem; }
  </style>
</head>
<body>
  <header>
    <p class="kicker">KICKER</p>
    <h1 class="hed">Statement the data actually supports.</h1>
    <p class="dek">Unit, window, definition.</p>
  </header>
  <figure class="chart">
    <!-- SVG marks. Direct labels. One annotation. -->
    <figcaption class="source">Source: … · Note: …</figcaption>
  </figure>
</body>
</html>
```
