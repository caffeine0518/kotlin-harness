# kotlin-harness

룰 기반 코틀린 프로젝트 리뷰용 Claude Code 플러그인. 현재 지원 platform: `android`

## 설치

```
/plugin marketplace add <이 리포 경로 또는 git URL>
/plugin install kotlin-harness@kotlin-harness
```

## 프로젝트 설정

프로젝트에 `.claude/kotlin-harness.json` 을 생성한다. 이 파일이 없으면 자동 리뷰는 동작하지 않는다.

```json
{
  "platform": "android",
  "excludeCategories": ["scope-functions"],
  "review": { "onWrite": true }
}
```

| 키 | 설명 |
|---|---|
| `platform` | `rules/` 아래 platform 디렉터리 이름. 현재 `android` |
| `excludeCategories` | 적용하지 않을 카테고리 목록 (선택). `rules/common/` 과 `rules/<platform>/` 에 같은 이름의 카테고리가 있으면 둘 다 제외한다. 없는 이름을 적으면 오류가 발생한다. 새로 추가된 카테고리는 자동으로 적용된다 |
| `review.autoFix` | 기본값 `true`. `/kotlin-harness:review` 가 위반을 수정하고 커밋한다. `false` 이면 수정하지 않는다. 두 경우 모두 리포트와 검수는 실행한다 |
| `review.onWrite` | `true` 이면 Claude 가 `.kt`/`.kts` 를 수정할 때마다 룰 확인을 요청한다 |

## 리뷰 시점

| 시점 | 방법 |
|---|---|
| Claude 가 코드를 쓸 때마다 | `review.onWrite: true` — `.kt`/`.kts` 수정 직후 룰 확인·수정을 Claude 에 요청 |
| 커밋되지 않은 변경 | `/kotlin-harness:review diff` |
| 브랜치 | `/kotlin-harness:review branch [base]` |
| PR | `/kotlin-harness:review pr [번호]` |
| 전체 프로젝트 | `/kotlin-harness:review project` |
| 파일 하나 | `/kotlin-harness:review file <경로>` |

## 위반 수정과 리포트

`/kotlin-harness:review` 는 기본적으로 위반을 수정하고 커밋한다.

- 수정 방법이 하나로 정해지는 위반만 수정한다. 기본값을 쓸지 예외를 발생시킬지처럼 판단이 필요한 위반은 리포트에만 남긴다.
- 같은 이유로 수정한 변경을 커밋 하나로 묶고, 커밋 메시지는 룰을 모르는 사람도 알 수 있게 평문으로 적는다. 룰 ID 는 커밋 메시지에 적지 않는다.
- 리뷰를 시작할 때 커밋되지 않은 변경이 있던 파일은 수정만 하고 커밋하지 않는다. 작업 중인 변경이 함께 커밋되지 않게 하기 위해서다. 따라서 `diff` 범위에서는 대부분 커밋되지 않는다.
- 푸시하지 않는다.

리뷰가 끝나면 별도 에이전트가 검수한다. 검수 에이전트는 리뷰 에이전트의 판단을 참고하지 않고, 리포트·코드·git 이력만으로 아래를 확인한다.

| 검수 항목 | 확인 내용 |
|---|---|
| 누락 | 모든 룰을 코드에 다시 대조해, 리포트에 없는 위반이나 수정이 완료되지 않은 위반이 없는지 |
| 항목별 처리 결과 | `수정함` 항목의 커밋이 실제로 그 코드를 수정했는지, `수정하지 않음` 의 이유가 타당한지 |
| 변경 범위 | 위반과 관계없는 변경, 작업 중인 파일이나 리포트 파일의 커밋, 푸시가 없는지 |
| 커밋 메시지 | 룰 ID 없이 평문으로 적었는지 |
| 리포트 형식 | 요약·집계·목록의 건수가 일치하는지 |

검수에서 문제가 나오면 새 에이전트가 문제를 반영한 뒤 한 번 더 검수한다. 2회차에도 남은 문제는 리포트의 `검수 결과` 섹션에 기록하고 사용자에게 알린다.

리뷰 결과는 `.claude/kotlin-harness/reports/<일시>-<범위>.md` 에 작성한다. 리포트에는 룰별 집계, 위반마다 위치·코드·근거 문서·수정 제안·처리 결과(커밋 해시 또는 수정하지 않은 이유), `## 허용` 에 해당해 제외한 코드가 포함된다. 리포트를 커밋하지 않으려면 프로젝트의 `.gitignore` 에 `.claude/kotlin-harness/reports/` 를 추가한다.

`onWrite` 훅으로 확인한 결과는 `.claude/kotlin-harness/reports/<YYYYMMDD>-onwrite.md` 에 확인할 때마다 한 행씩 기록한다. 위반이 없어도 기록한다.

## 룰 추가

`rules/common/` (모든 platform) 또는 `rules/<platform>/` 에 카테고리 디렉터리를 만들고 룰마다 마크다운 파일 하나를 추가한다. `rules/` 기준 상대 경로가 룰 ID 다 (예: `rules/common/null-safety/safe-cast.md` → `common/null-safety/safe-cast`).

```markdown
---
severity: error          # error: 버그·누수로 이어짐 | warning: 그 외
applies_to: "**/*.kt"    # 적용 대상 glob
source: https://...      # 근거 문서. common 룰은 공식 문서만 허용
---

# 규칙 한 줄

## 이유
## 위반     # don't
## 수정     # do
## 허용     # 위반으로 보지 않는 경우 (선택)
```

린터(ktlint·detekt)가 검사하는 네이밍·포맷팅 항목은 룰로 추가하지 않는다.

| 카테고리 | 룰 |
|---|---|
| null-safety | `not-null-assertion`, `platform-type-explicit`, `nullable-boolean-condition`, `safe-cast`, `filter-not-null` |
| immutability | `data-class-mutable-collection`, `expose-read-only-view`, `prefer-val`, `read-only-collection-factory`, `read-only-collection-type` |
| exceptions | `catch-order`, `error-function`, `exception-object-declaration`, `nothing-return-type`, `precondition-functions`, `try-expression`, `use-for-closeable` |
| coroutines | `cancel-custom-scope`, `cooperative-cancellation`, `global-scope`, `rethrow-cancellation-exception`, `run-blocking-in-suspend`, `shared-mutable-state` |
| types | `closed-state-as-sealed`, `data-class-body-property`, `enum-lookup-or-null`, `value-class-over-typealias`, `when-else-on-sealed` |
| scope-functions | `context-object-reference`, `let-elvis-null-result`, `nested-lambda-implicit-it`, `nested-scope-functions`, `scope-function-return-value` |
| collections | `combined-transformation`, `empty-collection-element`, `filter-then-terminal`, `remove-while-iterating`, `sequence-for-multi-step-chain`, `sorted-by-descending` |

새 platform(ktor·kmp 등)은 `rules/<platform>/` 디렉터리를 만들고 설정의 `platform` 값을 그 이름으로 지정한다.

## 테스트

```
python3 tests/test_on_write.py
```
