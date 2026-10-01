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
| `minSeverity` | `warning` |
| `excludeRules` | 없음 |
| `projectRules` | 없음 |
| `review.autoFix` | `true` |
| `review.redCommit` | `true` |

- git 리포에 `.kt`·`.kts` 파일이 하나도 없으면 코틀린 프로젝트가 아니라고 알리고 중단한다.
- `platform` 을 지정했는데 `${CLAUDE_PLUGIN_ROOT}/rules/<platform>/` 이 없으면 지원하지 않는 platform 이라고 알리고 중단한다.
- `excludeCategories` 의 값은 카테고리 경로다 (예: `ui` 는 `ui/` 전체, `ui/view` 는 `ui/view/` 만). `${CLAUDE_PLUGIN_ROOT}/rules/common/<경로>` 와 `rules/<platform>/<경로>` 가 모두 디렉터리가 아닌 값이 있으면 그 이름을 알리고 중단한다.
- `minSeverity` 의 값은 `error`·`warning`·`info` 중 하나다. 다른 값이면 그 값을 알리고 중단한다.
- `excludeRules` 의 값은 플러그인 룰 ID 다 (예: `common/naming/meaningless-name`). `${CLAUDE_PLUGIN_ROOT}/rules/<룰 ID>.md` 가 없는 값이 있으면 그 이름을 알리고 중단한다.
- `projectRules` 의 값은 프로젝트 루트 기준 디렉터리·파일 경로다 (예: `.claude/rules/kotlin`). 존재하지 않는 경로가 있으면 그 경로를 알리고 중단한다.

## 2. 시작 상태 기록

- 시작 커밋: `git rev-parse HEAD` (git 리포가 아니면 `없음`)
- 작업 중인 파일: `git status --porcelain` 에 나온 `.kt`·`.kts` 파일
- 리포트 경로: `.claude/kotlin-harness/reports/<YYYYMMDD-HHMMSS>-<범위>.md` (프로젝트 루트 기준, `date +%Y%m%d-%H%M%S`)
- `.claude/kotlin-harness/.gitignore` 가 없으면 내용 `*` 로 만든다. 리포트가 git 에 나타나지 않게 하기 위해서다.

## 3. 판정

룰 그룹마다 판정 에이전트를 병렬로 실행해 위반 후보를 모은다.

1. 적용할 룰 파일을 모은다. `rules/common`·`rules/<platform>` 에서 `excludeCategories`·`excludeRules` 를 제외한 룰 파일과 `projectRules` 의 파일이다. 그중 frontmatter `severity`(없으면 `warning`)가 `minSeverity` 보다 낮은 파일은 제외한다. 순서는 `error` > `warning` > `info` 다.
2. 룰 파일을 카테고리 디렉터리 단위로 묶어, 룰 수가 비슷한 그룹 3개로 나눈다. 카테고리 하나를 여러 그룹으로 나누지 않는다. 프로젝트 룰은 파일마다 `## ` 헤딩 수를 룰 수로 센다. 룰이 30개 미만이면 나누지 않고 그룹 1개로 둔다.
3. 한 메시지에서 그룹마다 general-purpose 에이전트를 하나씩 실행한다. 프롬프트에 `${CLAUDE_PLUGIN_ROOT}/skills/gate/detector.md` 를 읽고 따르라고 적고, 범위와 인자, 플러그인 경로, 1단계의 설정, 시작 커밋, 그 그룹의 룰 파일 목록을 전달한다.
4. 반환된 후보를 합친다. 같은 위치·같은 룰 ID 의 후보는 하나로 합친다.

에이전트 하나가 실패하면 그 그룹만 한 번 다시 실행한다. 다시 실패하면 그 그룹의 룰 파일 목록을 `판정하지 못한 룰` 로 4단계에 전달한다.

## 4. 수정

general-purpose 에이전트 하나를 실행한다. 프롬프트에 `${CLAUDE_PLUGIN_ROOT}/skills/gate/reviewer.md` 를 읽고 따르라고 적고, 범위와 인자, 플러그인 경로 `${CLAUDE_PLUGIN_ROOT}`, 1단계의 설정(`redCommit` 포함), 2단계의 값, 3단계에서 합친 후보 목록과 판정하지 못한 룰을 전달한다. 수정·커밋·리포트 작성은 이 에이전트 하나만 한다. 여러 에이전트가 같은 파일을 동시에 수정하지 않게 하기 위해서다.

## 5. 검수

수정 에이전트가 끝나면 general-purpose 에이전트 하나를 실행한다. 프롬프트에 `${CLAUDE_PLUGIN_ROOT}/skills/gate/verifier.md` 를 읽고 따르라고 적고, 4단계와 같은 값(후보 목록 제외)과 `회차: 1`, `기준 커밋: <시작 커밋>` 을 전달한다. 수정 에이전트의 반환 내용은 전달하지 않는다. 검수는 리포트·코드·git 이력만 근거로 해야 한다.

## 6. 반영과 재검수

검수가 문제를 반환하면 아래를 최대 2회 반복한다. 문제가 없으면 멈춘다.

1. `HEAD` 를 기록한다. 이번 회차의 기준 커밋이다.
2. 새 general-purpose 에이전트를 실행해 `reviewer.md` 의 5단계를 따르게 한다. 4단계의 값(후보 목록 제외)과 이번 회차의 문제 목록, 회차 번호를 전달한다.
3. 새 general-purpose 에이전트를 실행해 `verifier.md` 를 따르게 한다. 5단계의 값에 다음 회차 번호와 1에서 기록한 기준 커밋을 전달한다. 재검수는 기준 커밋 이후 바뀐 줄과, 이번 회차에 반영한 항목만 확인한다.

- 같은 위치·같은 룰의 문제가 이전 회차에 이어 다시 나오면 그 문제는 더 반영하지 않는다. 판정이 에이전트마다 달라지거나, 두 룰 사이에서 수정이 오가는 경우다. 7단계에 `반복되어 중단` 으로 표시한다.
- 2회를 반복한 뒤에도 남은 문제는 반영하지 않고 7단계에 표시한다.

## 7. 결과 출력

리포트를 읽고 아래만 출력한다.

```
리포트: .claude/kotlin-harness/reports/20260927-153000-branch.md
error 2건, warning 5건, info 0건 (파일 12개, 룰 34개) / 5건 수정, 2건 수정하지 않음
[error] app/src/main/.../SyncManager.kt:42  common/coroutines/global-scope  수정함
...
커밋:
a1b2c3d 동기화 작업이 화면을 닫은 뒤에도 계속 실행되지 않도록 수정
커밋하지 않은 수정 (리뷰 시작 시 작업 중이던 파일, 작업 중인 변경과 함께 작업 트리에 있음):
app/src/main/.../ProfileScreen.kt  2건
검수: 1회차 문제 3건 → 3건 반영, 2회차 문제 없음
```

- `커밋하지 않은 수정` 은 `수정함 (커밋하지 않음: …)` 항목이 있는 파일과 건수다. 없으면 이 부분을 생략한다. 있으면 마지막에 `git diff <파일>` 로 확인한 뒤 작업 중인 변경과 함께 커밋하라고 안내한다.
- 반영하지 않았거나 반복되어 중단했거나 회차 제한으로 남은 문제가 있으면, 그 목록과 사유를 함께 출력한다. 판정하지 못한 룰이 있으면 그 목록도 출력한다. 코드와 수정 제안은 리포트에만 적는다.

마지막 줄에 `결과에 문제가 있으면 /kotlin-harness:issue 로 등록할 수 있습니다.` 를 출력한다.
