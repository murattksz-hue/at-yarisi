#!/usr/bin/env python3
"""Evidence appraisal scorecard helper.

Scores one claim/source pair on a 1-5 strength scale using the rubric in
references/scorecard.md. Offline, stdlib only, no network calls.

    python3 evidence.py --claim "X reduces Y by 20%" --tier rct --n 200 --json
    python3 evidence.py --claim "..." --source "doi:10.1/x" --tier meta \
        --recency 8 --directness indirect --bias medium
"""
import argparse
import json
import sys

TIER_BASE = {
    "meta": 5.0,
    "rct": 4.0,
    "observational": 3.0,
    "case": 2.0,
    "expert": 1.5,
    "blog": 1.0,
}
BIAS_PENALTY = {"low": 0.0, "medium": 0.5, "high": 1.0}
MAX_RECENCY_PENALTY = 1.0
FRESH_YEARS = 2
DECAY_STEP_YEARS = 4
DECAY_PER_STEP = 0.25

LABELS = [
    (4.5, "decision-grade: act and cite"),
    (3.5, "usable with a caveat: look for one replication"),
    (2.5, "suggestive: do not let it carry a high-stakes decision alone"),
    (1.5, "hypothesis only: seek a better design"),
    (0.0, "anecdote/opinion: label it as such"),
]


def recency_penalty(years: int) -> float:
    if years <= FRESH_YEARS:
        return 0.0
    steps = (years - FRESH_YEARS) // DECAY_STEP_YEARS
    return min(MAX_RECENCY_PENALTY, steps * DECAY_PER_STEP)


def appraise(args) -> dict:
    base = TIER_BASE[args.tier]
    rec_pen = recency_penalty(args.recency)
    dir_pen = 0.5 if args.directness == "indirect" else 0.0
    bias_pen = BIAS_PENALTY[args.bias]
    raw = base - rec_pen - dir_pen - bias_pen
    strength = round(min(5.0, max(1.0, raw)), 1)

    label = next(text for cutoff, text in LABELS if strength >= cutoff)
    caution = None
    if args.bias == "high" and (args.n is not None and args.n < 100) and args.tier in ("rct", "observational"):
        strength = min(strength, 2.0)
        label = "capped at 2: high bias + small N + non-meta design"
        caution = "high bias with small N caps strength at 2"
    if args.directness == "indirect" and args.bias == "high" and strength > 3.0:
        strength = 3.0
        caution = "indirect outcome with high bias caps strength at 3"

    scorecard = {
        "claim": args.claim,
        "source": args.source,
        "tier": args.tier,
        "n": args.n,
        "effect": args.effect,
        "recency_years": args.recency,
        "directness": args.directness,
        "bias": args.bias,
        "strength": strength,
        "label": label,
        "components": {
            "tier_base": base,
            "recency_penalty": rec_pen,
            "directness_penalty": dir_pen,
            "bias_penalty": bias_pen,
            "raw": round(raw, 2),
        },
        "next_probe": next_probe(args),
    }
    if caution:
        scorecard["caution"] = caution
    return scorecard


def next_probe(args) -> str:
    if args.tier == "blog":
        return "find the primary study the post cites; score that instead"
    if args.tier == "expert":
        return "find empirical work by the same author or a systematic review of the claim"
    if args.tier == "case":
        return "look for a controlled or cohort study in the same population"
    if args.bias == "high":
        return "find an independent, lower-conflict replication"
    if args.directness == "indirect":
        return "find a study measuring the outcome you actually care about"
    if args.recency > FRESH_YEARS + DECAY_STEP_YEARS:
        return "check for a newer replication or updated meta-analysis"
    if args.tier == "observational":
        return "look for an RCT or natural experiment on the same question"
    if args.tier == "rct":
        return "look for an independent replication or meta-analysis"
    return "verify the cited sentence against the full text; check for retraction or erratum"


def human(row: dict) -> str:
    sep = "+" + "-" * 12 + "+" + "-" * 38 + "+"
    lines = [
        "Evidence scorecard",
        sep,
        f"| {'field':<10} | {'value':<36} |",
        sep,
    ]
    for key in ("claim", "source", "tier", "n", "effect", "recency_years", "directness", "bias"):
        value = row[key]
        if value is None:
            value = "-"
        lines.append(f"| {key:<10} | {str(value):<36} |")
    lines.append(f"| {'strength':<10} | {str(row['strength']) + ' / 5':<36} |")
    lines.append(sep)
    lines.append(f"label: {row['label']}")
    lines.append(
        "components: base {tier_base} - recency {recency_penalty} "
        "- indirect {directness_penalty} - bias {bias_penalty}".format(**row["components"])
    )
    if row.get("caution"):
        lines.append(f"caution: {row['caution']}")
    lines.append(f"next probe: {row['next_probe']}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="evidence.py",
        description="Score a claim/source pair on a 1-5 evidence-strength scale (offline).",
        epilog="Example: evidence.py --claim 'X reduces Y by 20%' --tier rct --n 200 --json",
    )
    p.add_argument("--claim", required=True, help="the claim as one falsifiable sentence")
    p.add_argument("--source", default=None, help="source identifier: DOI, URL, or short citation")
    p.add_argument("--tier", required=True, choices=sorted(TIER_BASE), help="study design tier")
    p.add_argument("--n", type=int, default=None, help="sample size (participants, studies, or cases)")
    p.add_argument("--effect", default=None, help="reported effect, e.g. 'RR 0.8' or '-20 pct'")
    p.add_argument(
        "--recency",
        type=int,
        default=0,
        help="years since publication (0 = current/unknown; penalty starts after 2 years)",
    )
    p.add_argument(
        "--directness",
        choices=("direct", "indirect"),
        default="direct",
        help="indirect = surrogate outcome or different population than the decision",
    )
    p.add_argument(
        "--bias",
        choices=("low", "medium", "high"),
        default="low",
        help="overall bias risk from the checklist",
    )
    p.add_argument("--json", action="store_true", help="emit the scorecard row as JSON")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.n is not None and args.n < 0:
        print("error: --n must be non-negative", file=sys.stderr)
        return 2
    if args.recency < 0:
        print("error: --recency must be non-negative", file=sys.stderr)
        return 2
    row = appraise(args)
    if args.json:
        print(json.dumps(row, indent=2))
    else:
        print(human(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
