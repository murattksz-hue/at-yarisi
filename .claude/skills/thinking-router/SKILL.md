---
name: thinking-router
description: Route to the right critical-thinking skill. Triages the task into five buckets — sharper judgment, better question, more ideas, broader perspectives, stronger options — then scores the eight critical methods and shortlists 1–2 for the user to confirm. Use when unsure which critical skill fits, when a task spans several methods, or when handing work between skills. Triggers: "which skill", "route this", "what method", "not sure which fits", "where do I start".
---

# Thinking Router

Not every doubt is the same deficit. The failure this prevents: answering every question with "think harder", or stacking five methods until the analysis stalls. Route first, then apply one method well.

## The five buckets

| Bucket | Question it asks | Default methods |
|---|---|---|
| Sharper judgment | Is this true, valid, and well supported? | evidence-appraisal, argument-mapping, fallacy-bias-spotting |
| Better question | What exactly are we asking or claiming? | socratic-elenchus, argument-mapping, evidence-appraisal |
| More ideas | What have we not generated yet? | none here — hand off to the creative-thinking track |
| Broader perspectives | Who disagrees, and are we being fair? | steelman-red-team, fallacy-bias-spotting |
| Stronger options | What should we do under uncertainty? | decision-analysis, calibration-forecasting, bayesian-updating |

`sharper judgment` is the fifth bucket, added because evaluation deserves its own lane: all eight methods sharpen judgment, but three are judgment-first.

## Process

1. **Intake (one line).** Restate the task as "we need to decide whether / choose / define X". Do not start analyzing. If the ask already names a method ("map this argument"), skip to handoff.
2. **Score the five buckets.** Match the ask against the signal words in [references/routing.md](references/routing.md). Name the top bucket and the runner-up. If `more ideas` wins, stop and hand off to the creative track — no critical skill fixes a generation deficit.
3. **Rank the eight methods.** Use [references/catalog.md](references/catalog.md) and `scripts/route.py`. Rank by keyword fit, then by the method whose artifact the user actually needs.
4. **Shortlist 1–2.** One method is the default. Two only when their artifacts compose: evidence-appraisal → argument-mapping, fallacy-bias-spotting → steelman-red-team, bayesian-updating → decision-analysis.
5. **Handoff.** Say `Route: <bucket> → <skill>`. Give the one-line artifact it will produce and why it fits. Ask one confirmation question: "Proceed with X, or swap to Y?"
6. **Apply.** Read the chosen skill's SKILL.md, run its intake, produce its artifact. If the user rejects the route, re-score; do not defend it.

## Bucket → skills

- **sharper judgment:** all eight; first pick evidence-appraisal, argument-mapping, fallacy-bias-spotting.
- **better question:** socratic-elenchus, argument-mapping, evidence-appraisal.
- **more ideas:** none of these — hand off to the creative-thinking track and say so explicitly.
- **broader perspectives:** steelman-red-team, fallacy-bias-spotting.
- **stronger options:** decision-analysis, calibration-forecasting, bayesian-updating.

## Handoff protocol

- Name the skill, bucket, artifact, and the missing input you need. No method tour.
- Confirm before producing the artifact: routing is cheap, a wrong frame is not.
- When two skills are routed, run them in order and keep both artifacts separate.
- Close the loop: record which skill was used so the next ask does not re-route.

## Script

```bash
python3 scripts/route.py --text "is this source credible, does the argument follow?" --json
python3 scripts/route.py --list
```

## Going deeper

- Full catalog: ranks, families, artifacts, decision tree: [references/catalog.md](references/catalog.md)
- Scoring rubric, confidence, tie-breaks, worked routes: [references/routing.md](references/routing.md)
