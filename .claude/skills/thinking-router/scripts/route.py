#!/usr/bin/env python3
"""Heuristic router for the critical-thinking track.

Scores five intent buckets from keyword signals, ranks the eight
critical-thinking skills, and prints a shortlist. Stdlib only.

Usage:
    route.py --text "is this source credible, does the argument follow?"
    route.py --text "..." --json
    route.py --text "..." --verbose
    route.py --list
"""

from __future__ import annotations

import argparse
import json
import re
import sys

TOKEN_RE = re.compile(r"[a-z0-9]+")

# Buckets in tie-break priority order. Later entries lose ties.
BUCKET_ORDER = [
    "sharper_judgment",
    "better_question",
    "broader_perspectives",
    "stronger_options",
    "more_ideas",
]

BUCKETS = {
    "sharper_judgment": {
        "label": "sharper judgment",
        "signals": [
            ("judgment", 1), ("judgement", 1), ("evaluate", 1), ("evaluation", 1),
            ("credible", 2), ("credibility", 2), ("source credible", 2),
            ("trust", 1), ("trustworthy", 1), ("valid", 1), ("validity", 1),
            ("sound", 1), ("soundness", 1), ("accurate", 1), ("accuracy", 1),
            ("assess", 1), ("assessment", 1), ("is this true", 2),
            ("is it true", 2), ("fact check", 2), ("does this follow", 2),
            ("does the argument follow", 2), ("source", 1), ("argument", 1),
            ("fallacy", 1), ("bias", 1), ("wrong", 1), ("mistake", 1),
            ("rigor", 1), ("rigorous", 1), ("critical", 1), ("skeptical", 1),
            ("follow", 1),
        ],
    },
    "better_question": {
        "label": "better question",
        "signals": [
            ("question", 1), ("reframe", 1), ("framing", 1), ("define", 1),
            ("definition", 1), ("what do you mean", 2), ("mean by", 2),
            ("clarify", 1), ("ambiguous", 1), ("vague", 1), ("precise", 1),
            ("precisely", 1), ("assumption", 1), ("assumptions", 1),
            ("scope", 1), ("problem statement", 2), ("what exactly", 2),
            ("term", 1), ("terms", 1), ("concept", 1), ("conceptual", 1),
            ("unpack", 1), ("restate", 1), ("interpret", 1), ("criteria", 1),
        ],
    },
    "more_ideas": {
        "label": "more ideas",
        "signals": [
            ("idea", 1), ("ideas", 1), ("brainstorm", 2), ("generate", 1),
            ("generative", 1), ("alternatives", 1), ("novel", 1),
            ("creative", 2), ("creativity", 2), ("diverge", 2),
            ("divergent", 2), ("more options", 2), ("possibilities", 1),
            ("ideate", 2), ("invent", 1), ("variations", 1), ("many ways", 2),
            ("come up with", 2), ("stuck", 1), ("blank page", 2),
        ],
    },
    "broader_perspectives": {
        "label": "broader perspectives",
        "signals": [
            ("perspective", 1), ("perspectives", 1), ("stakeholder", 1),
            ("stakeholders", 1), ("other side", 2), ("opposing", 1),
            ("opponent", 1), ("counterargument", 2), ("counter argument", 2),
            ("counterpoint", 1), ("dissent", 1), ("disagree", 1),
            ("disagreement", 1), ("blind spot", 2), ("worldview", 1),
            ("culture", 1), ("cultural", 1), ("steelman", 2), ("red team", 2),
            ("devils advocate", 2), ("fairness", 1), ("fair", 1),
            ("empathy", 1), ("point of view", 2), ("what am i missing", 2),
            ("groupthink", 2), ("echo chamber", 2),
        ],
    },
    "stronger_options": {
        "label": "stronger options",
        "signals": [
            ("decide", 1), ("decision", 1), ("choose", 1), ("choice", 1),
            ("prioritize", 1), ("priority", 1), ("tradeoff", 2),
            ("trade off", 2), ("risk", 1), ("risky", 1),
            ("expected value", 2), ("probability", 1), ("probabilities", 1),
            ("forecast", 1), ("prediction", 1), ("predict", 1),
            ("uncertain", 1), ("uncertainty", 1), ("stakes", 1), ("bet", 1),
            ("investment", 1), ("strategy", 1), ("plan", 1), ("recommend", 1),
            ("which one", 2), ("should we", 2), ("utility", 1),
            ("cost benefit", 2), ("downside", 1), ("base rate", 2),
            ("how confident", 2),
        ],
    },
}

# One entry per skill, in catalog rank order (rank = index + 1).
SKILLS = [
    {
        "slug": "evidence-appraisal",
        "buckets": ["sharper_judgment", "better_question"],
        "artifact": "source scorecard + claim strength 1-5 + what would change your mind",
        "signals": [
            ("source", 1), ("sources", 1), ("source credible", 2),
            ("is this source credible", 2), ("credible", 2), ("credibility", 2),
            ("trust", 1), ("trustworthy", 1), ("citation", 1), ("cite", 1),
            ("cited", 1), ("study", 1), ("studies", 1), ("paper", 1),
            ("papers", 1), ("preprint", 2), ("meta analysis", 2),
            ("systematic review", 2), ("peer review", 2), ("peer reviewed", 2),
            ("rct", 2), ("randomized", 1), ("sample", 1), ("sample size", 2),
            ("statistic", 1), ("statistics", 1), ("effect size", 2),
            ("p value", 2), ("p hacking", 2), ("conflict of interest", 2),
            ("funding", 1), ("replication", 1), ("reproducibility", 1),
            ("evidence", 1), ("evidence quality", 2), ("claim strength", 2),
            ("how much should i trust", 2), ("blog post", 1),
            ("expert opinion", 1), ("source tier", 2), ("observational", 1),
            ("correlational", 1), ("anecdote", 1), ("citation needed", 2),
        ],
    },
    {
        "slug": "argument-mapping",
        "buckets": ["sharper_judgment", "better_question"],
        "artifact": "claim-reason-warrant map + validity tag (deductive/inductive/abductive)",
        "signals": [
            ("argument", 1), ("arguments", 1), ("premise", 1), ("premises", 1),
            ("conclusion", 1), ("valid", 1), ("validity", 1), ("invalid", 1),
            ("follow", 1), ("follows", 1), ("warrant", 2), ("inference", 1),
            ("infer", 1), ("logic", 1), ("logical", 1), ("syllogism", 2),
            ("toulmin", 2), ("reasoning", 1), ("does it follow", 2),
            ("does the argument follow", 2), ("support the claim", 2),
            ("claim", 1), ("grounds", 1), ("backing", 1), ("qualifier", 1),
            ("rebuttal", 1), ("deductive", 2), ("inductive", 2),
            ("abductive", 2), ("persuasive", 1), ("rhetoric", 1),
            ("structure", 1), ("map the argument", 2), ("hidden premise", 2),
        ],
    },
    {
        "slug": "fallacy-bias-spotting",
        "buckets": ["sharper_judgment", "broader_perspectives"],
        "artifact": "annotated fallacy/bias sheet (Hit/Maybe/No) + de-bias move",
        "signals": [
            ("fallacy", 2), ("fallacies", 2), ("bias", 1), ("biases", 2),
            ("biased", 1), ("strawman", 2), ("straw man", 2),
            ("ad hominem", 2), ("slippery slope", 2), ("false dilemma", 2),
            ("false dichotomy", 2), ("equivocation", 2), ("circular", 1),
            ("begging the question", 2), ("post hoc", 2),
            ("appeal to authority", 2), ("appeal to emotion", 2),
            ("bandwagon", 2), ("anchoring", 2), ("availability heuristic", 2),
            ("confirmation bias", 2), ("survivorship", 2), ("sunk cost", 2),
            ("halo effect", 2), ("hindsight", 1), ("cognitive bias", 2),
            ("logical error", 2), ("logical fallacy", 2), ("feels right", 2),
            ("rationalize", 1), ("rationalization", 1), ("self deception", 2),
            ("motivated reasoning", 2), ("de bias", 2),
        ],
    },
    {
        "slug": "bayesian-updating",
        "buckets": ["sharper_judgment", "stronger_options"],
        "artifact": "prior -> likelihood ratio -> posterior + base-rate check + value of information",
        "signals": [
            ("bayes", 2), ("bayesian", 2), ("prior", 1), ("priors", 2),
            ("posterior", 2), ("likelihood", 1), ("likelihood ratio", 2),
            ("base rate", 2), ("base rates", 2), ("update", 1),
            ("updating", 1), ("how much should i update", 2),
            ("how much to move", 2), ("odds", 1), ("probability", 1),
            ("probabilities", 1), ("conditional", 1), ("false positive", 2),
            ("sensitivity", 1), ("specificity", 1), ("value of information", 2),
            ("belief", 1), ("should i believe", 2), ("new evidence", 2),
            ("diagnostic", 1), ("prevalence", 2), ("bayes factor", 2),
        ],
    },
    {
        "slug": "socratic-elenchus",
        "buckets": ["better_question", "sharper_judgment"],
        "artifact": "definition -> counterexample -> revision -> operational definition",
        "signals": [
            ("define", 1), ("definition", 1), ("means", 1), ("mean by", 2),
            ("what do you mean", 2), ("what does it mean", 2),
            ("term", 1), ("terms", 1), ("concept", 1), ("conceptual", 1),
            ("ambiguity", 1), ("ambiguous", 1), ("vague", 1), ("vagueness", 1),
            ("precise", 1), ("precisely", 1), ("clarify", 1),
            ("clarification", 1), ("counterexample", 2), ("counter example", 2),
            ("operational definition", 2), ("operationalize", 2),
            ("socratic", 2), ("elenchus", 2), ("criteria", 1),
            ("boundary case", 2), ("edge case", 1), ("distinction", 1),
            ("unpack", 1), ("undefined", 1), ("jargon", 1), ("weasel word", 2),
        ],
    },
    {
        "slug": "steelman-red-team",
        "buckets": ["broader_perspectives", "sharper_judgment"],
        "artifact": "steelman (strongest P) + red-team attack + pre-committed falsifier",
        "signals": [
            ("steelman", 2), ("steel man", 2), ("steelmanning", 2),
            ("red team", 2), ("red teaming", 2),
            ("strongest counterargument", 2), ("strongest objection", 2),
            ("strongest argument against", 2), ("strongest case", 2),
            ("opposing view", 2), ("other side", 1), ("counterargument", 2),
            ("counter argument", 2), ("attack", 1), ("falsify", 2),
            ("falsification", 1), ("devils advocate", 2), ("dissent", 1),
            ("disagreement", 1), ("objection", 1), ("rebut", 1),
            ("weak critique", 2), ("adversarial", 1),
            ("adversarial collaboration", 2), ("charitable", 1),
            ("charity", 1), ("what would change my mind", 2),
        ],
    },
    {
        "slug": "calibration-forecasting",
        "buckets": ["stronger_options", "sharper_judgment"],
        "artifact": "Brier-scored forecast + calibration curve + 3 testable predictions",
        "signals": [
            ("calibration", 2), ("calibrated", 2), ("overconfident", 2),
            ("overconfidence", 2), ("underconfident", 1), ("brier", 2),
            ("brier score", 2), ("forecast", 2), ("forecasting", 2),
            ("prediction", 2), ("predictions", 2), ("predict", 1),
            ("confidence interval", 2), ("how confident are you", 2),
            ("probability estimate", 2), ("track record", 1),
            ("superforecaster", 2), ("superforecasting", 2),
            ("testable predictions", 2), ("scoring rule", 2),
            ("accountable", 1), ("confidence level", 2),
            ("percentage chance", 2), ("what are the odds", 2),
        ],
    },
    {
        "slug": "decision-analysis",
        "buckets": ["stronger_options", "sharper_judgment"],
        "artifact": "EV sheet (options x outcomes x probabilities x utilities) + sensitivity + next probe",
        "signals": [
            ("decide", 1), ("decision", 1), ("choose", 1), ("choice", 1),
            ("options", 1), ("option", 1), ("expected value", 2),
            ("expected utility", 2), ("utility", 1), ("tradeoff", 2),
            ("trade off", 2), ("risk", 1), ("risky", 1), ("downside", 1),
            ("upside", 1), ("stakes", 1), ("cost benefit", 2),
            ("prioritize", 1), ("prioritization", 1),
            ("sensitivity analysis", 2), ("decision tree", 2),
            ("monte carlo", 2), ("which one", 2), ("should we", 2),
            ("should i", 2), ("recommend", 1), ("bet", 1), ("invest", 1),
            ("irreversible", 2), ("reversible", 1), ("opportunity cost", 2),
            ("under uncertainty", 2), ("uncertainty", 1), ("payoff", 2),
            ("probability weighted", 2),
        ],
    },
]

BUCKET_LABELS = {k: v["label"] for k, v in BUCKETS.items()}


def normalize(text: str) -> str:
    return text.lower().replace("\u2019", "").replace("'", "")


def tokens_of(text: str) -> list[str]:
    return TOKEN_RE.findall(normalize(text))


def score_signals(tokens: list[str], signals: list[tuple[str, float]]) -> tuple[float, list[str]]:
    token_set = set(tokens)
    padded = f" {' '.join(tokens)} "
    matched: list[str] = []
    raw = 0.0
    for keyword, weight in signals:
        parts = keyword.split()
        if len(parts) == 1:
            hit = parts[0] in token_set
        else:
            hit = f" {keyword} " in padded
        if hit:
            matched.append(keyword)
            raw += weight
    return raw, matched


def score_buckets(tokens: list[str]) -> list[dict]:
    rows = []
    for name, spec in BUCKETS.items():
        raw, matched = score_signals(tokens, spec["signals"])
        rows.append({"bucket": name, "label": spec["label"], "raw": raw, "matched": matched})
    best = max((r["raw"] for r in rows), default=0.0)
    for row in rows:
        row["score"] = round(row["raw"] / best, 3) if best else 0.0
    rows.sort(key=lambda r: (-r["raw"], BUCKET_ORDER.index(r["bucket"])))
    return rows


def primary_bucket(bucket_rows: list[dict]) -> tuple[str, float, float]:
    top = bucket_rows[0]
    second_raw = bucket_rows[1]["raw"] if len(bucket_rows) > 1 else 0.0
    return top["bucket"], top["raw"], second_raw


def confidence(top_raw: float, second_raw: float) -> str:
    if top_raw <= 0:
        return "low"
    margin = top_raw - second_raw
    if top_raw >= 3 and margin >= 2:
        return "high"
    if top_raw >= 2 and margin >= 1:
        return "medium"
    return "low"


def rank_skills(tokens: list[str], primary: str) -> list[dict]:
    token_set = set(tokens)
    padded = f" {' '.join(tokens)} "
    ranked = []
    for index, skill in enumerate(SKILLS):
        raw, matched = score_signals(tokens, skill["signals"])
        ranked.append({
            "slug": skill["slug"],
            "rank": index + 1,
            "raw": raw,
            "matched": matched,
            "buckets": skill["buckets"],
            "artifact": skill["artifact"],
            "in_primary_bucket": primary in skill["buckets"],
        })
    ranked.sort(key=lambda s: (-s["raw"], not s["in_primary_bucket"], s["rank"]))
    matched_any = any(s["raw"] > 0 for s in ranked)
    if not matched_any:
        # Fall back to the methods that serve the winning bucket, in catalog order.
        ranked = [s for s in ranked if s["in_primary_bucket"]] or ranked
    best = max((s["raw"] for s in ranked), default=0.0)
    for position, skill in enumerate(ranked):
        skill["score"] = round(skill["raw"] / best, 3) if best else 0.0
        skill["position"] = position + 1
    return [s for s in ranked if s["raw"] > 0] or ranked


def build_result(text: str, top_n: int) -> dict:
    tokens = tokens_of(text)
    bucket_rows = score_buckets(tokens)
    primary, top_raw, second_raw = primary_bucket(bucket_rows)
    conf = confidence(top_raw, second_raw)
    ranked = rank_skills(tokens, primary)
    skills = ranked[: max(1, top_n)]
    shortlist = skills[:1]
    if len(skills) > 1 and skills[0]["raw"] > 0 and skills[1]["raw"] >= 0.5 * skills[0]["raw"]:
        shortlist = skills[:2]
    handoff = f"Route: {BUCKET_LABELS[primary]} -> {', '.join(s['slug'] for s in shortlist)}"
    if primary == "more_ideas":
        handoff = (
            "Route: more ideas -> creative-thinking track. "
            "No critical-thinking skill fixes a generation deficit; come back to route judgment afterwards."
        )
    return {
        "text": text,
        "bucket": primary,
        "primary_bucket": primary,
        "primary_bucket_label": BUCKET_LABELS[primary],
        "confidence": conf,
        "buckets": bucket_rows,
        "ranking": skills,
        "shortlist": [s["slug"] for s in shortlist],
        "handoff": handoff,
    }


def render_text(result: dict, verbose: bool) -> str:
    lines = [
        f"Primary bucket: {result['primary_bucket_label']} ({result['primary_bucket']})",
        f"Confidence: {result['confidence']}",
        "",
        "Bucket scores:",
    ]
    for row in result["buckets"]:
        detail = ""
        if verbose and row["matched"]:
            detail = f"  [{', '.join(row['matched'])}]"
        lines.append(f"  {row['bucket']:<22} {row['raw']:>4.1f}{detail}")
    lines += ["", "Shortlist:"]
    for skill in result["ranking"]:
        labels = ", ".join(BUCKET_LABELS[b] for b in skill["buckets"])
        why = f"  why: {', '.join(skill['matched'])}" if verbose and skill["matched"] else ""
        lines.append(f"  {skill['position']}. {skill['slug']}  score {skill['score']:.2f}  buckets: {labels}")
        lines.append(f"     artifact: {skill['artifact']}{why}")
    lines += ["", f"Handoff: {result['handoff']}"]
    if result["confidence"] == "low":
        lines.append('Ask one clarifying question before routing: "Are we judging whether this is true, or deciding what to do about it?"')
    return "\n".join(lines)


def render_list() -> str:
    lines = ["Critical-thinking catalog (rank order):"]
    for index, skill in enumerate(SKILLS, 1):
        labels = ", ".join(BUCKET_LABELS[b] for b in skill["buckets"])
        lines.append(f"{index}. {skill['slug']}")
        lines.append(f"   buckets: {labels}")
        lines.append(f"   artifact: {skill['artifact']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Route a critical-thinking task to one or two methods.",
    )
    parser.add_argument("--text", help="the task or question to route")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--verbose", action="store_true", help="show matched keywords")
    parser.add_argument("--list", action="store_true", help="print the catalog and exit")
    parser.add_argument("--top", type=int, default=3, help="number of ranked skills to show (default 3)")
    args = parser.parse_args(argv)

    if args.list:
        print(render_list())
        return 0
    if not args.text or not args.text.strip():
        parser.error("--text is required unless --list is used")

    result = build_result(args.text, args.top)
    if args.json:
        payload = result
        if not args.verbose:
            payload = json.loads(json.dumps(result))
            for row in payload["buckets"]:
                row.pop("matched", None)
            for skill in payload["ranking"]:
                skill.pop("matched", None)
        print(json.dumps(payload, indent=2))
    else:
        print(render_text(result, args.verbose))
    return 0


if __name__ == "__main__":
    sys.exit(main())
