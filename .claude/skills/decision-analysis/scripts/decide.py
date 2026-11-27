#!/usr/bin/env python3
"""Expected-value decision sheet with optional probability sensitivity sweep.

Compute EV(option) = sum(p_outcome * utility), rank options, and (with
--sensitivity) sweep each outcome probability +/-20%, redistributing the
remaining mass proportionally, to see which assumption drives the ranking.

Usage:
    decide.py --options "Ship,Wait" --outcomes "hit,miss" \
              --probs "0.6,0.4" --utilities "100,0;20,20" --json
    decide.py --file decision.json --sensitivity

JSON input shape (list or dict form for options):
    {"outcomes": ["hit", "miss"],
     "probs": [0.6, 0.4],
     "options": [{"name": "Ship", "utilities": [100, 0]},
                 {"name": "Wait", "utilities": [20, 20]}]}
    # or "options": {"Ship": [100, 0], "Wait": [20, 20]}
    # or per-option utilities keyed by outcome: {"hit": 100, "miss": 0}
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

SWEEP = 0.20  # +/-20% relative perturbation on one probability


def parse_list(raw: str, label: str) -> list[str]:
    items = [part.strip() for part in raw.split(",")]
    if not items or any(not item for item in items):
        raise ValueError(f"{label} must be a non-empty comma-separated list")
    return items


def parse_floats(raw: str, label: str) -> list[float]:
    values = []
    for item in parse_list(raw, label):
        try:
            values.append(float(item))
        except ValueError:
            raise ValueError(f"{label}: '{item}' is not a number") from None
    return values


def parse_utilities(raw: str, n_outcomes: int, n_options: int) -> list[list[float]]:
    rows = [row.strip() for row in raw.split(";") if row.strip()]
    if len(rows) != n_options:
        raise ValueError(
            f"--utilities has {len(rows)} row(s); expected one per option ({n_options})"
        )
    utilities = []
    for i, row in enumerate(rows, 1):
        values = parse_floats(row, f"utilities row {i}")
        if len(values) != n_outcomes:
            raise ValueError(
                f"utilities row {i} has {len(values)} value(s); "
                f"expected one per outcome ({n_outcomes})"
            )
        utilities.append(values)
    return utilities


def load_file(path: str):
    try:
        data = json.loads(Path(path).read_text())
    except OSError as exc:
        raise ValueError(f"cannot read {path}: {exc}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from None

    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    outcomes = data.get("outcomes")
    if not isinstance(outcomes, list) or not outcomes:
        raise ValueError("JSON needs a non-empty 'outcomes' list")
    outcomes = [str(o) for o in outcomes]

    probs = data.get("probs", data.get("probabilities"))
    if not isinstance(probs, list):
        raise ValueError("JSON needs a 'probs' list")
    probs = [float(p) for p in probs]

    raw_options = data.get("options")
    names: list[str] = []
    utilities: list[list[float]] = []

    def add_option(name, utils):
        name = str(name)
        if name in names:
            raise ValueError(f"duplicate option name: {name}")
        if isinstance(utils, dict):
            missing = [o for o in outcomes if o not in utils]
            if missing:
                raise ValueError(f"option '{name}' missing outcomes: {', '.join(missing)}")
            utils = [float(utils[o]) for o in outcomes]
        utils = [float(u) for u in utils]
        if len(utils) != len(outcomes):
            raise ValueError(
                f"option '{name}' has {len(utils)} utilities; expected {len(outcomes)}"
            )
        names.append(name)
        utilities.append(utils)

    if isinstance(raw_options, dict):
        for name, utils in raw_options.items():
            add_option(name, utils)
    elif isinstance(raw_options, list):
        for item in raw_options:
            if isinstance(item, dict):
                if "name" not in item:
                    raise ValueError("each option object needs a 'name'")
                utils = item.get("utilities", item.get("utils"))
                if utils is None:
                    raise ValueError(f"option '{item['name']}' needs 'utilities'")
                add_option(item["name"], utils)
            elif isinstance(item, (list, tuple)) and len(item) == 2:
                add_option(item[0], item[1])
            else:
                raise ValueError("options must be objects, [name, utilities] pairs, or a mapping")
    else:
        raise ValueError("JSON needs an 'options' list or mapping")

    if not names:
        raise ValueError("JSON has no options")
    return outcomes, probs, names, utilities


def validate(outcomes, probs, names, utilities):
    if len(probs) != len(outcomes):
        raise ValueError(
            f"{len(probs)} probabilities for {len(outcomes)} outcomes; counts must match"
        )
    notes = []
    if any(not math.isfinite(p) or p < 0 for p in probs):
        raise ValueError("probabilities must be finite and non-negative")
    total = sum(probs)
    if total <= 0:
        raise ValueError("probabilities sum to zero")
    if not math.isclose(total, 1.0, abs_tol=1e-6):
        probs = [p / total for p in probs]
        notes.append(f"probabilities summed to {total:.6g}; normalized to 1")
    for utils in utilities:
        if any(not math.isfinite(u) for u in utils):
            raise ValueError("utilities must be finite numbers")
        if len(utils) != len(outcomes):
            raise ValueError("each option needs one utility per outcome")
    if not names:
        raise ValueError("at least one option is required")
    return probs, notes


def expected_values(probs, utilities):
    return [sum(p * u for p, u in zip(probs, utils)) for utils in utilities]


def sweep(probs, outcomes, names, utilities):
    entries = []
    for j, (name, p) in enumerate(zip(outcomes, probs)):
        low = max(0.0, p * (1 - SWEEP))
        high = min(1.0, p * (1 + SWEEP))
        others_total = 1.0 - p
        per_option = {}
        for label, value in (("low", low), ("high", high)):
            variant = list(probs)
            variant[j] = value
            if others_total > 0:
                scale = (1.0 - value) / others_total
                for k in range(len(variant)):
                    if k != j:
                        variant[k] *= scale
            else:
                variant[j] = 1.0
            per_option[label] = expected_values(variant, utilities)

        option_rows = {}
        for i, option in enumerate(names):
            ev_low, ev_high = per_option["low"][i], per_option["high"][i]
            option_rows[option] = {
                "ev_low": round(ev_low, 6),
                "ev_high": round(ev_high, 6),
                "swing": round(abs(ev_high - ev_low), 6),
            }

        best_low = names[per_option["low"].index(max(per_option["low"]))]
        best_high = names[per_option["high"].index(max(per_option["high"]))]
        entries.append(
            {
                "outcome": name,
                "p": round(p, 6),
                "p_low": round(low, 6),
                "p_high": round(high, 6),
                "options": option_rows,
                "best_low": best_low,
                "best_high": best_high,
                "flips": best_low != best_high,
            }
        )
    return entries


def render_markdown(result):
    outcomes = result["outcomes"]
    probs = result["probabilities"]
    header = "| Option | " + " | ".join(
        f"{name} (p={p:.2f})" for name, p in zip(outcomes, probs)
    ) + " | EV | Rank |"
    sep = "|" + "---|" * (len(outcomes) + 3)
    lines = ["## Decision sheet", "", header, sep]
    for row in result["table"]:
        cells = " | ".join(f"{u:g}" for u in row["utilities"])
        lines.append(
            f"| {row['option']} | {cells} | {row['ev']:.2f} | {row['rank']} |"
        )
    lines.append("")
    runner_up = result.get("runner_up")
    if runner_up is None:
        margin = "n/a (single option)"
    else:
        margin = f"{result['margin']:.2f} over {runner_up}"
    verdict = "tie — margin is zero" if result["tie"] else "no tie at this precision"
    lines.append(f"**Recommendation:** {result['best']} (EV {result['best_ev']:.2f}; {margin}); {verdict}.")

    sensitivity = result.get("sensitivity")
    if sensitivity is not None:
        best = result["best"]
        ordered = sorted(sensitivity, key=lambda e: e["options"][best]["swing"], reverse=True)
        lines += [
            "",
            "## Sensitivity (±20% probability sweep)",
            "",
            f"| Outcome | p range | {best} EV low–high | Swing on {best} | Ranking flips? |",
            "|---|---|---|---|---|",
        ]
        for entry in ordered:
            row = entry["options"][best]
            lines.append(
                f"| {entry['outcome']} | {entry['p_low']:.2f}–{entry['p_high']:.2f} "
                f"| {row['ev_low']:.2f}–{row['ev_high']:.2f} | {row['swing']:.2f} "
                f"| {'YES' if entry['flips'] else 'no'} |"
            )
        lines += [
            "",
            f"**Rank stability:** {'stable' if result['rank_stable'] else 'FLIPS under sweep'}. "
            "Probe the largest swing first; ignore inputs whose swing cannot change the choice.",
        ]

    if result.get("notes"):
        lines += ["", "Notes: " + "; ".join(result["notes"])]
    return "\n".join(lines)


def build(args):
    if args.file:
        outcomes, probs, names, utilities = load_file(args.file)
    else:
        missing = [
            flag
            for flag, value in (
                ("--options", args.options),
                ("--outcomes", args.outcomes),
                ("--probs", args.probs),
                ("--utilities", args.utilities),
            )
            if not value
        ]
        if missing:
            raise ValueError("missing " + ", ".join(missing) + " (or use --file)")
        names = parse_list(args.options, "--options")
        outcomes = parse_list(args.outcomes, "--outcomes")
        probs = parse_floats(args.probs, "--probs")
        utilities = parse_utilities(args.utilities, len(outcomes), len(names))

    probs, notes = validate(outcomes, probs, names, utilities)
    evs = expected_values(probs, utilities)

    order = sorted(range(len(names)), key=lambda i: evs[i], reverse=True)
    ranking = [names[i] for i in order]
    table = []
    for rank, i in enumerate(order, 1):
        table.append(
            {
                "option": names[i],
                "utilities": utilities[i],
                "ev": round(evs[i], 6),
                "rank": rank,
            }
        )

    best_i = order[0]
    best_ev = evs[best_i]
    second_ev = evs[order[1]] if len(order) > 1 else None
    margin = round(best_ev - second_ev, 6) if second_ev is not None else None
    tie = second_ev is not None and math.isclose(best_ev, second_ev, abs_tol=1e-9)

    result = {
        "outcomes": outcomes,
        "probabilities": [round(p, 6) for p in probs],
        "table": table,
        "ranking": ranking,
        "best": names[best_i],
        "best_ev": round(best_ev, 6),
        "runner_up": names[order[1]] if len(order) > 1 else None,
        "margin": margin,
        "tie": tie,
        "notes": notes,
    }

    if args.sensitivity:
        entries = sweep(probs, outcomes, names, utilities)
        result["sensitivity"] = entries
        result["rank_stable"] = all(
            entry["best_low"] == names[best_i] and entry["best_high"] == names[best_i]
            for entry in entries
        )
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Expected-value decision sheet with optional ±20% sensitivity sweep.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--options", help='comma-separated option names, e.g. "Ship,Wait"')
    parser.add_argument("--outcomes", help='comma-separated outcome names, e.g. "hit,miss"')
    parser.add_argument("--probs", help='comma-separated probabilities, e.g. "0.6,0.4"')
    parser.add_argument(
        "--utilities",
        help='semicolon-separated rows, one per option, e.g. "100,0;20,20"',
    )
    parser.add_argument("--file", help="JSON input instead of the four flags")
    parser.add_argument(
        "--sensitivity",
        action="store_true",
        help="sweep each probability ±20%% and report EV ranges / rank stability",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    args = parser.parse_args(argv)

    try:
        result = build(args)
    except ValueError as exc:
        parser.error(str(exc))
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
