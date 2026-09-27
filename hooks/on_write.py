#!/usr/bin/env python3
"""PostToolUse 훅: Claude 가 .kt/.kts 파일을 수정하면 적용할 룰 파일 목록을 컨텍스트로 전달한다.

프로젝트에 .claude/kotlin-harness.json 이 없거나 review.onWrite 가 true 가 아니면 아무것도 하지 않는다.
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path


ANDROID_MARKERS = ("com.android.application", "com.android.library", "android.application", "android.library")


def detect_platform(project: Path) -> str:
    """루트와 모듈 한 단계의 build.gradle(.kts) 에 Android Gradle 플러그인이 있으면 android."""
    for build in [*project.glob("build.gradle*"), *project.glob("*/build.gradle*")]:
        if any(m in build.read_text(errors="ignore") for m in ANDROID_MARKERS):
            return "android"
    return ""


def ensure_ignored(project: Path) -> None:
    """리포트가 git 에 나타나지 않도록 .claude/kotlin-harness/ 에 .gitignore 를 만든다."""
    d = project / ".claude" / "kotlin-harness"
    d.mkdir(parents=True, exist_ok=True)
    if not (d / ".gitignore").exists():
        (d / ".gitignore").write_text("*\n")


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
    platform = cfg.get("platform") or detect_platform(project)
    if platform and not (rules_root / platform).is_dir():
        print(f"kotlin-harness: 지원하지 않는 platform '{platform}'", file=sys.stderr)
        return 1

    # ponytail: applies_to 로 파일별 필터링하지 않고 common + platform 룰 전체를 전달한다. 룰이 많아지면 여기서 glob 필터링을 추가한다.
    dirs = [rules_root / "common"] + ([rules_root / platform] if platform else [])
    # 카테고리는 하위 경로로도 지정할 수 있다 (예: "ui" 는 ui/ 전체, "ui/view" 는 ui/view/ 만)
    excluded = {c.strip("/") for c in cfg.get("excludeCategories", [])}
    unknown = {c for c in excluded if not any((d / c).is_dir() for d in dirs)}
    if unknown:
        print(f"kotlin-harness: 없는 카테고리 {sorted(unknown)} (excludeCategories)", file=sys.stderr)
        return 1

    rules = [
        r for d in dirs for r in sorted(d.rglob("*.md"))
        if not any(r.relative_to(d).as_posix().startswith(c + "/") for c in excluded)
    ]
    if not rules:
        return 0

    now = datetime.now()
    report = project / ".claude" / "kotlin-harness" / "reports" / f"{now:%Y%m%d}-onwrite.md"
    ensure_ignored(project)
    msg = (
        f"kotlin-harness: `{path}` 이 수정되었습니다. 아래 룰 파일을 읽고, 이번 변경이 룰을 위반하면 수정하세요.\n"
        + "\n".join(f"- {r}" for r in rules)
        + f"\n\n확인을 마치면 위반이 없어도 `{report}` 에 결과를 기록하세요. 파일이 없으면 헤더를 먼저 작성합니다.\n"
        "| 시각 | 파일 | 룰 ID | 위반 내용 | 처리 |\n|---|---|---|---|---|\n"
        f"위반마다 한 행을 추가하고, 위반이 없으면 룰 ID 를 `-`, 처리를 `위반 없음` 으로 한 행을 추가합니다. 시각은 {now:%H:%M:%S} 입니다."
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
