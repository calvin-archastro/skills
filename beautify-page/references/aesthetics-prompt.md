# Frontend aesthetics — system injection

Canonical anti-slop block (Anthropic frontend-aesthetics cookbook lineage).
Inject into system prompt, CLAUDE.md, AGENTS.md, or agent instructions when generating UI.

## Distilled aesthetics prompt

```text
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend
design, this creates what users call the "AI slop" aesthetic. Avoid this:
make creative, distinctive frontends that surprise and delight. Focus on:

Typography: Choose fonts that are beautiful, unique, and interesting. Avoid
generic fonts like Arial and Inter; opt instead for distinctive choices that
elevate the frontend's aesthetics.

Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for
consistency. Dominant colors with sharp accents outperform timid,
evenly-distributed palettes. Draw from IDE themes and cultural aesthetics
for inspiration.

Motion: Use animations for effects and micro-interactions. Prioritize
CSS-only solutions for HTML. Use Motion library for React when available.
Focus on high-impact moments: one well-orchestrated page load with staggered
reveals (animation-delay) creates more delight than scattered micro-interactions.

Backgrounds: Create atmosphere and depth rather than defaulting to solid
colors. Layer CSS gradients, use geometric patterns, or add contextual
effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed
for the context. Vary between light and dark themes, different fonts,
different aesthetics. You still tend to converge on common choices (Space
Grotesk, for example) across generations. Avoid this: it is critical that
you think outside the box!
</frontend_aesthetics>
```

## Typography-only isolator

Use when you want better type without restyling color/layout:

```text
<use_interesting_fonts>
Typography instantly signals quality. Avoid boring, generic fonts.

Never use: Inter, Roboto, Open Sans, Lato, default system fonts

Impact choices:
- Code aesthetic: JetBrains Mono, Fira Code, Space Grotesk
- Editorial: Playfair Display, Crimson Pro, Fraunces
- Startup: Clash Display, Satoshi, Cabinet Grotesk
- Technical: IBM Plex family, Source Sans 3
- Distinctive: Bricolage Grotesque, Obviously, Newsreader

Pairing principle: high contrast = interesting.
Display + monospace, serif + geometric sans, variable font across weights.

Use extremes: 100/200 weight vs 800/900, not 400 vs 600.
Size jumps of 3x+, not 1.5x.

Pick one distinctive font, use it decisively. Load from Google Fonts.
State your choice before coding.
</use_interesting_fonts>
```

## Theme lock pattern

Replace the aesthetic name and cues; keep the "always design with" force:

```text
<always_use_THEME_theme>
Always design with [THEME] aesthetic:
- [palette cues]
- [shape / material cues]
- [atmosphere]
- [typography cues]
</always_use_THEME_theme>
```
