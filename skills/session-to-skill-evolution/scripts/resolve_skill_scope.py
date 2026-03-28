#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from collections import deque
from pathlib import Path


DEFAULT_SKILLS_ROOT = Path.home() / ".codex" / "skills"
TOKEN_RE = re.compile(r"`([a-z0-9][a-z0-9-]*)`|\$([a-z0-9][a-z0-9-]*)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve a recursive skill update scope from one or more root skills."
    )
    parser.add_argument(
        "--skills-root",
        action="append",
        default=[],
        help="Skill root to scan. Can be repeated.",
    )
    parser.add_argument(
        "--root-skill",
        action="append",
        default=[],
        help="Root skill name. Can be repeated.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Return all discovered skills instead of a recursive closure from roots.",
    )
    parser.add_argument(
        "--format",
        choices={"json", "text"},
        default="json",
        help="Output format.",
    )
    return parser.parse_args()


def discover_skill_files(roots: list[Path]) -> dict[str, list[Path]]:
    catalog: dict[str, list[Path]] = {}
    for root in roots:
        if not root.exists():
            continue
        for skill_md in root.rglob("SKILL.md"):
            name = skill_md.parent.name
            catalog.setdefault(name, []).append(skill_md.parent)
    return {name: sorted(paths) for name, paths in sorted(catalog.items())}


def extract_edges(catalog: dict[str, list[Path]]) -> dict[str, list[str]]:
    known = set(catalog)
    edges: dict[str, list[str]] = {}
    for name, paths in catalog.items():
        refs: set[str] = set()
        for path in paths:
            skill_md = path / "SKILL.md"
            if not skill_md.exists():
                continue
            text = skill_md.read_text()
            for match in TOKEN_RE.finditer(text):
                token = match.group(1) or match.group(2)
                if token and token in known and token != name:
                    refs.add(token)
        edges[name] = sorted(refs)
    return edges


def compute_closure(edges: dict[str, list[str]], roots: list[str]) -> list[str]:
    seen: set[str] = set()
    queue = deque(roots)
    while queue:
        current = queue.popleft()
        if current in seen:
            continue
        seen.add(current)
        for nxt in edges.get(current, []):
            if nxt not in seen:
                queue.append(nxt)
    return sorted(seen)


def format_text(payload: dict) -> str:
    lines: list[str] = []
    lines.append("Roots: " + (", ".join(payload["roots"]) or "(all)"))
    lines.append("Closure:")
    for item in payload["closure"]:
        lines.append(f"- {item}")
        for path in payload["skills"][item]["paths"]:
            lines.append(f"  path: {path}")
        if payload["skills"][item]["references"]:
            lines.append("  refs: " + ", ".join(payload["skills"][item]["references"]))
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    roots = [Path(p).expanduser() for p in args.skills_root] or [DEFAULT_SKILLS_ROOT]
    catalog = discover_skill_files(roots)
    edges = extract_edges(catalog)

    if args.all:
        closure = sorted(catalog)
        root_skills: list[str] = []
    else:
        root_skills = sorted(set(args.root_skill))
        missing = [name for name in root_skills if name not in catalog]
        if missing:
            raise SystemExit(f"Unknown root skill(s): {', '.join(missing)}")
        closure = compute_closure(edges, root_skills)

    payload = {
        "roots": root_skills,
        "skill_roots": [str(p) for p in roots],
        "closure": closure,
        "skills": {
            name: {
                "paths": [str(path) for path in catalog.get(name, [])],
                "references": edges.get(name, []),
            }
            for name in closure
        },
    }

    if args.format == "text":
        print(format_text(payload))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
