# Steelman, Charity, and Adversarial Challenge

## 1. Strawman vs steelman

A **strawman** substitutes a weaker version of the opposing position and defeats that. It is usually unintentional: we attack the version of the argument we can answer, not the one its best proponents hold.

A **steelman** (also "iron man") states the opposing position in its strongest defensible form: its best evidence, its strongest mechanism, the scope conditions under which it is most plausible, and the concessions it deserves. The target is *maximum* difficulty for your own view.

| | Strawman | Steelman |
|---|---|---|
| Target | Easiest rival | Strongest rival |
| Test | "They said something like this" | "Would a smart proponent sign this?" |
| Effect on your claim | Appears validated | Genuinely tested |
| Failure it hides | Weak evidence, unstated premises | None — it exposes them |

**The sign-off test:** write the counter-position as a paragraph, then ask whether an informed proponent would accept it as fair, or say "that's not my view." If they would quibble with the framing, you have not finished. Revise until the strongest critic says "yes, that is the case I would make."

**Steelmanning is not agreement.** It is a temporary suspension of rebuttal so the rival can be understood at full strength. You may still reject it afterwards — with reasons that survive it.

## 2. Principle of charity

From philosophy of language and informal logic (Rapoport, Dennett): interpret a claim in its most reasonable form before evaluating it. Operational rules:

1. Restate the opposing claim so its proponent agrees it is accurate — before responding.
2. List the *strongest* reasons for it, including ones the proponent did not give.
3. Grant shared premises and real evidence; dispute only what is actually disputable.
4. Prefer the interpretation that makes the argument valid over the one that makes it easy to refute.
5. Attribute error to missing information, different priors, or trade-off weighting before attributing it to stupidity or bad faith.

Charity is epistemic, not moral: a charitably reconstructed argument is the only version whose refutation tells you anything. Defeating a caricature updates nothing.

## 3. Adversarial collaboration

Tetlock's method for contested questions (used in forecasting tournaments and the "adversarial collaboration" projects): partisans of rival positions jointly design the test *before* seeing results.

Protocol:

1. Each side writes its claim and the conditions under which it would concede.
2. Both sides must accept one measurement plan, one outcome variable, and one analysis.
3. A neutral arbiter adjudicates disputes over design.
4. Results are published with both interpretations attached, including where each side was surprised.

Why it works: it converts a dispute about *conclusions* into a dispute about *tests*, where disagreement is cheap, checkable, and informative. It also prevents the post-hoc move of redefining success.

Agent version: write the rival's ideal test alongside yours; where they conflict, prefer the test the rival would accept as fair.

## 4. Red-team method (Zenko)

A red team is a structured, independent adversarial challenge to a plan or claim — not ordinary review, and not a devil's advocate performance. Zenko's field guide emphasizes:

- **Independence:** the attacker does not share the author's incentives or hopes.
- **Structure over vibes:** use named vectors and a checklist, not free-form skepticism.
- **Specificity:** produce the concrete failure or counter-case, not "have you considered risks?"
- **Ranking:** distinguish fatal, serious, and survivable attacks so the claim can be patched, not merely wounded.
- **Feedback:** the claim's author must respond to each attack in writing.

Five vectors (use all, then rank):

| Vector | Question | Strongest hit looks like |
|---|---|---|
| Evidence | Which empirical link is weakest? | A better-identified study in the opposite direction |
| Logic | Does the conclusion follow? | Unstated premise, equivocation, correlation→cause |
| Incentives | Who gains if this is believed? | Funding, career, or ideology shaping the evidence base |
| Alternative explanation | What else produces the same observation? | Selection effect, regression to the mean, confound |
| Cost | What does being wrong cost? | Irreversibility, trust, opportunity cost |

**Devil's advocacy vs red team:** a devil's advocate argues a position they do not hold, often thinly, to satisfy process. A red team produces the best case and the evidence that would support it. Aim for the latter.

## 5. Falsification pre-commitment

Popper's demarcation: a claim is empirical only if some observable outcome could refute it. In practice the binding constraint is not logic but *motivated reasoning* — we explain away disconfirmation after the fact. Pre-commitment closes that door.

Write, before defending:

1. **Observation:** the specific measurable result that would count against the claim.
2. **Threshold:** how large / how consistent it must be (effect size, confidence, replication).
3. **Deadline:** when you will check.
4. **Rationalization trap:** the excuse you would be most tempted to use ("the sample was too small", "the metric is flawed") — decide now whether it would be legitimate.
5. **Posterior:** your confidence now, and what it becomes if the test fails.

A claim that cannot name a falsifier is a value commitment or a definition, not an empirical belief. That is not automatically bad — but it should not be argued as if it were evidence-based.

## 6. Worked example A — "Remote work hurts productivity"

**Claim `P`:** Remote work reduces productivity.

**Steelman `¬P`:** Remote work does not reduce — and in knowledge work often raises — productivity, because output depends on focused time and retention more than on physical presence; measured output rose in several natural experiments, while apparent declines reflect manager visibility bias and onboarding costs for junior staff rather than remote work itself.

Premises: (1) output-based measures show flat-to-positive effects for experienced knowledge workers; (2) open-plan office interruptions impose real costs that remote work removes; (3) the studies showing harm concentrate on early-career workers and rapid-unplanned transitions, a scope limit not a general law.

**Attack vectors on `P`:**
- *Evidence* — the strongest negative findings are pre/post pandemic comparisons with confounded shocks; task-level RCTs find small positive effects. **Serious.**
- *Logic* — "productivity" shifts between output, hours, and manager ratings; the claim equivocates. **Fatal until defined.**
- *Incentives* — commercial-real-estate and managerial-visibility interests fund and amplify negative findings. **Serious.**
- *Alternative explanation* — onboarding and coordination debt explain early declines; tenure-stratified data would test this. **Serious.**
- *Cost* — wrong in the "does not hurt" direction: slower junior development and weaker weak-tie innovation, hard to reverse. **Survivable but price it.**

**Falsifier for `P`:** Abandon `P` if, within 12 months, a pre-registered comparison of comparable teams with output-based measures (not manager ratings) shows no negative effect of remote work on output and retention, and the effect for junior staff shrinks below the pre-set threshold once tenure is controlled. Trap to watch: dismissing positive results as "self-reported."

## 7. Worked example B — "We should adopt a four-day week"

**Claim `P`:** Our company should move to a four-day week at full pay.

**Steelman `¬P`:** The four-day-week evidence base is dominated by self-selected firms, self-reported productivity, and short follow-ups; where hours fall without a proportional output gain, the cost lands on customers or on the employees who absorb compressed schedules — so a firm should not adopt it before a controlled pilot with hard output measures.

Premises: (1) published trials are mostly voluntary adopters with strong selection; (2) measured gains are often cost savings and retention, not per-hour output; (3) compressed schedules raise intensity and may exclude caregivers, undermining the equity rationale.

**Attack vectors on `P`:**
- *Evidence* — trial effects may be Hawthorne/selection; a randomized pilot in your firm is cheap. **Serious.**
- *Logic* — from "trials succeeded elsewhere" to "it will succeed here" requires a similarity premise about work type and labor market. **Serious.**
- *Incentives* — advocates and consultancies sell the transition; managers may prefer it as a retention perk at no cash cost. **Survivable.**
- *Alternative explanation* — retention gains may come from any valued perk, not the schedule. **Serious.**
- *Cost* — customer coverage and scheduling complexity; reversibility is low once expectations reset. **Serious.**

**Falsifier for `P`:** Abandon if a 6-month pilot with pre-registered output, customer-response, and retention metrics shows output per week falling more than the hours reduction, or if the equity analysis shows caregivers disproportionately exiting. Trap: redefining success as "employees liked it."

## 8. Common failure modes

- **Decorative steelman:** a weak rival stated with a nod to fairness, refuted in one line.
- **Both-sidesism:** treating a well-evidenced claim and a fringe one as symmetric; steelmanning does not create evidential parity.
- **Attack laundering:** using the red-team format to relitigate a settled point without new evidence.
- **Unfalsifiable retreat:** each attack is met by a new auxiliary hypothesis. Cap the number of rescues; log them.
- **Persona attack:** psychoanalyzing the critic instead of answering the argument.
- **No posterior:** running the exercise and changing nothing, or changing everything, without stating confidence.
