"""Assemble the cached Kotlin compiler and the built verifier for the local pilot."""

import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import urllib.request
import zipfile


def setup(root: Path, verifier_repo: Path) -> dict:
    common, verifier = root / "common", root / "verifier"
    common.mkdir(parents=True, exist_ok=True)
    verifier.mkdir(parents=True, exist_ok=True)
    cache = Path.home() / ".gradle/caches/modules-2/files-2.1"
    modules = {"compiler": ("org.jetbrains.kotlin", "kotlin-compiler-embeddable", "2.3.0"),
               "stdlib": ("org.jetbrains.kotlin", "kotlin-stdlib", "2.3.0"),
               "reflect": ("org.jetbrains.kotlin", "kotlin-reflect", "2.3.0"),
               "script-runtime": ("org.jetbrains.kotlin", "kotlin-script-runtime", "2.3.0"),
               "coroutines": ("org.jetbrains.kotlinx", "kotlinx-coroutines-core-jvm", "1.8.0"),
               "annotations": ("org.jetbrains", "annotations", "13.0")}
    jars = {}
    hashes = {}
    for name, (group, artifact, version) in modules.items():
        paths = list((cache / group / artifact / version).glob("*/*.jar"))
        if len(paths) != 1:
            raise ValueError(f"Missing or ambiguous cached dependency: {artifact}:{version}")
        target = common / (name + ".jar")
        shutil.copyfile(paths[0], target)
        jars[name] = str(target)
        hashes[name] = hashlib.sha256(target.read_bytes()).hexdigest()
    annotations = next((verifier_repo / "formver.annotations/build/libs").glob("*.jar"))
    shutil.copyfile(annotations, common / "formver-annotations.jar")
    plugin = next((verifier_repo / "formver.compiler-plugin/build/libs").glob("*.jar"))
    shutil.copyfile(plugin, verifier / "plugin.jar")
    shutil.copyfile(verifier_repo / "SPECIFICATIONS.md", verifier / "SPECIFICATIONS.md")
    release = "z3-4.8.7-x64-osx-10.14.6"
    expected = "49fa41210ff572ae56476befafbeb4a82bbf921f843daf73ef5451f7bcd6d2c5"
    binary_hash = "572dd98ff32cfdbca636d929f122e8e96f9a9f42a6a52cdc4ce97da37494c3b3"
    target = verifier / "z3"
    if not target.exists():
        url = f"https://github.com/Z3Prover/z3/releases/download/z3-4.8.7/{release}.zip"
        archive = urllib.request.urlopen(url).read()
        if hashlib.sha256(archive).hexdigest() != expected:
            raise ValueError("Z3 archive hash does not match the repository's pinned checksum")
        with zipfile.ZipFile(io.BytesIO(archive)) as source:
            binary = source.read(f"{release}/bin/z3")
        if hashlib.sha256(binary).hexdigest() != binary_hash:
            raise ValueError("Z3 executable checksum mismatch")
        temporary = target.with_suffix(".tmp")
        temporary.write_bytes(binary)
        temporary.replace(target)
        target.chmod(0o755)
    if target.is_symlink() or hashlib.sha256(target.read_bytes()).hexdigest() != binary_hash:
        raise ValueError("Cached Z3 executable checksum mismatch")
    java = Path("/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home/bin/java")
    if not java.is_file():
        raise FileNotFoundError("Expected local Temurin JDK 21 is missing")
    common_config = {"java": str(java), "compiler_classpath": list(jars.values()),
                     "library_classpath": [jars["stdlib"], str(common / "formver-annotations.jar")],
                     "compiler_version": "2.3.0"}
    verifier_config = {"plugin": str(verifier / "plugin.jar"), "z3": str(target)}
    (common / "toolchain.json").write_text(json.dumps(common_config, indent=2) + "\n")
    (verifier / "toolchain.json").write_text(json.dumps(verifier_config, indent=2) + "\n")
    for name, path in [("plugin", verifier / "plugin.jar"), ("formver_annotations", common / "formver-annotations.jar"), ("z3", target)]:
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    report = {"compiler": common_config, "verifier": verifier_config, "sha256": hashes,
              "z3_archive_sha256": expected}
    (root / "provenance.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--verifier-repo", type=Path, required=True)
    args = parser.parse_args()
    setup(args.root.resolve(), args.verifier_repo.resolve())
