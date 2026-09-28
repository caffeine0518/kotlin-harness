"""python3 tests/test_on_write.py"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "hooks" / "on_write.py"


def run(project: Path, file_path: str) -> subprocess.CompletedProcess:
    # 실제 rules/ 대신 project 아래 임시 룰 디렉터리를 CLAUDE_PLUGIN_ROOT 로 지정한다
    env = {**os.environ, "CLAUDE_PLUGIN_ROOT": str(project), "CLAUDE_PROJECT_DIR": str(project)}
    event = {"tool_input": {"file_path": file_path}}
    return subprocess.run(["python3", str(HOOK)], input=json.dumps(event), capture_output=True, text=True, env=env)


def write_cfg(project: Path, cfg: dict) -> None:
    (project / ".claude").mkdir(exist_ok=True)
    (project / ".claude" / "kotlin-harness.json").write_text(json.dumps(cfg))


with tempfile.TemporaryDirectory() as d:
    p = Path(d)
    (p / "rules" / "common").mkdir(parents=True)
    (p / "rules" / "android" / "category").mkdir(parents=True)
    (p / "rules" / "android" / "category" / "sample-rule.md").write_text("---\nseverity: error\n---\n")

    # 설정 파일이 없으면 출력 없음
    assert run(p, "A.kt").stdout == ""

    # onWrite 비활성화
    write_cfg(p, {"platform": "android", "review": {"onWrite": False}})
    assert run(p, "A.kt").stdout == ""

    # onWrite 활성화: .kt 는 카테고리 하위 룰까지 목록에 포함, 그 외 파일은 무시
    write_cfg(p, {"platform": "android", "review": {"onWrite": True}})
    out = json.loads(run(p, "FooViewModel.kt").stdout)
    assert "sample-rule.md" in out["hookSpecificOutput"]["additionalContext"]
    assert "-onwrite.md" in out["hookSpecificOutput"]["additionalContext"]
    assert run(p, "README.md").stdout == ""

    # excludeCategories: 제외한 카테고리의 룰은 목록에서 제외
    (p / "rules" / "common" / "other").mkdir()
    (p / "rules" / "common" / "other" / "other-rule.md").write_text("---\nseverity: warning\n---\n")
    write_cfg(p, {"platform": "android", "excludeCategories": ["category"], "review": {"onWrite": True}})
    ctx = json.loads(run(p, "A.kt").stdout)["hookSpecificOutput"]["additionalContext"]
    assert "other-rule.md" in ctx and "sample-rule.md" not in ctx

    # 하위 경로: "ui/view" 는 ui/view/ 만, "ui" 는 ui/ 전체를 제외
    for sub_dir in ("view", "compose"):
        (p / "rules" / "android" / "ui" / sub_dir).mkdir(parents=True)
        (p / "rules" / "android" / "ui" / sub_dir / f"{sub_dir}-rule.md").write_text("---\n---\n")
    write_cfg(p, {"platform": "android", "excludeCategories": ["ui/view"], "review": {"onWrite": True}})
    ctx = json.loads(run(p, "A.kt").stdout)["hookSpecificOutput"]["additionalContext"]
    assert "compose-rule.md" in ctx and "view-rule.md" not in ctx
    write_cfg(p, {"platform": "android", "excludeCategories": ["ui"], "review": {"onWrite": True}})
    ctx = json.loads(run(p, "A.kt").stdout)["hookSpecificOutput"]["additionalContext"]
    assert "compose-rule.md" not in ctx and "view-rule.md" not in ctx and "sample-rule.md" in ctx

    # 없는 카테고리 이름은 exit 1
    write_cfg(p, {"platform": "android", "excludeCategories": ["nope"], "review": {"onWrite": True}})
    assert run(p, "A.kt").returncode == 1

    # platform 생략: Android Gradle 플러그인이 있으면 android 룰 포함, 없으면 common 룰만
    write_cfg(p, {"review": {"onWrite": True}})
    ctx = json.loads(run(p, "A.kt").stdout)["hookSpecificOutput"]["additionalContext"]
    assert "other-rule.md" in ctx and "sample-rule.md" not in ctx
    (p / "app").mkdir()
    (p / "app" / "build.gradle.kts").write_text('plugins { alias(libs.plugins.android.application) }')
    ctx = json.loads(run(p, "A.kt").stdout)["hookSpecificOutput"]["additionalContext"]
    assert "sample-rule.md" in ctx

    # excludeRules: 룰 ID 로 룰 하나만 제외, 없는 룰 ID 는 exit 1
    write_cfg(p, {"excludeRules": ["android/category/sample-rule"], "review": {"onWrite": True}})
    ctx = json.loads(run(p, "A.kt").stdout)["hookSpecificOutput"]["additionalContext"]
    assert "sample-rule.md" not in ctx and "other-rule.md" in ctx
    write_cfg(p, {"excludeRules": ["android/category/nope"], "review": {"onWrite": True}})
    assert run(p, "A.kt").returncode == 1

    # projectRules: 디렉터리는 하위 .md 전체, 파일은 그 파일만 포함, 없는 경로는 exit 1
    (p / ".claude" / "rules" / "kotlin").mkdir(parents=True)
    (p / ".claude" / "rules" / "kotlin" / "naming.md").write_text("# 네이밍\n")
    (p / ".claude" / "rules" / "_conflicts.md").write_text("# 충돌\n")
    write_cfg(p, {"projectRules": [".claude/rules/kotlin"], "review": {"onWrite": True}})
    ctx = json.loads(run(p, "A.kt").stdout)["hookSpecificOutput"]["additionalContext"]
    assert "naming.md" in ctx and "_conflicts.md" not in ctx and "프로젝트 룰" in ctx
    write_cfg(p, {"projectRules": [".claude/rules/_conflicts.md"], "review": {"onWrite": True}})
    ctx = json.loads(run(p, "A.kt").stdout)["hookSpecificOutput"]["additionalContext"]
    assert "_conflicts.md" in ctx and "naming.md" not in ctx
    write_cfg(p, {"projectRules": [".claude/rules/nope"], "review": {"onWrite": True}})
    assert run(p, "A.kt").returncode == 1

    # 리포트 디렉터리에 .gitignore 생성
    assert (p / ".claude" / "kotlin-harness" / ".gitignore").read_text() == "*\n"

    # 지원하지 않는 platform 은 exit 1
    write_cfg(p, {"platform": "nope", "review": {"onWrite": True}})
    assert run(p, "A.kt").returncode == 1

print("ok")
