# Codeforces verifier study

We compared ordinary coding tools, optional CrossHair access and an instructed
verification workflow using `gpt-5.6-luna` in mini-SWE-agent. The study contains
100 tasks and eight repetitions per condition: **2,400 evaluations**. Five
repetitions were planned in advance; three were added after interim inspection.

Read the [report](report.pdf) or its [LaTeX source](report.tex).

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

## Reproduction

The [root quick start](../../README.md#quick-start) unpacks `data.zip` and reproduces
the analysis and figure. The figure's bars are marginal 95% confidence intervals
for accuracy and cost. The bootstrap uses 10,000 draws, seed 20261123, and keeps
all repetitions and conditions together within each sampled task family. SD and
variance use n - 1 across repetition scores. Family intervals describe comparable
tasks rather than repeated-run uncertainty on this exact set.

To rebuild the PDF, run `latexmk -pdf -interaction=nonstopmode -halt-on-error report.tex`
in this directory. The report uses the accompanying `accuracy-vs-cost.pdf`.

## Data

[Data ZIP](data.zip) contains the 2,400 selected outcomes, their evaluation plan,
all-attempt costs, task manifest and validation reviews. It also contains aggregate
interaction evidence, protocol and source records, the executed source snapshot,
and checksums. The analysis and plot estimates are regenerated from these inputs.
Thirty-three infrastructure retries replace failed attempts; wrong answers and
resource exits remain scored. Total accounted cost is $44.22626659, excluding
preparation and retaining conservative uncertain-delivery charges.

## Sources

Tasks come from [plsd-verifier-project](https://github.com/dimativator/plsd-verifier-project)
at commit `3e0232b9458f0681853c1f4cbed76878b6ab2abe`, whose recorded source is
[DeepMind Code Contests](https://huggingface.co/datasets/deepmind/code_contests),
revision `802411c3010cb00d1b05bad57ca77365a3c699d6`, train split, Codeforces platform.
The source provenance declares CC-BY-4.0 for that dataset. Statements, tests and
reference programs remain in the upstream benchmark; this ZIP contains task
metadata and measured evaluation results. Kotlin HumanEval is not part of this
Python study. Existing data attributions still apply; the dataset license does
not assign a repository-wide software license.
