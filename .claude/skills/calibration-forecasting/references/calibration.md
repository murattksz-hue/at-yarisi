# Calibration and forecasting

Calibration is the match between stated confidence and realized frequency. It is separable from being informative: a forecaster who always says "50%" is perfectly calibrated on coin flips and useless. Score both.

## 1. The Brier score

For a binary claim with forecast probability `p` that the claim happens, and outcome `o ∈ {0,1}`:

$$B = (p - o)^2$$

Aggregate as the mean over resolved forecasts:

$$B = \frac{1}{N}\sum_{i=1}^{N}(p_i - o_i)^2$$

Properties: lower is better; range 0–1; it is a **strictly proper scoring rule** — you minimize expected score by stating your true belief. Confident-and-right (0.95, o=1) costs 0.0025; confident-and-wrong (0.95, o=0) costs 0.9025. The asymmetry is the point: overconfidence is punished quadratically.

A raw Brier score is hard to interpret alone. Compare to a **baseline**: always predict the observed base rate `b`, whose score is exactly `b(1-b)`. Then

$$\text{skill} = 1 - \frac{B}{b(1-b)}$$

Positive = better than the base rate; negative = you would have done better ignoring the case entirely. On small samples, report `n` alongside the score — 5 forecasts can swing the skill score wildly.

## 2. Calibration vs resolution (Murphy decomposition)

Brier decomposes into three terms:

$$B = \underbrace{\frac{1}{N}\sum_k n_k (f_k - o_k)^2}_{\text{reliability}} - \underbrace{\frac{1}{N}\sum_k n_k (o_k - \bar{o})^2}_{\text{resolution}} + \underbrace{\bar{o}(1-\bar{o})}_{\text{uncertainty}}$$

- **Reliability (calibration)** — distance between mean forecast `f_k` and observed frequency `o_k` within a confidence bin. Lower is better. This is the curve.
- **Resolution (discrimination)** — how far bin outcomes spread from the overall base rate. Higher is better. Saying 0.9 for the things that happen and 0.1 for the things that don't resolves outcomes; saying 0.5 for everything does not.
- **Uncertainty** — irreducible, a property of the outcome set, not of you.

Practical reading of the calibration curve (bins 0–0.2 … 0.8–1.0): for each bin, compare mean `p` to observed frequency. Points above the diagonal = overconfident; below = underconfident. Do not fit a curve to fewer than ~10 resolved forecasts unless you are only looking for gross errors.

## 3. Overconfidence: the dominant failure

Across lab studies, people's 90% confidence intervals contain the truth far less than 90% of the time (Lichtenstein, Fischhoff & Phillips 1982; Alpert & Raiffa 1982 on interval estimation). The usual result is **overprecision** — intervals too narrow — followed by **overestimation** of one's ability and **overplacement** relative to others (Moore & Healy 2008). Kahneman (2011) frames this as the *illusion of validity*: coherence of a story is mistaken for evidence about the world.

In forecasting tournaments, the failure is visible at the extremes: forecasts of 0.9+ resolve true roughly 70–75% of the time for average participants, while the best forecasters keep those bins near the diagonal. Tetlock's finding: the strongest predictor of accuracy was not expertise or ideology but **probability discipline** — granular probabilities, frequent small updates, and explicit base rates. His "foxes" (many small competing hypotheses, self-correcting) beat "hedgehogs" (one big theory, one big forecast).

Three cheap countermeasures:

1. **Refuse round confidence.** If you "feel 80%", first ask whether 0.75 or 0.85 is more defensible. Granularity resists anchoring.
2. **State 3 independent estimates** of a quantity and use their spread (equivalent to a 3-point estimate) rather than one point value.
3. **Pre-commit the resolution rule.** Write the observation that will count as 1 and as 0 *before* the event. Post-hoc criteria inflate apparent accuracy.

## 4. Reference classes and base rates

Before adjusting for case specifics, ask: *of comparable cases, what fraction turned out this way?* This is the **outside view** (Kahneman & Lovallo 1993). It is the single highest-yield step for forecast accuracy and the one most often skipped, because the inside view (this project, this team, this plan) always feels more informative than it is.

Practical procedure:

| Step | Question | Example |
|---|---|---|
| 1. Define the class | What population does this case belong to? | Internal tools shipped by a 6-person team |
| 2. Get the frequency | How often did members succeed on time? | 11 of 30 → base rate 0.37 |
| 3. Note the reference class's failures | What predicts the exceptions? | Scope grew > 2x in every failure |
| 4. Adjust, then shrink | Move from 0.37 toward your inside-view estimate, but not all the way | Inside view says 0.8 → forecast 0.5–0.55 |

Shrinking matters: forecasters who fully adopt the inside view lose the base rate; those who ignore the case specifics lose the resolution. Tetlock's superforecasters performed rough Bayesian averaging of outside and inside views, then updated incrementally as news arrived.

## 5. Worked example A — a mostly-calibrated log

Ten resolved forecasts, base rate 0.60.

| # | Prediction | p | o | (p − o)² |
|---|---|---|---|---|
| 1 | Migration ships by 2026-06-30 | 0.90 | 1 | 0.0100 |
| 2 | p95 under 200 ms after launch | 0.85 | 1 | 0.0225 |
| 3 | No rollback needed in two weeks | 0.80 | 0 | 0.6400 |
| 4 | Fewer than 2 P1 incidents | 0.75 | 1 | 0.0625 |
| 5 | Runbook reviewed before cutover | 0.70 | 1 | 0.0900 |
| 6 | On-call handover on day one | 0.65 | 0 | 0.4225 |
| 7 | Cost increase under 10% | 0.60 | 1 | 0.1600 |
| 8 | Dashboards migrated without rework | 0.55 | 0 | 0.3025 |
| 9 | Second sprint requested for cleanup | 0.40 | 0 | 0.1600 |
| 10 | Dependency upgrade lands in same release | 0.30 | 1 | 0.4900 |

Sum = 2.36 → **Brier = 0.236**. Baseline `0.6 × 0.4 = 0.24` → skill `+0.017`. Mean forecast 0.65 vs observed 0.60: aggregate overconfidence of 0.05.

| Bin | n | Mean p | Observed | Gap |
|---|---|---|---|---|
| 0.2–0.4 | 1 | 0.30 | 1.00 | −0.70 |
| 0.4–0.6 | 2 | 0.47 | 0.00 | +0.47 |
| 0.6–0.8 | 4 | 0.68 | 0.75 | −0.07 |
| 0.8–1.0 | 3 | 0.85 | 0.67 | +0.18 |

Reading: the aggregate looks fine, but two bins are badly off. The forecaster is overconfident above 0.8 (0.85 stated, 0.67 realized) and at 0.4–0.6 said "coin flip" about things that never happened. The corrective is not "be less confident everywhere" — it is to lower the top bin, raise the middle, and keep the 0.6–0.8 region as is.

## 6. Worked example B — the clustered-0.9 failure

Eight forecasts, all stated at 0.90 ("very likely"), five resolved 1:

$$B = \frac{5(0.01) + 3(0.81)}{8} = \frac{2.48}{8} = 0.31$$

Base rate 0.625, baseline `0.625 × 0.375 = 0.234`. Skill `= 1 − 0.31/0.234 = −0.32`.

| Bin | n | Mean p | Observed | Gap |
|---|---|---|---|---|
| 0.8–1.0 | 8 | 0.90 | 0.625 | +0.275 |

The log looks responsible — every entry says "very likely" — and still loses to guessing the base rate. Diagnostics:

- **Low resolution**: one confidence level for everything means no discrimination. Nine of the ten points of information in a forecast come from *ordering* cases, not from a global confidence level.
- **Compressed scale**: if the honest spread is 0.55–0.95, stating 0.9 for everything throws away the signal.
- **Missing base rate**: 5/8 successes is unsurprising for a team with a 60% track record. The forecast should have started there, not at 0.9.

Fix pattern: spread the forecasts (`0.55, 0.6, 0.65, 0.7, …`), tag each with the reference class, and log the resolution date so the log cannot quietly grow only winners.

## 7. Using the log

- **Three live predictions at all times.** Write them into the deliverable, not a personal note. Unresolved forecasts are the ones that never get scored.
- **Resolve on the date, not when convenient.** Late resolution biases toward claims that became obvious.
- **Score batches, not single forecasts.** Read the curve at n ≥ 10–20; act on it only when a bin gap persists across batches.
- **Keep the losers.** A log of hits is a press release; a log of misses is a measurement instrument.

`scripts/calibrate.py` computes the Brier score, skill score, bias, and bins for a JSON log; `--add`, `--resolve`, `--score`, and `--demo` cover the workflow.
