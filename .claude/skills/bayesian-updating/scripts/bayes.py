#!/usr/bin/env python3
"""Bayesian belief updating: prior -> likelihood ratio -> posterior.

Computes a posterior probability, its odds, and the Bayes factor. Supports
likelihood ratios given directly, or derived from a test's sensitivity and
specificity, or from hit rate and false-alarm rate. Handles sequential evidence
and reports a base-rate comparison.

Examples:
    bayes.py --prior 0.1 --lr 9 --json
    bayes.py --prior 0.01 --sensitivity 0.9 --specificity 0.8 --base-rate
    bayes.py --prior 0.2 --lrs "4,0.5,2"
    bayes.py --prior-odds 0.25 --lr 3:1 --base-rate --json

Stdlib only.
"""
import argparse
import json
import math
import sys


def parse_ratio(text: str) -> float:
    """Parse a positive likelihood ratio: '9', '9:1', or '9/1'."""
    raw = text.strip()
    if not raw:
        raise argparse.ArgumentTypeError("empty likelihood ratio")
    try:
        if ":" in raw:
            a, b = raw.split(":", 1)
            num, den = float(a), float(b)
        elif "/" in raw:
            a, b = raw.split("/", 1)
            num, den = float(a), float(b)
        else:
            value = float(raw)
            if not math.isfinite(value) or value <= 0:
                raise argparse.ArgumentTypeError(f"LR must be a finite number > 0, got {text!r}")
            return value
    except ValueError:
        raise argparse.ArgumentTypeError(f"cannot parse LR {text!r}; use 9, 9:1, or 9/1")
    if den == 0 or not math.isfinite(num) or not math.isfinite(den):
        raise argparse.ArgumentTypeError(f"invalid LR ratio {text!r}")
    value = num / den
    if value <= 0:
        raise argparse.ArgumentTypeError(f"LR must be > 0, got {text!r}")
    return value


def parse_prob(text: str, label: str) -> float:
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{label} must be a number, got {text!r}")
    if not math.isfinite(value):
        raise argparse.ArgumentTypeError(f"{label} must be finite, got {text!r}")
    return value


def parse_lr_list(text: str) -> list[float]:
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if not parts:
        raise argparse.ArgumentTypeError("--lrs needs at least one LR, e.g. '4,0.5,2'")
    return [parse_ratio(p) for p in parts]


def check_prior(prior: float) -> float:
    if not (0.0 < prior < 1.0):
        raise ValueError(f"prior must be strictly between 0 and 1 (got {prior}); "
                         "0 and 1 have infinite odds and cannot be updated")
    return prior


def odds_of(p: float) -> float:
    return p / (1.0 - p)


def prob_of(odds: float) -> float:
    if math.isinf(odds):
        return 1.0
    return odds / (1.0 + odds)


def posterior_of(prior: float, lr: float) -> dict:
    prior_odds = odds_of(prior)
    post_odds = prior_odds * lr
    posterior = prob_of(post_odds)
    return {
        "prior": prior,
        "prior_odds": prior_odds,
        "lr": lr,
        "bayes_factor": lr,
        "posterior_odds": post_odds,
        "posterior": posterior,
        "delta": posterior - prior,
        "log10_bayes_factor": math.log10(lr) if lr > 0 else None,
    }


def lr_from_test(sensitivity: float, specificity: float) -> float:
    if not (0.0 <= sensitivity <= 1.0):
        raise ValueError(f"sensitivity must be in [0, 1] (got {sensitivity})")
    if not (0.0 <= specificity <= 1.0):
        raise ValueError(f"specificity must be in [0, 1] (got {specificity})")
    if specificity == 1.0:
        raise ValueError("specificity 1.0 means zero false positives: the LR is infinite; "
                         "supply a finite --lr instead")
    if sensitivity == 0.0:
        raise ValueError("sensitivity 0.0 gives LR 0, which no evidence can produce; "
                         "check the inputs")
    lr = sensitivity / (1.0 - specificity)
    if not math.isfinite(lr):
        raise ValueError("computed likelihood ratio is not finite")
    return lr


def lr_from_rates(hit_rate: float, false_alarm: float) -> float:
    for name, value in (("hit-rate", hit_rate), ("false-alarm", false_alarm)):
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"{name} must be in [0, 1] (got {value})")
    if false_alarm == 0.0:
        raise ValueError("false-alarm rate 0 gives an infinite LR; supply a finite --lr")
    if hit_rate == 0.0:
        raise ValueError("hit-rate 0 gives LR 0; check the inputs")
    return hit_rate / false_alarm


def fmt_pct(p: float, digits: int) -> str:
    return f"{p * 100:.{digits}f}%"


def build_result(args) -> dict:
    if args.prior_odds is not None:
        if not (0.0 < args.prior_odds) or not math.isfinite(args.prior_odds):
            raise ValueError(f"--prior-odds must be finite and > 0 (got {args.prior_odds})")
        prior = prob_of(args.prior_odds)
    else:
        prior = check_prior(args.prior)

    lr_source = ""
    if args.lr is not None:
        lr = args.lr
        lr_source = f"given LR={lr:g}"
    elif args.sensitivity is not None:
        lr = lr_from_test(args.sensitivity, args.specificity)
        lr_source = (f"sensitivity={args.sensitivity:g}, specificity={args.specificity:g} "
                     f"-> LR+={lr:g}")
    else:
        lr = lr_from_rates(args.hit_rate, args.false_alarm)
        lr_source = f"hit-rate={args.hit_rate:g}, false-alarm={args.false_alarm:g} -> LR={lr:g}"

    result = posterior_of(prior, lr)
    result["lr_source"] = lr_source

    if args.base_rate:
        naive = prob_of(lr)  # equal (1:1) prior: base rate ignored
        shift_pp = (result["posterior"] - naive) * 100.0
        result["base_rate"] = {
            "naive_prior": 0.5,
            "naive_posterior": naive,
            "shift_pp": shift_pp,
            "flag": abs(shift_pp) >= 10.0,
            "verdict": ("base rate matters: ignoring it changes the answer by "
                        f"{abs(shift_pp):.1f} percentage points"),
        }

    if args.prior2 is not None:
        p2 = check_prior(args.prior2)
        result["alternates"] = [posterior_of(p2, lr)]

    if args.lrs:
        chain = []
        current = prior
        for i, next_lr in enumerate(args.lrs, 1):
            step = posterior_of(current, next_lr)
            step["step"] = i
            chain.append(step)
            current = step["posterior"]
        result["sequence"] = chain
        result["final_posterior"] = current

    return result


def print_text(result: dict, digits: int, only_posterior: bool) -> None:
    if only_posterior:
        print(f"{result['posterior']:.{digits}f}")
        return
    print(f"Prior:            {result['prior']:.{digits}f}  ({fmt_pct(result['prior'], digits)})")
    print(f"Prior odds:       {result['prior_odds']:.{digits}f} : 1")
    print(f"Evidence:         {result['lr_source']}")
    print(f"Likelihood ratio: {result['lr']:.{digits}f}  (Bayes factor)")
    print(f"Posterior odds:   {result['posterior_odds']:.{digits}f} : 1")
    print(f"Posterior:        {result['posterior']:.{digits}f}  ({fmt_pct(result['posterior'], digits)})")
    print(f"Movement:         {result['delta'] * 100:+.{digits}f} percentage points")

    if "alternates" in result:
        for alt in result["alternates"]:
            print(f"Alternate prior:  {alt['prior']:.{digits}f} -> posterior "
                  f"{alt['posterior']:.{digits}f} ({fmt_pct(alt['posterior'], digits)})")

    if "base_rate" in result:
        br = result["base_rate"]
        print()
        print("Base-rate check:")
        print(f"  Ignoring the base rate (50/50 prior) gives "
              f"{br['naive_posterior']:.{digits}f} ({fmt_pct(br['naive_posterior'], digits)}).")
        print(f"  True base rate shifts this by {br['shift_pp']:+.{digits}f} pp.")
        print(f"  {'FLAG: ' + br['verdict'] if br['flag'] else 'Modest shift; the prior is not doing much.'}")

    if "sequence" in result:
        print()
        print("Sequential evidence (posterior becomes next prior):")
        for step in result["sequence"]:
            print(f"  step {step['step']}: prior {step['prior']:.{digits}f} "
                  f"x LR {step['lr']:.{digits}g} -> {step['posterior']:.{digits}f}")
        print(f"  final posterior: {result['final_posterior']:.{digits}f} "
              f"({fmt_pct(result['final_posterior'], digits)})")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Update a belief with evidence using Bayes rule (odds form).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    prior_group = parser.add_mutually_exclusive_group(required=True)
    prior_group.add_argument("--prior", type=lambda s: parse_prob(s, "prior"),
                             help="prior probability in (0, 1), e.g. 0.1")
    prior_group.add_argument("--prior-odds", type=lambda s: parse_prob(s, "--prior-odds"),
                             help="prior as odds, e.g. 0.25 means 0.25:1 (p=0.2)")

    lr_group = parser.add_mutually_exclusive_group(required=True)
    lr_group.add_argument("--lr", type=parse_ratio,
                          help="likelihood ratio P(E|H)/P(E|not H); accepts 9, 9:1, or 9/1")
    lr_group.add_argument("--sensitivity", type=lambda s: parse_prob(s, "sensitivity"),
                          help="test sensitivity P(+|H); requires --specificity")
    lr_group.add_argument("--hit-rate", type=lambda s: parse_prob(s, "hit-rate"),
                          help="hit rate P(E|H); requires --false-alarm")

    parser.add_argument("--specificity", type=lambda s: parse_prob(s, "specificity"),
                        help="test specificity P(-|not H); LR+ = sensitivity/(1-specificity)")
    parser.add_argument("--false-alarm", type=lambda s: parse_prob(s, "false-alarm"),
                        help="false-alarm rate P(E|not H); LR = hit-rate/false-alarm")

    parser.add_argument("--prior2", type=lambda s: parse_prob(s, "prior2"),
                        help="alternative prior, updated with the same LR (prior sensitivity)")
    parser.add_argument("--lrs", type=parse_lr_list,
                        help="comma-separated LRs applied sequentially, e.g. '4,0.5,2'")
    parser.add_argument("--base-rate", action="store_true",
                        help="compare the posterior with the base-rate-neglect answer (50/50 prior)")
    parser.add_argument("--posterior", action="store_true",
                        help="print only the posterior probability")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--digits", type=int, default=4,
                        help="decimal places for text output")

    args = parser.parse_args(argv)

    if args.sensitivity is not None and args.specificity is None:
        parser.error("--sensitivity requires --specificity")
    if args.specificity is not None and args.sensitivity is None:
        parser.error("--specificity requires --sensitivity")
    if args.hit_rate is not None and args.false_alarm is None:
        parser.error("--hit-rate requires --false-alarm")
    if args.false_alarm is not None and args.hit_rate is None:
        parser.error("--false-alarm requires --hit-rate")

    try:
        result = build_result(args)
    except ValueError as exc:
        parser.error(str(exc))
        return 2  # unreachable; parser.error exits

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text(result, max(args.digits, 0), args.posterior)
    return 0


if __name__ == "__main__":
    sys.exit(main())
