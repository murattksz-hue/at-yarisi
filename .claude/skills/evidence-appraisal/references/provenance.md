# Provenance and limits

Where the appraisal moves come from, and what this skill does **not** claim.

## Intellectual lineage

- **Facione (1990), *Critical Thinking: A Statement of Expert Consensus for Purposes of Educational Assessment and Instruction* (the Delphi Report).** The consensus definition lists *interpretation, analysis, evaluation, inference, explanation, self-regulation*. This skill operationalises **evaluation** — judging the credibility of a statement and the strength of the evidence behind it — and borrows the discipline of stating the criterion you judged against.
- **Paul & Elder, *Critical Thinking: Tools for Taking Charge of Your Learning and Your Life* / the Paul–Elder framework.** The element *information* and the standards *accuracy, significance, sufficiency, relevance* map directly onto tier (sufficiency), directness (relevance), recency (accuracy over time), and bias (fair-mindedness). The "what would change it" step is the Paul–Elder habit of making criteria explicit.
- **Ioannidis (2005), "Why Most Published Research Findings Are False", *PLoS Medicine* 2(8):e124.** Source of the bias checklist (small studies, small effects, flexible designs, financial interest, hot fields) and of the rule that publication bias is a property of the *literature*, not a single paper.
- **OpenAlex** (openalex.org, formerly Microsoft Academic Graph lineage; works such as `W4407*` for methods/scientometrics) — used only as an optional, read-only metadata resolver for year, type, and funders. No content is fetched or embedded.

Adjacent influences worth naming: GRADE (certainty-of-evidence ratings: risk of bias, inconsistency, indirectness, imprecision, publication bias) is the closest clinical analogue of the four-dimension score; the tier ordering (meta > RCT > observational > case > expert) follows the conventional evidence hierarchy taught in evidence-based medicine. The scoring arithmetic here is a *simplified* version of GRADE, not a validated instrument.

## Honest limits

- **The weights are a heuristic, not a measurement.** The tier bases (5/4/3/2/1.5/1) and penalties (0.5, 0.25) were chosen to be legible and monotone, not fitted to data. Two careful appraisers using this rubric can legitimately differ by ±0.5. Report the components, not just the total.
- **No RCT isolates this skill.** There is no trial showing that using a scorecard improves decisions. Critical-thinking instruction generally shows modest, transferable gains when taught as an explicit procedure with practice (cf. the Sio & Lortie-Forgues 2024 meta-analysis on creativity training, used in this repo's plan as the honesty benchmark) — treat this skill as a *structured heuristic with a defensible audit trail*, not a proven booster.
- **Tier ≠ truth.** A meta-analysis of biased studies is worse than one good direct trial. The modifiers exist because the hierarchy is a prior, not a verdict.
- **Directness cannot be fully automated.** Whether a population or outcome "counts as the same" is a judgement about the decision at hand; the script only records the flag you pass.
- **Recency is field-dependent.** The 2-year freshness horizon and 4-year decay step fit fast-moving empirical fields. In history, mathematics, or stable engineering practice, pass `--recency 0` and judge relevance instead; do not let the arithmetic override domain sense.
- **No substitute for reading the source.** The scorecard is an intake filter; it cannot detect a retracted paper, a reversed coding error, or a claim the abstract does not support. Verify the sentence you cite against the source text before acting.
- **Conflicts of interest are disclosed, not scored away.** High funding conflict lowers the score; it does not prove the claim false, and low conflict does not prove it true.
