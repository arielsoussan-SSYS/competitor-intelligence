# Creative quality rubric

Benchmarks from ZenABM's analysis of 2,828 LinkedIn ads across 211 companies.
Source: https://zenabm.com/blog/linkedin-ad-library

Use it two ways. Score competitor creative, so "their ads are good" becomes a specific
claim. And score **our own** creative, because that is where it actually changes what
Ariel does next.

## Format efficiency

| Format | CTR | CPC | Read |
|---|---|---|---|
| Thought Leader Ad | 2.68% | $3.06 | ~6x the CTR at a fifth of the cost |
| Single Image | 0.42% | $13.23 | Workhorse, expensive per click |
| Video | 0.24% | $15.61 | Lowest CTR, highest CPC |

A competitor shifting weight into Thought Leader Ads is getting more attention per
dollar, not being self-indulgent. Note the mix, not just the volume.

## What correlates with top performance

| Trait | Share of top performers |
|---|---|
| Specific offer, not a generic invitation | 65% |
| Strong, explicit CTA | 59% |
| Real people in the creative | 47% |
| Humour or meme format | 35% |
| First-person "I" voice (Thought Leader Ads) | 65% |

## What correlates with underperformance

| Trait | Share of underperformers |
|---|---|
| Text-heavy creative | 40% |
| Stock photography | 35% |
| Generic minimalism | 45% |

## Scoring

Score each unique creative 0-5, one point per top trait present, minus one per
underperformer trait. Record as `creative_score` on the ad record with a one-line
reason. Report the competitor's median, not every score.

The output that matters is comparative: "HP's median creative score is 3, ours is 1,
and the gap is almost entirely specific offers and real people." That is a defensible
version of "HP out-markets us", and it names the fix.

## Standing caution

These are correlations from a third-party sample, not causal rules and not measured
performance for any competitor we track. Label `[Estimate]`. Never state or imply that
we know a competitor's actual CTR, CPC or conversion rate. We do not.
