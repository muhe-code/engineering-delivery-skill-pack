#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_SESSIONS_ROOT = Path.home() / ".codex" / "sessions"
DEFAULT_OUTPUT_ROOT = Path.home() / "codex-skill-retrospectives"
DEFAULT_SKILLS_ROOT = Path.home() / ".codex" / "skills"
TEXT_TYPES = {"input_text", "output_text"}
TOOL_CALL_TYPES = {"function_call", "custom_tool_call", "web_search_call"}
TOOL_OUTPUT_TYPES = {"function_call_output", "custom_tool_call_output"}
FAIL_RE = re.compile(r"Process exited with code (\d+)")
TOKEN_RE = re.compile(r"`([a-z0-9][a-z0-9-]*)`|\$([a-z0-9][a-z0-9-]*)")

GUIDANCE_RULES = {
    "completion_discipline": ("完成", "闭环", "不要停", "端到端", "done-means-done"),
    "intent_alignment": ("不懂我", "没懂我", "不通人意", "不是我想要", "机械", "真实意图"),
    "acceptance_specificity": ("验收", "测试用例", "用例", "交互", "视觉效果", "特殊案例"),
    "scope_control": ("只更新", "范围", "全局", "关联技能", "子技能", "孙技能"),
    "evidence_and_verification": ("验证", "证据", "不要包装", "真实路径", "对账"),
}

ISSUE_RULES = {
    "misunderstood_intent": ("不懂我", "没懂我", "不通人意", "不是我想要", "没理解"),
    "premature_completion": ("不要停", "匆匆交付", "别包装成", "可选"),
    "acceptance_gap": ("大量bug", "测试用例", "验收", "特殊案例", "视觉效果"),
    "real_path_gap": ("正式地址", "手机", "真实路径", "新建后", "已有对象"),
    "external_truth_gap": ("外部事实", "真相源", "对账", "外部系统"),
    "scope_confusion": ("只更新", "范围", "全局", "project-hub"),
}

UPDATE_SURFACES = {
    "misunderstood_intent": ["project-hub", "spec-to-ship", "done-means-done"],
    "premature_completion": ["done-means-done", "verification-before-completion"],
    "acceptance_gap": [
        "acceptance-test-design",
        "stateful-product-validation",
        "spec-to-ship",
        "done-means-done",
    ],
    "real_path_gap": ["stateful-product-validation", "spec-to-ship", "done-means-done"],
    "external_truth_gap": [
        "external-system-reconciliation",
        "spec-to-ship",
        "done-means-done",
    ],
    "scope_confusion": ["project-hub", "spec-to-ship"],
}


@dataclass
class MessageRecord:
    timestamp: str
    role: str
    text: str


@dataclass
class ToolFailure:
    timestamp: str
    tool_type: str
    tool_name: str
    exit_code: int | None
    snippet: str


@dataclass
class SessionSummary:
    session_id: str
    session_file: str
    date: str
    cwd: str
    source: str
    started_at: str
    messages: list[MessageRecord]
    tool_calls: dict[str, int]
    tool_failures: list[ToolFailure]
    error_count: int
    aborted_turns: int
    skill_hits: list[str]
    guidance_signals: dict[str, int]
    issue_signals: dict[str, int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a transcript and summary bundle for session-driven skill evolution."
    )
    parser.add_argument("--session-id", action="append", default=[], help="Session id to include.")
    parser.add_argument("--date", default=None, help="Single date in YYYY-MM-DD.")
    parser.add_argument("--date-from", default=None, help="Start date in YYYY-MM-DD.")
    parser.add_argument("--date-to", default=None, help="End date in YYYY-MM-DD.")
    parser.add_argument("--latest", type=int, default=0, help="Most recent N session files.")
    parser.add_argument("--sessions-root", default=str(DEFAULT_SESSIONS_ROOT))
    parser.add_argument("--skills-root", action="append", default=[], help="Skill roots for hit detection.")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--output-name", default=None)
    return parser.parse_args()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_text(content: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for item in content:
        if item.get("type") in TEXT_TYPES and item.get("text"):
            parts.append(str(item["text"]))
    return normalize(" ".join(parts))


def load_skill_names(roots: list[Path]) -> set[str]:
    names: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        for skill_md in root.rglob("SKILL.md"):
            names.add(skill_md.parent.name)
    return names


def extract_skill_hits(text: str, known_skills: set[str]) -> set[str]:
    hits: set[str] = set()
    lowered = text.lower()
    for skill in known_skills:
        if skill.lower() in lowered:
            hits.add(skill)
    for match in TOKEN_RE.finditer(text):
        token = match.group(1) or match.group(2)
        if token in known_skills:
            hits.add(token)
    return hits


def apply_rules(text: str, rules: dict[str, tuple[str, ...]]) -> Counter[str]:
    counter: Counter[str] = Counter()
    lowered = text.lower()
    for label, patterns in rules.items():
        if any(pattern.lower() in lowered for pattern in patterns):
            counter[label] += 1
    return counter


def date_from_path(session_file: Path, sessions_root: Path) -> str:
    rel = session_file.relative_to(sessions_root)
    return f"{rel.parts[0]}-{rel.parts[1]}-{rel.parts[2]}"


def select_files(args: argparse.Namespace, sessions_root: Path) -> list[Path]:
    files = sorted(sessions_root.rglob("*.jsonl"))
    chosen: list[Path] = []
    ids = set(args.session_id)
    if ids:
        for path in files:
            if any(session_id in path.name for session_id in ids):
                chosen.append(path)
    elif args.date:
        chosen = [path for path in files if date_from_path(path, sessions_root) == args.date]
    elif args.date_from or args.date_to:
        start = args.date_from or "0000-01-01"
        end = args.date_to or "9999-12-31"
        chosen = [
            path
            for path in files
            if start <= date_from_path(path, sessions_root) <= end
        ]
    else:
        count = args.latest or 1
        chosen = files[-count:]
    return sorted(chosen)


def parse_session_file(session_file: Path, sessions_root: Path, known_skills: set[str]) -> SessionSummary:
    session_id = session_file.stem.split("-")[-1]
    cwd = ""
    source = ""
    started_at = ""
    messages: list[MessageRecord] = []
    tool_calls: Counter[str] = Counter()
    tool_failures: list[ToolFailure] = []
    skill_hits: set[str] = set()
    guidance_signals: Counter[str] = Counter()
    issue_signals: Counter[str] = Counter()
    error_count = 0
    aborted_turns = 0
    tool_names_by_call_id: dict[str, str] = {}
    tool_types_by_call_id: dict[str, str] = {}

    with session_file.open() as fh:
        for raw_line in fh:
            obj = json.loads(raw_line)
            payload = obj.get("payload") or {}
            item_type = obj.get("type")
            ts = obj.get("timestamp", "")

            if item_type == "session_meta":
                session_id = payload.get("id", session_id)
                cwd = payload.get("cwd", "")
                source = payload.get("source", "")
                started_at = payload.get("timestamp", "")
                continue

            if item_type == "event_msg" and payload.get("type") == "turn_aborted":
                aborted_turns += 1
                continue

            if item_type != "response_item" or not isinstance(payload, dict):
                continue

            payload_type = payload.get("type")

            if payload_type == "message":
                role = payload.get("role", "")
                text = extract_text(payload.get("content") or [])
                if not text:
                    continue
                if role == "user" and text.startswith("<environment_context>"):
                    continue
                messages.append(MessageRecord(timestamp=ts, role=role, text=text))
                skill_hits |= extract_skill_hits(text, known_skills)
                if role == "user":
                    guidance_signals.update(apply_rules(text, GUIDANCE_RULES))
                    issue_signals.update(apply_rules(text, ISSUE_RULES))
                continue

            if payload_type in TOOL_CALL_TYPES:
                tool_name = payload.get("name") or payload.get("tool_name") or payload_type
                call_id = payload.get("call_id") or payload.get("id") or f"{ts}:{tool_name}"
                tool_calls[tool_name] += 1
                tool_names_by_call_id[call_id] = str(tool_name)
                tool_types_by_call_id[call_id] = str(payload_type)
                continue

            if payload_type in TOOL_OUTPUT_TYPES:
                call_id = payload.get("call_id") or payload.get("id") or ""
                tool_name = tool_names_by_call_id.get(call_id, "unknown")
                tool_type = tool_types_by_call_id.get(call_id, payload_type)
                output = normalize(str(payload.get("output") or ""))
                match = FAIL_RE.search(output)
                exit_code = int(match.group(1)) if match else None
                if exit_code not in (None, 0):
                    tool_failures.append(
                        ToolFailure(
                            timestamp=ts,
                            tool_type=tool_type,
                            tool_name=tool_name,
                            exit_code=exit_code,
                            snippet=output[:300],
                        )
                    )
                continue

            if payload_type == "error":
                error_count += 1
                continue

    return SessionSummary(
        session_id=session_id,
        session_file=str(session_file),
        date=date_from_path(session_file, sessions_root),
        cwd=cwd,
        source=source,
        started_at=started_at,
        messages=messages,
        tool_calls=dict(tool_calls),
        tool_failures=tool_failures,
        error_count=error_count,
        aborted_turns=aborted_turns,
        skill_hits=sorted(skill_hits),
        guidance_signals=dict(guidance_signals),
        issue_signals=dict(issue_signals),
    )


def render_transcript(sessions: list[SessionSummary]) -> str:
    lines: list[str] = ["# Transcript", ""]
    for session in sessions:
        lines.append(f"## Session `{session.session_id}`")
        lines.append("")
        lines.append(f"- File: `{session.session_file}`")
        lines.append(f"- Date: `{session.date}`")
        if session.cwd:
            lines.append(f"- CWD: `{session.cwd}`")
        lines.append("")
        for message in session.messages:
            heading = "User" if message.role == "user" else "Assistant"
            lines.append(f"### {heading} [{message.timestamp}]")
            lines.append("")
            lines.append(message.text)
            lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_summary(sessions: list[SessionSummary], selectors: dict[str, Any]) -> str:
    guidance_totals: Counter[str] = Counter()
    issue_totals: Counter[str] = Counter()
    tool_totals: Counter[str] = Counter()
    failure_count = 0
    candidate_updates: Counter[str] = Counter()

    for session in sessions:
        guidance_totals.update(session.guidance_signals)
        issue_totals.update(session.issue_signals)
        tool_totals.update(session.tool_calls)
        failure_count += len(session.tool_failures) + session.error_count + session.aborted_turns
        for issue, count in session.issue_signals.items():
            for skill in UPDATE_SURFACES.get(issue, []):
                candidate_updates[skill] += count

    lines: list[str] = ["# Session Retrospective Summary", ""]
    lines.append("## Selection")
    lines.append("")
    lines.append(f"- Sessions: {len(sessions)}")
    for key, value in selectors.items():
        if value:
            lines.append(f"- {key}: {value}")
    lines.append("")

    lines.append("## User Guidance Signals")
    lines.append("")
    if guidance_totals:
        for label, count in guidance_totals.most_common():
            lines.append(f"- {label}: {count}")
    else:
        lines.append("- none detected")
    lines.append("")

    lines.append("## Codex Issue Signals")
    lines.append("")
    if issue_totals:
        for label, count in issue_totals.most_common():
            lines.append(f"- {label}: {count}")
    else:
        lines.append("- none detected")
    lines.append("")

    lines.append("## Execution Surface")
    lines.append("")
    lines.append(f"- total_tool_calls: {sum(tool_totals.values())}")
    lines.append(f"- failure_events: {failure_count}")
    if tool_totals:
        for name, count in tool_totals.most_common(10):
            lines.append(f"- tool `{name}`: {count}")
    lines.append("")

    lines.append("## Candidate Skill Update Surfaces")
    lines.append("")
    if candidate_updates:
        for skill, count in candidate_updates.most_common():
            lines.append(f"- `{skill}`: {count}")
    else:
        lines.append("- no candidate surfaces inferred")
    lines.append("")

    lines.append("## Per-Session Notes")
    lines.append("")
    for session in sessions:
        lines.append(f"### `{session.session_id}`")
        lines.append(f"- file: `{session.session_file}`")
        lines.append(f"- cwd: `{session.cwd}`")
        lines.append(f"- skill_hits: {', '.join(session.skill_hits) or '(none)'}")
        lines.append(f"- guidance_signals: {json.dumps(session.guidance_signals, ensure_ascii=False)}")
        lines.append(f"- issue_signals: {json.dumps(session.issue_signals, ensure_ascii=False)}")
        lines.append(f"- tool_failures: {len(session.tool_failures)}")
        for failure in session.tool_failures[:5]:
            lines.append(
                f"- failure_snippet [{failure.tool_name} exit={failure.exit_code}]: `{failure.snippet}`"
            )
        if session.error_count:
            lines.append(f"- response_errors: {session.error_count}")
        if session.aborted_turns:
            lines.append(f"- aborted_turns: {session.aborted_turns}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def make_output_dir(output_root: Path, output_name: str | None) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    dirname = output_name or f"{stamp}-session-skill-retrospective"
    out = output_root / dirname
    out.mkdir(parents=True, exist_ok=True)
    return out


def main() -> int:
    args = parse_args()
    sessions_root = Path(args.sessions_root).expanduser()
    output_root = Path(args.output_root).expanduser()
    skills_roots = [Path(p).expanduser() for p in args.skills_root] or [DEFAULT_SKILLS_ROOT]
    known_skills = load_skill_names(skills_roots)
    selected_files = select_files(args, sessions_root)
    if not selected_files:
        raise SystemExit("No session files matched the requested selectors.")

    sessions = [
        parse_session_file(path, sessions_root=sessions_root, known_skills=known_skills)
        for path in selected_files
    ]

    output_dir = make_output_dir(output_root, args.output_name)
    transcript_path = output_dir / "transcript.md"
    summary_path = output_dir / "summary.md"
    json_path = output_dir / "sessions.json"

    selectors = {
        "session_id": ",".join(args.session_id),
        "date": args.date,
        "date_from": args.date_from,
        "date_to": args.date_to,
        "latest": args.latest or None,
    }

    transcript_path.write_text(render_transcript(sessions))
    summary_path.write_text(render_summary(sessions, selectors))
    json_path.write_text(
        json.dumps(
            {
                "selectors": selectors,
                "skills_roots": [str(p) for p in skills_roots],
                "sessions": [asdict(session) for session in sessions],
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    print(str(output_dir))
    print(str(json_path))
    print(str(transcript_path))
    print(str(summary_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
