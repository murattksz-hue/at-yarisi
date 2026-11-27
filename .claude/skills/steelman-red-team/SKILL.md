---
name: steelman-red-team
description: Stress-test a position against its strongest rival — steelman the counter-position (the best case for the other side), red-team your own claim with five attack vectors, then pre-commit to what would falsify it. Use when critique feels weak, when you might be strawmanning dissent, or before a high-stakes commitment. Trigger phrases: "steelman", "strongest counter", "red team this", "what would prove me wrong", "argue the other side", "am I strawmanning?".
---

# Steelman & Red-Team

The failure this prevents: *confident agreement with yourself*. A weak critique ("they just don't get it") feels like scrutiny but is reassurance. Strawmanning dissent lets a claim survive scrutiny it never faced.

A **premortem** asks "we failed — why?" (imagine the future outcome). **Steelman/red-team** asks "they're right — how?" (construct the strongest present case against your claim). Run this before you defend, decide, or ship.

## Process

1. **Steelman the counter-position.** Write the strongest opposing claim `¬P` — stronger than any critic has stated it. Give it its best premises, its best evidence, and the concessions it is owed. Test: *would a smart proponent of `¬P` sign this?* If not, you have a strawman; revise. (Principle of charity in [references/steelman.md](references/steelman.md).)
2. **Red-team your own claim.** Attack `P` along five vectors, one at a time:
   - **Evidence** — weakest empirical link; what would an expert cite against it?
   - **Logic** — unstated premise, equivocation, correlation-as-cause.
   - **Incentives** — who benefits if `P` is believed? What does that bias?
   - **Alternative explanation** — what else produces the same observation?
   - **Cost** — what does `P` cost in money, optionality, or trust if wrong?

   Rank each vector: *fatal / serious / survivable*. Fix or price the top two.
3. **Pre-commit to falsification.** Before defending, write what outcome would make you abandon `P` — a specific observation, threshold, and deadline. Name the observation you would otherwise rationalize. If nothing could change your mind, the claim is faith, not a belief.

## Artifact

| Item | Content |
|---|---|
| Steelman | `¬P` in one sentence + 3 premises + the concession it earns |
| Attack vectors | 5 rows: vector, strongest hit, severity, response or patch |
| Falsifier | "I abandon `P` if ___ by ___" + one result I'd be tempted to explain away |

## Guardrails

- Attack the claim, not the person. No motive-guessing substitutes for a counter-argument.
- Concessions must be real: if `¬P` wins on a sub-point, record it.
- Steelmanning is symmetric but not neutral — after the exercise, still state your posterior and act.
- Do not invent fake counter-evidence; mark unknowns as gaps to check.

## Going deeper

- Steelman vs strawman, charity, adversarial collaboration, red-team method, two worked examples: [references/steelman.md](references/steelman.md)
- Sources and epistemic honesty notes (Paul–Elder, Zenko, Tetlock, Popper): [references/provenance.md](references/provenance.md)
- Scaffold generator: `python scripts/redteam.py --claim "your claim" --json` (add `--position "the rival claim"` or `--vectors 3`).
