---
name: bayesian-updating
description: Update beliefs with evidence — prior → likelihood ratio → posterior, plus a base-rate check and value-of-information probe. Use when a prior belief meets new evidence and you need to know how much to move (or whether to move at all). Triggers: "base rate", "how much should I update", "posterior", "Bayes", "likelihood ratio", "prior odds".
---

# Bayesian Updating

Makes belief revision proportional to evidence instead of to surprise, rhetoric, or
recency. Scenario-planning enumerates *possibilities*; this skill assigns
*probabilities* to them and revises those probabilities when evidence arrives.

## When to use

- A forecast, diagnosis, candidate, or hypothesis has a prior and new evidence lands.
- Someone quotes a test result, metric, or anecdote as if it were `P(hypothesis | evidence)`.
- You must decide whether another probe (test, interview, pilot, sample) is worth its cost.

Do not use it to invent a prior from nothing — use [evidence-appraisal](../evidence-appraisal/SKILL.md)
or a reference class first.

## Process

1. **Elicit the prior, from a base rate.** Ask "out of comparable cases, what fraction
   were true?" — a reference class, not a vibe. State it as odds (`p : 1-p`) and write
   down where it came from. If no base rate exists, say so and use the widest defensible range.
2. **Estimate the likelihood ratio (LR).** `LR = P(evidence | H) / P(evidence | ¬H)`.
   For a test: `LR+ = sensitivity / (1 - specificity)`. Ask both questions explicitly:
   "how likely is this evidence if the claim is true?" *and* "how likely if it is false?"
   Most errors come from skipping the second.
3. **Compute the posterior in odds form.** `posterior odds = prior odds × LR`, then
   `p = odds / (1 + odds)`. Run the base-rate check: compare the result with the naive
   `LR / (1 + LR)` (a 50/50 prior). A large gap means base-rate neglect is the whole story.
4. **Price the next probe (value of information).** Ask which observation would move the
   posterior most and what it costs. Test the *discriminating* case: an LR near 1 is not
   worth collecting; an LR of 10+ is. Stop when no affordable probe can shift the decision.

## Artifact

Produce this table, not a paragraph:

| Prior (source) | Evidence | LR (P(E\|H)/P(E\|¬H)) | Posterior | Base-rate flag | Next probe worth it? |
|---|---|---|---|---|---|
| 0.10 (base rate of X in class) | positive test, sens .9 / spec .8 | 4.5 | 0.33 | yes — naive 0.82 overstates by 49 pp | repeat test (LR ≈ 5) only if it changes the action |

Then one line: **decision threshold** — the posterior at which you would act differently,
and whether the current posterior clears it.

## Helper

```bash
python scripts/bayes.py --prior 0.1 --lr 9 --json
python scripts/bayes.py --prior 0.01 --sensitivity 0.9 --specificity 0.8 --base-rate
python scripts/bayes.py --prior 0.2 --lrs "4,0.5,2"          # sequential evidence
```

`--prior2`, `--hit-rate`/`--false-alarm`, and `--prior-odds` are also supported;
`--help` lists every flag.

## Failure modes

- **Base-rate neglect:** reading `P(E|H)` as `P(H|E)`. Always show both.
- **Double-counting:** reusing the same evidence under two names; LRs are not independent.
- **Certainty inflation:** multiplying many LRs and landing on 0.99 from soft inputs.
- **Unfalsifiable prior:** a prior that no observation could move is a belief, not a model.

## Going deeper

- Bayes rule, odds/log-odds, base-rate fallacy, LR intuition, three worked examples:
  [references/bayes.md](references/bayes.md)
- Where the method comes from and how strong the evidence is:
  [references/provenance.md](references/provenance.md)
