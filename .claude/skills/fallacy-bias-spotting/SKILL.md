---
name: fallacy-bias-spotting
description: Scan a draft, argument, or decision against 20 logical fallacies and 20 cognitive biases, tag each Hit/Maybe/No with a one-line reason, and propose a de-bias move. Use when the reasoning feels right but may be systematically wrong — "what bias is this", "fallacy check", "is this reasoning sound", "de-bias this", "sanity-check my argument".
---

# Fallacy & Bias Spotting

Naming beats nagging. "You're being biased" changes nothing; "that's survivorship bias — you're counting only the companies that made it" hands the author a handle, a reason, and a repair. This skill converts a vague suspicion that an argument is wrong into a short sheet of named failure modes, each with evidence from the text and one de-bias move.

The failure mode it prevents: a persuasive passage that survives review because nobody can name what is off about it.

## When to use

- A draft, memo, or decision rationale feels right but you cannot say why it might be wrong.
- A debate is looping and both sides keep restating rather than testing claims.
- You are about to commit based on a story, a single case, or a confident forecast.
- Not for mapping argument structure → `argument-mapping`; not for scoring sources → `evidence-appraisal`.

## Process

1. **Intake.** Paste the passage verbatim (100–400 words of argument, not a whole document). Mark the load-bearing claim and the reasons offered for it. If there is no claim, there is nothing to screen.

2. **Scan.** Compare each reason against the catalog's cue phrases. Optionally run [scripts/fallacy.py](scripts/fallacy.py):
   `python3 scripts/fallacy.py --text "<passage>" --json`
   The script is a screening aid: cues are prompts to look, not verdicts.

3. **Tag three levels.** For every candidate, write **Hit** (cue plus a structural defect you can point to), **Maybe** (cue present, needs a closer read), or **No** (considered and dismissed). Silence is not a tag — the No column shows the scan was done.

4. **Keep at most three.** Rank by damage to the conclusion, not by count. A long list dilutes the fix; three tags force prioritization. Report the rest as "also considered".

5. **De-bias each hit.** Apply the matching move: **consider the opposite** (write the strongest case against your claim), **pre-mortem** (assume the plan failed; why?), **base-rate check** (replace the vivid case with a denominator). State the concrete repair — a reworded sentence, a new data point, a removed claim.

6. **Produce the artifact.** The annotated draft (tags inline or margin notes), a table of 2–3 tags with verdict, one-line why, and de-bias move, and a fixed revision of the load-bearing paragraph. The revision must differ from the original in substance, not just hedged wording.

## Rules

- Tag the move, not the person. "This is a false dilemma" — never "you are binary."
- Quote the cue. A tag without a quoted phrase is an opinion.
- A fallacy does not falsify the conclusion; it shows the argument as given is insufficient. Say what evidence would settle it.
- Bias cues are reasons to slow down, not clinical diagnoses. Avoid mind-reading intent.
- Steelman before tagging: if the strongest reading of the passage avoids the flaw, tag Maybe or No.
- Keep the scan proportionate: three high-risk tags beat twenty noisy ones.

## Going deeper

- All 40 entries with definition, cue, example, de-bias: [references/catalog.md](references/catalog.md)
- Sources, scope, and what the evidence does not support: [references/provenance.md](references/provenance.md)
- CLI scanner (`--list`, `--json`, `--top N`): [scripts/fallacy.py](scripts/fallacy.py)
