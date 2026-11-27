# Toulmin, Walton, and Ennis: the machinery behind the map

## Toulmin's model (1958)

Stephen Toulmin, *The Uses of Argument* (Cambridge, 1958), rejected the idea that all
good arguments are formal syllogisms. Everyday reasoning is field-dependent: what counts
as a good warrant in law differs from what counts in medicine. His layout has six slots.

| Slot | Definition | Test question |
|---|---|---|
| **Claim** (C) | The conclusion the argument asks you to accept. | What is being asserted? |
| **Grounds** (G) | The facts, data, or evidence offered in support. | What is given? |
| **Warrant** (W) | The general rule licensing the step from G to C. Usually implicit. | What must be true for G to count as support for C? |
| **Backing** (B) | Support for the warrant itself — field-specific evidence or authority. | Why should we accept the rule? |
| **Qualifier** (Q) | The degree of force the claim carries: *certainly, presumably, probably, in most cases*. | How strongly does C follow? |
| **Rebuttal** (R) | Conditions that would defeat or restrict the claim. | When would C not hold? |

Toulmin's key move: the warrant is not another premise in the same chain. It is a
**bridge rule**, and it is where most bad arguments hide, because prose leaves it
unstated and the reader silently supplies a version that happens to be true.

Note on terminology: Toulmin wrote "data" for grounds and "warrant" for the bridging
rule; later writers say "grounds" and sometimes "bridge". The relationship
$\text{G} \;\xrightarrow{\;W\;}\; \text{C}$ is the whole model in one line.

## Walton's argument schemes (2008)

Douglas Walton, *Informal Logic: A Pragmatic Approach* (2nd ed., 2008), supplies the
missing taxonomy for **inductive and abductive** arguments. Where Toulmin gives a layout,
Walton gives recurring schemes with critical questions:

- *Argument from example*: "In this case X, property P held; therefore generally P."
  Critical questions: Is the example representative? Are there counterexamples?
- *Argument from expert opinion*: "E says P; E is an expert; therefore P." Questions:
  Is E credible? Is E's claim within E's field? Is there dissent among experts?
- *Argument from sign*: "Y is present; Y indicates X; therefore X." Questions: How
  reliable is the sign? Are there defeating conditions?
- *Argument from cause to effect*: "A occurred; A typically causes B; therefore B."
  Questions: Is the causal link established? Are there intervening causes?
- *Inference to the best explanation* (abduction): "H explains the observations better
  than rivals; therefore H." Questions: Are rival hypotheses considered? Is H itself
  plausible? Does H predict anything beyond the data?

Walton's contribution to a map: the **scheme name plus its unanswered critical
questions** is a more honest verdict than "valid/invalid", which only fits deduction.

## Ennis's taxonomy (1987)

Robert Ennis, "A Taxonomy of Critical Thinking Dispositions and Abilities" (in Baron &
Sternberg, eds., *Teaching Thinking Skills*, 1987), supplies the evaluation checklist:

1. **Argument analysis**: identify the conclusion; identify the reasons; identify
   unstated assumptions.
2. **Judging credibility**: of a source, of an observation, of an authority.
3. **Deduction**: judge whether the conclusion follows necessarily.
4. **Induction**: judge the strength of generalization and analogy.
5. **Value judgment**: judge the soundness of value claims and definitions.

Ennis's rule of thumb matches this skill: an argument is **sound** only if it is valid
(or strong) *and* its premises are acceptable. Mapping answers the first half; premise
credibility is a separate job (see `evidence-appraisal`).

## Worked examples

### 1. Deductive

> "Every mammal is warm-blooded. Whales are mammals. So whales are warm-blooded."

- Claim: whales are warm-blooded.
- Grounds: every mammal is warm-blooded; whales are mammals.
- Warrant: if every mammal is warm-blooded and whales are mammals, then whales are
  warm-blooded. (Stated implicitly; here it is just the substitution rule.)
- Backing: definition of "mammal" plus the biological premise.
- Qualifier: certainly.
- Rebuttal: none needed — the form is universally quantified.
- **Verdict: valid** (and sound if the premises are true).

The giveaway is the universal quantifier plus a term that falls under it. If either
premise fails, the form stays valid but soundness collapses.

### 2. Inductive

> "Our last three releases shipped late. So the next one probably will too."

- Claim: the next release will probably ship late.
- Grounds: the last three releases shipped late.
- Warrant: past performance of a recurring process tends to predict its next run
  (supplied, not stated).
- Backing: none offered. Sample size is three, and the releases may not be comparable.
- Qualifier: probably.
- Rebuttal: unless the team changed staffing or scope, or the past delays had a
  one-off cause.
- **Verdict: weak** — a three-case sample with no stated comparability. Strong would
  require a larger, representative base and a mechanism, not just repetition.

### 3. Abductive

> "The server logs show a spike at 02:00 and the disk filled by 02:10. The nightly
> backup must have run away."

- Claim: the nightly backup caused the disk to fill.
- Grounds: log spike at 02:00; disk full by 02:10; backups run nightly.
- Warrant: the hypothesis that best explains the observations is the one to accept
  (supplied).
- Backing: the backup's timing and known disk consumption.
- Qualifier: must (overclaimed — should be "probably" or "plausibly").
- Rebuttal: a log rotation job, a runaway query, or an external upload could also
  explain the spike.
- **Verdict: plausible but overqualified** — the backup is a good candidate, but rival
  explanations were not excluded. Ask what observation would discriminate between them.

## Common mapping errors

- **Charitable rewrite**: mapping a stronger argument than the one given, then refuting
  it. Defeats the purpose and drifts into strawmanning.
- **Warrant smuggling**: accepting an unstated warrant without writing it down. The
  unstated version is exactly where the error lives.
- **Type confusion**: treating an inductive argument as deductive and declaring it
  "invalid". Inductive arguments are weak or strong, never valid.
- **Premise/mapping conflation**: a valid map does not make the claim true. Say
  "valid; premise P is what I doubt" rather than "valid, so true".
