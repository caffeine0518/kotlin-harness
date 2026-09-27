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

## 리뷰 리포트

`/kotlin-harness:review` 를 실행하면 결과를 `.claude/kotlin-harness/reports/<일시>-<범위>.md` 에 작성한다. 리포트에는 룰별 집계, 위반마다 위치·코드·근거 문서·수정 제안, `## 허용` 에 해당해 제외한 코드가 포함된다. 리포트를 커밋하지 않으려면 프로젝트의 `.gitignore` 에 `.claude/kotlin-harness/reports/` 를 추가한다.

`onWrite` 훅은 리포트를 작성하지 않는다.

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
