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

`rules/common/` (모든 platform) 또는 `rules/<platform>/` 에 마크다운 파일 하나를 추가한다. 파일명이 룰 ID 다.

```markdown
---
severity: error          # error | warning
applies_to: "**/*.kt"    # 적용 대상 glob
---

# 규칙 한 줄

## 이유
## 위반
## 수정
```

새 platform(ktor·kmp 등)은 `rules/<platform>/` 디렉터리를 만들고 설정의 `platform` 값을 그 이름으로 지정한다.

## 테스트

```
python3 tests/test_on_write.py
```
