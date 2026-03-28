#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "resolve_skill_scope.py"


def write_skill(root: Path, name: str, body: str) -> None:
    skill_dir = root / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: test\n---\n\n{body}\n"
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "skills"
        write_skill(root, "project-hub", "Use `spec-to-ship`, `done-means-done`, and `acceptance-test-design`.")
        write_skill(root, "spec-to-ship", "May route to `acceptance-test-design`.")
        write_skill(root, "done-means-done", "No children.")
        write_skill(root, "acceptance-test-design", "Leaf.")

        result = subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "--skills-root",
                str(root),
                "--root-skill",
                "project-hub",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        closure = payload["closure"]
        assert closure == [
            "acceptance-test-design",
            "done-means-done",
            "project-hub",
            "spec-to-ship",
        ], closure
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
