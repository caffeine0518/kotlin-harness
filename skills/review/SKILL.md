---
name: review
description: kotlin-harness 룰로 코틀린 코드를 리뷰한다. 범위는 file <경로> | diff | branch [base] | pr [번호] | project 중 하나.
argument-hint: "[file <path> | diff | branch [base] | pr [number] | project]"
context: fork
---

# kotlin-harness 리뷰

인자: `$ARGUMENTS` (비어 있으면 `diff`)

## 1. 설정 확인

프로젝트 루트의 `.claude/kotlin-harness.json` 에서 `platform` 과 `excludeCategories`(선택)를 읽는다. 파일이 없으면 아래 예시로 생성하라고 안내하고 중단한다.

```json
{ "platform": "android", "review": { "onWrite": false } }
```

## 2. 대상 파일 수집 (`.kt`, `.kts` 만)

| 범위 | 명령 | 리뷰 대상 |
|---|---|---|
| `file <경로>` | — | 파일 전체 |
| `diff` | `git diff HEAD` + `git ls-files --others --exclude-standard` | 커밋되지 않은 변경 줄 |
| `branch [base]` | `git diff $(git merge-base <base> HEAD)` (base 기본값 `main`) | 브랜치에서 변경된 줄 |
| `pr [번호]` | `gh pr diff [번호]` (번호가 없으면 현재 브랜치의 PR) | PR 에서 변경된 줄 |
| `project` | `git ls-files '*.kt' '*.kts'` | 파일 전체 |

변경 줄이 대상인 범위에서는 변경되지 않은 기존 코드의 위반을 결과에서 제외한다.

## 3. 룰 로드

- `${CLAUDE_PLUGIN_ROOT}/rules/common/**/*.md`
- `${CLAUDE_PLUGIN_ROOT}/rules/<platform>/**/*.md`

`excludeCategories` 에 적힌 카테고리 디렉터리(예: `rules/common/scope-functions/`)의 룰은 로드하지 않는다. 두 디렉터리 어디에도 없는 카테고리 이름이 있으면 그 이름을 알리고 중단한다.

룰 ID 는 `rules/` 기준 상대 경로(확장자 제외)다 (예: `common/null-safety/safe-cast`). frontmatter 의 `applies_to` glob 에 해당하는 파일에만 적용하고, `## 허용` 섹션에 해당하는 코드는 위반으로 보고하지 않는다.

## 4. 리포트 작성

소스 파일은 수정하지 않는다. 리뷰 결과를 프로젝트 루트의 `.claude/kotlin-harness/reports/<YYYYMMDD-HHMMSS>-<범위>.md` 에 아래 형식으로 작성한다 (예: `20260927-153000-branch.md`). 위반이 없어도 리포트를 작성한다.

````markdown
# kotlin-harness 리뷰 리포트

- 일시: 2026-09-27 15:30
- 범위: branch (base `main`, `a1b2c3d..e4f5g6h`)
- platform: android
- 제외한 카테고리: scope-functions (없으면 `없음`)
- 대상 파일: 12개 / 적용한 룰: 34개
- 결과: error 2건, warning 5건

## 룰별 집계

| 룰 ID | severity | 건수 |
|---|---|---|
| common/coroutines/global-scope | error | 2 |
| common/null-safety/not-null-assertion | warning | 3 |

## 위반 목록

### 1. [error] common/coroutines/global-scope

- 위치: `app/src/main/.../SyncManager.kt:42`
- 규칙: 룰 파일의 `#` 제목
- 근거: 룰의 `source` URL

```kotlin
// 위반한 코드. 앞뒤 2줄 정도를 포함한다
```

- 위반 내용: 이 코드가 룰을 위반하는 이유 한두 줄
- 수정 제안:

```kotlin
// 수정한 코드
```

## 허용으로 제외한 코드

| 위치 | 룰 ID | 해당한 허용 조건 |
|---|---|---|
| `.../Foo.kt:10` | common/null-safety/not-null-assertion | 근거를 주석으로 적은 `!!` |
````

- 위반 목록은 severity(`error` → `warning`), 같은 severity 안에서는 파일 경로·줄 번호 순으로 정렬한다.
- 룰에 해당하는 코드였지만 `## 허용` 에 해당해 보고하지 않은 코드는 `허용으로 제외한 코드` 에 기록한다. 없으면 이 섹션을 생략한다.

## 5. 결과 출력

리포트 경로와 요약만 출력한다.

```
리포트: .claude/kotlin-harness/reports/20260927-153000-branch.md
error 2건, warning 5건 (파일 12개, 룰 34개)
[error] app/src/main/.../SyncManager.kt:42  common/coroutines/global-scope
...
```

위반 목록은 한 줄씩만 출력하고, 코드와 수정 제안은 리포트에만 적는다.
