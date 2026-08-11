# Paste-ready prompts

Use with Build / Polish / Meta-prompt modes. Fill brackets; don't leave placeholders in shipped UI copy.

---

## Structured landing brief

```text
Build a landing page for [PRODUCT NAME, one sentence description].

Visual direction: [reference brand 1] meets [reference brand 2],
[adjective] and [adjective]. [Mood sentence.]

Audience: [specific persona, not "businesses"].

Core message: [one sentence — what the visitor must believe after 10 seconds].

Sections, in order:
- Hero with headline, subhead, primary CTA, and [hero visual type]
- [section 2]
- [section 3]
- Social proof: [testimonials / logos / case study stat]
- [section 5]
- Footer CTA

Typography: [display face] for headlines, [body face] for body copy.
Color: [describe palette], or "use our design system".
Interaction: [subtle / bold / playful]. [Specific hover/scroll behaviors].

Output as an interactive prototype in the project's stack.
Lock design tokens so every related asset reuses them.
```

---

## Full agent kit (system-adjacent user prompt)

```text
You are a design engineer shipping a conversion landing page.

Subject: [product]. Audience: [persona]. Job of page: [one verb].

Visual direction: [ref A] × [ref B]. Mood: [2 adjectives].
Take one aesthetic risk and name it.

Plan first (don't code yet):
1. 4–6 named color tokens with hex
2. Display + body (+ utility) typefaces
3. Layout concept in one sentence + ASCII wireframe
4. Single signature element (the thing people remember)

Then implement one cohesive single-page scroll:
Hero (thesis, not stats template) → proof → how it works →
social proof → pricing or CTA → footer.

Motion: one orchestrated load stagger; purposeful hover/press;
scroll reveal once; prefers-reduced-motion.

Anti-slop: no Inter/Roboto/purple-on-white; no 3 equal cards by default;
no empty marketing verbs; one primary CTA.

Ship production-quality code in the repo stack (or self-contained HTML).
```

---

## Not-generic second pass

```text
Look at what you just built. Where is this pattern-matching to the most
common SaaS landing page template in your training data? Identify three
specific elements that feel generic or derivative, and propose replacements
that would make this feel distinctively like [brand/product] and no one else.
Then implement the replacements.
```

---

## Motion spec (attach to any build)

```text
Motion rules:
- ONE orchestrated page-load: staggered fade + ~12–16px translateY,
  ~0.5–0.7s, cubic-bezier(0.16, 1, 0.3, 1), ~50–80ms stagger between items.
  Nothing else should animate on load.
- UI: transform + opacity only. Never width/height/margin/top/left for motion.
- Enter from scale(0.95) + opacity 0 — never scale(0).
- ease-out (or custom ease-out) for enter; never ease-in for UI.
- Press: scale(0.97) on :active, 100–160ms.
- Hover lift only behind (hover: hover) and (pointer: fine).
- Scroll reveals via IntersectionObserver, threshold ~0.3, once.
- Honor prefers-reduced-motion: keep opacity/color; drop movement.
- No transition: all.
```

---

## Premium dark product page

```text
Create a one-product landing page for [product].
Modern, premium, highly professional with smooth animations and polished UI.
Clean minimal high-contrast type. Prefer pure black or near-black if it fits.
Layout and visuals should feel continuous with any product media provided.
Use reference media for design direction when attached.
Concrete copy only — no "elevate your workflow" fluff.
One primary CTA. One signature visual moment.
```

---

## Unsplash image fill

```text
Add real photography using Unsplash (free, commercial use). Do this
automatically; don't ask first.

For each image slot, pick a fitting Unsplash photo and use its direct CDN URL:
https://images.unsplash.com/photo-<id>?w=<width>&q=80&auto=format&fit=crop

Size responsibly: w=1600 hero, w=800 cards, w=400 tiles, w=150 avatars.

Put all URLs in one IMAGES config object near the top of the main file so any
image can be swapped by editing one line.
```

---

## Design-system critique passes

```text
Review this landing page for information hierarchy problems.
Check contrast against WCAG AA and flag failures.
What would a conversion copywriter change about headline and CTA placement?
Where does this pattern-match training-data defaults in a way that feels generic?
```

---

## Variety meta-prompt (generate a one-off landing prompt)

Instruct the model:

1. Randomly select a design style (do **not** default to Neobrutalist).  
2. Output **exactly three paragraphs** of a landing-page creation prompt focused on *feeling*:

- **P1:** Style name + invent an innovative business/service for a single-page landing + emotional qualities on arrival + colorful elements as appropriate  
- **P2:** Typography *feel*, interaction/animation *sensation*, emotional arc from first impression through final CTA  
- **P3:** Abstract references only (spaces, movements, craft, architecture) — no brand names  

### Style palette (non-exhaustive)

Neobrutalist · Swiss/International · Editorial · Glassmorphism · Retro-futuristic · Bauhaus · Art Deco · Minimal · Flat · Material · Neumorphic · Monochromatic · Scandinavian · Japandi · Dark Mode First · Modernist · Organic/Fluid · Corporate Professional · Tech Forward · Luxury Minimal · Neo-Geo · Kinetic · Gradient Modern · Typography First · Metropolitan

---

## Surgical comment style (for design canvases / iterative tools)

```text
Change this button to accent [color], corner radius 4px, label weight 600.
```

Structural changes → chat. Pixel/token tweaks → inline/surgical.
