# Bayes Rule, Odds, and Likelihood Ratios

## The rule

For hypothesis `H` and evidence `E`:

```
P(H | E) = P(E | H) · P(H) / P(E)
```

`P(H)` is the prior, `P(E|H)` the likelihood, `P(H|E)` the posterior. The denominator
`P(E) = P(E|H)P(H) + P(E|¬H)P(¬H)` is just a normalizer — it is why the posterior sums to 1.

## Odds form (use this)

Beliefs are easier to update as odds. With `O(H) = P(H) / (1 - P(H))`:

```
O(H | E) = O(H) × LR,        LR = P(E | H) / P(E | ¬H)
```

The likelihood ratio is also called the **Bayes factor**. It is the entire evidential
content of `E`: how much more likely the observation is under `H` than under `¬H`.
- `LR = 1` — no information; posterior equals prior.
- `LR > 1` — supports `H`; `LR = 2` doubles the odds, `LR = 10` multiplies them by ten.
- `LR < 1` — supports `¬H`; `LR = 0.1` divides the odds by ten.

Convert back with `p = odds / (1 + odds)`.

### Log-odds (use when chaining)

```
logit(p) = ln(p / (1 - p))
logit(posterior) = logit(prior) + ln(LR)
```

Independent evidence adds in log-odds. This makes sequential updating trivial and keeps
numbers stable: ten "weak" LRs of 1.2 add to `ln(1.2) × 10 ≈ 1.82`, i.e. odds ×6.2 —
not the ×1.2 someone might assume. It also exposes double-counting: correlated evidence
must **not** be added as if independent.

## Likelihood ratio intuition

| LR | Strength (rough) | Typical source |
|---|---|---|
| 1 | none | uninformative test, base-rate restatement |
| 1–2 | barely worth collecting | noisy survey item |
| 2–5 | weak-to-moderate | single observational result |
| 5–10 | moderate | replicated correlational finding, decent test |
| 10–30 | strong | controlled experiment with clear effect |
| > 30 | very strong | near-deterministic measurement |

These are conventions, not laws. Derive the LR from the actual error rates whenever you
can, and state the assumption behind it.

## The base-rate fallacy

The most common Bayesian error is answering `P(E|H)` when asked `P(H|E)`. With a rare
hypothesis, even a good test yields mostly false positives.

Medical screening example: prevalence 1%, sensitivity 90%, specificity 80%.
`LR+ = 0.9 / (1 - 0.8) = 4.5`, prior odds `0.01/0.99 ≈ 0.0101`, posterior odds
`0.0455`, so `P(disease | positive) ≈ 4.3%` — not 90%. Out of 1,000 people: 10 sick,
9 detected; 990 healthy, 198 false positives. Of 207 positives, 9 are true (4.3%).
The naive "ignore the base rate" answer `LR/(1+LR) = 82%` is wrong by ~78 percentage points.

**Rule:** never report a test result without the prior. If someone gives you only
sensitivity, ask for prevalence.

## Worked example 1 — medical test

- Prior: prevalence of the condition in this age band = 1% → odds 0.0101.
- Evidence: positive screen, sensitivity 0.90, specificity 0.80 → `LR+ = 4.5`.
- Posterior odds `= 0.0101 × 4.5 = 0.0455` → `P = 0.0435` (4.3%).
- Base-rate flag: naive posterior 81.8%; the prior changes the answer by 77 pp.
- Next probe: a confirmatory test with `LR+ ≈ 10` would take odds to 0.455 (31%). Worth it
  only if treatment has real harms; otherwise "watch and retest" may dominate.

## Worked example 2 — hiring signal

- Hypothesis: this candidate will perform well (top-quartile within 18 months).
- Prior: base rate for this role/level = 30% → odds `0.3/0.7 ≈ 0.429`.
- Evidence: strong structured work sample. From past calibration, candidates who later
  performed well pass at 70%; those who did not pass at 25% → `LR = 0.70/0.25 = 2.8`.
- Posterior odds `= 0.429 × 2.8 = 1.20` → `P ≈ 0.545` (55%).
- Base-rate flag: naive 74%; the 30% base rate cuts this to 55%. Still a coin flip —
  one work sample does not make a hire certain. Next probe: a second independent work
  sample (`LR ≈ 2.8`) → odds 3.36 → 77%, if the two samples are genuinely independent.

## Worked example 3 — retention experiment

- Hypothesis: a new onboarding flow raises 30-day retention by ≥10% relative.
- Prior: from base rates of similar UI changes at this company, 20% ship a real lift
  of that size → odds 0.25.
- Evidence: pilot with n≈2,000 shows the lift at p≈0.05 with a plausible mechanism.
  Treating that as `LR ≈ 4` (not 20 — p-values are not Bayes factors and the mechanism
  was chosen post hoc): posterior odds `= 0.25 × 4 = 1.0` → `P = 0.50`.
- Base-rate flag: naive 80%; the prior halves it. Still not a ship decision on its own.
- Next probe: a holdout for one more full cohort. Halve the confidence interval before
  committing rollout spend; the probe is worth it because the decision is reversible but
  expensive.

## Sequential updating

`--lrs "4,0.5,2"` chains: posterior after 4 becomes the prior for 0.5, etc. Log-odds are
additive, so order does not matter *if* the LRs are conditionally independent. When two
observations share a cause (same sample, same source, same biased instrument), combine
them into one LR rather than multiplying.

## Reporting template

```
Prior 0.10 (base rate for class X, source: ...)
Evidence: positive test; P(E|H)=0.90, P(E|¬H)=0.20 → LR 4.5
Posterior odds 0.045 / 0.955 = 0.047 → P 0.33?  (compute, do not guess)
Base-rate check: naive LR/(1+LR) = 0.82 → prior matters
Decision threshold: act at P > 0.60 → not met
Next probe: confirmatory test (LR ≈ 10) at cost C; expected shift +0.5 odds
```
