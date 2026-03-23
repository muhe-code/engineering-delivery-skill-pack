#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="在仓库中初始化 spec-to-ship 文档脚手架。"
    )
    parser.add_argument("--feature", required=True, help="功能名称或特性名称")
    parser.add_argument(
        "--slug",
        help="可选文件标识。默认根据 --feature 自动生成。",
    )
    parser.add_argument(
        "--repo-root",
        help="可选仓库根目录。默认使用当前 git 根目录，若不存在则使用当前目录。",
    )
    parser.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="写入模板的日期字符串，默认是今天。",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="若目标文件已存在则覆盖，而不是直接失败。",
    )
    return parser.parse_args()


def detect_repo_root(explicit_root: str | None) -> Path:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()

    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        return Path(proc.stdout.strip()).resolve()
    except Exception:
        return Path.cwd().resolve()


def slugify(text: str) -> str:
    normalized = text.strip().lower().replace("_", "-")
    slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", normalized)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "feature"


def render_template(template: str, feature_name: str, feature_slug: str, date: str) -> str:
    return (
        template.replace("{{FEATURE_NAME}}", feature_name)
        .replace("{{FEATURE_SLUG}}", feature_slug)
        .replace("{{DATE}}", date)
    )


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} 已存在")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo_root = detect_repo_root(args.repo_root)
    skill_root = Path(__file__).resolve().parent.parent
    templates_root = skill_root / "assets" / "templates"

    feature_name = args.feature.strip()
    feature_slug = args.slug or slugify(feature_name)

    targets = {
        repo_root / "docs" / "product" / "01-requirements" / f"{feature_slug}.md":
            templates_root / "requirements-template.md",
        repo_root / "docs" / "product" / "02-prd" / f"{feature_slug}.md":
            templates_root / "prd-template.md",
        repo_root / "docs" / "engineering" / "03-tech-spec" / f"{feature_slug}.md":
            templates_root / "tech-spec-template.md",
        repo_root / "docs" / "engineering" / "04-plan" / f"{feature_slug}.md":
            templates_root / "implementation-plan-template.md",
        repo_root
        / "docs"
        / "engineering"
        / "05-execution"
        / f"{feature_slug}-tracker.md": templates_root / "execution-tracker-template.md",
    }

    created: list[Path] = []
    try:
        for target, template_path in targets.items():
            template = template_path.read_text(encoding="utf-8")
            content = render_template(template, feature_name, feature_slug, args.date)
            write_file(target, content, args.force)
            created.append(target)
    except FileExistsError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    print(f"仓库根目录={repo_root}")
    print(f"功能标识={feature_slug}")
    for path in created:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
