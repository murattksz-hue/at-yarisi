# Provenance and limits

What this skill's moves rest on, and what they do not claim.

## Sources

**Forecasting tournaments and superforecasting**

- Tetlock, P. E. (2005). *Expert Political Judgment: How Good Is It? How Can We Know?* Princeton University Press. — The two-decade IARPA-adjacent tournament finding: domain expertise and ideological confidence predicted *worse* accuracy; "foxes" with granular probabilities beat "hedgehogs" with one big theory. Source of the fox/hedgehog and granular-probability claims.
- Tetlock, P. E., & Gardner, D. (2015). *Superforecasting: The Art and Science of Prediction.* Crown. — Popular synthesis; source of the "frequent small updates, explicit base rates, granular probabilities" cluster of practices used in [calibration.md](calibration.md) §3–4.
- Mellers, B., Ungar, L., Baron, J., et al. (2014). Psychological strategies for winning a geopolitical forecasting tournament. *Psychological Science*, 25(5), 1106–1115. — The Good Judgment Project results: top performers' accuracy advantage was large and stable across questions; associated with probabilistic reasoning and frequent updating.

**Scoring rules**

- Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3. — The mean squared probability score.
- Murphy, A. H. (1973). A new vector partition of the probability score. *Journal of Applied Meteorology*, 12(4), 595–600. — Reliability/resolution/uncertainty decomposition.
- Good, I. J. (1952). Rational decisions. *Journal of the Royal Statistical Society B*, 14(1), 107–114. — Logarithmic score, the main alternative strictly proper rule; it punishes confident errors even harder than Brier.

**Overconfidence and the outside view**

- Lichtenstein, S., Fischhoff, B., & Phillips, L. D. (1982). Calibration of probabilities: The state of the art to 1980. In Kahneman, Slovic & Tversky (Eds.), *Judgment Under Uncertainty: Heuristics and Biases.* Cambridge University Press. — The canonical review of overconfident interval estimates.
- Alpert, M., & Raiffa, H. (1982). A progress report on the training of probability assessors. In the same volume. — Interval overprecision and the case for feedback-based training.
- Moore, D. A., & Healy, P. J. (2008). The trouble with overconfidence. *Psychological Review*, 115(2), 502–517. — Separates overestimation, overplacement, and overprecision; the three do not always move together.
- Kahneman, D. (2011). *Thinking, Fast and Slow.* Farrar, Straus and Giroux. — Ch. 19–20 (illusion of validity, intuition vs. formula), Ch. 24 (outside view); the "illusion of validity" framing in §3.
- Kahneman, D., & Lovallo, D. (1993). Timid choices and bold forecasts: A cognitive perspective on risk taking. *Management Science*, 39(1), 17–31. — The planning-fallacy/outside-view evidence behind the reference-class procedure in §4.

**Critical-thinking frame**

- Facione, P. A. (1990). *Critical Thinking: A Statement of Expert Consensus for Purposes of Educational Assessment and Instruction* (The Delphi Report). American Philosophical Association. — Places self-regulation (monitoring and correcting one's own inference) as a core critical-thinking disposition; calibration is that disposition made measurable.

## Limits and honesty notes

- **No RCT isolates this skill.** The evidence is tournament performance under feedback, not a trial of "teach calibration and accuracy improves." Treat the processes here as structured heuristics with a plausible mechanism, not a proven booster.
- **Small-n scores are noise.** Brier and skill scores on fewer than ~10–20 resolved forecasts are descriptive, not diagnostic. The script prints `n` for this reason.
- **Skill scores depend on the baseline.** Comparing to the base rate flatters forecasters on low-uncertainty question sets and punishes them on high-uncertainty ones; always state which baseline was used.
- **Reference classes can be shopped.** Choosing the class after seeing the outcome manufactures any base rate you want. Fix the class at forecast time and write it down.
- **Overconfidence results are task-dependent.** Overprecision of intervals is robust; "better than average" effects vary with task difficulty (Moore & Healy 2008). Do not import a blanket "people are overconfident" conclusion into a specific domain without the local curve.
- **Brier ≠ decision quality.** It scores the probability, not the value of acting on it. A well-calibrated forecast can still support a bad decision; pair with a decision/EV method for that.
- **Not a personality claim.** Being scored does not make anyone a "calibrated person"; it makes a specific set of forecasts auditable.

## Relation to adjacent skills

- `premortem` — one-shot hindsight rehearsal before committing. This skill is the repeated-foresight complement: dated, scored predictions.
- Bayesian updating — how much to move given evidence. This skill asks whether the resulting numbers survive aggregation.
- Decision analysis — turns probabilities into expected value. Calibration supplies the `p` inputs; the decision method supplies the payoffs.
