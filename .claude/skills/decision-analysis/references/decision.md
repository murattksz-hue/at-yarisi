# Decision Analysis: EV, Sensitivity, and Value of Information

## The core move

Decision analysis replaces "which option feels right?" with "which option has the best expected consequence given what I believe?" It is normative, not descriptive: it does not claim people compute EVs, only that a decision is defensible when its arithmetic is inspectable. Howard & Matheson (1984) framed it as the professional approach to decision making: decompose a decision into alternatives, information, values, and preferences; then choose the alternative whose expected utility is highest.

The four primitives:

| Primitive | Meaning | Common error |
|---|---|---|
| Options (alternatives) | Mutually exclusive actions you can take, including wait/do-nothing | Omitting the baseline; options that are not exclusive |
| Outcomes | Exhaustive, mutually exclusive results per option | Starting at 2 outcomes and ignoring "partial" cases |
| Probabilities | Degree of belief each outcome occurs, given the option | Using point estimates with no source; probs that don't sum to 1 |
| Utilities | Desirability of each outcome on one scale | Mixing dollars and "user happiness"; ignoring risk aversion |

## Expected value and expected utility

For option $i$ with outcomes $j$:

$$EV_i = \sum_j p_{ij}\, u_{ij}$$

Rank by EV. Two refinements matter:

- **Expected utility, not raw value.** If \$1M is life-changing and \$10M is merely better, the utility curve is concave; a 50/50 bet between \$0 and \$10M is worth less than its \$5M monetary EV. Use a stated utility scale (0–100) when the stakes are not linear in money.
- **One probability vector per sheet.** The helper takes a single shared vector of outcome probabilities. If two options face genuinely different risk profiles, represent that in the utilities (different outcomes) or run a separate sheet per option and compare EVs; do not splice probability rows from different outlooks into one table.

EV is only as good as its inputs; that is why steps 3–4 exist. A precise EV from fabricated probabilities is worse than a rough one from stated ones.

## Sensitivity and the tornado

Sensitivity asks: **which assumption is doing the work?** Vary one input at a time, hold the rest fixed, and record the resulting EV range.

Protocol used by `scripts/decide.py`:

1. For each outcome probability $p_j$, form $p_j^- = \max(0, 0.8 p_j)$ and $p_j^+ = \min(1, 1.2 p_j)$.
2. Keep the other outcomes' relative weights but rescale them so the vector still sums to 1: each other $p_k$ becomes $p_k \cdot (1 - p_j^{\pm}) / (1 - p_j)$.
3. Recompute every option's EV at both ends.
4. Report the swing (max EV − min EV) for the leading option, and whether the identity of the best option changes.

Sort by swing descending — that ordering is the tornado. A zero probability never moves under a relative sweep; if an outcome is plausible but assigned 0, that is a framing bug, not a sensitivity result.

**Rank stability beats EV precision.** If the leader survives every ±20% perturbation, the recommendation is robust and further precision is waste. If it flips, you have located the decision's hinge — go get information there, not everywhere.

## Value of information (VOI)

Information is worth buying only if it can change the decision. A rough upper bound:

$$VOI \le EV(\text{decide after the probe}) - EV(\text{decide now})$$

Practical rule: **probe the input with the largest tornado swing that is cheap to observe.** If the swing is small, or the probe costs more than the EV gap it could close, decide now. VOI is the antidote to analysis paralysis — it prices the next experiment instead of demanding certainty.

## Worked example 1: ship vs. wait

A team can **Ship** a feature now or **Wait** one sprint for a fix. Outcomes: hit (users adopt) or miss.

| Option | P(hit) | U(hit) | P(miss) | U(miss) | EV |
|---|---|---|---|---|---|
| Ship | 0.60 | 100 | 0.40 | 0 | **60** |
| Wait | 0.60 | 20 | 0.40 | 20 | **20** |

Ship wins by 40. But the utilities encode a judgment: waiting guarantees a modest 20 either way, shipping gambles on 100. If the team is risk-averse, the utility of 100 may be 60, not 100 — then Ship = 0.6·60 = 36 vs. Wait = 20, and the recommendation narrows. The tornado over P(hit) ±20% (0.48–0.72) moves Ship's EV from 48 to 72 and never flips the ranking against Wait's fixed 20: robust. A probe is not worth buying: the ranking would reverse only if P(hit) fell below 0.20, and no cheap test plausibly moves a 0.60 estimate that far. Recommendation: ship now.

## Worked example 2: hiring bet with a cheap probe

Options: **Hire A**, **Hire B**, or **Contract-to-hire**, under a shared outlook p(strong)=0.5, p(adequate)=0.3, p(weak)=0.2.

| Option | U(strong) | U(adequate) | U(weak) | EV |
|---|---|---|---|---|
| Hire A | 100 | 50 | −40 | 50 + 15 − 8 = **57** |
| Hire B | 70 | 50 | 30 | 35 + 15 + 6 = **56** |
| Contract | 40 | 40 | 10 | 20 + 12 + 2 = **34** |

A leads B by 1 — inside the noise of a 0–100 utility scale, so this is a tie in disguise. The sensitivity sweep settles it: moving p(weak) from 0.16 to 0.24 takes A from 61.85 down to 52.15 (it loses 9.7), while B moves from roughly 57.3 to 54.7 — the ranking flips. Sweeping p(strong) flips it too. The decision hinges on A's downside risk, and a one-day work sample resolves exactly that. Since a cheap probe can reverse the choice, its value of information exceeds its cost: run the sample, pre-commit to the cutoff, then hire.

## Warnings

- **Goodhart / operationalization.** Utilities are proxies. If you optimize "hours saved" or "tickets closed," people will produce hours and tickets, not outcomes. Name the construct the utility is meant to represent, and check that maximizing it is not reward-hacking the measure. A utility that is easy to score is not automatically the utility you care about.
- **Arkes & Blumer (1985): sunk cost.** Past spend is not an outcome of future options. If a cell's utility depends on what you already paid, you have smuggled in a sunk cost — rescore from the decision point forward.
- **Framing and anchoring.** The first option listed and the first probability stated anchor the rest. Generate the option set before scoring, and score each row independently before comparing.
- **False precision.** Two significant figures are enough. If the ranking depends on the third decimal, you have not measured anything that precisely.
- **Utility is not money.** For large or existential stakes, concavity and risk aversion can reverse a raw-EV ranking. Say which scale you used and why.
