#!/usr/bin/env python3
"""Heuristic fallacy and cognitive-bias scanner.

Scans a short text against a catalog of 20 fallacies and 20 biases. Each
catalog entry carries cue patterns; a match scores points, and the summed
score becomes a verdict: Hit (>= 2) or Maybe (1). Output is markdown or JSON.

This is a screening aid, not an oracle: a cue phrase is a prompt to look, not
proof of a fallacy. Always confirm against the passage's actual structure.

Usage:
    fallacy.py --text "We tried it once and it failed, so it will always fail"
    fallacy.py --text "..." --json --top 5
    fallacy.py --list
    echo "..." | fallacy.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys

HIT, MAYBE = 2, 1

CATALOG = [
    # ---------------------------------------------------------------- fallacies
    dict(
        id="strawman", kind="fallacy", name="Strawman",
        definition="Attacking a weakened, exaggerated version of the opposing claim instead of the claim itself.",
        cue="so you're saying / what they really want is",
        example="\"They want to slow hiring\" becomes \"they want the company to fail.\"",
        debias="Restate the opposing view in its strongest form, get agreement, then attack that.",
        patterns=[(r"\bso you('re| are) saying\b", 2), (r"\bwhat they really (want|mean)\b", 2),
                  (r"\bthe other side (just )?wants to\b", 1), (r"\bthat's just\b", 1)],
    ),
    dict(
        id="equivocation", kind="fallacy", name="Equivocation",
        definition="Sliding between two senses of the same word to make an argument appear valid.",
        cue="in one sense … in another / that depends on what X means",
        example="\"A theory is just an idea, so evolution is just an idea.\"",
        debias="Fix one operational definition per term and re-read the argument with it.",
        patterns=[(r"\bin one sense\b.{0,60}\bin another\b", 2), (r"\bthat depends on what\b.{0,30}\bmeans\b", 2),
                  (r"\b(freedom|fairness|rights?|theory|natural)\b.{0,40}\bmeans\b", 1),
                  (r"\bsame word\b", 1)],
    ),
    dict(
        id="post-hoc", kind="fallacy", name="Post hoc",
        definition="Assuming that because B followed A, A caused B.",
        cue="right after / since X happened, Y must have",
        example="\"Sales rose after the rebrand, so the rebrand worked.\"",
        debias="Name the mechanism and a comparison group; check whether B would have happened anyway.",
        patterns=[(r"\b(happened|started|began|changed)\b.{0,40}\bright after\b", 2),
                  (r"\bsince\b.{0,60}\b(must|caused|because of)\b", 2),
                  (r"\bafter\b.{0,80}\b(therefore|so|must have)\b", 2),
                  (r"\bcaused by\b", 1)],
    ),
    dict(
        id="false-dilemma", kind="fallacy", name="False dilemma",
        definition="Presenting two options as exhaustive when others exist.",
        cue="either … or / only two choices",
        example="\"Either we cut the budget or we go bankrupt.\"",
        debias="List a third and fourth option, including \"do less, later\" and \"test cheaply first\".",
        patterns=[(r"\beither\b.{0,60}\bor\b", 2), (r"\bonly (two|option|choice)\b", 2),
                  (r"\b(there is|there's) no (other|alternative)\b", 2),
                  (r"\b(with us or against us|if you('re| are) not with)\b", 2)],
    ),
    dict(
        id="ad-hominem", kind="fallacy", name="Ad hominem",
        definition="Rejecting a claim because of who made it rather than what it says.",
        cue="can't be trusted / what does he know",
        example="\"She's a consultant, so ignore her point about churn.\"",
        debias="Separate the speaker's credibility from the claim's evidence and evaluate the evidence.",
        patterns=[(r"\bcan't be trusted because\b", 2), (r"\bwhat does (he|she|they) know\b", 2),
                  (r"\b(idiot|moron|liar|clown|shill)\b", 1), (r"\b(he|she|they)('s| is) (just )?a\b", 1)],
    ),
    dict(
        id="slippery-slope", kind="fallacy", name="Slippery slope",
        definition="Claiming one small step inevitably leads to an extreme outcome without justifying the chain.",
        cue="next thing you know / where does it end",
        example="\"Allow remote Fridays and soon nobody comes in at all.\"",
        debias="Spell out each link and its probability; find where the chain actually breaks.",
        patterns=[(r"\bnext thing\b", 2), (r"\bbefore you know it\b", 2), (r"\bwhere does it end\b", 2),
                  (r"\binevitably\b", 1), (r"\blead(s|ing)? to\b.{0,40}\band then\b", 2),
                  (r"\bwill (eventually|soon)\b", 1)],
    ),
    dict(
        id="hasty-generalization", kind="fallacy", name="Hasty generalization",
        definition="Drawing a broad rule from one or a few cases.",
        cue="we tried it once / always / never",
        example="\"We tried it once and it failed, so it will always fail.\"",
        debias="Ask how many cases, how selected, and what the base rate is; downgrade to \"this case failed\".",
        patterns=[(r"\bonce\b.{0,40}\b(always|never)\b", 3), (r"\b(we|i) tried (it|this) once\b", 2),
                  (r"\b(always|never)\b", 1), (r"\bone (time|case|example)\b", 1),
                  (r"\beveryone knows\b", 2), (r"\ball (of )?(them|these|those)\b", 1)],
    ),
    dict(
        id="appeal-to-authority", kind="fallacy", name="Appeal to authority",
        definition="Treating an authority's say-so as proof, outside their expertise or against the evidence.",
        cue="experts say / trust the science",
        example="\"A Nobel economist likes this architecture, so it must scale.\"",
        debias="Check domain relevance, consensus, and the underlying evidence the authority would cite.",
        patterns=[(r"\b(experts?|scientists?|doctors?|studies) (say|agree|show|prove)\b", 2),
                  (r"\btrust the (experts|science)\b", 2),
                  (r"\b(he|she) is an? (expert|authority)\b", 1),
                  (r"\baccording to\b.{0,60}\b(therefore|so it must)\b", 1)],
    ),
    dict(
        id="appeal-to-popularity", kind="fallacy", name="Appeal to popularity",
        definition="Treating widespread belief or use as evidence of truth or quality.",
        cue="everyone is doing it / millions of users",
        example="\"Two million teams use it, so it must be right for us.\"",
        debias="Ask what the crowd's incentives were and whether their situation matches yours.",
        patterns=[(r"\beveryone (is|does|knows|uses)\b", 2), (r"\bmost people\b", 1),
                  (r"\b(millions|thousands) of (people|users|teams)\b", 2),
                  (r"\bbandwagon\b", 2), (r"\bmust be (good|true|right) because\b", 2)],
    ),
    dict(
        id="circular-reasoning", kind="fallacy", name="Circular reasoning",
        definition="Using the conclusion, or a restatement of it, as its own premise.",
        cue="it's true because it's true / obviously",
        example="\"The plan is sound because it's a sound plan.\"",
        debias="Ask for evidence that does not already assume the conclusion; name the independent premise.",
        patterns=[(r"\bit('s| is) true because\b", 2), (r"\bbegs? the question\b", 2),
                  (r"\bassumes? (what|the thing)\b", 2), (r"\bthat's just how it is\b", 1),
                  (r"\bobviously\b.{0,40}\bbecause\b", 1), (r"\bbecause\b.{0,50}\bbecause\b", 1)],
    ),
    dict(
        id="false-analogy", kind="fallacy", name="False analogy",
        definition="Arguing from a similarity that is irrelevant to the conclusion.",
        cue="just like / no different from",
        example="\"Managing engineers is just like managing sales reps.\"",
        debias="List the relevant dimensions and check whether the analogy matches on those, not just surface.",
        patterns=[(r"\bjust like\b", 1), (r"\bis (no different|the same as)\b", 2),
                  (r"\bthink of it (like|as)\b", 1), (r"\bcompared to\b.{0,60}\btherefore\b", 1),
                  (r"\b(it's|it is) like\b", 1)],
    ),
    dict(
        id="tu-quoque", kind="fallacy", name="Tu quoque",
        definition="Deflecting a criticism by accusing the critic of the same fault.",
        cue="you do it too / what about you",
        example="\"You missed the deadline too, so you can't criticize my slip.\"",
        debias="Evaluate the claim on its merits; hypocrisy affects credibility, not truth.",
        patterns=[(r"\byou('re| are) (the )?(one|same)\b", 2), (r"\bwhat about (you|your|them)\b", 2),
                  (r"\bhypocri(te|sy)\b", 2), (r"\bthey did it too\b", 2), (r"\byou too\b", 1)],
    ),
    dict(
        id="appeal-to-emotion", kind="fallacy", name="Appeal to emotion",
        definition="Substituting fear, outrage, or sympathy for relevant evidence.",
        cue="think of the children / how would you feel",
        example="\"If we don't approve this, families will suffer.\"",
        debias="Separate the emotional pull from the factual claim; ask what evidence would settle it.",
        patterns=[(r"\bthink of the (children|families|victims)\b", 2), (r"\bhow would you feel\b", 2),
                  (r"\b(disgusting|outrageous|heartbreaking|terrifying)\b", 1),
                  (r"\b(scary|panic|outrage|fear)\b", 1)],
    ),
    dict(
        id="red-herring", kind="fallacy", name="Red herring",
        definition="Introducing an irrelevant point that diverts attention from the issue.",
        cue="the real issue is / more importantly",
        example="\"Yes, the bug shipped, but the real issue is competitor pricing.\"",
        debias="Park the tangent, restate the original question, and answer that first.",
        patterns=[(r"\bthe real (issue|question|problem) is\b", 1), (r"\bwhat about\b", 1),
                  (r"\bmore importantly\b", 1), (r"\bnot to mention\b", 1),
                  (r"\bthat's (beside|irrelevant)\b", 1)],
    ),
    dict(
        id="burden-of-proof", kind="fallacy", name="Burden of proof shifting",
        definition="Asserting a claim, then demanding others disprove it.",
        cue="prove me wrong / unless you can show otherwise",
        example="\"Ghosts exist; prove that they don't.\"",
        debias="Whoever asserts must supply evidence; state the threshold before evaluating.",
        patterns=[(r"\bprove (me|it|that) (wrong|otherwise)\b", 2), (r"\bunless you can show\b", 2),
                  (r"\bif you can't disprove\b", 2), (r"\bcan you prove\b", 1),
                  (r"\babsence of evidence\b", 1)],
    ),
    dict(
        id="cherry-picking", kind="fallacy", name="Cherry picking",
        definition="Selecting only the evidence that supports a claim while ignoring the rest.",
        cue="the one study / look at these results",
        example="\"The one trial that showed a gain proves the program works.\"",
        debias="Ask for the full sample and the null results; check what was excluded and why.",
        patterns=[(r"\bthe (one|only) (study|trial|case)\b", 2), (r"\bcherry[- ]pick", 2),
                  (r"\bignores? (the|all) (other|rest|studies|evidence)\b", 2),
                  (r"\bselected (data|evidence|examples)\b", 2), (r"\bhand[- ]picked\b", 1)],
    ),
    dict(
        id="moving-goalposts", kind="fallacy", name="Moving the goalposts",
        definition="Changing the success criterion after evidence meets the original one.",
        cue="that doesn't count / that's not what I meant",
        example="\"Fine, adoption grew, but that's not real growth.\"",
        debias="Write the success criterion and threshold down before looking at the result.",
        patterns=[(r"\bthat doesn't count\b", 2), (r"\bthat's not what (i|we) meant\b", 2),
                  (r"\bmove the goalposts\b", 2), (r"\bnow you (have to|need to)\b", 1),
                  (r"\byes, but\b", 1)],
    ),
    dict(
        id="loaded-question", kind="fallacy", name="Loaded question",
        definition="Asking a question that presupposes an unproven or disputed fact.",
        cue="have you stopped / why did you ruin",
        example="\"Why did you ignore the security review?\"",
        debias="Split the presupposition out and ask it separately as a yes/no claim.",
        patterns=[(r"\bhave you (stopped|quit)\b", 3), (r"\bwhen did you stop\b", 3),
                  (r"\bwhy (do|did) you\b.{0,40}\b(ruin|lie|fail|steal|ignore)\b", 2),
                  (r"\b(admit|confess) that\b", 1)],
    ),
    dict(
        id="genetic-fallacy", kind="fallacy", name="Genetic fallacy",
        definition="Judging a claim by its origin rather than its current merit.",
        cue="it started as / where it comes from",
        example="\"That method came from the military, so it can't fit startups.\"",
        debias="Evaluate the claim as it stands today; origin is context, not a verdict.",
        patterns=[(r"\bwhere it comes from\b", 2), (r"\bstarted (as|out as)\b.{0,40}\bso\b", 2),
                  (r"\binvented by\b", 1), (r"\binherited from\b", 1),
                  (r"\bthe origins?\b.{0,40}\b(prove|mean|show)\b", 1)],
    ),
    dict(
        id="composition-division", kind="fallacy", name="Composition / division",
        definition="Assuming what is true of parts is true of the whole, or vice versa.",
        cue="each part is … so the whole is",
        example="\"Every engineer is fast, so the team will ship fast.\"",
        debias="Identify the emergent property (coordination, bottlenecks) that does not distribute.",
        patterns=[(r"\beach (part|one|member|engineer|player)\b.{0,50}\b(therefore|so)\b", 2),
                  (r"\bmade of\b.{0,50}\bso (the whole|it)\b", 2),
                  (r"\bwhat's true of (the parts|the whole)\b", 2),
                  (r"\bevery (member|part|player)\b.{0,40}\b(the team|the whole)\b", 1)],
    ),

    # ------------------------------------------------------------------- biases
    dict(
        id="confirmation-bias", kind="bias", name="Confirmation bias",
        definition="Seeking and weighting evidence that supports what you already believe.",
        cue="as I expected / that proves my point",
        example="\"As I expected, the two happy customers prove the redesign worked.\"",
        debias="Write down the disconfirming observation you have not looked for, then look for it.",
        patterns=[(r"\bas i (expected|thought|suspected)\b", 2), (r"\bi knew it\b", 2),
                  (r"\bthat proves (my|the) point\b", 2), (r"\bseems? to confirm\b", 2),
                  (r"\b(only|just) .{0,30}\b(supports|confirms)\b", 2), (r"\bjust as i said\b", 1)],
    ),
    dict(
        id="anchoring", kind="bias", name="Anchoring",
        definition="Letting an initial number or framing dominate later estimates.",
        cue="starting from / compared to the original",
        example="\"The list price was 50k, so 30k feels cheap.\"",
        debias="Estimate independently before seeing the anchor; then compare.",
        patterns=[(r"\binitial (number|estimate|offer|price)\b", 2), (r"\bfirst (offer|estimate|number)\b", 2),
                  (r"\banchor\b", 2), (r"\bcompared to (the )?(first|original)\b", 1),
                  (r"\bstarting (point|from)\b.{0,30}\badjust", 1)],
    ),
    dict(
        id="availability", kind="bias", name="Availability heuristic",
        definition="Judging likelihood by how easily examples come to mind.",
        cue="in my experience / it failed last time",
        example="\"We tried it once and it failed, so it will always fail.\"",
        debias="Replace the memory with a count: how many attempts, what were the denominators?",
        patterns=[(r"\b(we|i) tried (it|this) once\b", 2), (r"\bin my experience\b", 2),
                  (r"\bit (failed|worked) (before|last time)\b", 2),
                  (r"\b(comes? to mind|easy to (imagine|recall))\b", 2),
                  (r"\b(always|never) (fails|works)\b", 1), (r"\bvivid\b", 1),
                  (r"\brecently\b.{0,40}\b(so|therefore)\b", 1)],
    ),
    dict(
        id="survivorship-bias", kind="bias", name="Survivorship bias",
        definition="Drawing conclusions from the cases that survived while the failures are invisible.",
        cue="look at all the winners / it worked for them",
        example="\"Every founder we interview dropped out of college.\"",
        debias="Ask who is missing from the sample and what happened to them.",
        patterns=[(r"\bsurvivors?\b", 2), (r"\bwhat (all )?the winners (do|did)\b", 2),
                  (r"\bthe (ones|companies) that (made it|survived)\b", 2),
                  (r"\bsuccessful (people|companies|founders)\b", 1),
                  (r"\b(it|this) worked for\b", 1), (r"\bthey (made it|succeeded) so\b", 2)],
    ),
    dict(
        id="sunk-cost", kind="bias", name="Sunk cost",
        definition="Continuing an effort because of past investment rather than future value.",
        cue="we've already invested / too far to stop",
        example="\"We've spent two years on it; we can't quit now.\"",
        debias="Ask: if we were starting fresh today, would we begin this? Decide on marginal value.",
        patterns=[(r"\bwe('ve| have) (already )?(invested|spent|put)\b", 3),
                  (r"\btoo (much )?(invested|far) to (stop|quit|turn back)\b", 3),
                  (r"\bcan't quit now\b", 2), (r"\bdon't want to (waste|throw away)\b", 2),
                  (r"\bsunk cost\b", 2)],
    ),
    dict(
        id="hindsight-bias", kind="bias", name="Hindsight bias",
        definition="Believing an outcome was predictable after it is known.",
        cue="I knew it all along / it was obvious",
        example="\"It was obvious the launch would flop.\"",
        debias="Recover a dated pre-outcome forecast; score that, not the memory.",
        patterns=[(r"\bi (knew|said) (it|this) (all along|would happen)\b", 3),
                  (r"\bit was (always|bound) (going )?to\b", 2), (r"\bwe should have (known|seen)\b", 2),
                  (r"\bin hindsight\b", 1), (r"\bobvious(ly)? that\b", 1), (r"\bpredictable\b", 1)],
    ),
    dict(
        id="overconfidence", kind="bias", name="Overconfidence",
        definition="Stating more certainty than the evidence supports.",
        cue="without a doubt / guaranteed",
        example="\"There is zero chance this migration breaks checkout.\"",
        debias="Attach a number and an interval; ask what would falsify it and what you'd bet.",
        patterns=[(r"\b(zero|no) (chance|risk|doubt)\b", 2), (r"\bimpossible to fail\b", 2),
                  (r"\b100%|guarantee[ds]?\b", 2), (r"\bwithout a doubt\b", 1),
                  (r"\bi('m| am) (certain|sure)\b", 1), (r"\bdefinitely\b", 1)],
    ),
    dict(
        id="framing-effect", kind="bias", name="Framing effect",
        definition="Reaching different conclusions from logically equivalent descriptions.",
        cue="save $X / 90% survival",
        example="\"90% survival\" vs \"10% mortality\" for the same surgery.",
        debias="Restate the claim in the opposite frame; if the judgment flips, the frame did the work.",
        patterns=[(r"\b(save|saving) \$?\d+", 2), (r"\b9\d(\.\d+)? ?% (survival|success)\b", 2),
                  (r"\b(loss|mortality|failure) rate\b", 2), (r"\b(only|just) \$?\d+", 1),
                  (r"\b(reduced|discounted|sale) price\b", 1), (r"\bper day\b.{0,30}\bper (month|year)\b", 1)],
    ),
    dict(
        id="loss-aversion", kind="bias", name="Loss aversion",
        definition="Weighting losses roughly twice as heavily as equivalent gains.",
        cue="don't want to lose / protect what we have",
        example="\"We can't risk a small dip even for a large upside.\"",
        debias="Price the gain and the loss in the same units; ask if you'd take the bet reversed.",
        patterns=[(r"\bdon't (want to )?lose\b", 2), (r"\bavoid (losing|loss|losses)\b", 2),
                  (r"\b(risk|chance) of losing\b", 2), (r"\bworse to lose\b", 2),
                  (r"\bprotect (what|what we have|our)\b", 1)],
    ),
    dict(
        id="status-quo-bias", kind="bias", name="Status quo bias",
        definition="Preferring the current arrangement because it is current.",
        cue="how we've always done it / if it ain't broke",
        example="\"The current process works fine\" — it has never been measured.",
        debias="Include \"do nothing\" as an explicit option with its own costs and owner.",
        patterns=[(r"\bhow we('ve| have) always\b", 2), (r"\bif it ain't broke\b", 2),
                  (r"\bstay the course\b", 2), (r"\bstatus quo\b", 3),
                  (r"\bdon't (fix|change|rock)\b", 2), (r"\bcurrent (process|system) works\b", 1)],
    ),
    dict(
        id="in-group-bias", kind="bias", name="In-group bias",
        definition="Favoring members of your own group and discounting outsiders.",
        cue="us vs them / not one of us",
        example="\"Our team's estimate is credible; theirs is padded.\"",
        debias="Apply one rubric to all groups and score blind to affiliation.",
        patterns=[(r"\b(us|we) vs\.? (them|the other side)\b", 2),
                  (r"\b(our|the) team (is|are) better\b", 2),
                  (r"\bnot one of us\b", 2), (r"\b(they|those people) always\b", 2),
                  (r"\boutsiders?\b", 1)],
    ),
    dict(
        id="halo-effect", kind="bias", name="Halo effect",
        definition="Letting one good trait spill over into unrelated judgments.",
        cue="good at X, so good at Y",
        example="\"She was a great engineer, so she'll be a great manager.\"",
        debias="Score each dimension separately and name the evidence for that dimension alone.",
        patterns=[(r"\bgood at\b.{0,40}\bso good at\b", 2), (r"\bhalo\b", 2),
                  (r"\b(attractive|charismatic|famous|successful)\b.{0,40}\b(so|therefore|must)\b", 2),
                  (r"\btrusted (brand|name)\b", 1)],
    ),
    dict(
        id="fundamental-attribution-error", kind="bias", name="Fundamental attribution error",
        definition="Explaining others' failures by character and your own by circumstance.",
        cue="they're just lazy / their fault",
        example="\"They missed the deadline because they're careless\" — not because scope doubled.",
        debias="Swap the explanation: apply the situational story you'd use for yourself.",
        patterns=[(r"\b(they|he|she) (is|are) (just )?(lazy|careless|incompetent|sloppy)\b", 2),
                  (r"\b(they|he|she) did it because\b.{0,40}\b(kind of person|character|personality)\b", 2),
                  (r"\bbad apples?\b", 2), (r"\btheir fault\b", 1),
                  (r"\bi (failed|made a mistake) because\b", 1)],
    ),
    dict(
        id="planning-fallacy", kind="bias", name="Planning fallacy",
        definition="Underestimating time, cost, and risk of future projects.",
        cue="on schedule / should only take",
        example="\"It should only take two weeks, no major surprises.\"",
        debias="Use the outside view: base rate of similar past projects, then adjust.",
        patterns=[(r"\bon (schedule|time|budget)\b", 2), (r"\bshould (only )?take\b", 2),
                  (r"\bno (major )?(delays|problems|surprises)\b", 2),
                  (r"\bwill (be done|finish|ship) (by|in)\b", 1), (r"\bthis time is different\b", 2),
                  (r"\bworst case\b.{0,30}\bminor\b", 2)],
    ),
    dict(
        id="recency-bias", kind="bias", name="Recency bias",
        definition="Overweighting the latest data relative to the longer record.",
        cue="last quarter / these days",
        example="\"Last month was great, so the trend is up.\"",
        debias="Plot the full history with the recent point highlighted; ask what the base rate says.",
        patterns=[(r"\blast (week|month|quarter|time)\b", 1), (r"\brecent(ly)?\b.{0,40}\b(so|means|shows)\b", 2),
                  (r"\bthese days\b", 1), (r"\bthe latest\b", 1),
                  (r"\b(trend|trending) (is|shows)\b", 1), (r"\bright now\b.{0,30}\b(will|going to)\b", 1)],
    ),
    dict(
        id="regression-to-the-mean", kind="bias", name="Regression to the mean",
        definition="Reading natural reversion after an extreme result as a causal effect.",
        cue="record high / it can only get better",
        example="\"After last year's record, this quarter's dip proves the new policy failed.\"",
        debias="Ask how much of the extreme was luck; predict reversion before attributing cause.",
        patterns=[(r"\b(record|all-time) (high|low)\b", 1), (r"\bit can only get (better|worse)\b", 2),
                  (r"\bmean reversion|regression to the mean\b", 3),
                  (r"\b(worst|best) (year|quarter|month)\b.{0,50}\btherefore\b", 2),
                  (r"\brebounded\b", 1)],
    ),
    dict(
        id="dunning-kruger", kind="bias", name="Dunning–Kruger effect",
        definition="Overestimating competence in a domain precisely because expertise is missing.",
        cue="how hard can it be / anyone can do this",
        example="\"How hard can this migration be? It's just moving files.\"",
        debias="Ask a practitioner what the failure modes are; estimate again after the list.",
        patterns=[(r"\bhow hard can it be\b", 3), (r"\banyone can (do|see)\b", 2),
                  (r"\bdunning[- ]kruger\b", 3), (r"\b(it's|it is) (so )?simple\b", 1),
                  (r"\bi (already )?know (this|enough)\b", 1), (r"\bjust a matter of\b", 1)],
    ),
    dict(
        id="ambiguity-aversion", kind="bias", name="Ambiguity aversion",
        definition="Avoiding options whose probabilities are unknown, even when they are better.",
        cue="better the devil you know / avoid the unknown",
        example="\"We'll keep the known vendor; the new one's terms are unclear.\"",
        debias="Price the unknown: what would it cost to learn the odds? Compare expected value, not comfort.",
        patterns=[(r"\b(unclear|uncertain|ambiguous)\b.{0,50}\b(so|therefore) (avoid|don't|won't)\b", 2),
                  (r"\bprefer (the )?(known|familiar|sure)\b", 2),
                  (r"\bbetter the devil you know\b", 2), (r"\bavoid the unknown\b", 2),
                  (r"\bknown (risk|quantity)\b", 1)],
    ),
    dict(
        id="choice-supportive-bias", kind="bias", name="Choice-supportive bias",
        definition="Remembering a chosen option as better than it was, and the rejected one as worse.",
        cue="glad we chose / our decision was right",
        example="\"We picked vendor A, so of course its onboarding was the smoothest.\"",
        debias="Re-score the options on the criteria you used before the choice, from the original notes.",
        patterns=[(r"\b(glad|happy) we (chose|picked|did)\b", 2), (r"\bour (decision|choice) was\b", 1),
                  (r"\bwe (chose|picked)\b.{0,40}\bso\b", 2), (r"\bmy (pick|option) is better\b", 2),
                  (r"\binvested in\b.{0,30}\bso\b", 1)],
    ),
    dict(
        id="narrative-bias", kind="bias", name="Narrative bias",
        definition="Preferring a coherent story over the messier evidence.",
        cue="makes a great story / fits the narrative",
        example="\"The turnaround makes a great story, so the causal chain must be right.\"",
        debias="Write the version with luck, noise, and missing actors; check if it still explains the data.",
        patterns=[(r"\bmakes? a (great|compelling) (story|narrative)\b", 2),
                  (r"\bthe story (writes|tells) itself\b", 2), (r"\bfits the narrative\b", 2),
                  (r"\beverything (happened|fit) for a reason\b", 2),
                  (r"\btoo (good|clean) to be (true|coincidence)\b", 1), (r"\bnarrative\b", 1)],
    ),
]

BY_ID = {e["id"]: e for e in CATALOG}
KIND_LABEL = {"fallacy": "Fallacy", "bias": "Bias"}


def compile_patterns() -> None:
    for entry in CATALOG:
        entry["_rx"] = [(re.compile(p, re.I), w) for p, w in entry["patterns"]]


def scan(text: str) -> list[dict]:
    """Score every catalog entry against `text`; return matched tags, ranked."""
    tags = []
    for entry in CATALOG:
        score, why = 0, []
        for rx, weight in entry["_rx"]:
            m = rx.search(text)
            if m:
                score += weight
                snippet = m.group(0).strip()
                if snippet and snippet.lower() not in (w.lower() for w in why):
                    why.append(snippet)
        if score >= MAYBE:
            tags.append({
                "id": entry["id"],
                "kind": entry["kind"],
                "name": entry["name"],
                "verdict": "Hit" if score >= HIT else "Maybe",
                "score": score,
                "why": "matched: " + ", ".join(f"\"{w}\"" for w in why[:3]),
                "debias": entry["debias"],
            })
    tags.sort(key=lambda t: (-t["score"], t["name"].lower()))
    return tags


def render_tags(tags: list[dict], top: int) -> str:
    kept = tags[:top]
    if not kept:
        return "No fallacy or bias cues matched. Screening is not clearance: check the structure yourself.\n"
    lines = [
        "| # | Kind | Tag | Verdict | Why | De-bias move |",
        "|---|---|---|---|---|---|",
    ]
    for i, t in enumerate(kept, 1):
        why = t["why"].replace("|", "\\|")
        debias = t["debias"].replace("|", "\\|")
        lines.append(f"| {i} | {KIND_LABEL[t['kind']]} | {t['name']} | {t['verdict']} | {why} | {debias} |")
    hits = sum(1 for t in kept if t["verdict"] == "Hit")
    lines.append("")
    lines.append(f"{len(kept)} shown ({hits} Hit, {len(kept) - hits} Maybe) of {len(tags)} matched. "
                 "Keep the top 3; the rest is noise. A cue is a prompt to inspect, not proof.")
    return "\n".join(lines) + "\n"


def render_list() -> str:
    out = []
    for kind, title in (("fallacy", "Fallacies"), ("bias", "Cognitive biases")):
        out.append(f"## {title} (20)\n")
        out.append("| # | Name | Definition | Cue phrase | Example | De-bias |")
        out.append("|---|---|---|---|---|---|")
        entries = [e for e in CATALOG if e["kind"] == kind]
        for i, e in enumerate(entries, 1):
            cells = [e["name"], e["definition"], e["cue"], e["example"], e["debias"]]
            out.append(f"| {i} | " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
        out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Heuristic fallacy and bias scanner.")
    ap.add_argument("--text", help="text to scan; reads stdin when omitted")
    ap.add_argument("--list", action="store_true", help="print the 20 fallacies + 20 biases catalog")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    ap.add_argument("--top", type=int, default=3, help="max tags to show (default 3)")
    args = ap.parse_args(argv)

    if args.list:
        if args.json:
            print(json.dumps({k: [e for e in CATALOG if e["kind"] == k] for k in ("fallacy", "bias")},
                             indent=2, ensure_ascii=False))
        else:
            print(render_list(), end="")
        return 0

    compile_patterns()

    text = args.text if args.text is not None else sys.stdin.read()
    if not text.strip():
        ap.error("no text: pass --text or pipe stdin")
    tags = scan(text)
    kept = tags[: max(args.top, 1)]
    if args.json:
        print(json.dumps({
            "text": text,
            "tags": kept,
            "counts": {
                "hit": sum(1 for t in kept if t["verdict"] == "Hit"),
                "maybe": sum(1 for t in kept if t["verdict"] == "Maybe"),
                "matched_total": len(tags),
            },
        }, indent=2, ensure_ascii=False))
    else:
        print(render_tags(tags, max(args.top, 1)), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
