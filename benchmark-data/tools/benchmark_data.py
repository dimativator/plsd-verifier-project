"""Inspect a portable benchmark bundle and copy only public task files."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = {"function": {"prompt.txt", "task.json", "Solution.kt", "PublicTests.kt"},
                "program": {"prompt.txt", "task.json", "Main.kt", "public-tests.json"}}


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def inside(root: Path, relative: str) -> Path:
    path = root / relative
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes bundle or is a symlink: {relative}")
    return path


def tasks(root: Path, dataset: str, band: str | None = None) -> list[dict]:
    if dataset not in {"kotlinhumaneval", "codecontests"}:
        raise ValueError(f"Unknown dataset: {dataset}")
    directory = inside(root, dataset)
    with inside(directory, "tasks.jsonl").open(encoding="utf-8") as stream:
        rows = [json.loads(line) for line in stream if line.strip()]
    if band is not None:
        if dataset != "codecontests" or band not in {"800-1199", "1200-1599", "1600-1999", "2000-2399", "2400+"}:
            raise ValueError(f"Unknown rating band: {band}")
        rows = [row for row in rows if row["rating_band"] == band]
    return rows


def prepare(root: Path, dataset: str, task_id: str, destination: Path) -> None:
    row = next((row for row in tasks(root, dataset) if row["id"] == task_id), None)
    if row is None:
        raise ValueError(f"Unknown task: {task_id}")
    source = inside(root / dataset, row["public_dir"])
    files = list(source.iterdir())
    allowed = PUBLIC_FILES[row["submission_format"]]
    if any(p.is_symlink() or not p.is_file() or p.name not in allowed for p in files):
        raise ValueError("Unexpected file in public task directory")
    if destination.exists():
        raise FileExistsError(f"Workspace already exists: {destination}")
    destination.mkdir(parents=True)
    for path in files:
        shutil.copyfile(path, destination / path.name)


def validate(root: Path) -> dict:
    expected_hashes = load(root / "checksums.json")
    files = list(root.rglob("*"))
    if any(p.is_symlink() for p in files):
        raise ValueError("Symlinks are not allowed in the bundle")
    actual = {p.relative_to(root).as_posix() for p in files if p.is_file()
              and p.name != "checksums.json" and "__pycache__" not in p.parts}
    if actual != set(expected_hashes):
        raise ValueError("Bundle file inventory differs from checksums.json")
    for relative, expected in expected_hashes.items():
        path = inside(root, relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Checksum mismatch: {relative}")
    summary = {}
    selection = load(root / "codecontests" / "provenance" / "selection.json")
    for dataset, expected_count in (("kotlinhumaneval", 161), ("codecontests", selection["selected_count"])):
        rows = tasks(root, dataset)
        if len(rows) != expected_count or len({row["id"] for row in rows}) != expected_count:
            raise ValueError(f"Wrong unique task count: {dataset}")
        directory = root / dataset
        if load(directory / "groups" / "all.json") != [row["id"] for row in rows]:
            raise ValueError(f"All-task index differs: {dataset}")
        for row in rows:
            if load(inside(directory, row["metadata_file"])) != row:
                raise ValueError(f"Task metadata differs: {row['id']}")
            public = inside(directory, row["public_dir"])
            allowed = PUBLIC_FILES[row["submission_format"]]
            if any(p.name not in allowed or not p.is_file() for p in public.iterdir()):
                raise ValueError(f"Unexpected public file: {row['id']}")
            if row["submission_format"] == "function":
                original = (inside(directory, row["evaluator_dir"]) / "OriginalTests.kt").read_text(encoding="utf-8")
                hidden = inside(directory, row["evaluation_harness"]).read_text(encoding="utf-8")
                # The source suite uses one if assertion per case, as checked by the source packager.
                if len(re.findall(r"\bif\s*\(", hidden)) != row["unexposed_test_count"]:
                    raise ValueError(f"Wrong hidden case count: {row['id']}")
                if not original.endswith(hidden[len("fun main() {\n"):]):
                    raise ValueError(f"Hidden cases differ from original suite: {row['id']}")
            else:
                for filename, key, subfolder in (("public-tests.json", "public_test_count", public),
                                                ("private-tests.json", "private_test_count", inside(directory, row["evaluator_dir"])),
                                                ("generated-tests.json", "generated_test_count", inside(directory, row["evaluator_dir"]))):
                    tests = load(subfolder / filename)
                    if len(tests["input"]) != len(tests["output"]) or len(tests["input"]) != row[key]:
                        raise ValueError(f"Wrong test count: {row['id']}/{filename}")
        if dataset == "codecontests":
            bands = Counter(row["rating_band"] for row in rows)
            if bands != selection["selected_band_counts"]:
                raise ValueError("Wrong difficulty allocation")
            for band in bands:
                if load(directory / "groups" / f"{band}.json") != [row["id"] for row in rows if row["rating_band"] == band]:
                    raise ValueError(f"Rating-band index differs: {band}")
        summary[dataset] = len(rows)
    return {"status": "integrity_and_structure_passed", "files_checked": len(expected_hashes),
            "datasets": summary, "behavioral_validation": "not_run"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    for name in ("list", "show", "prepare"):
        command = commands.add_parser(name)
        command.add_argument("dataset", choices=["kotlinhumaneval", "codecontests"])
        if name == "list":
            command.add_argument("--band")
        else:
            command.add_argument("task_id")
        if name == "prepare":
            command.add_argument("destination", type=Path)
    args = parser.parse_args()
    if args.command == "validate":
        result = validate(args.root)
    elif args.command == "list":
        result = [row["id"] for row in tasks(args.root, args.dataset, args.band)]
    elif args.command == "show":
        result = next((row for row in tasks(args.root, args.dataset) if row["id"] == args.task_id), None)
        if result is None:
            parser.error(f"Unknown task: {args.task_id}")
    else:
        prepare(args.root, args.dataset, args.task_id, args.destination)
        result = {"workspace": str(args.destination.resolve()), "contains": "public task files only"}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
