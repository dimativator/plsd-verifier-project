# Running evaluations

The runner uses mini-SWE-agent to solve tasks from a blank Python file. It supports
three conditions: `baseline`, `verifier` (optional CrossHair access), and
`guided_verifier` (an instructed verification workflow). Both verifier conditions
receive the same technical guide; the task statements and tests stay the same.

## Setup

Install the agent dependency and build the two execution images:

```shell
python -m pip install -e ".[agent]"
docker build --target base -t plinse-eval:20261123 -f experiments/Dockerfile experiments
docker build --target crosshair -t plinse-crosshair:20261123 -f experiments/Dockerfile experiments
```

Docker must use Linux containers. The controller runs on Linux or native Windows;
agent commands run as Bash in Docker. Docker Desktop's WSL backend is sufficient
for a Windows controller.

## Prepare and run

This example prepares 24 calibration evaluations: four tasks, two repetitions
and three conditions. Preparation checks the task data and images and writes
`expected.json`, which records the inputs and settings.

```shell
python -m experiments.run --manifest studies/codeforces-20261124/task-manifest.json --output runs/example-calibration --spend-root runs/example-calibration/spend --models gpt-5.6-luna --conditions baseline verifier guided_verifier --phase calibration --task-count 4 --repetitions 2 --workers 2 --per-run-cap-usd 0.12 --total-cap-usd 4.00 --prepare-only
```

Set `OPENAI_API_KEY`, then repeat the command without `--prepare-only` to run it.
A `.env` one directory above the checkout takes precedence over the environment.
Model IDs and prices are recorded in `model_catalog.py`; check them when planning
a new collection. The default limits are 100 agent steps, 600 seconds for solving
and 16,384 output tokens per request.

The example's initial attempts have a combined ceiling of $2.88. Its $4.00 ledger
also covers retries and uncertain request charges. The runner admits a batch only
when its pending attempts fit at their full ceilings. Create
`runs/example-calibration/STOP` to stop new work after active evaluations finish.
Locks and `STOP` sit in the parent directory of `--spend-root`.

Repeat the same command to resume completed work. Use a new output directory when
changing settings; inspect any unfinished attempt before resuming it. A ledger
coordinates local processes sharing its directory. Runs on separate machines
need separate budget allocations even if they use the same API key.

For a main collection, use `--phase main` and choose the repetition count before
collection. The supplied manifest contains 100 study tasks and 10 calibration
tasks. Preparation freezes the selected tasks, source, prompts, images and limits.

## Retry and analyze

After all original attempts finish, resolve infrastructure failures and analyze
the selected results:

```shell
python -m experiments.resolve_runs --batch runs/example-calibration --manifest studies/codeforces-20261124/task-manifest.json --retry invalid --workers 2
python -m experiments.three_arm_analysis --results runs/example-calibration/resolved-results.json --expected runs/example-calibration/expected.json --phase calibration --output runs/example-calibration/analysis.json
```

Each infrastructure failure can be replaced once. Wrong answers and resource
exits remain scored; the latter use the last saved program. Retries share the
original ledger and do not add repetitions. Missing results stay missing rather
than becoming agent failures.

To reproduce the completed study, use the commands in the [root README](../README.md).
They read the exported JSON and CSV files without running agents. The study keeps
its five planned repetitions separate from the three added after interim
inspection, and clusters all repetitions within each task family.

[Distributed execution](distributed.py) can assign complete repetitions or whole
families to workers. The study used complete repetitions and rating-only
statistical strata. [Extension queues](EXTENSION_RUNS.md) can add repetitions to
a compatible frozen plan. The study's executed source is archived alongside its
results; maintained code has changed, so new runs need a fresh freeze.
