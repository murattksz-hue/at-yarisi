---
name: socratic-elenchus
description: Clarify what a key term actually means before arguing about it. Runs a Socratic elenchus chain — initial definition, counterexample, revision, operational definition plus a test — and emits a reusable term card. Use when an important word is used but never defined, or shifts meaning mid-discussion. Triggers - "what do you mean by X", "define X precisely", "operationalize X", "conceptual clarity", "that term is vague", "we keep using X differently".
---

# Socratic Elenchus

Arguments built on an undefined term feel productive while each participant imports a different referent. This is the Paul–Elder **concepts** gap: people reason fluently with a word and never expose the definition, model, or theory doing the work. Elenchus fixes the referent in public, breaks it with counterexamples, then rebuilds it as something a test could confirm or refute.

## When to use

- A load-bearing term (goal, metric, criterion, category) is asserted, not defined.
- Two parties use the same word for different things, or the definition drifts mid-thread.
- A decision or measurement depends on the term ("engagement", "fair", "risky", "ready").
- Not for: terms with an agreed operational definition, purely rhetorical labels, or low-stakes prose.

## Process

Work **one term at a time**.

1. **Definition.** Capture the definition verbatim — do not improve it yet. Classify it: ostensive (pointing/examples), reportive (how people actually use it), stipulative (a decision to use it this way), or persuasive (definition smuggles the conclusion). Note what work the term is doing in the argument.
2. **Counterexample.** Test the definition against cases. Hunt **false positives** (definition applies, term clearly does not) and **false negatives** (clear case of the term, definition excludes it). Add a boundary case, a scaling case, and a degenerate case (zero/negative/extreme).
3. **Revision.** Narrow, widen, or disambiguate. If two senses are doing different jobs, **split the term** rather than averaging them. Restate as: category + differentiator + at least one clause that could be checked.
4. **Operational definition + test.** Specify indicator, measurement, threshold, data source, baseline. Then state the observation that would count **against** the term applying. A definition with no possible disconfirming observation is not yet operational.

## Artifact: the term card

| Field | Content |
|---|---|
| Term | The word, plus the sentence it appeared in |
| Initial definition | Verbatim, plus type (ostensive/reportive/stipulative/persuasive) |
| Counterexamples | Case → verdict → which clause broke |
| Revised definition | Category + differentiator (+ split senses if needed) |
| Operational definition | Indicator, measure, threshold, source, baseline |
| Test | Prediction, observation, falsifier |

```
Term: <X>
Initial: "<verbatim>"  [type]
Counterexamples:
  - <case> → term applies? yes/no; clause that broke: <clause>
  - <case> → ...
Revised: <X> is a <category> that <differentiator>.
Operational: <X> = <indicator> measured as <unit> over <window>, present when <threshold>.
Test: if <X>, we should observe <Y>; <Z> would count against it.
```

## Guardrails

- **No badgering.** Two or three probes per term; a definition that survives them is good enough. Elenchus is clarification, not interrogation.
- **One term at a time.** Chasing every undefined word produces aporia, not clarity.
- **Do not smuggle in your preferred definition.** Offer revisions as candidates; the definer chooses.
- **Respect stipulation.** A declared technical or legal definition is a decision, not an error — test it for usefulness instead.
- **Name the stakes.** If precision changes nothing about the decision, say so and stop.
- **Separate verbal from genuine disputes.** If the parties agree on all cases and differ only in wording, the disagreement is verbal.

## Going deeper

- Method, Paul–Elder concepts framework, Ennis definition tests, counterexample and thought-experiment techniques, two worked examples: [references/elenchus.md](references/elenchus.md)
- Sources, trace of each move, and honest limits: [references/provenance.md](references/provenance.md)
- Probe generator: `python scripts/elenchus.py --term "engagement" --definition "users like the product" --json`
