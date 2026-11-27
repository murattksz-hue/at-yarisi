---
name: argument-mapping
description: Map whether reasons actually support a claim — Toulmin parse (claim/grounds/warrant/backing/qualifier/rebuttal) + validity tag (deductive valid/invalid, inductive strong/weak, abductive). Use when reasoning sounds persuasive but may not follow. Trigger: "does this follow", "is this valid", "map the argument", "missing warrant", "what's the reasoning here".
---

# Argument Mapping

Purpose: stop rhetoric from passing as truth. Persuasive prose hides its load-bearing
assumption — usually the **warrant**, the rule that licenses the move from grounds to
claim. Surface it, name the argument type, and judge whether the conclusion is earned.

## Process

1. **Extract the claim.** The one sentence the arguer wants you to accept. If there are
   several, map the main conclusion and treat the rest as grounds.
2. **List the grounds.** Stated reasons, data, observations. Only what is actually given;
   do not import charitable premises the arguer never supplied.
3. **State the warrant.** The general rule that connects grounds to claim
   ("if G, then C"). If it is implicit, write the strongest version the arguer could
   defend, then mark it as supplied.
4. **Check backing.** What supports the warrant itself — a study, a definition, a
   precedent, an authority? No backing means the warrant is an assumption, not a fact.
5. **Record the qualifier.** How strongly does the claim follow: *certainly, probably,
   plausibly, in most cases*? A mismatch between qualifier and warrant strength is a
   defect (overclaiming).
6. **Record the rebuttal.** Conditions under which the claim would fail. Absent rebuttal
   on a broad claim is a warning sign, not proof of error.
7. **Tag the type and verdict.** Deductive / inductive / abductive, then one of the
   verdicts below.

## Validity rubric

| Type | Question | Verdict |
|---|---|---|
| Deductive | If grounds are true, **must** the claim be true? | `valid` / `invalid` |
| Inductive | Do grounds make the claim **probable**? How probable? | `strong` / `weak` |
| Abductive | Is this the **best** explanation among rivals? | `plausible` / `gap` |

Then apply the **warrant test**: can you state the warrant in one sentence, and is it
true (or at least backed)? If not, the verdict is `gap — warrant W needed`, regardless of
how confident the prose sounds. A valid form with a false premise is still unsound; say
which premise you doubt and what evidence would settle it.

## Artifact

Produce a map table plus a verdict:

```
| Slot | Content |
|---|---|
| Claim | ... |
| Grounds | ... |
| Warrant | ... (stated / supplied) |
| Backing | ... |
| Qualifier | ... |
| Rebuttal | ... |
Verdict: valid | plausible | gap — warrant W needed
Type: deductive | inductive | abductive
```

Keep it short: the verdict line is the deliverable, the table is the audit trail. Do not
rewrite the argument into something stronger and then attack the rewrite — map what was
said, and note separately what a charitable version would need.

## Going deeper

- Toulmin's six slots, Walton's argument schemes, Ennis's taxonomy, and three worked
  examples: [references/toulmin.md](references/toulmin.md)
- Sources, lineage, and what this method cannot do: [references/provenance.md](references/provenance.md)
- Heuristic parser for long text: `python scripts/argmap.py --text "..." --infer --json`
