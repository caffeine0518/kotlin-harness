---
name: review
description: kotlin-harness 룰로 코틀린 코드를 리뷰하고, 위반을 수정해 커밋한다. 범위는 file <경로> | diff | branch [base] | pr [번호] | project 중 하나.
argument-hint: "[file <path> | diff | branch [base] | pr [number] | project]"
context: fork
---

# kotlin-harness 리뷰

인자: `$ARGUMENTS` (비어 있으면 `diff`)

## 1. 설정 확인

프로젝트 루트의 `.claude/kotlin-harness.json` 에서 `platform`, `excludeCategories`(선택), `review.autoFix`(선택, 기본값 `true`)를 읽는다. 파일이 없으면 아래 예시로 생성하라고 안내하고 중단한다.

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

## 4. 위반 수정과 커밋

`review.autoFix` 가 `false` 이면 이 단계를 건너뛰고 소스 파일을 수정하지 않는다.

### 수정 대상

- 룰의 `## 수정` 에 따라 수정 방법이 하나로 정해지는 위반만 수정한다.
- 아래 경우는 수정하지 않고, 리포트에 `수정하지 않음` 과 이유를 적는다.
  - 수정 방법이 여러 가지이고 어느 쪽이 맞는지 코드만으로 판정할 수 없는 경우 (예: `null` 일 때 기본값을 쓸지 예외를 발생시킬지)
  - 파일 밖의 호출부나 public API 시그니처를 함께 수정해야 하는 경우
- 위반과 관계없는 코드는 수정하지 않는다.

### 커밋

- git 리포가 아니거나, 리뷰를 시작할 때 대상 파일에 커밋되지 않은 변경이 있었으면 그 파일은 수정만 하고 커밋하지 않는다. 사용자의 작업 중인 변경이 함께 커밋되지 않게 하기 위해서다. 리포트에 이유를 적는다.
- 같은 이유로 수정한 변경을 커밋 하나로 묶는다. 같은 식에서 나온 위반 여러 건은 이유가 달라도 커밋 하나로 묶는다. 커밋할 파일은 `git add <경로>` 로 하나씩 지정하고, `git add -A`·`git add .` 는 사용하지 않는다.
- 리포트 파일은 커밋하지 않는다. 푸시하지 않는다.

### 커밋 메시지

룰을 모르는 사람도 무엇을 왜 수정했는지 알 수 있게 평문으로 적는다. 언어와 형식은 프로젝트의 기존 커밋 메시지를 따른다.

- 제목: 어떤 코드를 어떻게 수정했는지
- 본문: 수정하지 않았으면 어떤 문제가 생기는지, 수정한 파일
- 금지: 룰 ID·카테고리 이름, `룰 위반`·`N번째 룰` 같은 표현, 줄 번호 나열, `kotlin-harness` 등 도구 이름

```
# 금지
fix: common/null-safety/not-null-assertion 위반 수정 (Sample.kt:3, 6)

# 올바른 예
프로필 화면에서 닉네임이 없을 때 앱이 종료되지 않도록 수정

닉네임이 비어 있으면 강제 언래핑(!!)에서 NullPointerException 이 발생해
앱이 종료됐다. 닉네임이 없으면 기본 문구를 표시하도록 바꿨다.

- app/src/main/java/.../ProfileViewModel.kt
```

## 5. 리포트 작성

리뷰 결과를 프로젝트 루트의 `.claude/kotlin-harness/reports/<YYYYMMDD-HHMMSS>-<범위>.md` 에 아래 형식으로 작성한다 (예: `20260927-153000-branch.md`). 위반이 없어도 리포트를 작성한다.

````markdown
# kotlin-harness 리뷰 리포트

- 일시: 2026-09-27 15:30
- 범위: branch (base `main`, `a1b2c3d..e4f5g6h`)
- platform: android
- 제외한 카테고리: scope-functions (없으면 `없음`)
- 대상 파일: 12개 / 적용한 룰: 34개
- 결과: error 2건, warning 5건
- 수정: 5건 수정 (커밋 3개), 2건 수정하지 않음

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

- 처리: `수정함 (커밋 a1b2c3d)` | `수정함 (커밋하지 않음: 이유)` | `수정하지 않음: 이유` | `autoFix 비활성화`

## 허용으로 제외한 코드

| 위치 | 룰 ID | 해당한 허용 조건 |
|---|---|---|
| `.../Foo.kt:10` | common/null-safety/not-null-assertion | 근거를 주석으로 적은 `!!` |
````

- 위반 목록은 severity(`error` → `warning`), 같은 severity 안에서는 파일 경로·줄 번호 순으로 정렬한다.
- 룰에 해당하는 코드였지만 `## 허용` 에 해당해 보고하지 않은 코드는 `허용으로 제외한 코드` 에 기록한다. 없으면 이 섹션을 생략한다.

## 6. 결과 출력

리포트 경로, 요약, 생성한 커밋 목록만 출력한다.

```
리포트: .claude/kotlin-harness/reports/20260927-153000-branch.md
error 2건, warning 5건 (파일 12개, 룰 34개) / 5건 수정, 2건 수정하지 않음
[error] app/src/main/.../SyncManager.kt:42  common/coroutines/global-scope  수정함
...
커밋:
a1b2c3d 동기화 작업이 화면을 닫은 뒤에도 계속 실행되지 않도록 수정
```

위반 목록은 한 줄씩만 출력하고, 코드와 수정 제안은 리포트에만 적는다.
