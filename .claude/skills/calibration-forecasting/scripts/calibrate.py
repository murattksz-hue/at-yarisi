#!/usr/bin/env python3
"""Score probabilistic forecasts: Brier score, calibration bins, skill score.

Log format (JSON array, or {"forecasts": [...]}):

    [
      {"id": 1, "prediction": "Ship by June", "p": 0.70, "o": 1,
       "resolves": "2026-06-30"},
      {"id": 2, "prediction": "No P1 incidents", "p": 0.60, "o": null}
    ]

`p` is the probability that the claim happens (0-1, or 0-100 as a percent).
`o` is 1 if it happened, 0 if not, null/absent while unresolved.

Usage:
    calibrate.py --demo
    calibrate.py --demo --json
    calibrate.py --forecasts forecasts.json --markdown
    calibrate.py --score "80% ship on time => 1; 60% under budget"
    calibrate.py --add "Ship by June" --confidence 0.7
    calibrate.py --add "Ship by June" --confidence 0.7 --log my_forecasts.json
    calibrate.py --resolve 3 --outcome 0

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

BIN_EDGES = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
DEFAULT_LOG = "forecasts.json"

DEMO = [
    {"id": 1, "prediction": "Migration ships to prod by 2026-06-30", "p": 0.90, "o": 1},
    {"id": 2, "prediction": "p95 latency stays under 200 ms after launch", "p": 0.85, "o": 1},
    {"id": 3, "prediction": "No rollback needed in first two weeks", "p": 0.80, "o": 0},
    {"id": 4, "prediction": "Fewer than 2 P1 incidents post-launch", "p": 0.75, "o": 1},
    {"id": 5, "prediction": "Runbook reviewed before cutover", "p": 0.70, "o": 1},
    {"id": 6, "prediction": "On-call handover completed on day one", "p": 0.65, "o": 0},
    {"id": 7, "prediction": "Cost increase under 10%", "p": 0.60, "o": 1},
    {"id": 8, "prediction": "Dashboards migrated without rework", "p": 0.55, "o": 0},
    {"id": 9, "prediction": "Team requests a second sprint for cleanup", "p": 0.40, "o": 0},
    {"id": 10, "prediction": "A dependency upgrade lands in the same release", "p": 0.30, "o": 1},
]


def normalize_p(value) -> float:
    p = float(value)
    if p > 1.0:
        p = p / 100.0
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"probability out of range: {value}")
    return p


def is_resolved(o) -> bool:
    return o is not None and o != "" and str(o).lower() not in {"null", "none"}


def outcome_value(o) -> int:
    if isinstance(o, str):
        o = o.strip().lower()
        if o in {"1", "true", "yes", "y", "hit", "happened"}:
            return 1
        if o in {"0", "false", "no", "n", "miss", "didn't"}:
            return 0
        raise ValueError(f"cannot read outcome {o!r}; use 1 or 0")
    return 1 if float(o) >= 0.5 else 0


def load_forecasts(source: str):
    """Load from a JSON file, or parse an inline spec like '80% x => 1; 60% y'."""
    path = Path(source)
    if path.is_file():
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            data = data.get("forecasts", [])
        if not isinstance(data, list):
            raise ValueError(f"{path}: expected a JSON array of forecasts")
        return data
    if "%" in source or "=>" in source:
        return parse_inline(source)
    raise FileNotFoundError(f"no such forecast file: {source}")


def parse_inline(spec: str):
    """Parse '80% claim happened => 1; 60% other claim' into forecast dicts."""
    out = []
    for i, chunk in enumerate(spec.split(";"), start=1):
        chunk = chunk.strip()
        if not chunk:
            continue
        m = re.match(r"^(?:p\s*=\s*)?(\d+(?:\.\d+)?)\s*%\s*(.*)$", chunk)
        if not m:
            raise ValueError(
                f"cannot parse forecast {chunk!r}; expected 'NN% claim text [=> 0|1]'"
            )
        p = normalize_p(m.group(1))
        rest = m.group(2).strip()
        o = None
        if "=>" in rest:
            rest, raw = rest.rsplit("=>", 1)
            rest = rest.strip()
            o = outcome_value(raw.strip())
        out.append({"id": i, "prediction": rest or "(unnamed)", "p": p, "o": o})
    if not out:
        raise ValueError("no forecasts found in inline spec")
    return out


def bin_index(p: float) -> int:
    for i in range(len(BIN_EDGES) - 1):
        if p < BIN_EDGES[i + 1]:
            return i
    return len(BIN_EDGES) - 2


def score(rows):
    resolved = []
    for row in rows:
        o = row.get("o")
        if not is_resolved(o):
            continue
        p = normalize_p(row["p"])
        y = outcome_value(o)
        resolved.append({"row": row, "p": p, "o": y, "brier": (p - y) ** 2})

    n = len(resolved)
    if n == 0:
        return {
            "n": len(rows),
            "n_resolved": 0,
            "n_unresolved": len(rows),
            "brier": None,
            "skill": None,
            "mean_p": None,
            "observed_rate": None,
            "bias": None,
            "bins": [],
            "forecasts": [],
        }

    brier = sum(r["brier"] for r in resolved) / n
    mean_p = sum(r["p"] for r in resolved) / n
    base = sum(r["o"] for r in resolved) / n
    baseline_brier = base * (1.0 - base)
    skill = 1.0 - brier / baseline_brier if baseline_brier > 0 else None

    buckets = [[] for _ in range(len(BIN_EDGES) - 1)]
    for r in resolved:
        buckets[bin_index(r["p"])].append(r)

    bins = []
    for i, group in enumerate(buckets):
        if not group:
            continue
        f = sum(r["p"] for r in group) / len(group)
        obs = sum(r["o"] for r in group) / len(group)
        bins.append(
            {
                "range": f"{BIN_EDGES[i]:.1f}-{BIN_EDGES[i + 1]:.1f}",
                "n": len(group),
                "mean_p": round(f, 4),
                "observed": round(obs, 4),
                "gap": round(f - obs, 4),
            }
        )

    scored = []
    for r in resolved:
        scored.append(
            {
                "id": r["row"].get("id"),
                "prediction": r["row"].get("prediction", ""),
                "p": round(r["p"], 4),
                "o": r["o"],
                "brier": round(r["brier"], 4),
            }
        )

    return {
        "n": len(rows),
        "n_resolved": n,
        "n_unresolved": len(rows) - n,
        "brier": round(brier, 4),
        "skill": None if skill is None else round(skill, 4),
        "mean_p": round(mean_p, 4),
        "observed_rate": round(base, 4),
        "bias": round(mean_p - base, 4),
        "bins": bins,
        "forecasts": scored,
    }


def verdict(result) -> str:
    if not result["n_resolved"]:
        return "No resolved forecasts yet — resolve some before reading a score."
    if result["n_resolved"] < 10:
        return (
            f"Only {result['n_resolved']} resolved forecast(s): directional at best. "
            "Collect ~20 before trusting the curve."
        )
    if result["skill"] is not None and result["skill"] < 0:
        return "Worse than always predicting the base rate: confidence is unearned."
    if abs(result["bias"]) <= 0.05:
        return "Roughly calibrated in the aggregate; check per-bin gaps for offsets."
    if result["bias"] > 0:
        return f"Overconfident overall by {result['bias']:.2f} — forecast too high."
    return f"Underconfident overall by {abs(result['bias']):.2f} — forecast too low."


def to_markdown(result) -> str:
    lines = ["# Forecast score", ""]
    lines.append(
        f"- Resolved: **{result['n_resolved']}** / {result['n']} "
        f"({result['n_unresolved']} pending)"
    )
    if result["brier"] is not None:
        lines.append(f"- Brier score: **{result['brier']:.4f}** (lower is better, 0-1)")
        if result["skill"] is not None:
            lines.append(f"- Skill vs base rate: **{result['skill']:+.3f}**")
        lines.append(
            f"- Mean forecast {result['mean_p']:.2f} vs observed {result['observed_rate']:.2f} "
            f"(bias {result['bias']:+.2f})"
        )
    lines.append("")
    lines.append(verdict(result))
    lines.append("")
    lines.append("| ID | Prediction | p | o | Brier (p-o)^2 |")
    lines.append("|---|---|---|---|---|")
    for f in result["forecasts"]:
        lines.append(
            f"| {f['id']} | {f['prediction']} | {f['p']:.2f} | {f['o']} | {f['brier']:.4f} |"
        )
    if result["bins"]:
        lines.append("")
        lines.append("| Confidence bin | n | Mean p | Observed | Gap |")
        lines.append("|---|---|---|---|---|")
        for b in result["bins"]:
            lines.append(
                f"| {b['range']} | {b['n']} | {b['mean_p']:.2f} | "
                f"{b['observed']:.2f} | {b['gap']:+.2f} |"
            )
        lines.append("")
        lines.append("Positive gap = overconfident in that bin.")
    return "\n".join(lines)


def write_log(path: Path, rows) -> None:
    path.write_text(json.dumps(rows, indent=2) + "\n")


def read_log(path: Path):
    if path.is_file():
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            data = data.get("forecasts", [])
        return data
    return []


def cmd_add(args) -> int:
    if args.confidence is None:
        print("--add requires --confidence (e.g. 0.7 or 70)", file=sys.stderr)
        return 2
    p = normalize_p(args.confidence)
    log = Path(args.log or args.forecasts or DEFAULT_LOG)
    rows = read_log(log)
    next_id = 1 + max([int(r.get("id", 0)) for r in rows], default=0)
    entry = {
        "id": next_id,
        "prediction": args.add,
        "p": round(p, 4),
        "o": None,
        "added": date.today().isoformat(),
    }
    if args.resolves:
        entry["resolves"] = args.resolves
    rows.append(entry)
    write_log(log, rows)
    if args.json:
        print(json.dumps(entry, indent=2))
    else:
        print(f"Added #{next_id} to {log}: p={entry['p']:.2f} — {entry['prediction']}")
        print(f"{len(rows)} forecast(s) in log; {sum(is_resolved(r.get('o')) for r in rows)} resolved.")
    return 0


def cmd_resolve(args) -> int:
    if args.outcome is None:
        print("--resolve requires --outcome 0 or 1", file=sys.stderr)
        return 2
    log = Path(args.log or args.forecasts or DEFAULT_LOG)
    rows = read_log(log)
    for row in rows:
        if str(row.get("id")) == str(args.resolve):
            row["o"] = outcome_value(args.outcome)
            row["resolved"] = date.today().isoformat()
            write_log(log, rows)
            print(f"Resolved #{row['id']}: o={row['o']} — {row.get('prediction', '')}")
            return 0
    print(f"No forecast with id {args.resolve} in {log}", file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Score forecasts with the Brier score and a calibration curve.",
        epilog=(
            "Inline specs: --score '80% ship on time => 1; 60% under budget'. "
            "Log format: JSON array of {prediction, p, o} where p is 0-1 (or a percent) "
            "and o is 1/0/null."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--forecasts", metavar="FILE|SPEC",
                        help="JSON forecast file, or an inline 'NN%% text [=> 0|1]' spec")
    parser.add_argument("--add", metavar="PREDICTION",
                        help="append a forecast to the log")
    parser.add_argument("--confidence", type=float, metavar="P",
                        help="probability for --add (0-1, or 0-100 percent)")
    parser.add_argument("--resolve", metavar="ID", help="mark forecast ID as resolved")
    parser.add_argument("--outcome", metavar="0|1", help="outcome for --resolve")
    parser.add_argument("--resolves", metavar="DATE",
                        help="resolution date to record with --add")
    parser.add_argument("--log", metavar="FILE",
                        help=f"log file for --add/--resolve (default ./{DEFAULT_LOG})")
    parser.add_argument("--score", action="store_true",
                        help="score the forecasts given by --forecasts")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--markdown", action="store_true", help="emit markdown")
    parser.add_argument("--demo", action="store_true", help="score a built-in 10-forecast demo")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if args.demo:
            rows = DEMO
        elif args.add:
            return cmd_add(args)
        elif args.resolve:
            return cmd_resolve(args)
        elif args.forecasts:
            rows = load_forecasts(args.forecasts)
        else:
            print("Nothing to score. Try --demo, --forecasts FILE, or --help.", file=sys.stderr)
            return 2

        result = score(rows)
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(to_markdown(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
