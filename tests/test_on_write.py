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
    assert run(p, "README.md").stdout == ""

    # 지원하지 않는 platform 은 exit 1
    write_cfg(p, {"platform": "nope", "review": {"onWrite": True}})
    assert run(p, "A.kt").returncode == 1

print("ok")
