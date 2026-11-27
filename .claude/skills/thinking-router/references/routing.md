# Routing rubric

Routing is a coarse sort, not a diagnosis. Use this page when the one-line intake does not obviously land in one bucket, or when the user challenges the route.

## Step 1 — score the five buckets

Match the user's words against these signals. A multi-word phrase counts double; a single word counts once. Repeated words count once. Do not score intent you inferred but the user did not say — write the inferred intent into the intake line first, and score that.

| Bucket | Signal words and phrases |
|---|---|
| `sharper_judgment` | judgment, evaluate, credible, credibility, trust, trustworthy, valid, validity, sound, accurate, is this true, fact check, does this follow, does the argument follow, source, argument, fallacy, bias, wrong, mistake, rigor, critical, skeptical |
| `better_question` | question, reframe, framing, define, definition, what do you mean, mean by, clarify, ambiguous, vague, precise, assumption, scope, problem statement, what exactly, term, concept, unpack, restate, interpret, criteria |
| `more_ideas` | idea, ideas, brainstorm, generate, generative, alternatives to explore, novel, creative, diverge, divergent, more options, possibilities, ideate, invent, variations, many ways, come up with, stuck, blank page |
| `broader_perspectives` | perspective, stakeholder, other side, opposing, opponent, counterargument, counterpoint, dissent, disagree, blind spot, worldview, culture, steelman, red team, devil's advocate, fairness, empathy, point of view, what am I missing, groupthink, echo chamber |
| `stronger_options` | decide, decision, choose, choice, prioritize, tradeoff, risk, risky, expected value, probability, forecast, prediction, uncertain, uncertainty, stakes, bet, investment, strategy, plan, recommend, which one, should we, utility, cost benefit, downside, base rate, how confident |

Ambiguous signals: "options" belongs to both `more ideas` and `stronger options`; prefer `more ideas` only when the user wants *unconsidered* alternatives ("more options"), and `stronger options` when they want to *choose among* known ones ("which option"). "Confidence" is `stronger options` when it concerns a choice and `calibration-forecasting` when it concerns a forecast.

## Step 2 — pick the primary bucket

Highest weighted score wins. Tie-break order, because this is a critical-thinking track:

1. `sharper_judgment`
2. `better_question`
3. `broader_perspectives`
4. `stronger_options`
5. `more_ideas`

`more ideas` last is deliberate: if it still wins outright, the task is generative and belongs in the creative track, not here.

## Step 3 — confidence

- **High:** top bucket ≥ 3 weighted hits and leads the runner-up by ≥ 2.
- **Medium:** top bucket ≥ 2 and leads by ≥ 1.
- **Low:** everything else, including no matches, one weak hit, or two buckets within one point.

Low confidence is not a failure. It means ask one clarifying question before routing: "Are we judging whether this is true, or deciding what to do about it?"

## Step 4 — rank the methods, then shortlist

1. Rank by skill keyword score (see `scripts/route.py`).
2. Tie-break by membership in the primary bucket, then by catalog rank (evidence-appraisal first, decision-analysis last).
3. Shortlist one method. Add a second only if its score is at least half the leader's and the two artifacts compose (see catalog). Never shortlist three.

## Worked routes

**1. "Is this source credible, does the argument follow?"**
Buckets: sharper judgment 5, everything else 0 → primary `sharper_judgment`, high confidence.
Methods: evidence-appraisal (source, credible) and argument-mapping (argument, follow) tie near the top. Route: `sharper judgment → evidence-appraisal + argument-mapping`; score the source first, then check the inference.

**2. "Everyone keeps saying 'platform' — what do we actually mean?"**
Buckets: better question 4, sharper judgment 1 → primary `better_question`, high.
Method: socratic-elenchus. Route to one method only; do not start evaluating claims until the term is operationalized.

**3. "Our critique of the proposal feels weak. What is the strongest case against us?"**
Buckets: broader perspectives 4 (critique, strongest case, against), sharper judgment 1 → primary `broader_perspectives`, high.
Method: steelman-red-team. If the critique is weak because of a named fallacy, compose fallacy-bias-spotting first.

**4. "Should we ship the beta or keep testing?"**
Buckets: stronger options 3 (should we, ship/keep as choice), sharper judgment 1 → primary `stronger_options`, medium.
Method: decision-analysis (EV sheet, sensitivity). Add calibration-forecasting only if the disagreement is about the probability of failure, not about the utilities.

**5. "I'm stuck — give me more angles on this."**
Buckets: more ideas 3, broader perspectives 1 → primary `more_ideas`, medium.
No critical skill fits. Route out: "This is a generation deficit; use the creative-thinking track. Come back to thinking-router when you need to judge what it produced."

**6. "A pilot worked. How much should that move our belief that the program works?"**
Buckets: stronger options 2 (belief, move), sharper judgment 2 (evidence implied) → tie; tie-break gives `sharper_judgment`, low confidence.
Method: bayesian-updating (prior, likelihood ratio, base rate). Note the low confidence and confirm the framing before computing.

## Failure modes to avoid

- **Method stacking:** routing to four methods "to be safe". Shortlist one, two at most.
- **Bucket drift:** letting "more ideas" win because the user is frustrated, then applying a critical method to a generation problem.
- **Routing as analysis:** a long explanation of all eight methods. The handoff is one line plus one confirmation question.
- **Ignoring the artifact:** if the user cannot use the artifact the method produces, the route is wrong regardless of topic fit.
