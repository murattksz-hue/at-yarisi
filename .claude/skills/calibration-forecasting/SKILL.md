---
name: calibration-forecasting
description: Make confidence accountable — Brier-scored forecasts, a calibration curve, and 3 testable predictions. Use when confidence ≠ accuracy, when a judgment must survive contact with the future, or when you need repeated foresight instead of one hindsight review. Trigger phrases: "how confident are you", "calibrate", "forecast", "Brier score", "what would you bet", "prediction log", "are we overconfident", "track record".
---

# Calibration & Forecasting

Confidence is cheap to state and never audited. `premortem` looks back once ("what would have made us fail?"); this skill looks forward repeatedly and scores the result. A forecast without a resolution date, a probability, and a scoring rule is a vibe, not a judgment. Expressed as one number per claim, confidence becomes falsifiable, comparable, and improvable.

## When to use

- A plan, estimate, or deadline carries a confidence word ("likely", "confident", "should be fine").
- You need to know whether a person or model is overconfident, underconfident, or merely lucky.
- Stakes justify a short prediction log you can actually resolve.

Skip it when the claim is already decided by definition or when no resolution event exists.

## Process

1. **Forecast with a number.** State the claim as a resolvable proposition, with resolution date and criteria: `"By 2026-06-30, the migration ships to prod with p95 < 200 ms."` Then attach a probability in `p = 0.01…0.99`. Never 0 or 1 — leave room to be wrong.
2. **Classify and anchor the reference class.** Ask "what fraction of comparable cases had this outcome?" (base rate) before adjusting for case specifics. Overconfidence usually enters here, not in the adjustment.
3. **Resolve against the stated criteria.** At the resolution date, record `o = 1` (happened) or `o = 0` (did not). No post-hoc redefinition of the claim.
4. **Score and inspect.** Brier per forecast: `(p − o)²`. Skill score: `1 − Brier / Brier_baseline`, with baseline = always predicting the base rate (or 0.5). Then read the calibration curve: bin forecasts, compare mean `p` to observed frequency.

A forecast log needs at least ~10–20 resolved entries before the curve means anything. Until then, report the count, not the conclusion.

## Artifact

Keep a running table; three live predictions at all times so the habit does not decay.

| # | Prediction (resolvable, dated) | p | Resolves | o | Brier |
|---|---|---|---|---|---|
| 1 | Migration ships to prod by 2026-06-30 with p95 < 200 ms | 0.70 | 2026-06-30 | — | — |
| 2 | Fewer than 2 P1 incidents in the first month post-launch | 0.60 | 2026-07-31 | — | — |
| 3 | Rollback required within 2 weeks of launch | 0.25 | 2026-07-14 | — | — |

Report: Brier score, skill score vs base rate, calibration curve (bins 0–0.2 … 0.8–1.0), n resolved, and the **3 new predictions** that replace resolved rows.

## Going deeper

- Tetlock's superforecasters, Brier score, calibration vs resolution, reference classes, overconfidence: [references/calibration.md](references/calibration.md)
- Sources and what this skill does *not* claim: [references/provenance.md](references/provenance.md)
- Scorer: `python scripts/calibrate.py --forecasts log.json --markdown` (or `--add "claim" --confidence 0.7`, `--demo`). See `--help`.
