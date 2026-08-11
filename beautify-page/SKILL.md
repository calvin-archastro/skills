---
name: beautify-page
description: >
  Build or polish marketing/landing pages with distinctive visuals, purposeful motion,
  and anti-AI-slop craft. Use when the user wants a beautiful landing page, marketing
  homepage, hero polish, premium UI, motion graphics on a page, anti-slop redesign, or
  runs /beautify-page. Triggers: beautify this page, make it feel premium, landing page
  that doesn't look AI, motion on the hero, polish marketing UI, distinctive frontend.
---

# Beautify Page

One job: ship a **marketing or landing page** that looks intentional for *this* subject —
not Inter + purple gradient + three equal cards.

Works for **new builds** and **polish of existing pages**. Product dashboards use a quieter
register (still use anti-slop; skip kinetic heroes).

## Operating order (non-negotiable)

1. **Ground** — product, audience, single job of the page  
2. **Plan tokens** — color / type / layout / one signature (before code)  
3. **Foundations** — hierarchy, type, space, contrast, concrete copy  
4. **Interaction** — default / hover / active / focus / loading for CTAs + cards  
5. **Motion** — one orchestrated moment + essential feedback only  
6. **Critique** — Chanel rule (remove one accessory); mobile + keyboard + reduced-motion  

Animation on a weak foundation makes the work *cheaper*. Foundations first.

---

## Mode selection

| User intent | Mode |
| --- | --- |
| New landing / marketing page | **Build** |
| Existing page looks generic / flat | **Polish** |
| "Give me a prompt for v0 / Gemini / Claude Design" | **Meta-prompt** |
| Only motion / micro-interactions | **Motion pass** (foundations already good) |

If ambiguous, default to **Polish** when code/files exist; else **Build**.

---

## 1. Ground the subject

State explicitly (fill unknowns with a named assumption):

- **Product** — what it is in one concrete sentence  
- **Audience** — specific persona, not "businesses"  
- **Job of page** — one verb (sign up / book demo / start trial / download)  
- **Belief after 10s** — what they must believe  

Subject materials (domain, tools, vernacular) drive distinctive choices — not "SaaS website."

---

## 2. Plan before code (token sheet)

Output a short plan, then build only after it passes the uniqueness check:

| Token | Required |
| --- | --- |
| **Color** | 4–6 named hex (bg, surface, text, muted, accent, optional danger) |
| **Type** | Display + body (+ utility for captions/data if needed). Load real fonts + fallbacks |
| **Layout** | One-sentence concept + rough section order |
| **Signature** | The *one* memorable element (type treatment, interactive hero, material, motion motif…) |

**Uniqueness check:** if the plan matches what you'd ship for *any* similar SaaS page, revise
the free axes. Brief wins when it pins a look.

### AI-default looks (avoid unless brief demands)

1. Cream `#F4F1EA` + high-contrast serif + terracotta  
2. Near-black + acid-green or vermilion accent  
3. Broadsheet hairlines + zero radius + dense columns  
4. Purple-on-white gradient + Inter + three equal cards + emoji bullets  

Also still banned by reflex: Space Grotesk as the "creative" default, glassmorphism stacks,
neon glows, numbered `01/02/03` when order isn't real information.

Full paste block for system injection: [references/aesthetics-prompt.md](references/aesthetics-prompt.md).

---

## 3. Visual foundations

### Hierarchy

- Contrast = importance; closeness = relatedness  
- Squint test: primary action must win  
- Hero is a **thesis** (headline, live demo, characteristic image) — not auto "big number + gradient"

### Typography

- Pair display + body for *this* product  
- Extremes beat mild: weight 100–200 vs 800–900; size jumps ~3× not 1.5×  
- Never default to Inter / Roboto / Arial / system-ui / Open Sans / Lato  

### Color & atmosphere

- One dominant + sharp accent beats timid even palettes  
- CSS variables for all tokens  
- Backgrounds: intentional atmosphere (gradient layer, texture, pattern) *or* pure minimal white — never purple-gradient-on-white cliché  

### Layout restraint

- Don't center everything  
- Don't force three identical feature cards  
- Structural devices (eyebrows, dividers, numbers) only if they encode real content structure  
- Match complexity to vision: maximalism needs craft; minimalism needs precision  

### Copy is design material

**Ban:** empower, seamless, one-stop, unlock potential, disrupt, revolutionize, next-generation, streamline, elevate your workflow, Lorem ipsum, fake social proof.

Write concrete product language. One primary CTA on landings. Active voice. Sentence case.

---

## 4. Motion budget

Purpose required. Valid: feedback · spatial consistency · state · prevent jarring change ·
explanation (marketing) · rare delight.

| Surface | Budget |
| --- | --- |
| Page load | **One** orchestrated sequence (stagger 30–80ms). Prefer over scattered micro-wiggles |
| Hover / press | Subtle; press `scale(0.97)` ~100–160ms ease-out |
| Scroll | Optional one-shot reveals (e.g. IntersectionObserver ~0.3); don't re-fire spam |
| Keyboard / 100+/day UI | **No** animation |

**Craft rules:**

- Animate **transform + opacity only**  
- Enter from `scale(0.9–0.97)` + `opacity: 0` — never `scale(0)`  
- Prefer `ease-out` / custom ease-out for enter; **never `ease-in` for UI**  
- No `transition: all`  
- Gate hover motion: `(hover: hover) and (pointer: fine)`  
- Honor `prefers-reduced-motion` (opacity/color only, drop movement)  

Suggested load curve: `cubic-bezier(0.16, 1, 0.3, 1)` or `cubic-bezier(0.23, 1, 0.32, 1)`.

Paste-ready motion spec: [references/prompts.md](references/prompts.md) § Motion.

---

## 5. Build mode — section order

Default single-scroll narrative (cut/reorder for brief):

1. **Hero** — thesis, subhead, primary CTA, signature visual  
2. **Proof** — logos / metric / quote (real if available)  
3. **How it works / features** — not three generic cards unless content is truly three peers  
4. **Deep proof** — case study, demo, comparison  
5. **Pricing or secondary CTA** (if relevant)  
6. **Footer CTA** + footer  

Implement with real stack in repo (or self-contained HTML if greenfield). Derive every color/type from the token sheet.

---

## 6. Polish mode — procedure

1. Screenshot or read the page; note first 3 "generic" tells  
2. Run anti-slop checklist (below)  
3. Fix foundations before motion  
4. Add or tighten **one** signature + load orchestration  
5. Second pass: **not-generic critique** (implement fixes)

### Not-generic second pass (always for Polish; after first Build draft)

```text
Where does this pattern-match the most common SaaS landing template?
Name 3 generic/derivative elements. Replace each with something that could
only belong to [this product/brand]. Implement the replacements.
```

---

## 7. Meta-prompt mode

When the user needs a *prompt* for another tool (v0, Claude Design, Gemini):

1. Randomize a design style (do not default to Neobrutalist) — list in [references/prompts.md](references/prompts.md)  
2. Emit **exactly three paragraphs**: (a) style + concept + emotional arrival, (b) type/interaction/scroll as *feeling*, (c) abstract references only — no brand names  
3. Or fill the structured landing brief template in the same file  

---

## 8. Ship checklist

- [ ] Subject-specific (not default look #1–4)  
- [ ] Token sheet followed (no invent-as-you-go colors/fonts)  
- [ ] Squint: primary CTA obvious  
- [ ] One signature; rest quiet  
- [ ] Motion: purpose + frequency justified; reduced-motion respected  
- [ ] Copy concrete; banned fluff absent  
- [ ] Responsive; visible focus; real images (not empty gray boxes / HTML doodles) when photos matter  
- [ ] Chanel: removed one accessory  

If images needed and no assets exist, use a single `IMAGES` config with Unsplash CDN URLs (template in [references/prompts.md](references/prompts.md)).

---

## Anti-slop hard floor

| Rule | Detail |
| --- | --- |
| Tokens only | One accent; no invented purple gradients/halos unless aesthetic allows |
| Real fonts | Public fonts + fallbacks; no Inter/Roboto/Arial reflex |
| No emoji by default | Unless playful brand asks |
| Layout | Deliberate alignment; no forced triple-card grid |
| Readable body | 16–20px; sufficient contrast |
| Landing CTAs | Usually **one** primary |

---

## Output shape when reporting

Keep responses dense:

1. **Plan** (token sheet + signature) — Build / first Polish  
2. **What changed** (bullets) — after implementation  
3. **Still generic?** (0–3 residual risks)  
4. **Verify** — how to view (route, command, file)  

Do not lecture design theory. Ship the page.

## Related skills (load if present)

- **frontend-design** — general distinctive UI identity  
- **interaction-design** / **review-interactions** — deeper motion craft and critique  
- **find-exemplar** — mirror a sibling page in the same product  

This skill owns **marketing/landing beautification procedure + paste prompts**. Don't restate their full bodies.
