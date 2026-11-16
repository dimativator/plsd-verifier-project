"""Use Codex CLI as a text-only model backend for mini-SWE-agent."""

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import subprocess
import signal
import time


DISABLED_FEATURES = (
    "shell_tool", "unified_exec", "apps", "plugins", "multi_agent", "computer_use",
    "browser_use", "in_app_browser", "image_generation", "workspace_dependencies",
    "goals", "hooks", "plugin_hooks", "memories", "shell_snapshot", "code_mode",
    "code_mode_host", "deferred_executor", "token_budget", "current_time_reminder",
    "request_permissions_tool", "tool_search", "tool_suggest", "standalone_web_search",
    "skill_search", "skill_mcp_dependency_install", "terminal_visualization_instructions",
)


@dataclass(frozen=True)
class CodexConfig:
    model_name: str
    reasoning_effort: str
    codex_home: str
    log_dir: str
    executable: str = "/opt/homebrew/bin/codex"


def prepare_codex_home(path: Path) -> None:
    """Reuse CLI login without copying tokens or loading the user's configuration."""
    path.mkdir(parents=True, exist_ok=True)
    auth = Path.home() / ".codex" / "auth.json"
    if not auth.is_file():
        raise FileNotFoundError("Codex CLI auth.json is missing. Log in with codex login first.")
    link = path / "auth.json"
    if not link.exists():
        link.symlink_to(auth)
    if not link.is_symlink() or link.resolve() != auth.resolve():
        raise ValueError("Unexpected authentication file in isolated Codex home")
    config = {
        "features": {name: False for name in DISABLED_FEATURES},
        "web_search": "disabled",
        "project_doc_max_bytes": 0,
        "include_environment_context": False,
        "include_permissions_instructions": False,
        "include_collaboration_mode_instructions": False,
        "include_apps_instructions": False,
    }
    lines = [f"{key} = {json.dumps(value)}" for key, value in config.items() if key != "features"]
    lines += ["[features]"] + [f"{name} = false" for name in DISABLED_FEATURES]
    lines += ["[tools.update_plan]", "enabled = false", "[tools.experimental_request_user_input]", "enabled = false",
              "[skills]", "include_instructions = false"]
    # json.dumps emits JSON booleans, which are also valid TOML booleans.
    (path / "config.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")


class CodexModel:
    def __init__(self, config: CodexConfig):
        self.config = config
        self.call_count = 0
        self.last_usage = {}

    def _completion(self, messages: list[dict]) -> str:
        self.call_count += 1
        logs = Path(self.config.log_dir)
        logs.mkdir(parents=True, exist_ok=True)
        prefix = logs / f"call-{self.call_count:03d}"
        env = {key: value for key, value in os.environ.items()
               if key not in {"OPENAI_API_KEY", "OPENAI_BASE_URL", "CODEX_THREAD_ID"}}
        env["CODEX_HOME"] = self.config.codex_home
        with prefix.with_suffix(".stderr.txt").open("w") as stderr, \
                prefix.with_suffix(".events.jsonl").open("w") as events:
            process = subprocess.Popen(
                [self.config.executable, "app-server", "--stdio"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr,
                text=True, cwd=self.config.codex_home, env=env, start_new_session=True)
            try:
                def send(message: dict) -> None:
                    process.stdin.write(json.dumps(message) + "\n")
                    process.stdin.flush()

                def receive() -> dict:
                    line = process.stdout.readline()
                    if not line:
                        raise RuntimeError(f"Codex CLI closed its output. See {prefix}.stderr.txt")
                    item = json.loads(line)
                    events.write(line)
                    events.flush()
                    if "method" in item and "id" in item:
                        # A model backend must never fulfill tools, approval, or user-input requests.
                        send({"id": item["id"], "error": {"code": -32601, "message": "Tools are disabled in the model-only backend"}})
                        raise RuntimeError(f"Unexpected Codex server request: {item['method']}")
                    method = item.get("method", "")
                    if method == "model/rerouted":
                        raise RuntimeError(f"Codex rerouted the requested model: {item.get('params')}")
                    if method in {"item/started", "item/completed"}:
                        kind = item.get("params", {}).get("item", {}).get("type", "")
                        if kind not in {"userMessage", "agentMessage", "reasoning"}:
                            raise RuntimeError(f"Unexpected Codex item: {kind}")
                    if item.get("error"):
                        raise RuntimeError(f"Codex CLI error: {item['error']}")
                    return item

                def response(request_id: int) -> dict:
                    while True:
                        item = receive()
                        if item.get("id") == request_id:
                            return item["result"]

                send({"id": 1, "method": "initialize", "params": {
                    "clientInfo": {"name": "plsd_model_only", "version": "0.1.0"},
                    "capabilities": {"experimentalApi": True}}})
                response(1)
                send({"method": "initialized", "params": {}})
                system = "\n\n".join(message["content"] for message in messages if message["role"] == "system")
                send({"id": 2, "method": "thread/start", "params": {
                    "model": self.config.model_name, "allowProviderModelFallback": False,
                    "baseInstructions": system, "developerInstructions": "",
                    "ephemeral": True, "environments": [], "dynamicTools": [],
                    "approvalPolicy": "never", "sandbox": "read-only",
                    "config": {"model_reasoning_effort": self.config.reasoning_effort},
                    "experimentalRawEvents": False}})
                thread = response(2)
                if thread["model"] != self.config.model_name:
                    raise RuntimeError(f"Model changed: {thread['model']}")
                conversation = [{"role": message["role"], "content": message.get("content", "")}
                                for message in messages if message["role"] != "system"]
                prompt = ("The following JSON array is the complete conversation with your mini-SWE-agent harness. "
                          "Continue it with exactly one assistant response. Its command will be executed by mini-SWE-agent.\n\n"
                          + json.dumps(conversation, ensure_ascii=False))
                send({"id": 3, "method": "turn/start", "params": {
                    "threadId": thread["thread"]["id"], "environments": [],
                    "model": self.config.model_name, "effort": self.config.reasoning_effort,
                    "input": [{"type": "text", "text": prompt, "text_elements": []}]}})
                response(3)
                content = []
                while True:
                    item = receive()
                    method, params = item.get("method"), item.get("params", {})
                    if method == "item/completed" and params.get("item", {}).get("type") == "agentMessage":
                        content.append(params["item"]["text"])
                    elif method == "thread/tokenUsage/updated":
                        self.last_usage = params.get("tokenUsage", {})
                    elif method == "turn/completed":
                        turn = params["turn"]
                        if turn["status"] != "completed":
                            raise RuntimeError(f"Codex turn failed: {turn}")
                        break
                if not content:
                    raise RuntimeError("Codex returned no assistant text")
                text = "\n".join(content)
                prefix.with_suffix(".response.txt").write_text(text, encoding="utf-8")
                return text
            finally:
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.wait()

    def query(self, messages: list[dict], **kwargs) -> dict:
        import re
        from minisweagent.exceptions import FormatError
        content = self._completion(messages)
        actions = re.findall(r"```(?:mswea_bash_command|bash)\s*\n(.*?)\n```", content, re.DOTALL)
        extra = {"cost": 0.0, "cost_status": "not_reported_by_codex_cli", "timestamp": time.time(),
                 "usage": self.last_usage, "codex_native_tools_enabled": False}
        if len(actions) != 1:
            raise FormatError(
                {"role": "assistant", "content": content, "extra": extra},
                {"role": "user", "content": "Return exactly one mswea_bash_command code block. To finish, run echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT."})
        extra["actions"] = [{"command": actions[0]}]
        return {"role": "assistant", "content": content, "extra": extra}

    def format_message(self, **kwargs) -> dict:
        return kwargs

    def format_observation_messages(self, message: dict, outputs: list[dict], template_vars: dict | None = None) -> list[dict]:
        return [{"role": "user", "content": json.dumps(output, ensure_ascii=False)[:24000]} for output in outputs]

    def get_template_vars(self, **kwargs) -> dict:
        return asdict(self.config)

    def serialize(self) -> dict:
        return {"info": {"config": {"model": asdict(self.config), "model_type": "pilot.codex_model.CodexModel"},
                         "model_backend": "codex_cli_app_server_no_environment_no_tools"}}
