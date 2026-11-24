Task selection and source-reference preflight
============================================

Run from the repository root:

```powershell
python -m unittest experiments.test_validation -v
python -m experiments.validate_tasks
python -m experiments.validation_preflight --kind all --workers 4 --output runs/calibration-20261123/reference-preflight-final.json --freeze-output runs/calibration-20261123/validated-task-manifest.json
```

The Docker image and `experiments.runtime.run_isolated` must already be available.
Reference code is never executed on the host. The controller copies only the
chosen source references, tests, and trusted worker into a private workspace;
the runtime mounts that workspace in a container without networking or host
credentials. These workspaces contain hidden data and must never be mounted in
an agent container. The worker refuses to execute outside Docker.

Selection rules
---------------

The default provisional main sample contains 50 tasks rated 2000–2399 and 50
rated 2400+, with the next 10 reviewed tasks per band designated as reserves.
SHA-256 of `20261123:task_id` determines order. Ten previously exposed tasks,
five per band, are reserved for calibration. All earlier selection manifests
are conservatively treated as exposure, whether or not a run was completed.
Indexed sibling versions such as B2/B3 share a family and cannot cross the
development/main split or count as independent selected families.

Main eligibility requires a nonempty private suite, no supplied quality flags
for repeated-input conflicting outputs or public/hidden overlap, and an
explicit accepted output-contract review in `validation_reviews.json`.
Unknown, constructive/witness, tolerance-based, and missing-image cases are
excluded. Output evidence and complete Input sections are retained in the
generated manifest. A full-statement ambiguity scan was also reviewed; 91-E is
explicitly rejected because its body permits any maximizing walrus, even
though its Output section omits that qualification.

The pipeline independently checks array alignment, expected-output types,
nonempty suites, conflicting duplicate inputs, and public/private overlap after
conservative whitespace normalization. It checks metadata case counts and
records portable LF-normalized source hashes. The integer checker accepts
integer formatting differences such as leading zeroes; literal token checking
is retained for significant bit strings, named outcomes, and ordered strings.

Generated tests remain excluded before any new model outcomes because their
input domains have not been established. Statement input sections are screened
for missing content and retained for review. The pipeline does **not** claim an
exhaustive semantic proof that every original private input satisfies every
problem constraint. References and tests originate in the same source bundle;
passing source references is a sanity check, not an independent oracle proof.

Behavioral preflight
--------------------

For every selected candidate and reserve, the worker compiles the preserved
C++ source with GNU++17, `-DONLINE_JUDGE`, and `-O2`; GNU++14 is a recorded
compilation fallback for old sources that conflict with newer standard-library
names. `ONLINE_JUDGE` suppresses source-local debugging file redirections, as
on the original contest service. A copied C++ file's legacy MSVC `%I64d` and
related formats are normalized to ISO `%lld` formats, with source and executed
hashes and replacement counts retained. Original benchmark files are untouched.
Python references run with Python 3; Python 2 references are reported as
incompatible rather than translated. Java references are not run by this image.

Each public/private input receives a fresh process with a ten-second timeout.
At least one supported source reference must pass every case. A wrong answer
from another executable source reference quarantines the candidate; compilation
incompatibility or a slow secondary source is recorded. Final selection takes
the first 50 passing families in each prespecified seeded order. It never uses
model outcomes. `replacement_record` records changes to the initial sample.

The final status is `reference_sanity_passed_ready_for_protocol_freeze`: model,
agent budgets, repetition count, retry policy and analysis still need their own
protocol freeze. The source data, reviews and all output files are separate.
Generated outputs live under ignored `runs/calibration-20261123/`.

On 2026-11-23 the initial unadapted results were preserved in
`reference-preflight.json`, I64-only retries in
`reference-preflight-portable.json`, and the complete standardized rerun in
`reference-preflight-final.json`. These are engineering preflight attempts,
not extra model experiments. The original provisional manifest is retained as
`task-validation-initial.json`; subsequent review removes 91-E explicitly.

The unit tests cover leakage rejection, conflicting and malformed oracles,
significant string preservation, numeric output handling, source portability,
sibling exclusion, deterministic sampling, and replacements that use only
passed source checks.
