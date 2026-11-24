# Analysis

The analysis reports task success, variation between repeated benchmark runs,
and paired differences between conditions. It uses Python's standard library.

```shell
python -m experiments.three_arm_analysis --results studies/codeforces-20261124/combined-results.json --expected studies/codeforces-20261124/combined-expected.json --phase main --output analysis.json
```

Supply the complete expected manifest, including unfinished runs. Missing or
duplicate results, unresolved infrastructure failures, inconsistent task metadata
and unequal condition assignments block the comparison. A retry replaces a failed
infrastructure attempt; it is not another repetition. Wrong answers and resource
exits retain the score of the final saved program.

## Inputs

Results may be JSON/JSONL files or directories containing `result.json` files.
Each row identifies a model, task, condition and repetition and includes:

| Field | Meaning |
| --- | --- |
| `family_id`, `rating_band` | Source problem and difficulty stratum |
| `hidden_passed` | Whether the program passed the retained private tests |
| `valid_run`, `infrastructure_error` | Whether the attempt can be scored |
| `model_cost_usd`, `cost_is_upper_bound` | Selected-attempt API cost and accounting status |
| `solve_seconds`, `evaluation_seconds` | Separate solving and evaluation times |

The expected manifest lists the same identities and task metadata. The
three-arm tool requires `baseline`, `verifier` and `guided_verifier`, with the
same repetition IDs for every condition of a task. Models are analyzed separately.
If `phase` is present, it must match the requested analysis phase.

## Scores and uncertainty

Average each task's repeated Boolean outcomes, then average the task scores with
equal weights. Paired comparisons subtract baseline success from treatment
success on each task before averaging.

Confidence intervals use 10,000 seeded bootstrap draws by default. Within each
rating band, resample source families with replacement, keeping all their tasks,
conditions and repetitions together. Preserve each band's original task weight.
These intervals describe uncertainty over comparable task families. Repeated
attempts on the same task do not count as additional independent families.

Each arm gets a descriptive 95% interval. The two baseline comparisons use 97.5%
intervals, a Bonferroni adjustment for approximately 95% familywise coverage.
Bootstrap coverage is approximate. Small or degenerate samples receive warnings;
when applicable, a conservative bounded-mean interval is reported separately.

The November 2026 study has 100 families split equally between two rating bands.
It uses rating-only strata. Other prespecified stratifications can be supplied
through `analysis_stratum`; a family cannot span strata, and planned and observed
assignments must agree.

`repeated_benchmark_scores` lists the score of each complete repetition, their
mean, and sample SD and variance with `ddof=1`. SD is in percentage points;
variance is in squared percentage points. These describe run-to-run variation
on the fixed benchmark, not a confidence interval over task families. Incomplete
or unbalanced rounds suppress these summaries.

## Costs and plots

Result rows describe the selected attempt only. Add superseded infrastructure
attempts from the shared spending ledger when reporting total evaluation cost.
Uncertain-delivery reservations remain conservative charges, not exact invoices.

The public study supplies these totals in `all-attempt-costs.csv`. Plot them with:

```shell
python -m experiments.report --study studies/codeforces-20261124 --output figures
```

Horizontal and vertical bars are marginal 95% family-bootstrap intervals for
cost and accuracy, using the same sampled families. They are not a joint 95%
confidence region or a measure of billing uncertainty.

The study's first five repetitions were planned before collection; three more
followed inspection of the interim results. The report retains the planned
analysis and labels the pooled eight-repetition analysis exploratory. Passing
`--phase main` does not change that interpretation.
