"""Docker isolation for agent actions and trusted evaluation controllers."""

import json
import re
from pathlib import Path
import subprocess
import threading
import time
import uuid

BASE_IMAGE = "plinse-eval:20261123"
VERIFIER_IMAGE = "plinse-crosshair:20261123"
OUTPUT_LIMIT = 4 * 1024 * 1024


def matches(actual: str, expected: str, checker: str = "tokens") -> bool:
    if checker == "tokens":
        return actual.split() == expected.split()
    if checker == "casefold_tokens":
        return actual.casefold().split() == expected.casefold().split()
    if checker == "integer_tokens":
        try:
            if not all(re.fullmatch(r"[+-]?[0-9]+", x) for x in actual.split() + expected.split()):
                return False
            return [int(x) for x in actual.split()] == [int(x) for x in expected.split()]
        except ValueError:
            return False
    raise ValueError(f"Unsupported checker: {checker}")


def run_isolated(
    workspace: Path,
    command: str,
    *,
    timeout: float = 60,
    input_text: str | None = None,
    image: str = BASE_IMAGE,
    persistent_tmp: bool = True,
) -> dict:
    workspace = Path(workspace).resolve()
    if not workspace.is_dir():
        raise ValueError("Workspace must be an existing directory")
    name = "plinse-" + uuid.uuid4().hex
    args = [
        "docker",
        "run",
        "--rm",
        "--name",
        name,
        "--network",
        "none",
        "--log-driver",
        "none",
        "--read-only",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--pids-limit",
        "128",
        "--cpus",
        "1",
        "--memory",
        "1g",
        "--memory-swap",
        "1g",
        "--user",
        "65534:65534",
        "--mount",
        f"type=bind,source={workspace},target=/work",
        "--workdir",
        "/work",
        "--env",
        "HOME=/tmp",
        "--env",
        "PYTHONDONTWRITEBYTECODE=1",
    ]
    if persistent_tmp:
        temporary = workspace / ".tmp"
        if temporary.is_symlink():
            raise ValueError("Reserved .tmp directory cannot be a symbolic link")
        try:
            temporary.mkdir()
        except FileExistsError:
            if not temporary.is_dir():
                raise ValueError("Reserved .tmp path must be a directory")
        else:
            # Only this newly created scratch directory changes permissions.
            # Native Linux bind mounts retain host ownership, unlike Windows.
            temporary.chmod(0o1777)
        if not temporary.resolve().is_relative_to(workspace):
            raise ValueError("Reserved .tmp directory must remain in the workspace")
        args += ["--mount", f"type=bind,source={temporary},target=/tmp"]
    else:
        args += ["--tmpfs", "/tmp:rw,noexec,nosuid,size=128m"]
    if input_text is not None:
        args.append("-i")
    args += [image, "/bin/bash", "-c", command]
    started = time.monotonic()
    try:
        process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        return {
            "returncode": 125,
            "stdout": "",
            "stderr": "docker: " + str(error)[:1000],
            "timed_out": False,
            "elapsed_seconds": time.monotonic() - started,
            "output_truncated": False,
            "infrastructure_error": {"type": "DockerLaunchError", "message": str(error)[:1000]},
        }
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    output_lock = threading.Lock()
    output_exceeded = threading.Event()

    def consume(pipe, label):
        try:
            while chunk := pipe.read(65536):
                with output_lock:
                    available = max(0, OUTPUT_LIMIT - sum(len(saved) for saved in buffers.values()))
                    buffers[label].extend(chunk[:available])
                    if len(chunk) > available:
                        output_exceeded.set()
                # Continue draining until termination, without retaining more data.
        finally:
            pipe.close()

    def feed():
        try:
            process.stdin.write(input_text.encode("utf-8"))
            process.stdin.flush()
        except (BrokenPipeError, OSError):
            pass
        finally:
            process.stdin.close()

    readers = [
        threading.Thread(target=consume, args=(process.stdout, "stdout"), daemon=True),
        threading.Thread(target=consume, args=(process.stderr, "stderr"), daemon=True),
    ]
    for reader in readers:
        reader.start()
    writer = threading.Thread(target=feed, daemon=True) if input_text is not None else None
    if writer:
        writer.start()

    def terminate_container():
        try:
            subprocess.run(
                ["docker", "rm", "-f", name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=20,
            )
        except (OSError, subprocess.TimeoutExpired):
            pass
        if process.poll() is None:
            process.kill()
        process.wait(timeout=10)

    timed_out = False
    try:
        while process.poll() is None:
            if output_exceeded.is_set():
                terminate_container()
                break
            if time.monotonic() - started >= timeout:
                timed_out = True
                terminate_container()
                break
            time.sleep(0.01)
    except BaseException:
        terminate_container()
        raise
    finally:
        for reader in readers:
            reader.join(timeout=10)
        if writer:
            writer.join(timeout=10)
    stdout = bytes(buffers["stdout"]).decode("utf-8", "replace")
    stderr = bytes(buffers["stderr"]).decode("utf-8", "replace")
    elapsed = time.monotonic() - started
    result = {
        "returncode": process.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "timed_out": timed_out,
        "elapsed_seconds": elapsed,
        "output_truncated": output_exceeded.is_set(),
    }
    diagnostic = stderr.lower()
    if (process.returncode in (125, 126, 127) and "docker" in diagnostic) or any(
        text in diagnostic
        for text in (
            "cannot connect to the docker daemon",
            "is the docker daemon running",
            "error during connect:",
        )
    ):
        result["infrastructure_error"] = {"type": "DockerLaunchError", "message": stderr[:1000]}
    return result


# Only inputs enter this private container; expected outputs stay on the host.
EVALUATOR = """import json,os,signal,subprocess,sys,tempfile,time
inputs=json.load(sys.stdin)
results=[]
for index,given in enumerate(inputs):
 started=time.monotonic()
 timed_out=False
 output_truncated=False
 with tempfile.TemporaryFile() as child_input,tempfile.TemporaryFile() as out,tempfile.TemporaryFile() as err:
  child_input.write(given.encode('utf-8'));child_input.seek(0)
  p=subprocess.Popen([sys.executable,'-B','main.py'],stdin=child_input,stdout=out,stderr=err,start_new_session=True)
  try:
   while True:
    output_truncated=os.fstat(out.fileno()).st_size>200000 or os.fstat(err.fileno()).st_size>10000
    if output_truncated:break
    if p.poll() is not None:break
    if time.monotonic()-started>=10:
     timed_out=True
     break
    time.sleep(.01)
  finally:
   try:os.killpg(p.pid,signal.SIGKILL)
   except ProcessLookupError:pass
   p.wait()
  output_truncated=output_truncated or os.fstat(out.fileno()).st_size>200000 or os.fstat(err.fileno()).st_size>10000
  out.seek(0);err.seek(0)
  stdout=out.read(200000).decode('utf-8','replace')
  stderr=err.read(3000).decode('utf-8','replace')
  results.append({'case':index,'returncode':124 if timed_out else p.returncode,'stdout':stdout,'stderr':stderr,'elapsed_seconds':time.monotonic()-started,'timed_out':timed_out,'output_truncated':output_truncated})
 if results[-1]['returncode']!=0 or results[-1]['output_truncated']:
  break
print(json.dumps(results))
"""


def evaluate_python(submission: Path, tests: dict, scratch: Path, checker: str = "tokens") -> dict:
    import ast
    import shutil

    if not tests.get("input") or len(tests["input"]) != len(tests.get("output", [])):
        raise ValueError("Hidden suite must be nonempty and aligned")
    if not submission.is_file() or submission.is_symlink():
        return {"passed": False, "stage": "missing_submission", "test_count": len(tests["input"])}
    try:
        ast.parse(submission.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeError) as error:
        return {
            "passed": False,
            "stage": "syntax_error",
            "error": str(error),
            "test_count": len(tests["input"]),
        }
    scratch.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(submission, scratch / "main.py")
    (scratch / "_evaluate.py").write_text(EVALUATOR, encoding="utf-8")
    executed = run_isolated(
        scratch,
        "python -B _evaluate.py",
        timeout=20 + 10 * len(tests["input"]),
        input_text=json.dumps(tests["input"]),
        persistent_tmp=False,
    )
    if executed.get("infrastructure_error"):
        return {
            "passed": False,
            "stage": "execution_worker",
            "worker": executed,
            "infrastructure_error": executed["infrastructure_error"],
            "test_count": len(tests["input"]),
        }
    if executed["returncode"] in (137, 143) or executed["timed_out"]:
        return {
            "passed": False,
            "stage": "execution_worker",
            "worker": executed,
            "test_count": len(tests["input"]),
        }
    if executed["returncode"] != 0 or executed["output_truncated"]:
        return {
            "passed": False,
            "stage": "execution_worker",
            "worker": executed,
            "infrastructure_error": {
                "type": "EvaluatorWorkerError",
                "message": "Trusted evaluator failed or exceeded its output limit",
            },
            "test_count": len(tests["input"]),
        }
    try:
        rows = json.loads(executed["stdout"])
        if not isinstance(rows, list) or not 1 <= len(rows) <= len(tests["input"]):
            raise ValueError("Unexpected evaluator row count")
        for index, row in enumerate(rows):
            if (
                not isinstance(row, dict)
                or row.get("case") != index
                or not isinstance(row.get("returncode"), int)
                or not isinstance(row.get("stdout"), str)
                or not isinstance(row.get("timed_out"), bool)
                or not isinstance(row.get("output_truncated"), bool)
            ):
                raise ValueError("Malformed evaluator row")
    except (ValueError, TypeError) as error:
        return {
            "passed": False,
            "stage": "execution_worker",
            "worker": executed,
            "infrastructure_error": {
                "type": "EvaluatorProtocolError",
                "message": str(error)[:1000],
            },
            "test_count": len(tests["input"]),
        }
    for row in rows:
        row["passed"] = (
            row["returncode"] == 0
            and not row["timed_out"]
            and not row["output_truncated"]
            and matches(row["stdout"], tests["output"][row["case"]], checker)
        )
    return {
        "passed": len(rows) == len(tests["input"]) and all(r["passed"] for r in rows),
        "stage": "hidden_tests",
        "test_count": len(tests["input"]),
        "executed_count": len(rows),
        "passed_count": sum(r["passed"] for r in rows),
        "elapsed_seconds": executed["elapsed_seconds"],
        "cases": rows,
    }
