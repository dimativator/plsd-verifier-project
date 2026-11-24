# Extending a frozen repetition-based study

`experiments.extend_rounds` queues successive complete-benchmark repetitions
without changing an existing protocol. The supported benchmark has 100 tasks and
three conditions, so each planned repetition contains 300 evaluations. New global
repetition IDs start after the largest ID in the source plan. The controller
waits for the specified predecessor worker's successful `worker-report.json` and
validates frozen source, prompts, task data, Docker images and limits before calls.

The published study in `studies/codeforces-20261124/` contains the original five
repetitions and three exploratory extension repetitions. Its original executed
source is archived there. Maintained code intentionally differs from that source;
historical plans must not be made executable by disabling hash checks. New agent
collections, including extensions, need a compatible fresh freeze. Saved JSON/CSV
analysis can be reproduced without executing agents.

## Prepare and execute

Install `.[agent]` in an editable checkout and build the Linux Docker images as
described in [README.md](README.md). A native Windows controller is supported;
agent commands still execute as Bash inside Linux containers.

The paths below are placeholders for a **newly frozen** repetition-assignment
plan and its completed predecessor worker. Freeze that plan with the explicit
public task manifest shown here, or supply another validated manifest consistently:

```shell
python -m experiments.extend_rounds run --plan runs/new-protocol/plan.json --manifest studies/codeforces-20261124/task-manifest.json --after-worker runs/completed-worker --output runs/new-extension --cap-usd 20.00 --workers 8 --prepare-only
```

Preparation validates the plan/environment without loading credentials or making
model calls. It writes the immutable extension definition. To execute a paid
queue, configure the controller's API key and run the same command without
`--prepare-only`. Use the same output directory for resumption. Changing the
output can duplicate global repetition IDs and create a separate ledger.

## Budget scope and stop behavior

One local ledger covers all batches from this extension controller, across every
condition and repetition. `--cap-usd` is the cap for that controller's allocation;
it does not automatically include unrelated runs or another machine using the
same API key. Prior spending and a separately enforced remote allocation can be
deducted with `--prior-charge-usd` and `--remote-reserve-usd`. These are explicit
accounting offsets, not remote enforcement. A live remote spending snapshot does
not bound future remote requests. A strict combined cap needs final ledgers or
independently enforced allocations whose totals fit the combined ceiling.

Before each dispatch, the controller holds every active run's full remaining
per-attempt allowance in addition to accounted API charges. Pending requests and
ambiguous-delivery charges count toward the cap. A controller lock prevents a
second extension queue from claiming the same output. It stops admissions when
another run cannot fit, when an infrastructure failure requires inspection, or
when the extension output's `STOP` file exists. Active evaluations finish normally.
The maintained single-batch runner and resolver place their controller and
dispatch locks, plus the `STOP` file, in the parent directory of `--spend-root`.
With the conventional `OUTPUT/spend` ledger layout, that is the output directory.
Use the controls belonging to the active controller; do not start a second queue
against an already claimed ledger.

After execution has started, inspect or stop the queue with:

```shell
python -m experiments.extend_rounds status --output runs/new-extension
python -m experiments.extend_rounds stop --output runs/new-extension
```

The final planned repetition can be partial. Preserve all outcomes; unstarted
identities remain missing and the partial repetition is excluded from complete
repetition averages and sample variance. Never encode a budget admission stop as
an agent failure. Keep the original planned analysis separate from a continuation
chosen after inspecting results, and label the pooled extension exploratory.

## Outputs and recovery

The extension output contains `extension-plan.json`, `status.json`,
`spend/ledger.json`, and per-repetition `expected.json` and `batch-report.json`
files inside `extension-rep-XXXX/` folders. Completed attempts are skipped on
resume; raw results are never overwritten. An incomplete attempt directory or
invalid infrastructure outcome requires explicit inspection and resolution.
Wrong answers and resource exits do not qualify for infrastructure replacement.

Use the recovery tools only with a matching frozen source/environment and the
original explicit manifest and shared ledger. `experiments.finish_repetition`
can finish the never-started identities of one interrupted repetition and then
resolve recognized external failures, stopping after that repetition. Its selected
`resolved-results.json` is the analysis input; originals and separate retry
attempts remain audit artifacts. No retry becomes a new repetition.
