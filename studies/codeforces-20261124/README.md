# Codeforces verifier study

We compared ordinary coding tools, optional CrossHair access and an instructed
verification workflow using `gpt-5.6-luna` in mini-SWE-agent. The study contains
100 tasks and eight repetitions per condition: **2,400 evaluations**. Five
repetitions were planned in advance; three were added after interim inspection.

Read the [report](report.pdf), [report text](report.md) or [LaTeX source](latex/main.tex).

| Condition | Accuracy | Sample SD | Mean API cost/task |
| --- | ---: | ---: | ---: |
| Baseline | 82.50% | 1.69 pp | $0.01942 |
| Optional | 81.38% | 3.11 pp | $0.01618 |
| Instructed | 85.50% | 1.69 pp | $0.01968 |

Instructed minus baseline was +3.00 percentage points (paired 97.5% CI
[-0.38, +6.50]); optional minus baseline was -1.13 points [-4.38, +2.13]. Both
intervals include zero. Verifier invocation was observed in 0/800 optional runs
and 639/800 instructed runs. These compare access and instruction policies;
they do not isolate the effect of verifier feedback.

## Reproduce the analysis

From the repository root with Python 3.12 or newer:

```shell
python -m pip install -e ".[report]"
python -m experiments.three_arm_analysis --results studies/codeforces-20261124/combined-results.json --expected studies/codeforces-20261124/combined-expected.json --phase main --output reproduced-analysis.json
python -m experiments.report --study studies/codeforces-20261124 --output reproduced-figures
```

These commands use the saved results. The figure shows marginal 95% confidence
intervals for accuracy and cost. The bootstrap uses 10,000 draws, seed 20261123,
and keeps all repetitions and conditions together within each sampled task family.
SD and variance use n - 1 across repetition scores. The intervals describe
comparable task families, rather than repeated-run uncertainty on this exact set.

To rebuild the report, copy the regenerated plot PDF to `latex/images/`, then run
`latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` in
`latex/`.

## Data

- `combined-results.json` and `combined-expected.json` contain the selected
  outcomes and complete evaluation plan.
- `analysis_original_5.json`, `analysis_all_8.json` and `accuracy-cost-points.csv`
  contain the reported estimates. `all-attempt-costs.csv` includes original and
  retry costs; the total is $44.22626659, excluding preparation and retaining
  conservative charges after uncertain delivery.
- `task-manifest.json` identifies the study and calibration tasks.
  [DATA_SOURCES.md](DATA_SOURCES.md) records their source and attribution.
- `executed-experiment-source.zip` preserves the collection code;
  `protocol-provenance.json` records its settings. The remaining audit and
  checksum files document the exported results.

The dataset selects one outcome for each evaluation. Thirty-three infrastructure
retries replace failed attempts; wrong answers and resource exits remain scored.
