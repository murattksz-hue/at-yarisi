# Provenance & Honesty Notes

## Primary sources

- **Halpern, D. F. (2014). *Thought and Knowledge: An Introduction to Critical Thinking* (5th ed.). Psychology Press — Ch. 10, "Decision Making."** Frames decision making as a core critical-thinking competency alongside verbal reasoning, argument analysis, hypothesis testing, and likelihood. Halpern's treatment supplies the pedagogical frame used here: make alternatives explicit, weigh consequences against probabilities, and check the decision process rather than only the outcome. The skill's four steps are a compressed operationalization of that chapter's procedure, not a new theory.
- **Howard, R. A., & Matheson, J. E. (1984). "Influence Diagrams." In *The Principles and Applications of Decision Analysis*, Vol. II. Strategic Decisions Group.** The canonical statement of decision analysis as a professional discipline: alternatives, information, values, and preferences decomposed before choice. Source for the normative EV/expected-utility framing, the insistence on exhaustive alternatives, and the idea that information has value only through its effect on the decision (value of information).
- **Arkes, H. R., & Blumer, C. (1985). "The psychology of sunk cost." *Organizational Behavior and Human Decision Processes*, 35(1), 124–140.** Documents the sunk-cost fallacy: people let unrecoverable past investments distort forward-looking choice. Used here as a guardrail — utilities must be scored from the decision point forward, never as recovery of past spend.

## Method lineage (not directly cited in the skill body)

- **Expected utility theory** — Bernoulli (1738) on utility vs. value; von Neumann & Morgenstern (1944) axiomatization. Justifies using a 0–100 utility scale when monetary EV ignores risk aversion.
- **Sensitivity analysis / tornado diagrams** — standard decision-analysis practice from the Howard–Matheson school; one-at-a-time parameter sweeps ordered by output swing. The ±20% relative sweep in `decide.py` is a conventional stress test, not a claim of a privileged interval.
- **Value of information** — Howard (1966), "Information Value Theory," *IEEE Transactions on Systems Science and Cybernetics*. The upper bound "EV with free information minus EV now" is the textbook ideal-probe bound; real probes capture less.

## Evidence honesty

- Like every skill in this track, this is a **structured heuristic, not a validated booster**. There are no RCTs isolating "EV sheets" as an intervention, and the plan's caution applies: critical-thinking instruction shows modest, transferable gains when taught as explicit procedures with practice — do not promise large effects.
- Expected-value reasoning is **normative, not descriptive**. People reliably violate it (Kahneman & Tversky's prospect theory: loss aversion, probability weighting). The skill prescribes the arithmetic; it does not claim unaided humans follow it.
- **Goodhart's law** (Goodhart 1975; Strathern 1997) is the built-in failure mode: once a utility proxy becomes the target, it stops measuring the construct. Utility scales must be paired with a construct statement and a gaming check, or the EV sheet optimizes the wrong thing.
- Known limits: EV is only as good as its inputs; probabilities below ~0.05 and utilities on heavy-tailed outcomes are poorly served by point estimates; and concave utility curves can reverse a raw-EV ranking. Say which scale you used.
