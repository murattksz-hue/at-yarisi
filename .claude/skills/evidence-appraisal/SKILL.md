---
name: evidence-appraisal
description: Evaluate how much a source or claim is actually worth — source tier, recency, directness, bias risk → claim strength 1-5 and the next probe that would move it. Use when a claim cites a source, when two sources disagree, or when stakes ride on evidence quality. Triggers: "how credible is this", "is this source any good", "claim strength", "how much should I trust this", "what evidence would change my mind".
---

# Evidence Appraisal

Prevents the most common citation error: treating a blog post, a single case study, and a meta-analysis as interchangeable support. A claim is only as strong as its weakest link — tier, recency, directness, and bias — and that strength is a number you can defend, not a vibe.

## Process

### 1. Name the claim and what hangs on it

Write the claim as one falsifiable sentence (`X reduces Y by 20% in Z`). Note the decision it feeds. A claim that changes nothing needs no appraisal; one that changes a big decision deserves every column below.

### 2. Score four dimensions

For each claim, fill one row per source (template: [references/scorecard.md](references/scorecard.md)):

| Dimension | Values | Effect on strength |
|---|---|---|
| **Tier** | meta-analysis 5, RCT 4, observational 3, case 2, expert 1.5, blog 1 | starting base |
| **Recency** | years since publication | −0.25 per 4 years beyond 2, capped −1 |
| **Directness** | direct / indirect (surrogate outcome, different population) | indirect −0.5 |
| **Bias risk** | low 0, medium −0.5, high −1 | see bias checklist |

`strength = clamp(tier_base − recency_penalty − indirect_penalty − bias_penalty, 1, 5)`

Helper: `python3 scripts/evidence.py --claim "…" --tier rct --n 200 --json` prints the row, or omit `--json` for a table.

### 3. Interpret and state what would move it

- **4.5–5** — decision-grade; act and cite.
- **3.5–4.4** — usable with a caveat; look for one replication.
- **2.5–3.4** — suggestive; do not let it carry a high-stakes decision alone.
- **1.5–2.4** — hypothesis only; seek a better design.
- **1–1.4** — anecdote/opinion; label it as such.

Then write the **next probe**: the single cheapest action that would raise the score by ≥1 point (find the meta-analysis, check the replication, look for the registered report, ask for the direct outcome). A score without a next probe is a verdict; with one, it is a decision procedure.

## Guardrails

- **No source, no score.** If the claim has no traceable source, strength = 1 and the next probe is "find one".
- **Tier is not truth.** A well-run RCT in the wrong population loses to an observational study in yours; directness is a modifier, not a tiebreak.
- **Do not average errors.** Two weak sources do not make one strong source — score the best single source and note corroboration separately.
- **Publication bias is a property of the literature, not just the paper.** If only positive results are cited, discount the tier.
- **Say what you have not checked.** "Assumed peer review; not verified" is honest; silence is not.

## Going deeper

- Tier table, 5-point rubric, and bias checklist: [references/scorecard.md](references/scorecard.md)
- Provenance (Facione, Paul–Elder, Ioannidis, OpenAlex) and limits: [references/provenance.md](references/provenance.md)
