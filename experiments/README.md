# Running evaluations

The runner uses mini-SWE-agent to solve tasks from a blank Python file. It supports
three conditions: `baseline`, `verifier` (optional CrossHair access), and
`guided_verifier` (an instructed verification workflow). Both verifier conditions
receive the same technical guide; the task statements and tests stay the same.

## Setup

Install the agent dependency, unpack the study data and build the execution images:

```shell
python -m pip install -e ".[agent]"
python -m zipfile -e studies/codeforces-20261124/data.zip runs/codeforces-study
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
python -m experiments.run --manifest runs/codeforces-study/task-manifest.json --output runs/example-calibration --spend-root runs/example-calibration/spend --models gpt-5.6-luna --conditions baseline verifier guided_verifier --phase calibration --task-count 4 --repetitions 2 --workers 2 --per-run-cap-usd 0.12 --total-cap-usd 4.00 --prepare-only
```

Set `OPENAI_API_KEY`, then repeat the command without `--prepare-only` to run it.
A `.env` one directory above the checkout takes precedence over the environment.
Check the model ID and prices in `model_catalog.py` when planning a collection.
The default limits are 100 agent steps, 600 seconds for solving and 16,384 output
tokens per request.

The example's initial attempts have a combined ceiling of $2.88. Its $4.00 ledger
also covers retries and uncertain request charges. The runner admits a batch only
when its pending attempts fit at their full ceilings. Create
`runs/example-calibration/STOP` to stop new work while active evaluations finish.
Locks and `STOP` sit in the parent directory of `--spend-root`.

Repeat the same command to resume a batch. Use a new output directory when changing
settings; inspect any unfinished attempt before resuming it. A ledger coordinates
local processes sharing its directory. Separate machines need separate budget
allocations even when they use the same API key.

For a main collection, use `--phase main` and choose the repetition count before
collection. The supplied manifest contains 100 study tasks and 10 calibration
tasks. Preparation freezes the selected tasks, source, prompts, images and limits.
The collection code is archived inside the study's data ZIP; new runs with the
maintained code need a fresh freeze.

## Retry and analyze

After all original attempts finish, resolve infrastructure failures and analyze
the selected results:

```shell
python -m experiments.resolve_runs --batch runs/example-calibration --manifest runs/codeforces-study/task-manifest.json --retry invalid --workers 2
python -m experiments.three_arm_analysis --results runs/example-calibration/resolved-results.json --expected runs/example-calibration/expected.json --phase calibration --output runs/example-calibration/analysis.json
```

Each infrastructure failure can be replaced once. Wrong answers and resource
exits remain scored; the latter use the last saved program. Retries share the
original ledger and do not add repetitions. Missing results stay missing rather
than becoming agent failures.

Analysis expects one selected result for each planned
`(model, task_id, condition, repetition)` identity. Missing, duplicate or unresolved
outcomes block complete-study estimates. Scores first average repetitions within
each task, then give tasks equal weight. Sample SD and variance use n - 1 across
complete repetition scores. Family-bootstrap intervals keep all conditions and
repetitions of a sampled task family together, within rating strata. Arm intervals
are 95%; main-phase paired baseline comparisons use 97.5% intervals. Calibration
reports descriptive results rather than main-effect intervals. Family intervals
describe comparable task families rather than Monte Carlo uncertainty on this exact set.

The [completed study](../studies/codeforces-20261124/README.md) retains its five
planned repetitions separately from the three added after interim inspection.
Its cost figure uses all original and retry charges; the ordinary analysis cost
summary covers selected attempts only. Use the root [quick start](../README.md#quick-start)
to reproduce it from the ZIP.

## Task validation

To rebuild the candidate selection and inspect checker reviews:

```shell
python -m experiments.validate_tasks --reviews runs/codeforces-study/validation_reviews.json --output runs/task-validation.json
```

Selection uses deterministic family ordering and separates calibration tasks.
Checks cover test structure, conflicting outputs, public/private overlap and
reviewed output contracts; constructive or ambiguous-output tasks are excluded.
The output is a provisional selection, not a reference-execution certificate.
Source-reference checks established the study's supplied task manifest. Passing
the packaged private tests remains a test-suite outcome rather than a proof of
correctness or complete Codeforces judge acceptance.
