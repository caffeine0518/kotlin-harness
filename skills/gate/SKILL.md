---
name: gate
description: kotlin-harness 룰로 코틀린 코드를 리뷰하고, 위반을 수정해 커밋한다. 범위는 file <경로> | diff | branch [base] | pr [번호] | project 중 하나.
argument-hint: "[file <path> | diff | branch [base] | pr [number] | project]"
---

# kotlin-harness 리뷰

인자: `$ARGUMENTS` (비어 있으면 `diff`)

## 1. 설정 확인

프로젝트 루트의 `.claude/kotlin-harness.json` 을 읽는다. 파일이 없거나 키가 없으면 아래 기본값을 쓴다. 설정 파일을 만들지 않는다.

| 키 | 기본값 |
|---|---|
| `platform` | 자동 판정. 루트와 모듈 한 단계의 `build.gradle`·`build.gradle.kts` 에 `com.android.application`·`com.android.library`·`android.application`·`android.library` 가 있으면 `android`, 없으면 platform 없음(common 룰만 적용) |
| `excludeCategories` | 없음 |
| `review.autoFix` | `true` |
| `review.redCommit` | `false` |

- git 리포에 `.kt`·`.kts` 파일이 하나도 없으면 코틀린 프로젝트가 아니라고 알리고 중단한다.
- `platform` 을 지정했는데 `${CLAUDE_PLUGIN_ROOT}/rules/<platform>/` 이 없으면 지원하지 않는 platform 이라고 알리고 중단한다.
- `excludeCategories` 의 값은 카테고리 경로다 (예: `ui` 는 `ui/` 전체, `ui/view` 는 `ui/view/` 만). `${CLAUDE_PLUGIN_ROOT}/rules/common/<경로>` 와 `rules/<platform>/<경로>` 가 모두 디렉터리가 아닌 값이 있으면 그 이름을 알리고 중단한다.

## 2. 시작 상태 기록

- 시작 커밋: `git rev-parse HEAD` (git 리포가 아니면 `없음`)
- 작업 중인 파일: `git status --porcelain` 에 나온 `.kt`·`.kts` 파일
- 리포트 경로: `.claude/kotlin-harness/reports/<YYYYMMDD-HHMMSS>-<범위>.md` (프로젝트 루트 기준, `date +%Y%m%d-%H%M%S`)
- `.claude/kotlin-harness/.gitignore` 가 없으면 내용 `*` 로 만든다. 리포트가 git 에 나타나지 않게 하기 위해서다.

## 3. 리뷰

general-purpose 에이전트를 실행한다. 프롬프트에 `${CLAUDE_PLUGIN_ROOT}/skills/gate/reviewer.md` 를 읽고 따르라고 적고, 범위와 인자, 플러그인 경로 `${CLAUDE_PLUGIN_ROOT}`, 1단계의 설정(`redCommit` 포함), 2단계의 값을 전달한다.

## 4. 검수

리뷰 에이전트가 끝나면 새 general-purpose 에이전트를 실행한다. 프롬프트에 `${CLAUDE_PLUGIN_ROOT}/skills/gate/verifier.md` 를 읽고 따르라고 적고, 3단계와 같은 값을 전달한다. 검수는 한 번만 실행한다. 리뷰 에이전트의 반환 내용은 전달하지 않는다. 검수는 리포트·코드·git 이력만 근거로 해야 한다.

## 5. 검수 결과 반영

검수 에이전트가 문제를 반환하면 새 general-purpose 에이전트를 실행해 `reviewer.md` 의 5단계를 따르게 한다. 3단계의 값과 문제 목록을 전달한다. 반영한 뒤 다시 검수하지 않는다. 반영 결과는 리포트의 `## 검수 결과` 아래 `### 반영 결과` 에 기록되고, 6단계에서 사용자에게 알린다.

## 6. 결과 출력

리포트를 읽고 아래만 출력한다.

```
리포트: .claude/kotlin-harness/reports/20260927-153000-branch.md
error 2건, warning 5건 (파일 12개, 룰 34개) / 5건 수정, 2건 수정하지 않음
[error] app/src/main/.../SyncManager.kt:42  common/coroutines/global-scope  수정함
...
커밋:
a1b2c3d 동기화 작업이 화면을 닫은 뒤에도 계속 실행되지 않도록 수정
검수: 문제 2건 → 2건 반영
```

반영하지 못한 문제가 있으면 그 목록을 함께 출력한다. 코드와 수정 제안은 리포트에만 적는다.

마지막 줄에 `결과에 문제가 있으면 /kotlin-harness:issue 로 등록할 수 있습니다.` 를 출력한다.
