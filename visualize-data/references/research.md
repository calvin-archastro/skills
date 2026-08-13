# Visualize-data research

Evidence base for the skill. Load when choosing a **register**, a **chart type**, or citing an exemplar. Do not dump this file into the user-facing response.

Researched 2026-08. Sources: year-end lists (FlowingData, GIJN, Pudding Cup, Datawrapper Dispatch, AnyChart 2025 wrap), FT Visual Vocabulary, Datawrapper chart/color/type guides, From Data to Viz, The Pudding process + 2025 pieces, Our World in Data, Visual Capitalist, Reuters Graphics, Visual Cinnamon / Data Sketches, Venngage + Grow-with-AI prompt writeups.

---

## 1. What "best" actually is

The field splits into four crafts that get called "best" for different reasons. Do not mix their jobs.

| Register | Job | Who | Success looks like |
|---|---|---|---|
| **Newsroom** | One claim, fast, true | FT, Economist, Datawrapper, OWID Grapher, Pew | A reader can quote the title + take the number |
| **Visual essay** | A feeling that becomes a fact | The Pudding, NYT Graphics, WaPo, Guardian interactives | Scroll changes what you believe; interaction is the argument |
| **Scale poster** | Hidden scale, shareable | Visual Capitalist, Information is Beautiful, Voronoi | One image that survives a feed crop |
| **Data art / custom form** | Memorability + subject-specific metaphor | Nadieh Bremer, Shirley Wu, Giorgia Lupi, Pudding Cup winners | The form could only belong to this dataset |

2025 consensus picks (appeared on 2+ year-end lists):

1. Alvin Chang, *30 Minutes with a Stranger* — The Pudding
2. NYT *Swept Away* (Camp Mystic flood reconstruction)
3. Straits Times *Inside the Confusing World of Women's Clothing Sizes*
4. Guardian *Bird Migration Is Changing*
5. Reuters *How California Fights Fires from the Skies* + *Iran's Sanctioned Oil Fleet*
6. OWID *Measles Vaccines Save Millions of Lives*
7. Bloomberg AI-deals network + ICE-flight cost maps
8. Pudding Cup: *Dithering — Part I*, *Legislative Network Behind State Trans Laws*, *Benford's Law*

---

## 2. Case studies

Each: what they do well / poorly / stylistically / as a website. Steal the first two columns; ignore the house chrome unless the brief asks for that publication.

### 2.1 The Pudding — visual essays

**Exemplars:** [pudding.cool](https://pudding.cool) index; *30 Minutes with a Stranger* (2025); *Dicing Onions*; *Love Songs*; process essay *How to Make Dope Shit, Part 2*.

**Do well**

1. **Thesis in the first screen**, then the viz *is* the evidence, not a figure dropped under a blog.
2. **Custom encoding per story.** Mood of 1,700 conversations = little people, not a bar chart of "affect +1.4." Clothing sizes = 3D bodies. Onions = animated cuts.
3. **Scrollytelling as argument.** Time is the x-axis of the page: 0m → 30m in *Stranger*; moods flip as you scroll.
4. **Guide the read.** "Here's how to read this figure" appears *before* the crowd of marks.
5. **Source + method at the moment of the claim**, not a graveyard footer.
6. Design happens in Keynote/Figma first; code second. They say this out loud.

**Don't**

1. Heavy JS; some pieces are unreadable without scroll-jacking or a fat viewport.
2. Index is sticker-collage cute; individual stories sometimes inherit that playfulness when the subject is grave.
3. Interaction can bury the finding — you can play with people and miss "most felt better by minute 24."
4. Accessibility of custom SVG encodings is uneven (no table fallback).

**Style**

- Type: large, slightly off-kilter display; body is readable magazine sans; captions are small and dry.
- Color: one story, one palette. *Stranger* is muted flesh/stone + a single mood gradient (neg → pos). Not a 12-hue rainbow.
- Motion: scroll-linked, not hover-wiggle. Marks accumulate.
- Texture: paper-ish, hand-drawn callouts, occasional illustration that *is* the data.

**Website**

- Home = numbered archive, thumbnail + two-line tease, filter stickers. No dashboard chrome.
- Story pages: almost no global nav during the read. Full-bleed canvas, then a narrow text column that docks to the viz.
- Mobile gets a second SVG (`trust.svg` / `trust_mobile.svg`) rather than shrinking the desktop chart.
- Footer is credits, method, data — after the emotional close.

**Steal:** one custom encoding; dual desktop/mobile charts; "how to read this" before the swarm; claim restated after the play.

### 2.2 New York Times Graphics

**Exemplars:** annual *Year in Visual Stories and Graphics* (2025: Trump admin, AI, wars, weather); *Swept Away*; Upshot *Zodiac* (2025); Sednaya 3D prison; historical yield-curve 3D.

**Do well**

1. **Reconstruction.** Video + map + clock. You are *there*. Best-in-class for events in space-time.
2. **Annotation over decoration.** The sentence sits on the chart, pointing at the mark.
3. **Small multiples and locators** before 3D. 3D is reserved for "you cannot understand this as a plan."
4. **Type hierarchy of a newspaper:** kicker → hed → dek → chart title → annotation → source.
5. They escalate complexity (Datawrapper's own advice, which they follow): one line first, then the scatter.

**Don't**

1. Paywall + tracker weight. The craft is not portable to a self-contained HTML file.
2. 3D and WebGL pieces age badly and fail on low-power phones.
3. Breaking-news graphics sometimes ship with default NYT blue before a designed piece replaces them.

**Style**

- Off-black text on warm-white. NYT Imperial / Cheltenham display + Franklin/Helvetica-ish utility.
- Rules, not cards. Hairlines. Almost no drop shadow.
- Color is semantic (party, land, water) or a restrained sequential. Rarely decorative.
- Locator maps are tiny and constant.

**Website**

- Graphics live *inside* article chrome (masthead, share, "gift this"). The viz is a chapter, not a microsite — except for the big interactives, which go full-bleed and hide chrome on scroll.
- Year-in-graphics is a curated magazine, not a data portal.

**Steal:** annotation-as-sentence; escalate complexity; locator always on; 3D only when 2D lies.

### 2.3 Reuters Graphics

**Exemplars:** reuters.com/graphics; *California aerial firefighting*; *Iran oil fleet*; *Eroding Protections for Public Lands* (atlas aesthetic); *Torrent of Trash*.

**Do well**

1. **Diagram + map + chart in one frame.** How a firefighting aircraft works, then where it flew.
2. **Satellite / OSINT materiality.** The page looks like an investigation: crops, tracks, timestamps.
3. **Atlas register** when the subject is land/policy — antique-map texture used as argument, not steampunk.
4. Lead with the graphic; text captions it.

**Don't**

1. Homepage is a thin index of cards; individual pieces are the product. Easy to miss older work.
2. Some pieces are image sequences more than data. Beautiful, less queryable.
3. Heavy GIFs/video for "mapping the eclipse" style posts — pretty, not inspectable.

**Style**

- Darker, more cinematic than FT. Full-bleed photography under type.
- Diagrams in a technical-pen line weight. Labels set in a condensed sans.
- Color from the subject (fire orange, oil black, forest green) rather than a house categorical.

**Website**

- `/graphics` is a river of large stills + one-sentence ledes. Click → immersive longread.
- Little UI chrome. The graphic *is* the page.

**Steal:** subject-derived color; diagram-then-map; investigation materiality (crops, timestamps, sources on the mark).

### 2.4 Our World in Data

**Exemplars:** ourworldindata.org; Grapher; Data Insights (AC adoption, road deaths, carbon price); *Measles vaccines* heatmap.

**Do well**

1. **Claim is the title.** "Air conditioning is almost universal in the US and Japan — but not elsewhere." The chart is proof.
2. **One chart, then the caveat.** They narrate *what the number is*, then *what it is not*.
3. **Reusable Grapher** (line / map / table tabs, country picker, download, source). 14,000 charts, one object.
4. **Licensing and method as first-class.** CC BY, source named on the figure.
5. Long-run series. They will show 1800–now when the story is "this used to be everyone."

**Don't**

1. Grapher chrome is utilitarian. Not a "beautiful page." The beauty is the sentence + the honest axis.
2. Default blue/red country lines become spaghetti past ~8 series.
3. Topic pages are encyclopedic; a first-time reader can drown.
4. Playfair Display + Lato is now a recognizable OWID costume — distinctive as a *site*, generic if you copy it onto an unrelated brief.

**Style**

- White, generous. Display serif for article titles; Lato for UI and chart chrome.
- Chart titles are sentences. Subtitles are definitions. Footer is source + license.
- Color: country colors are stable across the site ( comparability > local beauty ).
- No illustration. No texture. The grid is almost invisible.

**Website**

- Home: mission line, then Grapher demos, then Data Insights as a vertical river of *chart + 200 words*.
- Article = narrow prose column, Grapher full-width between sections, "Explore the data" CTA under every figure.
- Explorers are a separate IA: filters, not essays.

**Steal:** sentence-titles; caveat immediately after; source on the figure; one object reused; do **not** steal Playfair+Lato unless the brief is "look like OWID."

### 2.5 Visual Capitalist / Voronoi

**Exemplars:** *Top 25 of 2025* — $117T world economy; rivers by discharge; Africa true-size overlay; coal as smoke-ring; books-as-bars for education/salary.

**Do well**

1. **Hidden scale.** The Amazon's discharge, Africa's true size, one company vs a country. The "wow" *is* the insight.
2. **Metaphor from the subject.** Coal → smoke ring. Salary × education → stacked books. Rivers → satellite water.
3. **Ranked lists people already wanted.** "Most educated," "most reliable car" — the format matches search intent.
4. Designed as a **single shareable frame**. Survives Twitter/LinkedIn crop.

**Don't**

1. **3D pie / radial / giant mosaic** often win the feed and lose the comparison. Rank is clearer as a sorted bar.
2. Clickbait-adjacent titles. Some pieces are "every country's richest billionaire" — scale porn, thin claim.
3. Dark-navy + gold + isometric cards is a **house costume**. Copying it reads as "VC clone."
4. Data footnotes exist but are easy to skip; viral pieces get quoted without the caveats.
5. Not a website experience — it's an image factory with a blog wrapped around it.

**Style**

- Dark navy or charcoal ground. Bold condensed titles. Big type, big numbers, icon-country flags.
- Saturated categorical colors, often 8–12. Works on a poster; fails colorblind and print.
- Isometric illustration, globe-from-space, metallic highlights.

**Website**

- Home is a magazine grid. Post = hero image (the viz) → short prose → more images → subscribe wall.
- Voronoi is the app-ification: same posters, community authors, "most viewed / discussed."

**Steal:** one subject-metaphor; design for a single frame; ranking when rank *is* the question. Do **not** steal the navy-gold isometric kit.

### 2.6 Information is Beautiful (David McCandless)

**Do well:** trivia and "sizes of things" as bright, flat, highly labeled compositions. A beginner can read them. *Best in Show* dog chart is the canonical "color + size + position = three variables, no chrome."

**Don't:** some pieces prefer cleverness to statistical hygiene (bubble area vs radius; cherry-picked "kinds of"). The site is a shop + archive more than a reading experience.

**Steal:** multivariate encoding in one composition; labels as design; high-key flat color *when the subject is playful*.

### 2.7 Nadieh Bremer / Data Sketches / Visual Cinnamon

**Exemplars:** *Searching for Birds* (2026 Webby Best Data Visualization); *Data Sketches* book (with Shirley Wu); *Elemental Flows*; SciAm *Radius Gap*; NYT trackers.

**Do well**

1. **Form invented for the dataset.** Bird searches ≠ bar chart. Commit history ≠ Gantt. The encoding *is* the insight.
2. They publish the **sketch → dead end → final** trail. Design is iterative, not a template.
3. Technical ceiling (d3, custom math) in service of a first-glance read.
4. Data art when the brief is emotion; news-graphics restraint when the client is SciAm/NYT.

**Don't**

1. Unrepeatable. A skill that says "be Nadieh" produces mush.
2. Some pieces need a long legend. Beautiful, slow.
3. Portfolio site is image-forward; the interactive often lives elsewhere.

**Steal:** the *discipline* (sketch first, custom form, iteration), not a particular radial-arc look.

### 2.8 FT / Economist / Datawrapper (the craft of the chart)

**Exemplars:** [FT Visual Vocabulary](https://github.com/Financial-Times/chart-doctor); Economist Graphic Detail; Lisa Charlotte Muth's Datawrapper guides (chart types, color, type).

**Do well**

1. **Chart type chosen by the *statement*, not the dataset.** "The chart's main statement becomes a compass."
2. **Boring charts on purpose.** Bars/lines win comparisons. Stream/slope/Marimekko are seasoning.
3. **Sentence titles. Direct labels. No legends if 1–4 series.** Source + note in the footer.
4. Color: stand off the background, distinct from each other *and* for colorblind, similar visual weight unless one series is the point. Blue+orange is the industry default for a reason.
5. FT publishes almost **no clickable graphics** — interaction is expensive and usually hides the claim.

**Don't**

1. House style (FT pink, Economist red) is copyrighted identity. Copying it is costume.
2. Vocabulary posters tempt people into rare chart types they cannot execute.
3. Datawrapper-default Roboto is fine inside Datawrapper and generic everywhere else.

**Style**

- White/cream, thin rules, small-caps kicker, 1 accent.
- Economist: Econ Sans / Econ Sans Condensed for *everything* in the chart.
- Bloomberg: Neue Haas Grotesk, markets-black, one highlight.
- Urban Institute (sibling newsroom guide): Lato, cyan/gray/black, title case titles, 1pt rule under header.

**Website**

- Charts embed in articles. The page is the newspaper. Graphic Detail / Chart Doctor are columns.
- Datawrapper blog is itself a teaching site: large example images, boxed asides, downloadable posters.

**Steal:** statement-first chart pick; sentence title; direct labels; equal-importance color; skip interaction that doesn't change the claim.

### 2.9 Bloomberg Graphics

**Do well:** money and systems — circular AI deals, grid-level electricity prices, ICE flight routes as motion. Network + map + small multiples. Dark, expensive, dense.

**Don't:** paywall; WebGL; density that assumes a markets reader. Network hairballs still happen ("OpenAI/Nvidia web of deals" is informative *because* they edited it down).

**Steal:** follow the money as a visual system; edit networks until a pattern remains; motion on *routes*, not on decoration.

### 2.10 Explainers: r2d3, Distill, Pudding Cup *Dithering* / *Benford*

**Do well:** the visual *is* the pedagogy. r2d3's visual intro to ML (Stephanie Yee + Tony Chu) still sets the bar: you see a decision tree grow. *Dithering — Part I* lets motion teach a technical idea. Distill.pub made equations into scrubbable figures.

**Don't:** long; authorial; not a dashboard. Distill shut down — the form is costly to maintain.

**Steal:** one concept per scroll-step; never introduce a new encoding and a new idea in the same beat.

### 2.11 Classics still worth stealing from

| Piece | Why it still wins | Failure mode if copied blindly |
|---|---|---|
| **The Fallen of WWII** (Neil Halloran) | Unit is a person; time + theatre become architecture | 40-minute film, not a page |
| **Periscopic *U.S. Gun Deaths*** | "Stolen years" as the visual verb | Easy to turn into trauma-aesthetic |
| **Climate spiral** (Ed Hawkins) | Form = the finding (a spiral, not a line) | Spiral is now a cliché for any cyclic data |
| **Otto Neurath ISOTYPE** | One icon = N units; no sliced icons | Clip-art pictograms |
| **Minard *Napoleon*** | Flow + geography + temperature + time | Students remake it instead of their own data |

---

## 3. Chart type → data (use this, don't invent a 12th taxonomy)

Two taxonomies cover almost every brief. **FT Visual Vocabulary** (by *what you want to say*) and **Datawrapper / From Data to Viz** (by *goal* and *data shape*). Combined cheat sheet:

### 3.1 By statement

**Change over time**

| If… | Use | Avoid |
|---|---|---|
| Continuous series, 1–4 lines | **Line.** Markers only if irregular | Dual axis; 12-line spaghetti |
| Many categories overlapping | **Small-multiple lines** | One panel, 15 colors |
| Only start vs end matters | **Slope** or **arrow plot** | Full line that adds nothing |
| Few time points | **Columns** (grouped if 2–3 series) | Line through 3 points dressed as a trend |
| Composition over time | **Stacked column** or **area** (totals); small multiples (parts) | Stacked area if the part-trend is the claim |
| Attention / metaphor | Stream (knowing values are unreadable) | Stream as the *only* chart |

**Magnitude / ranking**

| If… | Use | Avoid |
|---|---|---|
| Compare sizes, long labels | **Horizontal bars, sorted** | Alphabetical bars; columns on mobile |
| Rank *is* the story | Ordered bar / lollipop / slope | Unsorted |
| Huge range, precision secondary | Proportional symbol / ISOTYPE | Bubbles for 12% vs 14% |
| Two numbers per category | Dot plot / split bar / Cleveland | Grouped columns past 3 series |

**Part-to-whole**

| If… | Use | Avoid |
|---|---|---|
| 2–5 parts, "this is a %" | Pie/donut *or* (better) bars | Comparing two pies |
| Many parts / hierarchy | Treemap (hierarchy), waffle (counts) | 12-slice pie |
| Survey / Likert | **Diverging stacked bars** | Radar |
| Size *and* share | Marimekko — only if you will teach it | Marimekko as decoration |

**Distribution**

| If… | Use | Avoid |
|---|---|---|
| Shape of one variable | Histogram (try bin sizes) or density | One bin width, one take |
| Compare distributions | Box + jitter, violin, ridgeline | 12 overlapping densities |
| Age × sex | Population pyramid | Two independent bars with no mirror |

**Correlation / relationship**

| If… | Use | Avoid |
|---|---|---|
| Two continuous | **Scatter** | Dual-axis line pretending to be a relation |
| + a third magnitude | Bubble (**area**, not radius) | Unlabelled bubble size |
| Overplotting | 2d density / hexbin | 40k raw dots |
| "Don't imply causation" | Say so in the title | Connected scatter that looks causal |

**Deviation**

| If… | Use |
|---|---|
| vs 0 / target / average | Diverging bars, surplus/deficit area, spine |

**Flow**

| If… | Use | Avoid |
|---|---|---|
| Volume through stages | Sankey (edit tiny flows out) | Hairball Sankey |
| Category → category over time | Alluvial | Alluvial with 40 nodes |
| Two-way matrix | Chord — only with a reading guide | Chord as hero with no legend |

**Spatial** — only when *location* is the claim (FT Chart Doctor: "use fewer maps").

| Data | Use |
|---|---|
| Rates by admin unit | Choropleth (normalize; sequential, not rainbow) |
| Counts / events | Symbol / dot density |
| "Where is this" | Locator |
| Movement | Flow map / great-circle |
| Area-size bias is the problem | Cartogram or hexbin — teach it |

### 3.2 Hard rules the best rooms share

1. **Bars for comparison. Lines for time. Scatter for relationship. Map only for geography.**
2. **Sort.** Unsorted categorical bars are a mistake (From Data to Viz #1 caveat).
3. **Bar/column axes include 0. Lines may not** — and then you *say so* (ONS, Quartz, Vox, FT Chart Doctor all agree).
4. **No dual axis** unless you are willing to be accused of lying. Prefer indexed lines, small multiples, or connected scatter.
5. **Pie: ≤5 slices, no 3D, no legend-to-the-side, slices sum to 100%, never compare two pies.** Prefer bars.
6. **Rainbow palettes are for categories, never for a quantity.**
7. **Mobile: prefer bars to columns.** Columns with 20 categories die at 360px.
8. **Direct-label instead of a legend** when series ≤4.
9. **One claim per chart.** A second claim is a second chart.
10. **Escalate:** simple sentence-chart first, then the scatter that only the curious need.

---

## 4. Stylistic grammar (what to actually copy)

### 4.1 The chart object

Every serious newsroom treats a chart as a **typographic object** with a fixed anatomy:

```
[kicker / section label]
TITLE AS A SENTENCE (the claim)
Optional dek: definition, units, time window
[the marks]
[direct labels on the marks]
[annotation sentence pointing at the interesting mark]
---
Source: …  ·  Note: …  ·  Get the data
```

Urban Institute, Economist, OWID, Datawrapper embeds — same skeleton, different fonts.

**Type in the chart**

- Chart UI/labels: a **tabular or grocer sans** with a real italic and tabular lining figures. Display serif is for the *page* title, not tick labels.
- Datawrapper: sans for charts (they use Roboto in-product; you should pick a better one). Economist: one family, many cuts.
- Sizes jump: title ≫ labels ≫ source. ~3×, not 1.2×.
- Never set long labels at 45°. Flip to horizontal bars.

**Color**

- **Stand off the background.** Pastel yellow on white is a failed line.
- **Distinct, including for deuteranopia.** Check in Viz Palette / Color Buddy.
- **Equal visual weight** unless one series is the point. ColorBrewer Paired is for *pairs*.
- **Subject-derived > categorical defaults.** Fire = ember. Vaccines = a single sequential. Conversation mood = one diverging scale.
- Blue+orange is the safe 2-series (every major tool defaults here). Use it when the brief is "clear," not when the brief is "memorable."
- One highlight + grays beats 8 hues of equal shout.

**Marks**

- Thin, confident strokes. Area fills at ~15–25% opacity.
- Grid: horizontal only, hairline, low contrast. Or none, if you direct-label.
- No 3D. No gradients on bars. No drop shadows on marks.
- Annotation wins over chrome: an arrow + seven words > a tooltip the reader never opens.

### 4.2 The page (when the viz is hosted)

Four site patterns. Pick one; don't hybridize.

| Pattern | Who | Page architecture |
|---|---|---|
| **Essay** | Pudding, NYT interactive | No chrome. Narrow prose (60–70ch). Full-bleed viz between sections. Scroll is the UI. Progress or time ticker optional. |
| **Proof column** | OWID, Datawrapper blog, Pew | Article column. Chart is a full-width figure with the anatomy above. "Explore" is a secondary button. |
| **Investigation** | Reuters, Bloomberg, Forensic Architecture | Full-bleed lead visual. Sticky chapter nav. Side captions, crops, timestamps. Darker ground. |
| **Poster / share** | Visual Capitalist, IIB | The image *is* the page. Prose is a caption. CTA is subscribe/share. |

**Shared website craft**

1. **The first viewport is the claim**, not a filter bar.
2. **Filters after the thesis.** OWID puts the Grapher under a written claim. Dashboards that open on 12 slicers are the anti-pattern.
3. **Two widths:** measure for prose, `min(100%, 1100–1280px)` for the chart. Full-bleed only when the encoding needs the horizon (maps, scrolly swarms).
4. **Ship a mobile chart**, not a scaled desktop. Pudding duplicates SVGs. Datawrapper reflows to bars.
5. **Hover = detail. Click = commit.** The thesis must be visible with hover disabled (FT: most graphics aren't clickable).
6. **Sticky is for orientation** (chapter, year, "how to read"), never for a cookie banner of filters.
7. **Source, method, download** live on the figure. Credits live at the end.
8. **Reduced motion:** fade, don't parallax. Scrollytelling must have a no-JS or no-motion path (stacked static figures).
9. **No dashboard costume** (sidebar, 4 KPI cards, purple gradient, Inter) unless the brief *is* an ops dashboard — and even then, quieter.

### 4.3 Registers as token recipes

Use these as *starting constraints*, then deviate for the subject.

**Newsroom / proof**
- Ground: warm white or paper (`#f7f4ef`–`#fff`)
- Ink: near-black, not `#000`
- One accent (not purple)
- Hairlines, 0–2px radius
- Type: grotesque + optional display serif for the hed only
- Motion: none, or a 200ms highlight

**Visual essay**
- Ground: subject-derived (can be dark)
- One custom encoding
- Type with character in the hed; quiet body
- Motion: one scroll-linked sequence
- Illustration allowed if it *is* data

**Scale poster**
- One frame, designed at 1600×2000 and 1080×1350
- Giant number or giant comparison
- Subject metaphor, then stop
- Still needs a source line

**Explainer**
- Stepper or scrolly, one idea per step
- Encoding introduced before it is used
- No new color and new mark at the same time

### 4.4 Anti-patterns that read as AI / amateur

1. Four KPI cards + a default Chart.js line + a doughnut
2. Rainbow 12-category palette on a sequential quantity
3. 3D pie, exploded pie, donut with "65%" in the hole and no other context
4. Dual axis with independent scales
5. Inter / Roboto / Arial / system-ui as the "clean" choice
6. Purple-on-white, neon-on-navy, glassmorphism cards
7. Legends for two series that could have been direct-labeled
8. Unsorted bars; 45° labels; truncated bar axis
9. Tooltip-only insights
10. "Dashboard" nav on a story
11. Playfair + Lato OWID costume on a SaaS recap
12. Visual Capitalist navy-gold isometric on a 12-row table
13. Word clouds
14. Radar charts for anything that isn't a true polar profile
15. Invented statistics

---

## 5. Prompt research — what actually works

Collected from Venngage's Claude-infographic guide (2026), Grow-with-AI's NotebookLM workflow, Datawrapper's "statement = compass," FT vocabulary, Lisa Muth color prompts, and the landing-page prompt discipline in this repo's `beautify-page`.

### 5.1 Prompts that fail

| Prompt shape | Why it dies |
|---|---|
| "Make an infographic about X" | No audience, no claim, no source, no format → generic stacked cards |
| "Use D3 and make it stunning" | Tool before statement; stunning = rainbow force layout |
| "Dashboard of this CSV" | Becomes 4 KPIs + pie |
| "Make it look like The Pudding" | Costume without a custom encoding |
| Unsourced numbers | Hallucinated stats, the #1 published failure mode |

### 5.2 Prompts that work (patterns, not magic words)

The winning workflows all **separate jobs**. Nobody good asks one prompt to research, choose a chart, design a page, and export a PNG.

**Job 1 — Extract, don't invent** (Grow-with-AI / NotebookLM)

```
From the uploaded sources only, extract:
1. CORE CONCEPT — one line
2. MAIN CATEGORIES — 4–6, each with 2–3 facts
3. KEY DATA POINTS — numbers + units + date + source
4. NOTABLE DISTINCTIONS — common misunderstandings
Rules: no outside knowledge; flag ambiguity; one short sentence each.
```

**Job 2 — Force a statement** (Datawrapper / OWID)

```
Write the chart's main statement as one sentence a reader could quote.
Then name the comparison (time / rank / part / relation / place).
If you cannot, you do not have a chart yet.
```

**Job 3 — Pick the type from a vocabulary, not from vibes** (FT)

```
Given the statement and the data grain, pick from the FT Visual Vocabulary
category (deviation / correlation / ranking / distribution / change over time /
part-to-whole / magnitude / spatial / flow). Name the specific chart.
Say which 8 types you are ignoring and why.
```

**Job 4 — Structure the page before pixels** (Venngage)

```
Audience, goal, format, export target, tone, max word count.
Then: one headline, one dek, 3–5 sections, one insight per section,
suggested mark type per section, layout order.
Do not design yet.
```

**Job 5 — Tokens before code** (beautify-page / frontend-design)

```
4–6 named hex, display+body+tabular, one-sentence layout, one signature.
Uniqueness check: if this token sheet would work for any other dataset, revise.
```

**Job 6 — Constraints that kill slop**

```
Self-contained HTML. SVG marks. CSS variables only.
No Chart.js/Recharts defaults. No Inter/Roboto/purple.
Sentence title. Direct labels. Source on the figure.
Mobile: horizontal bars, not squeezed columns.
prefers-reduced-motion. Contrast ≥ 3:1 for marks vs ground.
```

**Job 7 — Edit like an editor** (Venngage follow-ups)

```
Reduce copy 30%. One takeaway per section.
Replace generic icons. Increase contrast.
Verify every number against the source table; delete unverified ones.
```

**Job 8 — Color as a spec, not a mood** (Muth)

```
N colors, equal visual importance, distinguishable at 8px,
≥3:1 on [bg], colorblind-safe, [vibe only as a last adjective].
Return hex + which series each binds to.
```

### 5.3 Format-specific prompt fragments

- **Web page:** "self-contained HTML, inlined data, no build step, works at 360 and 1280."
- **Visual essay:** "scroll is the argument; hover is optional; no-JS fallback = stacked static figures."
- **Poster:** "one frame, 1080×1350, readable at 200px thumbnail, source still present."
- **Explainer:** "one new idea per step; introduce the encoding in step 1 with three fake rows."
- **Newsroom embed:** "figure only — title, chart, source — 700px wide, no page chrome."

### 5.4 What the literature agrees on

1. **Source material in the prompt** beats "you are an expert data journalist."
2. **Statement → type → tokens → build → cut** is the only order that doesn't slop.
3. **First output is a structure, not a visual.**
4. **Verify numbers by hand.** Every published guide says this; most agents skip it.
5. **Export target changes the design.** A Pudding essay and a LinkedIn 4:5 are different objects.
6. **Costume prompts** ("make it NYT") produce chrome. **Mechanism prompts** ("annotation is a sentence on the mark") produce craft.

---

## 6. Implications for the skill

1. Default register is **newsroom/proof** unless the data *wants* a custom encoding or a single-frame poster.
2. The agent must write the **quoteable sentence** before it opens a `<svg>`.
3. Chart pick is a **lookup**, not a flourish. Vocabulary lives in this file §3.
4. Page chrome follows §4.2. Marketing-landing instincts (hero/CTA/three cards) are the wrong sibling — that's `beautify-page`.
5. Prompts in `prompts.md` are the paste versions of §5.
6. Imitate the **chart-object anatomy** and the **Pudding dual-SVG mobile** pattern. Do not imitate Playfair+Lato or VC navy-gold.
