# Data sources and attribution

The study uses Codeforces tasks distributed by the upstream
[plsd-verifier-project](https://github.com/dimativator/plsd-verifier-project) at
commit `3e0232b9458f0681853c1f4cbed76878b6ab2abe`. Its recorded source is
[deepmind/code_contests](https://huggingface.co/datasets/deepmind/code_contests)
at revision `802411c3010cb00d1b05bad57ca77365a3c699d6`, train split, Codeforces
platform. The upstream provenance declares **CC-BY-4.0** for that dataset.
Original statements, tests and reference programs remain in the upstream data
bundle; the public study exports task IDs, metadata/hashes and newly measured
evaluation results. Benchmark selection and checker choices are recorded in
`task-manifest.json`.

The original repository also contains Kotlin HumanEval data, but it is not part
of this Python/CrossHair study. Existing source attributions and dataset licenses
are not replaced by this report or the experiment package. The upstream
repository currently declares no root code license; a repository-wide software
license should be agreed with its maintainer rather than inferred from a dataset
license. No new code license has been assigned by this change.
