#!/usr/bin/env python3
"""Generate a steelman + red-team scaffold for a claim.

Builds the strongest counter-position template (with premises), five attack
vectors, and a falsification pre-commitment. The scaffold is a fill-in
structure, not an argument: the operator supplies the evidence.

Usage:
    python redteam.py --claim "Remote work hurts productivity"
    python redteam.py --claim "X" --position "Y" --vectors 3 --json

stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# Word-level opposites used to auto-derive a counter-position. Deliberately
# small: the auto-counter is a starting point the operator must sharpen.
OPPOSITES = {
    "hurts": "helps",
    "harms": "benefits",
    "reduces": "increases",
    "increases": "reduces",
    "decreases": "increases",
    "improves": "worsens",
    "worsens": "improves",
    "helps": "hurts",
    "causes": "does not cause",
    "prevents": "enables",
    "supports": "undermines",
    "undermines": "supports",
    "slows": "accelerates",
    "boosts": "depresses",
    "raises": "lowers",
    "lowers": "raises",
    "leads to": "does not lead to",
    "drives": "does not drive",
    "is": "is not",
    "are": "are not",
    "was": "was not",
    "were": "were not",
    "will": "will not",
    "would": "would not",
    "can": "cannot",
    "could": "could not",
    "should": "should not",
    "must": "need not",
    "does": "does not",
    "do": "do not",
    "has": "lacks",
    "have": "lack",
}

CONTRACTIONS = {
    "doesn't": "does not",
    "don't": "do not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "won't": "will not",
    "wouldn't": "would not",
    "shouldn't": "should not",
    "couldn't": "could not",
    "can't": "cannot",
    "hasn't": "has not",
    "haven't": "have not",
    "didn't": "did not",
}

AUX_NOT = re.compile(
    r"\b(is|are|was|were|does|do|did|will|would|should|must|can|could|has|have)"
    r"\s+not\b",
    re.I,
)

VECTORS = [
    {
        "id": "evidence",
        "vector": "Evidence",
        "question": (
            "Which empirical link in '{claim}' is weakest, and what would a "
            "well-identified study in the opposite direction look like?"
        ),
        "what_would_count": (
            "A larger-N, better-identified or pre-registered result that "
            "contradicts the best current evidence."
        ),
        "fix_hint": "Cite the study that most undermines the claim and say why it wins.",
    },
    {
        "id": "logic",
        "vector": "Logic",
        "question": (
            "Does the counter-position follow, and does '{claim}' rest on an "
            "unstated premise, an ambiguous term, or correlation-as-cause?"
        ),
        "what_would_count": (
            "A missing warrant that, once stated explicitly, is false or "
            "unsupported; or a term used in two senses."
        ),
        "fix_hint": "State the unstated warrant, then test it separately.",
    },
    {
        "id": "incentives",
        "vector": "Incentives",
        "question": (
            "Who benefits if '{claim}' is believed, and how might that shape "
            "the evidence or the framing you are relying on?"
        ),
        "what_would_count": (
            "Documented funding, career, commercial, or ideological interest "
            "in the conclusion, with a plausible path to biased evidence."
        ),
        "fix_hint": "Name the interest and the specific evidence it could distort.",
    },
    {
        "id": "alternative-explanation",
        "vector": "Alternative explanation",
        "question": (
            "What else produces the observation behind '{claim}' — selection, "
            "regression to the mean, confounding, reverse causation?"
        ),
        "what_would_count": (
            "A rival mechanism that predicts the same observations more "
            "simply, or a stratification that makes the effect disappear."
        ),
        "fix_hint": "Give one rival mechanism with equal or better fit.",
    },
    {
        "id": "cost",
        "vector": "Cost",
        "question": (
            "If '{claim}' is wrong, what does it cost in money, optionality, "
            "trust, or irreversibility?"
        ),
        "what_would_count": (
            "A downside that is large or hard to reverse relative to the "
            "claimed benefit."
        ),
        "fix_hint": "Price the downside or make the decision reversible.",
    },
]


def clean(text: str) -> str:
    def expand(m: re.Match) -> str:
        return CONTRACTIONS.get(m.group(0).lower(), m.group(0))

    text = re.sub(
        r"\b(?:doesn't|don't|isn't|aren't|wasn't|weren't|won't|wouldn't|shouldn't"
        r"|couldn't|can't|hasn't|haven't|didn't)\b",
        expand,
        text,
        flags=re.I,
    )
    return re.sub(r"\s+", " ", text.strip()).rstrip(".")


def derive_counter_position(claim: str) -> str:
    """Best-effort opposite of a claim. Always flagged as auto-derived."""
    match = AUX_NOT.search(claim)
    if match:
        # Drop the negation but keep the auxiliary ("does not hurt" -> "does hurt").
        return claim[: match.start()] + match.group(1) + claim[match.end() :]
    for neg in (r"\bnever\s+", r"\bno longer\s+"):
        if re.search(neg, claim, re.I):
            return re.sub(neg, "", claim, count=1, flags=re.I)
    for word in re.findall(r"[a-zA-Z']+(?:\s+to)?", claim):
        key = word.lower()
        if key in OPPOSITES:
            pattern = r"\b" + re.escape(word) + r"\b"
            return re.sub(pattern, OPPOSITES[key], claim, count=1, flags=re.I)
    return f"It is not the case that {claim}"


def build(claim: str, position: str | None, n_vectors: int) -> dict:
    if position:
        counter, derivation = clean(position), "supplied by operator"
    else:
        counter = derive_counter_position(claim)
        derivation = "auto-derived — sharpen until a proponent would sign it"

    steelman = {
        "thesis": counter,
        "derivation": derivation,
        "premises": [
            {
                "id": "S1",
                "kind": "empirical",
                "premise": (
                    "The strongest available evidence on this question measures "
                    "___ and finds ___, which the claim's account does not predict."
                ),
                "status": "unverified — fill with the best supporting study",
            },
            {
                "id": "S2",
                "kind": "mechanism",
                "premise": (
                    "There is a credible causal channel (___) by which the "
                    "counter-position holds, and the claim ignores or "
                    "underweights it."
                ),
                "status": "unverified — name the mechanism",
            },
            {
                "id": "S3",
                "kind": "scope",
                "premise": (
                    "The evidence behind the claim comes from ___, which does "
                    "not generalize to ___ because ___."
                ),
                "status": "unverified — specify population, period, setting",
            },
            {
                "id": "S4",
                "kind": "tradeoff",
                "premise": (
                    "Even where the claim holds narrowly, the costs (___) "
                    "outweigh the benefit because ___."
                ),
                "status": "unverified — quantify if possible",
            },
        ],
        "concession_owed": (
            "One sub-point on which the counter-position is right and the "
            "claim must give ground — be specific."
        ),
        "charity_test": (
            "Would a smart proponent of the counter-position sign this "
            "steelman as fair? If not, revise before attacking."
        ),
    }

    attacks = []
    for template in VECTORS[:n_vectors]:
        attacks.append(
            {
                "id": template["id"],
                "vector": template["vector"],
                "question": template["question"].format(claim=claim),
                "what_would_count": template["what_would_count"],
                "strongest_hit": "",
                "severity": "unrated (fatal / serious / survivable)",
                "fix_hint": template["fix_hint"],
            }
        )

    falsifier = {
        "abandon_claim_if": [
            (
                "A pre-specified test measuring the outcome implied by "
                f"'{claim}' shows the opposite direction at the stated "
                "threshold (effect ___, confidence ___)."
            ),
            (
                "The mechanism the claim depends on (___) is shown absent "
                "under conditions where the claim says it must operate."
            ),
            (
                "A higher-quality study (larger N, better identification, "
                "replication) contradicts the best current evidence."
            ),
        ],
        "threshold": "state effect size and confidence level before checking",
        "deadline": "state a date",
        "rationalization_trap": (
            "The excuse you will be most tempted to use to explain away a "
            "disconfirming result — decide now whether it would be legitimate."
        ),
        "template": (
            f"I abandon \"{claim}\" if ___ (observable threshold) by ___ "
            "(date), and I name now the result I would be tempted to explain "
            "away: ___."
        ),
        "confidence_now": None,
        "confidence_if_falsified": None,
    }

    return {
        "claim": claim,
        "steelman": steelman,
        "attack_vectors": attacks,
        "falsifier": falsifier,
    }


def render_markdown(data: dict) -> str:
    sm = data["steelman"]
    lines = [
        f"# Steelman + Red-Team: {data['claim']}",
        "",
        f"**Your claim (P):** {data['claim']}",
        "",
        f"**Steelman, strongest counter-position (¬P):** {sm['thesis']}",
        "",
        f"_{sm['derivation']}_",
        "",
        "## Steelman premises",
        "",
    ]
    for p in sm["premises"]:
        lines.append(f"{p['id']} ({p['kind']}). {p['premise']}")
        lines.append(f"    status: {p['status']}")
    lines += [
        "",
        "## Concession owed",
        "",
        sm["concession_owed"],
        "",
        f"**Charity test:** {sm['charity_test']}",
        "",
        "## Attack vectors",
        "",
        "| # | Vector | Question | Strongest hit | Severity |",
        "|---|---|---|---|---|",
    ]
    for v in data["attack_vectors"]:
        q = v["question"].replace("|", "\\|")
        lines.append(
            f"| {v['id']} | {v['vector']} | {q} | "
            f"{v['strongest_hit'] or '___'} | {v['severity']} |"
        )
        lines.append(f"| | | _{v['fix_hint']}_ | | |")

    f = data["falsifier"]
    lines += ["", "## Falsification pre-commit", "", "I abandon P if:"]
    for item in f["abandon_claim_if"]:
        lines.append(f"- {item}")
    lines += [
        "",
        f"- Threshold: {f['threshold']}",
        f"- Check by: {f['deadline']}",
        f"- Rationalization trap: {f['rationalization_trap']}",
        "",
        f"**Template:** {f['template']}",
        "",
        "**Confidence now:** ___ / 100  →  "
        "**if falsifier observed:** ___ / 100",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a steelman + red-team scaffold for a claim."
    )
    parser.add_argument("--claim", required=True, help="the claim you hold (P)")
    parser.add_argument(
        "--position",
        default=None,
        help="the rival position; omit to auto-derive the opposite of --claim",
    )
    parser.add_argument(
        "--vectors",
        type=int,
        default=5,
        help="number of attack vectors to include (default 5, range 1-5)",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    args = parser.parse_args(argv)

    if not clean(args.claim):
        parser.error("--claim must not be empty")
    if args.position is not None and not clean(args.position):
        parser.error("--position must not be empty when supplied")
    n_vectors = max(1, min(5, args.vectors))

    data = build(args.claim, args.position, n_vectors)
    print(json.dumps(data, indent=2) if args.json else render_markdown(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
