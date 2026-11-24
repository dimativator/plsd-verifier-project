# Verifier-assisted coding experiments

A benchmark and runner for testing whether program verification helps coding
agents. The Python experiments compare ordinary coding tools, optional CrossHair
access, and an instructed verification workflow. The repository also contains
the original Kotlin HumanEval and Codeforces pilots.

The [Codeforces study](studies/codeforces-20261124/README.md) evaluates 100 tasks
in all three conditions over eight repetitions. Its [report](studies/codeforces-20261124/report.pdf)
includes accuracy, variation between repetitions, costs and confidence intervals.

## Quick start

With Python 3.12 or newer, unpack the results and reproduce the analysis and figure:

```shell
python -m pip install -e ".[report]"
python -m zipfile -e studies/codeforces-20261124/data.zip runs/codeforces-study
python -m experiments.three_arm_analysis --results runs/codeforces-study/combined-results.json --expected runs/codeforces-study/combined-expected.json --phase main --output runs/analysis.json
python -m experiments.report --study runs/codeforces-study --output runs/figures
```

This works locally from saved results; it does not call a model. The
[execution guide](experiments/README.md) covers new runs, validation and metrics.
[Benchmark usage](benchmark-data/USAGE.txt) describes the source data.

## Development

```shell
python -m pip install -e ".[agent,report,dev]"
python -m unittest discover -s experiments -p "test_*.py"
python -m ruff check experiments
```

The default tests mock model requests. Docker integration tests use locally built
images and `PLINSE_DOCKER_TESTS=1`.
