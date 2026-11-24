# Verifier-assisted coding experiments

A benchmark and runner for testing whether program verification helps coding
agents. The Python experiments compare ordinary coding tools, optional CrossHair
access, and an instructed verification workflow. The repository also contains
the original Kotlin HumanEval and Codeforces pilots.

The [Codeforces study](studies/codeforces-20261124/README.md) evaluates 100 tasks
in all three conditions over eight repetitions. Its [report](studies/codeforces-20261124/report.pdf)
includes accuracy, variation between repetitions, costs and confidence intervals.

## Quick start

With Python 3.12 or newer, reproduce the saved analysis and figure:

```shell
python -m pip install -e ".[report]"
python -m experiments.three_arm_analysis --results studies/codeforces-20261124/combined-results.json --expected studies/codeforces-20261124/combined-expected.json --phase main --output reproduced-analysis.json
python -m experiments.report --study studies/codeforces-20261124 --output reproduced-figures
```

This works locally from the exported results; it does not call a model.

For new evaluations, follow the [execution guide](experiments/README.md).
The [analysis guide](experiments/analysis_readme.md) explains the metrics, and
[benchmark usage](benchmark-data/USAGE.txt) covers the source data and attribution.

## Development

```shell
python -m pip install -e ".[agent,report,dev]"
python -m unittest discover -s experiments -p "test_*.py"
python -m ruff check experiments
```

The default tests mock model requests. Docker integration tests use locally built
images and `PLINSE_DOCKER_TESTS=1`.
