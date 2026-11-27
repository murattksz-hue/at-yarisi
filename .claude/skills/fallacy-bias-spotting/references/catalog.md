# Fallacy & Bias Catalog

40 named failure modes: 20 logical fallacies (the argument does not follow) and 20 cognitive biases (the judgment drifts). Use the cue phrases as search prompts, not as proof. One cue can be innocent; a cluster of cues plus a structural check is a finding.

## How to read an entry

- **Definition** — what breaks, in one line.
- **Cue phrase** — wording that often precedes the failure mode. Scan for these first.
- **Example** — a minimal sentence that commits the error.
- **De-bias** — the repair that changes the reasoning, not just the phrasing.

## Fallacies vs biases

A **fallacy** is a defect in the move from reasons to claim: the premises can be true and the conclusion still unsupported. A **bias** is a defect in the judge: the same evidence gets weighted differently depending on history, memory, or framing. Fallacies are argued; biases are felt. Most real drafts contain both, and a fallacy is often the visible symptom of a bias underneath (sunk cost produces the false dilemma of "continue or waste everything").

## Caution: the fallacy fallacy

Finding a fallacy does not make the conclusion false. It makes the *argument* insufficient as stated. Tag the move, then ask what evidence would settle the claim. Likewise, a bias cue is a reason to slow down, not a diagnosis of the person.

## Fallacies (20)

| # | Name | Definition | Cue phrase | Example | De-bias |
|---|---|---|---|---|---|
| 1 | Strawman | Attacking a weakened, exaggerated version of the opposing claim instead of the claim itself. | so you're saying / what they really want is | "They want to slow hiring" becomes "they want the company to fail." | Restate the opposing view in its strongest form, get agreement, then attack that. |
| 2 | Equivocation | Sliding between two senses of the same word to make an argument appear valid. | in one sense … in another / that depends on what X means | "A theory is just an idea, so evolution is just an idea." | Fix one operational definition per term and re-read the argument with it. |
| 3 | Post hoc | Assuming that because B followed A, A caused B. | right after / since X happened, Y must have | "Sales rose after the rebrand, so the rebrand worked." | Name the mechanism and a comparison group; check whether B would have happened anyway. |
| 4 | False dilemma | Presenting two options as exhaustive when others exist. | either … or / only two choices | "Either we cut the budget or we go bankrupt." | List a third and fourth option, including "do less, later" and "test cheaply first". |
| 5 | Ad hominem | Rejecting a claim because of who made it rather than what it says. | can't be trusted / what does he know | "She's a consultant, so ignore her point about churn." | Separate the speaker's credibility from the claim's evidence and evaluate the evidence. |
| 6 | Slippery slope | Claiming one small step inevitably leads to an extreme outcome without justifying the chain. | next thing you know / where does it end | "Allow remote Fridays and soon nobody comes in at all." | Spell out each link and its probability; find where the chain actually breaks. |
| 7 | Hasty generalization | Drawing a broad rule from one or a few cases. | we tried it once / always / never | "We tried it once and it failed, so it will always fail." | Ask how many cases, how selected, and what the base rate is; downgrade to "this case failed". |
| 8 | Appeal to authority | Treating an authority's say-so as proof, outside their expertise or against the evidence. | experts say / trust the science | "A Nobel economist likes this architecture, so it must scale." | Check domain relevance, consensus, and the underlying evidence the authority would cite. |
| 9 | Appeal to popularity | Treating widespread belief or use as evidence of truth or quality. | everyone is doing it / millions of users | "Two million teams use it, so it must be right for us." | Ask what the crowd's incentives were and whether their situation matches yours. |
| 10 | Circular reasoning | Using the conclusion, or a restatement of it, as its own premise. | it's true because it's true / obviously | "The plan is sound because it's a sound plan." | Ask for evidence that does not already assume the conclusion; name the independent premise. |
| 11 | False analogy | Arguing from a similarity that is irrelevant to the conclusion. | just like / no different from | "Managing engineers is just like managing sales reps." | List the relevant dimensions and check whether the analogy matches on those, not just surface. |
| 12 | Tu quoque | Deflecting a criticism by accusing the critic of the same fault. | you do it too / what about you | "You missed the deadline too, so you can't criticize my slip." | Evaluate the claim on its merits; hypocrisy affects credibility, not truth. |
| 13 | Appeal to emotion | Substituting fear, outrage, or sympathy for relevant evidence. | think of the children / how would you feel | "If we don't approve this, families will suffer." | Separate the emotional pull from the factual claim; ask what evidence would settle it. |
| 14 | Red herring | Introducing an irrelevant point that diverts attention from the issue. | the real issue is / more importantly | "Yes, the bug shipped, but the real issue is competitor pricing." | Park the tangent, restate the original question, and answer that first. |
| 15 | Burden of proof shifting | Asserting a claim, then demanding others disprove it. | prove me wrong / unless you can show otherwise | "Ghosts exist; prove that they don't." | Whoever asserts must supply evidence; state the threshold before evaluating. |
| 16 | Cherry picking | Selecting only the evidence that supports a claim while ignoring the rest. | the one study / look at these results | "The one trial that showed a gain proves the program works." | Ask for the full sample and the null results; check what was excluded and why. |
| 17 | Moving the goalposts | Changing the success criterion after evidence meets the original one. | that doesn't count / that's not what I meant | "Fine, adoption grew, but that's not real growth." | Write the success criterion and threshold down before looking at the result. |
| 18 | Loaded question | Asking a question that presupposes an unproven or disputed fact. | have you stopped / why did you ruin | "Why did you ignore the security review?" | Split the presupposition out and ask it separately as a yes/no claim. |
| 19 | Genetic fallacy | Judging a claim by its origin rather than its current merit. | it started as / where it comes from | "That method came from the military, so it can't fit startups." | Evaluate the claim as it stands today; origin is context, not a verdict. |
| 20 | Composition / division | Assuming what is true of parts is true of the whole, or vice versa. | each part is … so the whole is | "Every engineer is fast, so the team will ship fast." | Identify the emergent property (coordination, bottlenecks) that does not distribute. |

## Cognitive biases (20)

| # | Name | Definition | Cue phrase | Example | De-bias |
|---|---|---|---|---|---|
| 1 | Confirmation bias | Seeking and weighting evidence that supports what you already believe. | as I expected / that proves my point | "As I expected, the two happy customers prove the redesign worked." | Write down the disconfirming observation you have not looked for, then look for it. |
| 2 | Anchoring | Letting an initial number or framing dominate later estimates. | starting from / compared to the original | "The list price was 50k, so 30k feels cheap." | Estimate independently before seeing the anchor; then compare. |
| 3 | Availability heuristic | Judging likelihood by how easily examples come to mind. | in my experience / it failed last time | "We tried it once and it failed, so it will always fail." | Replace the memory with a count: how many attempts, what were the denominators? |
| 4 | Survivorship bias | Drawing conclusions from the cases that survived while the failures are invisible. | look at all the winners / it worked for them | "Every founder we interview dropped out of college." | Ask who is missing from the sample and what happened to them. |
| 5 | Sunk cost | Continuing an effort because of past investment rather than future value. | we've already invested / too far to stop | "We've spent two years on it; we can't quit now." | Ask: if we were starting fresh today, would we begin this? Decide on marginal value. |
| 6 | Hindsight bias | Believing an outcome was predictable after it is known. | I knew it all along / it was obvious | "It was obvious the launch would flop." | Recover a dated pre-outcome forecast; score that, not the memory. |
| 7 | Overconfidence | Stating more certainty than the evidence supports. | without a doubt / guaranteed | "There is zero chance this migration breaks checkout." | Attach a number and an interval; ask what would falsify it and what you'd bet. |
| 8 | Framing effect | Reaching different conclusions from logically equivalent descriptions. | save $X / 90% survival | "90% survival" vs "10% mortality" for the same surgery. | Restate the claim in the opposite frame; if the judgment flips, the frame did the work. |
| 9 | Loss aversion | Weighting losses roughly twice as heavily as equivalent gains. | don't want to lose / protect what we have | "We can't risk a small dip even for a large upside." | Price the gain and the loss in the same units; ask if you'd take the bet reversed. |
| 10 | Status quo bias | Preferring the current arrangement because it is current. | how we've always done it / if it ain't broke | "The current process works fine" — it has never been measured. | Include "do nothing" as an explicit option with its own costs and owner. |
| 11 | In-group bias | Favoring members of your own group and discounting outsiders. | us vs them / not one of us | "Our team's estimate is credible; theirs is padded." | Apply one rubric to all groups and score blind to affiliation. |
| 12 | Halo effect | Letting one good trait spill over into unrelated judgments. | good at X, so good at Y | "She was a great engineer, so she'll be a great manager." | Score each dimension separately and name the evidence for that dimension alone. |
| 13 | Fundamental attribution error | Explaining others' failures by character and your own by circumstance. | they're just lazy / their fault | "They missed the deadline because they're careless" — not because scope doubled. | Swap the explanation: apply the situational story you'd use for yourself. |
| 14 | Planning fallacy | Underestimating time, cost, and risk of future projects. | on schedule / should only take | "It should only take two weeks, no major surprises." | Use the outside view: base rate of similar past projects, then adjust. |
| 15 | Recency bias | Overweighting the latest data relative to the longer record. | last quarter / these days | "Last month was great, so the trend is up." | Plot the full history with the recent point highlighted; ask what the base rate says. |
| 16 | Regression to the mean | Reading natural reversion after an extreme result as a causal effect. | record high / it can only get better | "After last year's record, this quarter's dip proves the new policy failed." | Ask how much of the extreme was luck; predict reversion before attributing cause. |
| 17 | Dunning–Kruger effect | Overestimating competence in a domain precisely because expertise is missing. | how hard can it be / anyone can do this | "How hard can this migration be? It's just moving files." | Ask a practitioner what the failure modes are; estimate again after the list. |
| 18 | Ambiguity aversion | Avoiding options whose probabilities are unknown, even when they are better. | better the devil you know / avoid the unknown | "We'll keep the known vendor; the new one's terms are unclear." | Price the unknown: what would it cost to learn the odds? Compare expected value, not comfort. |
| 19 | Choice-supportive bias | Remembering a chosen option as better than it was, and the rejected one as worse. | glad we chose / our decision was right | "We picked vendor A, so of course its onboarding was the smoothest." | Re-score the options on the criteria you used before the choice, from the original notes. |
| 20 | Narrative bias | Preferring a coherent story over the messier evidence. | makes a great story / fits the narrative | "The turnaround makes a great story, so the causal chain must be right." | Write the version with luck, noise, and missing actors; check if it still explains the data. |
