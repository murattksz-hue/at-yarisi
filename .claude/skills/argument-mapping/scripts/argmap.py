#!/usr/bin/env python3
"""Build a Toulmin argument map from prose or explicit slots.

Heuristic, stdlib-only. Use as a first pass; always review the labels.

Usage:
    argmap.py --text "All birds fly; penguins are birds; therefore penguins fly" --json
    argmap.py --claim "..." --grounds "..." --warrant "..." 
    argmap.py --text "..." --infer
"""
from __future__ import annotations

import argparse
import json
import re
import sys

CONCLUSION_RE = re.compile(
    r"\b(?:therefore|thus|hence|consequently|it follows that|which means|"
    r"proves that|ergo|so\b(?! that))[,:]?\s*",
    re.I,
)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+|\n+")
REBUTTAL_RE = re.compile(r"\b(?:unless|except|however|although|though|but|"
                         r"notwithstanding|counterexample)\b", re.I)
QUALIFIER_RE = re.compile(
    r"\b(probably|likely|unlikely|possibly|presumably|plausibly|perhaps|"
    r"certainly|definitely|clearly|apparently|in most cases|generally|"
    r"may|might|must|should)\b", re.I)
WARRANT_RE = re.compile(r"\b(?:all|every|any|whenever|always|never|no)\b"
                        r"|\bif\b.*\bthen\b", re.I)
BACKING_RE = re.compile(
    r"\b(?:according to|studies show|research shows|evidence suggests|"
    r"data show|data shows|as shown by|reported by)\b", re.I)
GROUNDS_RE = re.compile(r"\b(?:because|since|given that|as|for|evidence|"
                        r"data|observed|observed that|studies|research)\b", re.I)
CLAIM_CUE_RE = re.compile(
    r"\b(?:we should|i conclude|the answer is|clearly|obviously|must|"
    r"the point is|what matters is)\b", re.I)
DEDUCTIVE_RE = re.compile(r"\b(?:all|every|no|none|never|must|certainly)\b", re.I)
ABDUCTIVE_RE = re.compile(
    r"\b(?:best explanation|explains|explanation|consistent with|"
    r"must have|the cause is|hypothesis)\b", re.I)
INDUCTIVE_RE = re.compile(
    r"\b(?:most|typically|usually|generally|probably|likely|sample|"
    r"evidence|data|observed|past|pattern|trend)\b", re.I)
EXPLICIT_REBUTTAL_RE = re.compile(r"\b(?:unless|except|except when|"
                                  r"unless .*)\b", re.I)

SUPPLIED_WARRANTS = {
    "deductive": "If the grounds are true, the claim follows by logical form (supplied).",
    "inductive": "What has held in observed cases will probably hold in the next case (supplied).",
    "abductive": "The hypothesis that best explains the grounds is the one to accept (supplied).",
}

VERDICT_NOTES = {
    "deductive": "Valid form; soundness depends on the premises, not the form.",
    "inductive": "Strength depends on sample size, representativeness, and a mechanism.",
    "abductive": "Plausible only if rival explanations were considered and excluded.",
}


def split_sentences(text: str) -> list[str]:
    return [s.strip(" \t") for s in SENTENCE_RE.split(text.strip()) if s.strip()]


def split_conclusion(sentence: str):
    """Return (before, after) at the first conclusion marker, or None."""
    m = CONCLUSION_RE.search(sentence)
    if not m:
        return None
    before = sentence[: m.start()].strip(" ,;:")
    after = sentence[m.end():].strip(" ,;:")
    return before, after


def split_grounds(sentence: str) -> list[str]:
    parts = [p.strip(" ,;:") for p in re.split(r"[;]", sentence)]
    return [p for p in parts if p]


def first_match(regex: re.Pattern[str], text: str) -> str | None:
    m = regex.search(text)
    return m.group(0) if m else None


def detect_type(claim: str, grounds: list[str], warrant: str) -> str:
    blob = " ".join([claim, *grounds, warrant])
    if ABDUCTIVE_RE.search(blob):
        return "abductive"
    if DEDUCTIVE_RE.search(" ".join(grounds)) or re.search(
            r"\bif\b.*\bthen\b", warrant, re.I):
        return "deductive"
    if INDUCTIVE_RE.search(blob):
        return "inductive"
    return "unclear"


def infer(text: str, aggressive: bool) -> dict:
    """Heuristically label slots. `aggressive` enables cue-based claim picking."""
    sentences = split_sentences(text)
    grounds: list[str] = []
    claim = ""
    warrant = ""
    backing = ""
    qualifier = ""
    rebuttal = ""

    claim_idx = None
    claim_prefix = ""
    for i, sentence in enumerate(sentences):
        split = split_conclusion(sentence)
        if split:
            claim_prefix, claim = split
            claim_idx = i
            break

    if claim_idx is None and aggressive and sentences:
        # No explicit marker: use a claim cue, else the last sentence.
        for i, sentence in enumerate(sentences):
            if CLAIM_CUE_RE.search(sentence) and i > 0:
                claim, claim_idx = sentence, i
                break
        if claim_idx is None:
            claim, claim_idx = sentences[-1], len(sentences) - 1
    if claim_idx is None:
        claim = text.strip()

    for i, sentence in enumerate(sentences):
        if i < claim_idx:
            grounds.extend(split_grounds(sentence))
        elif i == claim_idx:
            if claim_prefix:
                grounds.extend(split_grounds(claim_prefix))
        else:
            if REBUTTAL_RE.search(sentence):
                rebuttal = (rebuttal + " " + sentence).strip()
            elif QUALIFIER_RE.search(sentence) and not qualifier:
                qualifier = REBUTTAL_RE.sub("", sentence).strip()
            elif BACKING_RE.search(sentence):
                backing = (backing + " " + sentence).strip()
            elif aggressive and WARRANT_RE.search(sentence):
                warrant = (warrant + " " + sentence).strip()
            else:
                grounds.extend(split_grounds(sentence))

    if not qualifier:
        q = first_match(QUALIFIER_RE, claim)
        if q:
            qualifier = q
    if not rebuttal:
        r = EXPLICIT_REBUTTAL_RE.search(text)
        if r:
            start = max(0, r.start() - 40)
            rebuttal = text[start: r.start() + 80].strip()

    return {
        "claim": claim,
        "grounds": grounds,
        "warrant": warrant,
        "backing": backing,
        "qualifier": qualifier,
        "rebuttal": rebuttal,
    }


def build_map(slots: dict, aggressive: bool) -> dict:
    inferred = infer(slots.get("text") or "", aggressive) if (
        slots.get("text") and not all(
            slots.get(k) for k in ("claim", "grounds", "warrant"))
    ) else {"claim": "", "grounds": [], "warrant": "", "backing": "",
            "qualifier": "", "rebuttal": ""}

    def pick(key: str):
        value = slots.get(key)
        if value:
            return value
        return inferred.get(key) or ""

    claim = pick("claim")
    raw_grounds = slots.get("grounds") or inferred.get("grounds") or []
    if isinstance(raw_grounds, str):
        grounds = split_grounds(raw_grounds)
    else:
        grounds = [g for g in raw_grounds if g]
    warrant = pick("warrant")
    backing = pick("backing")
    qualifier = pick("qualifier")
    rebuttal = pick("rebuttal")

    arg_type = detect_type(claim, grounds, warrant)
    missing = [name for name, value in (
        ("claim", claim), ("grounds", grounds), ("warrant", warrant),
    ) if not value]

    warrant_source = "stated" if warrant else "missing"
    if not warrant and claim and grounds and arg_type in SUPPLIED_WARRANTS:
        warrant = SUPPLIED_WARRANTS[arg_type]
        warrant_source = "supplied"

    if not claim:
        verdict, detail = "gap", "No identifiable claim."
    elif not grounds:
        verdict, detail = "gap", "No grounds supplied; the claim is unsupported."
    elif warrant_source == "missing":
        verdict, detail = "gap", "Warrant W needed: name the rule that licenses grounds -> claim."
    elif arg_type == "deductive":
        verdict, detail = "valid", VERDICT_NOTES["deductive"]
    else:
        verdict, detail = "plausible", VERDICT_NOTES.get(
            arg_type, "Check whether the warrant is true and adequately backed.")

    if qualifier and arg_type in ("deductive", "unclear") and qualifier.lower() in (
            "probably", "likely", "possibly", "perhaps", "plausibly"):
        detail += " Qualifier is weaker than the form; no defect."

    return {
        "claim": claim,
        "grounds": grounds,
        "warrant": warrant,
        "warrant_source": warrant_source,
        "backing": backing,
        "qualifier": qualifier,
        "rebuttal": rebuttal,
        "type": arg_type,
        "verdict": verdict,
        "verdict_detail": detail,
        "missing": missing,
    }


def esc(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def to_markdown(m: dict) -> str:
    grounds = "<br>".join(f"{i}. {esc(g)}" for i, g in enumerate(m["grounds"], 1)) or "_(none)_"
    rows = [
        ("Claim", m["claim"] or "_(none)_"),
        ("Grounds", grounds),
        ("Warrant", (m["warrant"] or "_(none)_") +
         (f" _({m['warrant_source']})_" if m["warrant"] else "")),
        ("Backing", m["backing"] or "_(none)_"),
        ("Qualifier", m["qualifier"] or "_(none)_"),
        ("Rebuttal", m["rebuttal"] or "_(none)_"),
    ]
    lines = ["# Argument map", "", "| Slot | Content |", "|---|---|"]
    lines += [f"| {slot} | {esc(value)} |" for slot, value in rows]
    lines += [
        "",
        f"**Type:** {m['type']}",
        f"**Verdict:** {m['verdict']}",
        f"**Note:** {m['verdict_detail']}",
    ]
    if m["missing"]:
        lines.append(f"**Missing:** {', '.join(m['missing'])}")
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Build a Toulmin argument map from prose or explicit slots.")
    p.add_argument("--text", default=None,
                   help="Argument text; use '-' to read stdin.")
    p.add_argument("--claim")
    p.add_argument("--grounds", help="Grounds, separated by ';'.")
    p.add_argument("--warrant")
    p.add_argument("--backing")
    p.add_argument("--qualifier")
    p.add_argument("--rebuttal")
    p.add_argument("--infer", action="store_true",
                   help="Aggressive heuristic span labelling (claim/grounds cues).")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    args = p.parse_args(argv)

    text = args.text
    if text == "-":
        text = sys.stdin.read()
    if not text and not any((args.claim, args.grounds, args.warrant, args.backing,
                             args.qualifier, args.rebuttal)):
        p.error("provide --text or at least one explicit slot")

    slots = {
        "text": text, "claim": args.claim, "grounds": args.grounds,
        "warrant": args.warrant, "backing": args.backing,
        "qualifier": args.qualifier, "rebuttal": args.rebuttal,
    }
    result = build_map(slots, args.infer)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json
          else to_markdown(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
