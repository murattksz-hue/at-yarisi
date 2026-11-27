# Provenance and limits

## Lineage

- **Stephen Toulmin, *The Uses of Argument*** (Cambridge University Press, 1958; updated
  ed. 2003). Source of the six-slot layout (claim, grounds/data, warrant, backing,
  qualifier, rebuttal) and of the claim that everyday argument is field-dependent rather
  than syllogistic. The layout is descriptive, not a decision procedure: Toulmin does not
  tell you when a warrant is good, only where to look.
- **Douglas Walton, *Informal Logic: A Pragmatic Approach*** (2nd ed., Cambridge, 2008).
  Source of argument schemes and their critical questions, and of the dialogical view
  that an argument's quality depends on the purpose of the exchange (persuasion,
  inquiry, negotiation). Extends the map to inductive and abductive reasoning, which
  Toulmin's layout alone does not grade.
- **Robert H. Ennis, "A Taxonomy of Critical Thinking Dispositions and Abilities"**
  (1987). Source of the analysis checklist — conclusion, reasons, unstated assumptions —
  and of the soundness rule: valid form plus acceptable premises.
- **Facione, *Critical Thinking: A Statement of Expert Consensus for Purposes of
  Educational Assessment and Instruction*** (1990 Delphi report). Places "analysis" and
  "evaluation" as core critical-thinking abilities; this skill is the analysis half.

## What the method does

- Makes the inferential step explicit and auditable, so a confident tone cannot substitute
  for a missing link.
- Separates **form** (does it follow?) from **content** (are the premises true?), which
  are routinely conflated in debate.
- Forces the type tag, which prevents the common error of judging an inductive argument
  by deductive standards.

## Limits

- **Not a truth machine.** A valid map with false grounds yields a false conclusion.
  Premise credibility needs `evidence-appraisal` or domain knowledge.
- **Warrant selection is interpretive.** When the arguer leaves the warrant unstated,
  the mapper supplies it. A hostile mapper can supply a bad warrant and "refute" an
  argument the arguer never made. State explicitly that the warrant is supplied and
  choose the strongest defensible version.
- **Real arguments are nested.** Grounds are often themselves conclusions of sub-arguments.
  Map the top level first; recurse only where the verdict depends on it. A full tree
  grows fast and hides the load-bearing link.
- **Rhetorical and multimodal arguments** (images, narratives, tone) do not reduce to
  propositions cleanly. The map will under-represent them.
- **Validity is not persuasiveness, and invalidity is not falsity.** An invalid argument
  can have a true conclusion; a valid one can have a false one. Report the map, not a
  verdict on the world.
- **No automated scoring.** `scripts/argmap.py` labels spans heuristically from cue
  words. It is a first pass for long text, not an oracle; always review its output.
