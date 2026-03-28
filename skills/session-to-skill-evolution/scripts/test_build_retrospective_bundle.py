#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "build_retrospective_bundle.py"


def make_session_file(path: Path) -> None:
    records = [
        {
            "timestamp": "2026-03-28T10:00:00.000Z",
            "type": "session_meta",
            "payload": {
                "id": "session-abc",
                "timestamp": "2026-03-28T09:59:59.000Z",
                "cwd": "/tmp/project",
                "source": "cli",
            },
        },
        {
            "timestamp": "2026-03-28T10:00:01.000Z",
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "请使用 $project-hub 深入分析这个 session，并更新相关技能。你之前没懂我，测试用例也不够。",
                    }
                ],
            },
        },
        {
            "timestamp": "2026-03-28T10:00:02.000Z",
            "type": "response_item",
            "payload": {
                "type": "function_call",
                "name": "exec_command",
                "call_id": "call-1",
                "arguments": "{\"cmd\":\"false\"}",
            },
        },
        {
            "timestamp": "2026-03-28T10:00:03.000Z",
            "type": "response_item",
            "payload": {
                "type": "function_call_output",
                "call_id": "call-1",
                "output": "Command: false\nProcess exited with code 1\nOutput:\n",
            },
        },
        {
            "timestamp": "2026-03-28T10:00:04.000Z",
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": "我会更新 `project-hub` 和 `spec-to-ship`。"}],
            },
        },
    ]
    with path.open("w") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def make_skills(root: Path) -> None:
    for name in ["project-hub", "spec-to-ship", "done-means-done"]:
        skill_dir = root / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(f"---\nname: {name}\ndescription: test\n---\n")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        sessions_root = tmp_root / "sessions" / "2026" / "03" / "28"
        sessions_root.mkdir(parents=True)
        make_session_file(sessions_root / "rollout-2026-03-28T10-00-00-session-abc.jsonl")
        skills_root = tmp_root / "skills"
        make_skills(skills_root)
        output_root = tmp_root / "out"

        result = subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "--session-id",
                "session-abc",
                "--sessions-root",
                str(tmp_root / "sessions"),
                "--skills-root",
                str(skills_root),
                "--output-root",
                str(output_root),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        out_dir = Path(result.stdout.splitlines()[0].strip())
        summary = (out_dir / "summary.md").read_text()
        transcript = (out_dir / "transcript.md").read_text()
        payload = json.loads((out_dir / "sessions.json").read_text())

        assert "misunderstood_intent" in summary
        assert "project-hub" in summary
        assert "请使用 $project-hub" in transcript
        assert payload["sessions"][0]["session_id"] == "session-abc"
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
