---
name: decision-analysis
description: Price a decision under uncertainty with real stakes — build an expected-value sheet (options × outcomes × probabilities × utilities), rank the options, stress-test the ranking with a sensitivity sweep, and name the cheapest next probe. Use when choosing between options under uncertainty where being wrong costs something. Trigger phrases - "expected value", "decision matrix", "sensitivity analysis", "which option bets best", "should we ship or wait", "price this bet", "EV sheet".
---

# Decision Analysis

Ranking methods pick a favorite by feel; this skill prices the bet. `options-portfolio` deliberately keeps variety and refuses to choose early — that is correct upstream. Once the option set is stable and stakes are real, uncertainty has to be made explicit: which outcomes are possible, how likely each is, and how much each is worth. The failure this prevents is choosing from a vivid narrative instead of from the arithmetic implied by your own beliefs.

## Process

1. **Frame options × outcomes.** List 2–5 mutually exclusive options, including a real "do nothing / wait" baseline. For each, list 2–4 exhaustive, mutually exclusive outcomes. Keep outcomes at the same grain across options — if "success" means different things per row, the sheet is invalid.
2. **Assign probabilities and utilities.** Give each outcome a probability in [0,1] summing to 1 per option (shared across options when the uncertainty is common). Give each cell a utility on one consistent scale — money, expected users, days saved, or a stated 0–100 preference scale. Record the source of each number: data, base rate, or judgment. Never mix scales.
3. **Compute EV and rank.** EV(option) = Σ pᵢ·uᵢ. Rank descending. Report the margin between #1 and #2, not just the winner — a margin smaller than your utility noise is a tie in disguise.
4. **Sensitivity, then one probe.** Sweep each probability ±20% (renormalizing the rest) and check whether the ranking flips. The outcome with the biggest EV swing is what your decision actually hinges on; the cheapest way to shrink that swing is your next probe. If a cheap probe can reverse the ranking, buy it before deciding (value of information).

## Artifact

Deliver four things, then stop:

- **EV table** — options as rows, outcomes as columns, with p, utility, and row EV.
- **Ranking with margin** — #1, #2, EV gap, and a one-line tie/no-tie verdict.
- **Tornado** — one line per swept probability, ordered by EV swing on the leading option; mark any flip.
- **Recommendation + probe** — the chosen option, the assumption it is most exposed to, the next test that would change the answer, and a decision rule pre-committed before the test runs.

Script: `python scripts/decide.py --options "A,B" --outcomes "hit,miss" --probs "0.6,0.4" --utilities "100,0;20,20" --json` or `--file decision.json`, add `--sensitivity` for the sweep.

## Going deeper

- Method, formulas, two worked examples, and the Goodhart warning: [references/decision.md](references/decision.md)
- Sources and honesty notes: [references/provenance.md](references/provenance.md)
