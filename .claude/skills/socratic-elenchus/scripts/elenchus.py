#!/usr/bin/env python3
"""Socratic elenchus probe generator.

Given a term and its current definition, emit a probe set: definition tests,
counterexample hunts, an operationalization checklist, and a falsifiable test.
Standard library only; no network.

Usage:
    python elenchus.py --term "engagement" --definition "users like the product"
    python elenchus.py --term "engagement" --definition "..." \
        --counterexample "daily opens driven by notifications" --json
"""
from __future__ import annotations

import argparse
import json
import re

VAGUE_TERMS = {
    "like", "likes", "love", "loves", "good", "better", "best", "quality",
    "value", "nice", "effective", "successful", "significant", "meaningful",
    "appropriate", "reasonable", "real", "true", "important", "often",
    "soon", "fast", "slow", "large", "small", "many", "few", "some",
    "stuff", "things", "etc",
}

MEASURE_HINTS = (
    "count", "number", "rate", "percent", "%", "per ", "within", "days",
    "weeks", "months", "hours", "minutes", "score", "ratio", "share",
    "frequency", "duration", "average", "median", "at least", "threshold",
)

OPERATIONAL_CHECKS = [
    "Indicator: which observable, recorded event counts as one unit of the term?",
    "Instrument: how is it measured — count, rate, duration, rating scale, or coded judgment?",
    "Threshold: what value separates present from absent, and who chose that number?",
    "Source: where does the data come from, and who could alter or game it?",
    "Baseline: compared with what reference period or comparison group?",
    "Inter-rater: would two independent observers code the same case identically?",
    "Disconfirming observation: what observation would count against the term applying?",
    "Goodhart guard: if someone optimized this indicator directly, what would degrade?",
]


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", text))


def analyze(term: str, definition: str) -> dict:
    low_def = definition.lower()
    low_term = term.lower()
    words = re.findall(r"[a-z']+", low_def)
    vague = sorted({w for w in words if w in VAGUE_TERMS})
    has_measure = bool(re.search(r"\d", definition)) or any(
        h in low_def for h in MEASURE_HINTS
    )
    circular = low_term in low_def
    notes: list[str] = []
    if circular:
        notes.append(
            f"Circular: the definition contains '{term}', so it cannot fix the referent."
        )
    if vague:
        notes.append(
            "Vague or evaluative words with no criterion: "
            + ", ".join(f"'{w}'" for w in vague)
            + "."
        )
    if not has_measure:
        notes.append(
            "No measurable clause: nothing here says how to observe or count the term."
        )
    if word_count(definition) < 5:
        notes.append("Very short definition: likely a label, not a criterion.")
    return {
        "circular": circular,
        "vague_terms": vague,
        "has_measurable_clause": has_measure,
        "word_count": word_count(definition),
        "notes": notes,
    }


def definition_tests(term: str, definition: str) -> list[dict]:
    return [
        {
            "probe": "Clear case",
            "question": f"What is an uncontroversial case of {term}? State it without using the word.",
            "targets": "anchors the concept",
        },
        {
            "probe": "Substitution",
            "question": (
                f"Replace '{term}' with '{definition}' in the original sentence. "
                "Does the sentence still make the same claim?"
            ),
            "targets": "definition fits actual use",
        },
        {
            "probe": "Two-appliers",
            "question": (
                "Could two informed people apply this definition to the same case "
                "and reach different verdicts? Where exactly does it underdetermine?"
            ),
            "targets": "precision",
        },
        {
            "probe": "Necessary clauses",
            "question": (
                "Remove each clause of the definition in turn. Which removal changes "
                "which cases? Every clause should earn its place."
            ),
            "targets": "too broad / redundant criteria",
        },
        {
            "probe": "Category check",
            "question": (
                f"Is {term} a thing, a process, a judgment, or a quantity? "
                "Does the definition's head noun match that category?"
            ),
            "targets": "category error",
        },
        {
            "probe": "Alternative concept",
            "question": (
                f"Name a rival definition of {term} from another tradition or domain. "
                "What would change in the conclusion if it were adopted?"
            ),
            "targets": "conceptual lock-in",
        },
    ]


def counterexample_probes(term: str, definition: str, provided: str | None) -> list[dict]:
    probes: list[dict] = []
    if provided:
        probes.append(
            {
                "probe": "Reported counterexample",
                "question": (
                    f"You reported: '{provided}'. Does the definition classify it correctly? "
                    "If not, which clause broke — and is the clause necessary?"
                ),
                "targets": "known failure",
            }
        )
    probes.extend(
        [
            {
                "probe": "False positive",
                "question": (
                    f"What satisfies '{definition}' but is clearly not {term}? "
                    "This tests whether the definition is too broad."
                ),
                "targets": "too broad",
            },
            {
                "probe": "False negative",
                "question": (
                    f"What is clearly {term} but fails the definition? "
                    "This tests whether the definition is too narrow."
                ),
                "targets": "too narrow",
            },
            {
                "probe": "Boundary case",
                "question": (
                    f"Give a case reasonable people would split on for {term}. "
                    "What single feature decides it?"
                ),
                "targets": "missing criterion",
            },
            {
                "probe": "Contrast case",
                "question": (
                    f"What is the nearest thing that is not {term}? "
                    "State the minimal difference."
                ),
                "targets": "missing differentiator",
            },
            {
                "probe": "Scaling case",
                "question": (
                    f"Double the quantity involved. Does {term} double, plateau, or disappear? "
                    "If it cannot scale, is it a category rather than a degree?"
                ),
                "targets": "scalar vs categorical",
            },
            {
                "probe": "Degenerate case",
                "question": (
                    f"What happens at zero, negative, or extreme values? "
                    "Does the definition still classify sensibly?"
                ),
                "targets": "undefined limits",
            },
            {
                "probe": "Adversarial case",
                "question": (
                    f"What counterexample would the most informed skeptic offer against {term}?"
                ),
                "targets": "confirmation bias",
            },
            {
                "probe": "Cross-context case",
                "question": (
                    f"Apply the definition in a different setting or population. "
                    f"Does {term} still hold, or did the definition smuggle in context?"
                ),
                "targets": "overgeneralization",
            },
        ]
    )
    return probes


def build(term: str, definition: str, counterexample: str | None) -> dict:
    diagnostics = analyze(term, definition)
    revision_prompt = (
        f"Restate {term} as: a <category> that <differentiator>, with at least one "
        "checkable clause. If the probes revealed two distinct senses, split the term "
        "into two definitions and say which one the argument needs."
    )
    operational_prompt = (
        f"Define {term} operationally: name the indicator, unit, threshold, data source, "
        "and baseline window. Then state the observation that would count against it."
    )
    return {
        "term": term,
        "initial_definition": definition,
        "definition_type_prompt": (
            "Classify the definition: ostensive (examples), reportive (actual usage), "
            "stipulative (declared for a purpose), or persuasive (embeds the conclusion)."
        ),
        "diagnostics": diagnostics,
        "elenchus_chain": [
            "definition",
            "counterexample",
            "revision",
            "operational definition + test",
        ],
        "definition_tests": definition_tests(term, definition),
        "counterexample_probes": counterexample_probes(term, definition, counterexample),
        "revision": {
            "prompt": revision_prompt,
            "template": (
                f"{term} is a <category> that <differentiator>; "
                "it is present when <checkable clause>."
            ),
        },
        "operational_definition": {
            "prompt": operational_prompt,
            "checklist": OPERATIONAL_CHECKS,
            "template": (
                f"{term} = <indicator> measured as <unit> over <window>, "
                "present when <threshold>; source <source>; baseline <baseline>."
            ),
        },
        "test": {
            "prompt": (
                f"If {term} is really present, what should we observe? "
                "What observation would count against it?"
            ),
            "prediction": f"If {term}, then <observation>.",
            "falsifier": f"<observation> would count against {term} being present.",
        },
        "provided_counterexample": counterexample,
        "next_step": (
            "Answer the false-positive and false-negative probes first; they decide "
            "whether to narrow, widen, or split the definition."
        ),
    }


def render_markdown(result: dict) -> str:
    lines = [
        f"# Elenchus probes: {result['term']}",
        "",
        f"**Initial definition:** \"{result['initial_definition']}\"",
        "",
        f"**Type check:** {result['definition_type_prompt']}",
        "",
        "## Diagnostics",
        "",
    ]
    diag = result["diagnostics"]
    flags = []
    flags.append("circular" if diag["circular"] else "not circular")
    flags.append(
        "has a measurable clause" if diag["has_measurable_clause"] else "no measurable clause"
    )
    lines.append(
        f"- {diag['word_count']} words; {flags[0]}; {flags[1]}."
    )
    if diag["vague_terms"]:
        lines.append("- Vague terms: " + ", ".join(diag["vague_terms"]))
    for note in diag["notes"]:
        lines.append(f"- {note}")
    lines += ["", "## Definition tests", ""]
    for p in result["definition_tests"]:
        lines.append(f"- **{p['probe']}:** {p['question']}")
    lines += ["", "## Counterexample probes", ""]
    for p in result["counterexample_probes"]:
        lines.append(f"- **{p['probe']}:** {p['question']}")
    lines += ["", "## Revision", "", result["revision"]["prompt"], "", "```",
              result["revision"]["template"], "```"]
    lines += ["", "## Operational definition", "", result["operational_definition"]["prompt"], ""]
    for item in result["operational_definition"]["checklist"]:
        lines.append(f"- {item}")
    lines += ["", "```", result["operational_definition"]["template"], "```"]
    lines += ["", "## Test", "", result["test"]["prompt"], "",
              f"- Prediction: {result['test']['prediction']}",
              f"- Falsifier: {result['test']['falsifier']}"]
    lines += ["", "## Next step", "", result["next_step"], ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Socratic elenchus probes for a contested term."
    )
    parser.add_argument("--term", required=True, help="the term to clarify")
    parser.add_argument("--definition", required=True, help="its current definition, verbatim")
    parser.add_argument("--counterexample", default=None, help="a known counterexample, if any")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    args = parser.parse_args()

    result = build(args.term, args.definition, args.counterexample)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
