# Scorecard: tiers, rubric, bias checklist

One topic: turning source metadata into a defensible claim strength.

## 1. Source tier table

Tier answers: *how much does this design control for confounding and chance?*
Base values are for a **direct, recent, low-bias** instance.

| Tier | Base | What it is | Typical weakness |
|---|---|---|---|
| `meta` | 5.0 | Systematic review / meta-analysis of comparable studies, with heterogeneity reported | Garbage-in-garbage-out; publication bias in the pooled literature; protocol not pre-registered |
| `rct` | 4.0 | Randomised controlled trial | Small N, unblinded outcomes, surrogate endpoints, single site, selective reporting |
| `observational` | 3.0 | Cohort, case-control, cross-sectional, natural experiment | Confounding; reverse causation; measurement error |
| `case` | 2.0 | Case study, case series, anecdote with detail | No control group; cannot establish causation or base rate |
| `expert` | 1.5 | Named expert opinion, review without systematic method, textbook | Authority, not evidence; conflicts of interest |
| `blog` | 1.0 | Blog, news, social post, undated web page | No method disclosure; second-hand; often uncited |

**Tier modifiers (apply before penalties):**
- Meta-analysis with **no heterogeneity statistic or no search protocol** → treat as `observational` (3.0).
- RCT that is **pre-registered and independently replicated** → 4.5.
- Observational study with a **natural experiment / difference-in-differences** design → 3.5.
- Expert opinion that is explicitly a **structured consensus process** (Delphi) → 2.5.
- A blog post that **links and correctly summarises a primary study** → score the primary study, not the blog.

## 2. Five-point rubric

| Strength | Label | Meaning | Allowed use |
|---|---|---|---|
| 5 | Established | Multiple independent replications, direct outcome, low bias | Act; cite as settled |
| 4 | Supported | One good direct study or a consistent body, minor caveats | Act with caveat; monitor |
| 3 | Suggestive | Real signal, but indirect outcome, confounding, or single study | Use as one input; seek confirmation |
| 2 | Weak | Anecdote, unreplicated, or high bias | Hypothesis generation only |
| 1 | Unsupported | No traceable source, or source contradicts claim | Do not cite; find evidence or drop |

**Scoring arithmetic**

```
base   = tier_base(tier)
recency_penalty = 0.25 * floor(max(0, years - 2) / 4), capped at 1.0
directness_penalty = 0.5 if indirect else 0
bias_penalty = {"low": 0.0, "medium": 0.5, "high": 1.0}[bias]
strength = round(clamp(base - recency_penalty - directness_penalty - bias_penalty, 1, 5), 1)
```

Recency rationale: in fast-moving fields 2 years is the freshness horizon; slower fields should pass `--recency 0` and judge relevance by hand. Do not let a stale source fall below 1 — staleness is a caveat, not a refutation.

**What moves it one point** (state exactly one):
- `+1` by finding a meta-analysis or independent replication at the same tier or higher.
- `+1` by replacing a surrogate with the outcome you actually care about (directness).
- `+0.5` each by confirming pre-registration, increasing N past the field's convention, or removing a funding conflict.
- `−1` by discovering the result was not replicated, the outcome was switched post hoc, or the cited source does not say what is claimed.

## 3. Bias checklist

Scan all eight; each **yes** is a point of suspicion, not an automatic −1.

**Selection & design**
1. **Selection bias** — participants/studies chosen in a way correlated with the outcome (survivorship, self-selection, convenience sample).
2. **Attrition** — differential drop-out; check whether the analysis is intention-to-treat.
3. **Confounding** — a third variable explains both exposure and outcome; was it measured or only asserted away?

**Analysis & reporting**
4. **P-hacking / garden of forking paths** — many outcomes or subgroups, only the significant one reported. Look for pre-registration and for the number of comparisons.
5. **Outcome switching** — registered primary outcome differs from the reported one.
6. **Publication bias** — the literature contains only positive findings; funnel-plot asymmetry, file-drawer problem. This applies to the *tier*, not the single paper.
7. **Effect-size inflation** — small studies with large effects; check whether the effect shrinks with N.

**Interest**
8. **Funding / affiliation / ideology** — who paid, who benefits from the claim, and does the conclusion match the funder's interest? Disclosure alone is not a disqualifier; undisclosed interest is.

**Aggravating combinations:** high bias + small N (<100) + non-meta design → cap strength at 2. Indirect outcome + high bias → cap at 3.

## 4. Optional: OpenAlex metadata check

If online access is available, resolve the source and fill the row mechanically:

```
https://api.openalex.org/works?filter=doi:<DOI>
https://api.openalex.org/works?search=<title>
```

Read back: `publication_year` (recency), `type` (article / preprint / review), `cited_by_count`, `primary_location.source.is_oa`, `authorships[].institutions`, and `grants`/`funders` for funding. A `type: preprint` without peer review cannot score above `observational` unless it reports a registered RCT.

The helper script makes no network calls; it scores only the flags you pass. Use this section manually when a DOI is available.
