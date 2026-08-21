"""Tests for MCP runtime enable/disable and gateway meta-tools."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from router.mcp_runtime import (
    McpRuntimeError,
    disable_server,
    enable_server,
    load_desired_enabled,
    runtime_status,
)
from router.mcp_providers import set_server_enabled

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTIT_CLI = REPO_ROOT / "agentit"
GATEWAY = REPO_ROOT / "mcp" / "gateway.py"


class McpRuntimeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.project = Path(self.tmpdir.name)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_enable_disable_project_provider(self) -> None:
        plan = enable_server(
            "context7",
            project_root=self.project,
            providers=["project"],
            apply=False,
        )
        self.assertEqual(plan["action"], "enable")
        self.assertFalse(plan["apply"])
        self.assertEqual(plan["provider_results"][0]["status"], "planned")

        applied = enable_server(
            "context7",
            project_root=self.project,
            providers=["project"],
            apply=True,
        )
        self.assertTrue(applied["apply"])
        mcp_json = self.project / ".mcp.json"
        self.assertTrue(mcp_json.is_file())
        data = json.loads(mcp_json.read_text(encoding="utf-8"))
        self.assertIn("context7", data["mcpServers"])
        self.assertIn("context7", load_desired_enabled(self.project))

        disabled = disable_server(
            "context7",
            project_root=self.project,
            providers=["project"],
            apply=True,
        )
        self.assertEqual(disabled["action"], "disable")
        data2 = json.loads(mcp_json.read_text(encoding="utf-8"))
        entry = data2["mcpServers"].get("context7")
        self.assertTrue(entry is None or entry.get("disabled") is True)
        self.assertNotIn("context7", load_desired_enabled(self.project))

    def test_risk3_requires_force(self) -> None:
        with self.assertRaises(McpRuntimeError):
            enable_server(
                "postgres",
                project_root=self.project,
                providers=["project"],
                apply=True,
                force=False,
            )
        ok = enable_server(
            "postgres",
            project_root=self.project,
            providers=["project"],
            apply=True,
            force=True,
        )
        self.assertEqual(ok["server_id"], "postgres")

    def test_status_shape(self) -> None:
        st = runtime_status(project_root=self.project, providers=["project"])
        self.assertIn("available", st)
        self.assertIn("desired_enabled", st)
        self.assertTrue(st["policy"]["agent_may_toggle"])

    def test_cli_status(self) -> None:
        proc = subprocess.run(
            [str(AGENTIT_CLI), "mcp", "status", "--project", str(self.project)],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(proc.stdout)
        self.assertIn("available", data)

    def test_cli_enable_apply_project_only(self) -> None:
        proc = subprocess.run(
            [
                str(AGENTIT_CLI),
                "mcp",
                "enable",
                "context7",
                "--providers",
                "project",
                "--project",
                str(self.project),
                "--apply",
            ],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(proc.stdout)
        self.assertEqual(data["action"], "enable")
        self.assertTrue((self.project / ".mcp.json").is_file())

    def test_cli_enable_stack_rejects_unknown_stack_instead_of_falling_back(self) -> None:
        proc = subprocess.run(
            [
                str(AGENTIT_CLI),
                "mcp",
                "enable-stack",
                "does-not-exist",
                "--providers",
                "project",
                "--project",
                str(self.project),
            ],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(REPO_ROOT),
        )

        self.assertNotEqual(0, proc.returncode)
        self.assertIn("unknown MCP stack", proc.stderr)
        self.assertNotIn('"stack": "developer_core"', proc.stdout)

    def test_gateway_self_test(self) -> None:
        proc = subprocess.run(
            ["python3", str(GATEWAY), "--self-test"],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(proc.stdout)
        self.assertIn("mcp_enable", data["tools"])
        self.assertIn("mcp_recommend", data["tools"])
        self.assertTrue(data["ok"])

    def test_gateway_tools_call_status(self) -> None:
        # One-shot JSON-RPC over stdin
        reqs = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "mcp_list_available",
                    "arguments": {"tier": "core"},
                },
            },
        ]
        payload = "\n".join(json.dumps(r) for r in reqs) + "\n"
        proc = subprocess.run(
            [
                "python3",
                str(GATEWAY),
                "--project",
                str(self.project),
                "--repo",
                str(REPO_ROOT),
            ],
            input=payload,
            capture_output=True,
            text=True,
            check=True,
            cwd=str(REPO_ROOT),
        )
        lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
        self.assertGreaterEqual(len(lines), 2)
        second = json.loads(lines[1])
        self.assertIn("result", second)
        text = second["result"]["content"][0]["text"]
        body = json.loads(text)
        ids = {s["id"] for s in body["servers"]}
        self.assertIn("context7", ids)
        self.assertIn("agentit-manager", ids)

    def test_gateway_recommend_uses_explicit_stack_id(self) -> None:
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "mcp_recommend",
                "arguments": {"stack_id": "developer_core"},
            },
        }
        proc = subprocess.run(
            [
                "python3",
                str(GATEWAY),
                "--project",
                str(self.project),
                "--repo",
                str(REPO_ROOT),
            ],
            input=json.dumps(req) + "\n",
            capture_output=True,
            text=True,
            check=True,
            cwd=str(REPO_ROOT),
        )
        response = json.loads(proc.stdout.strip())
        self.assertFalse(response["result"]["isError"])
        body = json.loads(response["result"]["content"][0]["text"])
        self.assertEqual(body["stack"], "developer_core")

    def test_gateway_recommend_rejects_task_text_contract(self) -> None:
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "mcp_recommend",
                "arguments": {"task": "implement figma design"},
            },
        }
        proc = subprocess.run(
            [
                "python3",
                str(GATEWAY),
                "--project",
                str(self.project),
                "--repo",
                str(REPO_ROOT),
            ],
            input=json.dumps(req) + "\n",
            capture_output=True,
            text=True,
            check=True,
            cwd=str(REPO_ROOT),
        )
        response = json.loads(proc.stdout.strip())
        self.assertTrue(response["result"]["isError"])
        self.assertIn("stack_id required", response["result"]["content"][0]["text"])

    def test_toml_upsert_via_provider_helpers(self) -> None:
        # project provider only for isolation — codex/grok touch $HOME
        r = set_server_enabled(
            "project",
            "playwright",
            enabled=True,
            project_root=self.project,
            apply=True,
        )
        self.assertEqual(r["status"], "applied")


if __name__ == "__main__":
    unittest.main()
