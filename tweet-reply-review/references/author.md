# Default author + live fetch

Default handle: **`@CalvinGrunewald`**  
Override when the user names another account, or when autopsying a posted URL (use that post's author).

This file is the only place the default handle lives. Playbook stays anonymized.

## Fetch (required before scoring)

Use whatever X/Twitter search the harness exposes. Query contract:

```
from:<handle> since:<YYYY-MM-DD> -filter:replies
sort: Latest
limit: 10
```

`since` = today minus 14 days.

If fewer than 5 originals come back, drop the date filter and retry Latest / 10.

If search is unavailable or empty: Timing line is `no live fetch — timing from playbook only`. Continue. Do not invent counts.

Do not fetch replies/RTs for the cadence window — For You is originals.

## Derive (keep the raw list off the review)

From the 10 originals, compute:

| Signal | How | Changes the review |
| --- | --- | --- |
| **Last original** | newest timestamp + hours ago | If **<2h** and it has replies → farm that, don't ship a new original. If **>48h** → For You is dead; a new original is fine. |
| **24h count** | originals with timestamp in last 24h | **≥2 already today** → wait. Ranker decays the 2nd+ post from the same author (see `x-algorithm.md`). |
| **7d count** | originals in last 7 days | High volume + low replies → stop spraying; one stronger original. |
| **Working now** | highest **replies** in the window (tie-break: bookmarks, then views) | Rewrite into that **pattern**, not a stale playbook favorite. |
| **Dead shapes** | originals with replies ≤1 despite views | Do not rewrite the draft into that shape. |
| **Topic fatigue** | last 3 originals share topic or shape | Switch pattern unless that shape is still the reply leader. |
| **Voice** | see below | Convert and rewrite in *this week's* voice, not a persona. |

Reply count on the fetched originals is the live learning signal. Likes/views are secondary.

## Voice (from the same 10 originals)

Do not invent a house style. Copy what is actually on the account this week:

1. **Casing** — title case vs lowercase vs mixed
2. **Length** — one-liners vs `1/` threads vs screenshot + caption
3. **Person** — I / we / no subject
4. **Ask** — how they invite a reply (or that they usually don't — then add a light one, don't bolt on "What do you think??")
5. **Texture** — slang, excitement, parentheticals, @-credits when load-bearing
6. **Media habit** — if 6/10 have photos, say "attach a screenshot" rather than writing an essay

If fetch fails: Account A playbook templates, still not LinkedIn.

## Cadence → the call (same headlines as SKILL.md)

- **Post it** — 0 originals in last 24h, last original ≥4h old or already dead for replies
- **Farm the last post first** — last original <2h old *or* still pulling replies
- **Wait — you already posted today** — ≥2 originals in last 24h (diversity decay). Suggest a clock time, not "later"
- **Wait — you already posted today** (stronger) — 3+ originals in last 24h, or last 3 are the same shape with weak replies. Say they dumped too many.
