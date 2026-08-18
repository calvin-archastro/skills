# For You ranking (xai-org/x-algorithm)

Source: [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) (Aug 13–14 2026 dump).  
Weights: `home-mixer/params/param.rs`, last synced **2026-08-12**.  
Arithmetic: `home-mixer/scorers/ranking_scorer.rs`.  
Visibility drops: `visibility-filtering/rules/registry.rs`.

Load this when judging format, distribution, or "will this rank." Do not dump it into a review.

For You is personalized: Phoenix reads the viewer's last ~1022 actions and predicts **that viewer's** P(reply), P(quote), P(share), P(report), etc. Same post can rank #1 for one person and #0 for another. There is no verified boost, follower-count feature, or hand-tuned "media type" weight.

## Score

```
score = Σ (weight_i × predicted P(you do action_i))
      then × author-diversity × OON/reply-RT haircut
      then DPP reorder (less-similar neighbors)
```

Weights multiply **predicted probabilities** (or predicted dwell seconds), not raw like/report counts. Do not say "1 report cancels 468 likes." Reports are ~1000× rarer than likes; the huge negative weight exists so a non-zero P(report) can move the score at all.

Only engagements on posts **served in Home** count. Group-chat brigades and direct-navigated reports do not.

## Action weights (production defaults)

| Action | Weight | Review meaning |
| --- | ---: | --- |
| Copy-link share | **20.0** | Highest. Artifact people paste elsewhere. |
| Reply on a **mutual-follow original** | **20.0** (5 + 15) | Friends talking on originals. Boost is originals only — not their replies/RTs. |
| Reply / DM-share / Quote | **5.0** | Conversation + redistribution. This skill's objective. |
| Follow author | **4.0** | "I want more of this person." |
| In-app share | **2.0** | |
| Repost | **1.0** | Cheap vs quote. |
| Like | **0.5** | Weak. Like-farming is the wrong objective. |
| Click post | **0.4** | |
| Open link | **0.2** | |
| Photo expand / video open / quality view | **0.05** | Media is almost a rounding error. |
| Predicted dwell time | **0.004 × seconds** | 30s ≈ 0.12; 2 min ≈ 0.48. Real, not king. |
| Binary dwell / profile click | **0.0** | Off. |

Negatives (same "predicted P" caveat): report −234, mute −58.8, not-interested −43.2, block −31.2, no-dwell −0.02.

Retrieval (getting *into* the candidate set) is trained with **likes as the positive**. Ranking is where reply/quote/share take over.

## Structural prefs (applied after the weighted sum)

1. **Originals from follows beat everything else structurally.** In-network replies and RTs get the same **×0.75** haircut as strangers (`EnableOonRescoreForInNetworkRepliesRetweets = true`).
2. **Stranger replies/RTs never enter For You** — filtered before scoring (`OONRetweetReplyFilter`).
3. **>48 hours is dropped** (`AgeFilter`). Recycle = new original.
4. **Already seen/served is dropped.**
5. **Author diversity:** 2nd post from the same author ×0.5, down to a **0.25 floor**. Then VMRanker DPP (θ 0.65) separates similar neighbors.
6. **Stranger originals ×0.75.** Topic feeds ×0.5.
7. **Small-account first-day slot:** author <1k impressions, <1k followers, post <24h old → lifted toward positions 15–16.
8. **Your own posts are filtered.**

## Visibility (never ranked)

Hard drops: suspended/deactivated/protected authors, blocks, mutes, muted keywords, subscriber-only you can't access, spam, hate, violent speech, civic-integrity, legal takedown.

**Followers still see; strangers do not:** high-recall spam, NSFW, gore, "do not amplify," malicious URLs, impersonation, compromised, abusive-high-recall. NSFW from a follow → interstitial; from a stranger → gone.

## Flag these in review

| Draft move | Problem | Fix |
| --- | --- | --- |
| Post the take as a **reply** to a big account | Stranger replies never enter For You | Rewrite as an **original** |
| "Just RT it" / "reply for reach" | In-network replies/RTs ×0.75; OON ones are dropped | Original, or a **quote** (weight 5) |
| Like-bait one-liner | Like = 0.5; no answer-path | Reply/quote/copy-link path |
| Burst of 4–8 posts | Diversity decay buries #2–#8 | One original, farm 30–60m |
| Essay split into many originals | Same decay; only tweet 1 of a thread ranks | One `1/` `2/` thread, not a series |
| Recycle a >48h post | Age filter deletes it | New original |
| Screenshot-less take / no stealable thing | Copy-link is the #1 weight | Add a repo, recipe, or real screenshot |
| Write only for strangers | Mutual-follow originals get reply weight 5→20 | Write so people who follow you back will answer |
| NSFW / spammy if they want discovery | OON NSFW and high-recall spam are dropped | Keep discovery-safe; followers are more forgiving |

## Do not claim

- Follower count, blue check, or "post at 9am" as ranking features. Not in the ranker.
- "1 report = N likes." Weights scale predictions, not counts.
- That coordinated blocks/reports will sink a post for everyone. Predictions are personalized; only Home-served engagements count.
