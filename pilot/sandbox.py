"""macOS isolation for agent commands and submitted Kotlin programs."""

import json
import os
from pathlib import Path
import signal
import subprocess


def profile(workspace: Path, readable: list[Path]) -> str:
    workspace = workspace.resolve()
    allow_reads = " ".join(f"(subpath {json.dumps(str(p.resolve()))})" for p in [workspace, *readable])
    parents = {parent for path in [workspace, *readable] for parent in path.resolve().parents}
    metadata = " ".join(f"(literal {json.dumps(str(p))})" for p in sorted(parents))
    return ("(version 1)(allow default)(deny network*)(deny process-info*)"
            "(allow process-info* (target self))"
            '(deny file-read* (subpath "/Users") (subpath "/Volumes"))'
            f"(allow file-read* {allow_reads})"
            f"(allow file-read-metadata {metadata})"
            "(deny file-write*)"
            f"(allow file-write* (subpath {json.dumps(str(workspace))}) (literal \"/dev/null\"))")


def environment(workspace: Path, executable_paths: list[Path]) -> dict[str, str]:
    for directory in (workspace / ".home", workspace / ".tmp", workspace / ".cache"):
        directory.mkdir(exist_ok=True)
    return {"PATH": ":".join(str(p) for p in executable_paths) + ":/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin",
            "HOME": str(workspace / ".home"), "TMPDIR": str(workspace / ".tmp"),
            "XDG_CACHE_HOME": str(workspace / ".cache"),
            "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            "JAVA_TOOL_OPTIONS": f"-XX:-UsePerfData -Djava.io.tmpdir={workspace / '.tmp'} -Duser.home={workspace / '.home'}"}


def run(command: list[str], *, cwd: Path, env: dict[str, str], sandbox: str | None = None,
        input_text: str | None = None, timeout: float | None = None) -> dict:
    args = (["/usr/bin/sandbox-exec", "-p", sandbox] if sandbox else []) + command
    process = subprocess.Popen(args, cwd=cwd, env=env, stdin=subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace",
                               start_new_session=True)
    timed_out = False
    try:
        stdout, stderr = process.communicate(input_text, timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
    return {"returncode": process.returncode, "stdout": stdout, "stderr": stderr,
            "timed_out": timed_out}
