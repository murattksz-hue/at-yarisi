# Provenance — Bayesian Updating

## Primary sources

- **Bayes, T. (1763).** "An Essay towards Solving a Problem in the Doctrine of Chances."
  *Philosophical Transactions of the Royal Society of London*, 53, 370–418. Read by
  Richard Price posthumously. The inverse-probability rule; the modern odds form is
  Laplace's.
- **Laplace, P.-S. (1812).** *Théorie analytique des probabilités*. Unified the theorem,
  introduced the normalizer, and applied it to astronomy and error.
- **Kahneman, D. (2011).** *Thinking, Fast and Slow*, Ch. 30 ("A Case Study in
  Availability: Tom W.") and Ch. 14–16. Base-rate neglect, the outside view, and why
  System 1 forms a confident posterior from a resemblance and forgets prevalence.
- **Tversky, A., & Kahneman, D. (1974).** "Judgment under Uncertainty: Heuristics and
  Biases." *Science*, 185(4157), 1124–1131. The base-rate experiments and the
  representativeness heuristic.
- **Tetlock, P. E. (2005).** *Expert Political Judgment: How Good Is It? How Can We Know?*
  Princeton University Press. Forecasters who update incrementally outperform those who
  defend fixed positions; hedgehogs over-update in the wrong places and under-update in
  the right ones.
- **Tetlock, P. E., & Gardner, D. (2015).** *Superforecasting: The Art and Science of
  Prediction*. Crown. Superforecasters use base rates, update frequently in small
  increments, and distinguish evidence strength from vividness.
- **Gigerenzer, G., & Hoffrage, U. (1995).** "How to improve Bayesian reasoning without
  instruction: Frequency formats." *Psychological Review*, 102(4), 684–704. Natural
  frequencies make the base-rate structure visible; use the 1,000-person framing.
- **McGee, H. (2019).** "Bayes's Theorem and the Test Paradox." *Synthese* 196, 1865–1885.
  On why test sensitivity alone is not an answer.

## What this skill is and is not

- It is a **bookkeeping discipline**: state a prior, state the evidence's likelihood ratio
  under both hypotheses, compute, and check the base rate. The arithmetic is trivia; the
  discipline of writing `P(E|¬H)` down is the skill.
- It is **not** a claim that people can introspect a true prior. Priors are reference-class
  estimates, revisable, and should be reported with their source.
- It is **not** a substitute for causal inference. A likelihood ratio summarizes the
  observation; it does not tell you whether the sample, instrument, or mechanism was valid.
  Pair with `evidence-appraisal` and `argument-mapping`.

## Evidence honesty

- No RCT isolates "Bayesian updating training" as a transferable skill. The nearest evidence
  is the forecasting literature (Tetlock 2005/2015): structured, incremental updating with
  scoring improves forecast accuracy relative to unstructured punditry, with modest effect
  sizes. Present the method as a structured heuristic with strong normative footing, not as
  a proven performance booster.
- The base-rate fallacy itself is one of the most replicated findings in judgment research
  (Tversky & Kahneman 1974; replicated many times, including in expert populations).
- The likelihood-ratio table in `references/bayes.md` is a reporting convention, not a
  validated measurement scale. Prefer computed error rates when available.

## Attribution in artifacts

When you present an update, name the prior's source and the LR's basis:
`prior 0.1 (base rate of X, 2025 internal data); LR 4.5 (sens .9 / spec .8, vendor specs)`.
If either is a guess, label it a guess. This is the same disclosure rule the repo applies
to research citations.
