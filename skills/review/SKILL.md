---
name: review
description: kotlin-harness 룰로 코틀린 코드를 리뷰한다. 범위는 file <경로> | diff | branch [base] | pr [번호] | project 중 하나.
argument-hint: "[file <path> | diff | branch [base] | pr [number] | project]"
context: fork
---

# kotlin-harness 리뷰

인자: `$ARGUMENTS` (비어 있으면 `diff`)

## 1. 설정 확인

프로젝트 루트의 `.claude/kotlin-harness.json` 에서 `platform` 을 읽는다. 파일이 없으면 아래 예시로 생성하라고 안내하고 중단한다.

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

룰 ID 는 `rules/` 기준 상대 경로(확장자 제외)다 (예: `common/null-safety/safe-cast`). frontmatter 의 `applies_to` glob 에 해당하는 파일에만 적용하고, `## 허용` 섹션에 해당하는 코드는 위반으로 보고하지 않는다.

## 4. 결과 보고

파일을 수정하지 않는다. 위반을 severity(`error` → `warning`) 순으로 정렬해 아래 형식으로 보고한다.

```
[error] app/src/main/.../Foo.kt:42  common/null-safety/safe-cast
  위반 내용 한 줄
  수정 제안 한 줄
```

위반이 없으면 `위반 없음 (룰 N개, 파일 M개)` 만 출력한다.
