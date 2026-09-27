#!/usr/bin/env python3
"""PostToolUse 훅: Claude 가 .kt/.kts 파일을 수정하면 적용할 룰 파일 목록을 컨텍스트로 전달한다.

프로젝트에 .claude/kotlin-harness.json 이 없거나 review.onWrite 가 true 가 아니면 아무것도 하지 않는다.
"""
import json
import os
import sys
from pathlib import Path


def main() -> int:
    event = json.load(sys.stdin)
    path = event.get("tool_input", {}).get("file_path", "")
    if not path.endswith((".kt", ".kts")):
        return 0

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or ".")
    try:
        cfg = json.loads((project / ".claude" / "kotlin-harness.json").read_text())
    except FileNotFoundError:
        return 0
    if not cfg.get("review", {}).get("onWrite"):
        return 0

    rules_root = Path(os.environ["CLAUDE_PLUGIN_ROOT"]) / "rules"
    platform = cfg.get("platform", "")
    if not platform or not (rules_root / platform).is_dir():
        print(f"kotlin-harness: 지원하지 않는 platform '{platform}'", file=sys.stderr)
        return 1

    # ponytail: applies_to 로 파일별 필터링하지 않고 common + platform 룰 전체를 전달한다. 룰이 많아지면 여기서 glob 필터링을 추가한다.
    dirs = [rules_root / "common", rules_root / platform]
    excluded = set(cfg.get("excludeCategories", []))
    unknown = excluded - {c.name for d in dirs if d.is_dir() for c in d.iterdir() if c.is_dir()}
    if unknown:
        print(f"kotlin-harness: 없는 카테고리 {sorted(unknown)} (excludeCategories)", file=sys.stderr)
        return 1

    rules = [r for d in dirs for r in sorted(d.rglob("*.md")) if r.relative_to(d).parts[0] not in excluded]
    if not rules:
        return 0

    msg = (
        f"kotlin-harness: `{path}` 이 수정되었습니다. 아래 룰 파일을 읽고, 이번 변경이 룰을 위반하면 수정하세요.\n"
        + "\n".join(f"- {r}" for r in rules)
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
