# Catalog — eight critical methods, ranked

Ranked by evidence base × non-overlap × agent scriptability × offline-helper leverage. Every method produces one concrete artifact; route to the artifact the task needs, not to the most impressive-sounding method.

| # | Slug | Family | Use when | Artifact | Why build (gap + fit) | Key refs |
|---|---|---|---|---|---|---|
| 1 | `evidence-appraisal` | Evaluation — Facione *evaluation*, Paul-Elder *information* | A claim cites a source: how much should you trust it? | One-row scorecard: source tier, N, effect, bias risk, claim strength 1–5, next probe | Largest gap: no skill evaluated sources; every generative skill can hallucinate citations. High agent leverage: metadata → score. | Facione 1990 Delphi; Paul & Elder *information*; Ioannidis 2005; OpenAlex `W4407*` |
| 2 | `argument-mapping` | Analysis — Facione *analysis* | A paragraph sounds persuasive: does it actually follow? | Toulmin map (claim–grounds–warrant–backing–qualifier–rebuttal) + validity tag: valid / plausible / gap | Nothing mapped inference structure; prevents rhetoric-to-truth slippage. | Toulmin 1958; Walton 2008 *Informal Logic*; Ennis 1987 |
| 3 | `fallacy-bias-spotting` | Self-regulation — Facione *self-regulation* | The draft feels right but may be systematically wrong. | Annotated sheet: fallacy/bias Hit–Maybe–No + one-line why + de-bias move | Most teachable critical skill: naming beats nagging; scannable by an agent. | Kahneman 2011; Tversky & Kahneman 1974; Hamblin 1970; Halpern 2014 |
| 4 | `bayesian-updating` | Inference / likelihood — Facione *inference*, Halpern *likelihood* | Prior belief plus new evidence: how much should you move? | Prior → likelihood ratio → posterior + base-rate check + value of information | Creative scenario work gives possibilities; this prices probabilities. Agent can compute. | Bayes; Tetlock 2005/2015; Kahneman ch. 30 |
| 5 | `socratic-elenchus` | Interpretation / concepts — Facione *interpretation*, Paul-Elder *concepts* | A key term is used but never defined, or means two things. | Definition → counterexample → revision → operational definition chain | Paul-Elder *concepts* was entirely absent; prevents undefined terms steering a whole meeting. | Paul & Elder 2006; Ennis 1996 |
| 6 | `steelman-red-team` | Fair-minded evaluation — Paul-Elder intellectual empathy | The critique feels weak or strawmanned; need the strongest counter-case. | Steelman (strongest P) + red-team attack + pre-committed falsifier | `premortem` asks "how might we fail?"; this asks "how might they be right?" Covers intellectual empathy. | Paul-Elder fair-mindedness; Zenko 2015 *Red Team*; Tetlock adversarial collaboration |
| 7 | `calibration-forecasting` | Self-regulation — Facione *self-regulation*, Halpern *hypothesis testing* | Confidence is not accuracy; forecasts need to be accountable. | Brier-scored forecast + calibration curve + 3 testable predictions | Extends premortem from one hindsight to repeated foresight; the agent can track outcomes. | Tetlock & Gardner 2015; Kahneman *overconfidence*; Facione self-regulation |
| 8 | `decision-analysis` | Decision making — Halpern *decision making* | Choosing under uncertainty with real stakes. | EV sheet (options × outcomes × probabilities × utilities) + sensitivity + next probe | `options-portfolio` keeps variety; this prices risk. Complements, does not duplicate. | Halpern ch. 10; Howard & Matheson 1984; Arkes & Blumer |

## Bucket membership

| Bucket | Skills (primary first) |
|---|---|
| `sharper_judgment` | evidence-appraisal, argument-mapping, fallacy-bias-spotting, bayesian-updating, calibration-forecasting, decision-analysis, socratic-elenchus, steelman-red-team |
| `better_question` | socratic-elenchus, argument-mapping, evidence-appraisal |
| `more_ideas` | none — creative-thinking track |
| `broader_perspectives` | steelman-red-team, fallacy-bias-spotting |
| `stronger_options` | decision-analysis, calibration-forecasting, bayesian-updating |

## Decision tree

```text
Task arrives
├─ Need new options or raw ideas?
│  └─ more ideas → creative-thinking track (no critical skill fixes this)
├─ A claim, source, or argument is on the table?
│  ├─ Is the evidence/source trustworthy? → evidence-appraisal
│  ├─ Does the reasoning follow? → argument-mapping
│  ├─ Does it feel right for hidden reasons? → fallacy-bias-spotting
│  └─ Is the opposing case under-built? → steelman-red-team
├─ Is a key term or frame fuzzy?
│  └─ better question → socratic-elenchus
└─ Is a choice or belief at stake?
   ├─ How much should new evidence move belief? → bayesian-updating
   ├─ Do we need a probability or forecast? → calibration-forecasting
   └─ Do we need to choose? → decision-analysis
```

## Compositions

- `evidence-appraisal` → `argument-mapping`: first score the inputs, then test the inference.
- `fallacy-bias-spotting` → `steelman-red-team`: name the flaw, then build the strongest opposing case.
- `bayesian-updating` → `decision-analysis`: update beliefs, then price the options.
- `socratic-elenchus` → any: define the term before scoring or deciding.

## Not in the catalog

Runners-up for a later release: `measurement-validity` (operationalization, construct validity, Goodhart) and `dialectical-reasoning` (thesis–antithesis–synthesis). Do not route to them yet.
