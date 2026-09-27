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
{ "platform": "android", "review": { "onWrite": true } }
```

## 리뷰 시점

| 시점 | 방법 |
|---|---|
| Claude 가 코드를 쓸 때마다 | `review.onWrite: true` — `.kt`/`.kts` 수정 직후 룰 확인·수정을 Claude 에 요청 |
| 커밋되지 않은 변경 | `/kotlin-harness:review diff` |
| 브랜치 | `/kotlin-harness:review branch [base]` |
| PR | `/kotlin-harness:review pr [번호]` |
| 전체 프로젝트 | `/kotlin-harness:review project` |
| 파일 하나 | `/kotlin-harness:review file <경로>` |

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

새 platform(ktor·kmp 등)은 `rules/<platform>/` 디렉터리를 만들고 설정의 `platform` 값을 그 이름으로 지정한다.

## 테스트

```
python3 tests/test_on_write.py
```
