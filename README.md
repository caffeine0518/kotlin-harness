<p align="center"><img src="assets/knight.svg" width="160" alt="칼을 바닥에 세우고 손잡이에 두 손을 얹은 기사 스케치"></p>

<h1 align="center">kotlin-harness</h1>

<p align="center"><em>Delegate the writing, fix the bar.</em></p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-plugin-111111?style=flat-square" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/kotlin-common-111111?style=flat-square" alt="kotlin common">
  <img src="https://img.shields.io/badge/platform-android-111111?style=flat-square" alt="platform android">
</p>

<p align="center"><sub>코드 작성은 계속 발전하는 AI 에 맡기고, 품질은 룰로 고정한다.</sub></p>

---


## Before / after

```kotlin
fun recentTags(posts: ArrayList<Post>): MutableList<String> {
    val result = ArrayList<Post>()
    for (post in posts) {
        if (post.isPublished ?: false) result.add(post)
    }
    val sorted = result.sortedBy { it.createdAt }.reversed()
    val tags = sorted.map { it.tags }.flatten()
    return tags.toMutableList()
}
```

```kotlin
fun recentTags(posts: List<Post>): List<String> =
    posts.filter { it.isPublished == true }
        .sortedByDescending { it.createdAt }
        .flatMap { it.tags }
```

<sub>적용 룰: [`read-only-collection-type`](rules/common/immutability/read-only-collection-type.md) · [`higher-order-function-over-loop`](rules/common/control-flow/higher-order-function-over-loop.md) · [`nullable-boolean-condition`](rules/common/null-safety/nullable-boolean-condition.md) · [`sorted-by-descending`](rules/common/collections/sorted-by-descending.md) · [`combined-transformation`](rules/common/collections/combined-transformation.md)</sub>

## 설치

```
/plugin marketplace add caffeine0518/kotlin-harness
```
```
/plugin install kotlin-harness@kotlin-harness
```

## 사용

코틀린 프로젝트에서 바로 실행한다. 설정 파일은 필요 없다.

| 범위 | 명령 |
|---|---|
| 브랜치 | `/kotlin-harness:gate branch [base]` |
| 커밋되지 않은 변경 | `/kotlin-harness:gate diff` |
| PR | `/kotlin-harness:gate pr [번호]` |
| 전체 프로젝트 | `/kotlin-harness:gate project` |
| 파일 하나 | `/kotlin-harness:gate file <경로>` |
| 맥락 힌트와 함께 | `/kotlin-harness:gate branch #123 docs/spec.md` |
| 오탐·누락 신고 | `/kotlin-harness:issue <문제 설명>` |



## 설정 (선택)

기본값을 바꿀 때만 `.claude/kotlin-harness.json` 을 만든다.

```json
{
  "excludeCategories": ["scope-functions"],
  "excludeRules": ["common/naming/meaningless-name"],
  "onWrite": ["common/null-safety/not-null-assertion", "android/ui/compose/state"],
  "minSeverity": "warning",
  "projectRules": [".claude/rules/kotlin"]
}
```

<details>
<summary><strong>전체 키</strong></summary>

| 키 | 설명 |
|---|---|
| `platform` | 기본값은 자동 판정. platform 이 없으면 common 룰만 적용한다 |
| `excludeCategories` | 제외할 카테고리 경로. `ui` 는 `ui/` 전체, `ui/view` 는 `ui/view/` 만 제외한다. common 과 platform 에 같은 경로가 있으면 둘 다 제외한다. 없는 이름이면 오류가 발생한다 |
| `excludeRules` | 제외할 룰 ID. 없는 ID 면 오류가 발생한다 |
| `onWrite` | 기본값 없음. Claude 가 `.kt`·`.kts` 를 수정할 때마다 확인할 룰 ID 또는 카테고리 경로. 지정한 룰만 확인하고 수정한다. gate 의 판정에는 영향이 없다 |
| `minSeverity` | 기본값 `info`. `error` 는 버그·누수·보안, `warning` 은 설계까지, `info` 는 표기 관례까지 적용한다. 프로젝트 룰에도 적용한다 |
| `projectRules` | 함께 적용할 프로젝트 룰의 디렉터리·파일 경로 (프로젝트 루트 기준). 기본값이 없으므로 `.claude/rules` 도 지정해야 적용된다 |
| `review.autoFix` | 기본값 `true`. `false` 면 수정하지 않고 리포트만 작성한다 |
| `review.redCommit` | 기본값 `true`. 실패하는 테스트를 먼저 커밋하고 수정을 따로 커밋한다. 그 커밋에서 CI 가 실패하므로, 원하지 않으면 `false` 로 지정해 커밋 하나로 묶는다 |
| `review.structureAutoFix` | 기본값 `true`. `structure` 카테고리 룰 위반을 상태 모델 등 접근 방식을 바꾸는 대안으로 수정한다. `false` 면 리포트에 대안만 적고, 그 코드 범위의 다른 룰 위반도 수정하지 않는다 |

</details>

<details>
<summary><strong>프로젝트 룰</strong></summary>

플러그인 룰로 일반화하지 않은 팀 규칙을 `projectRules` 로 지정하면 플러그인 룰과 같은 방식으로 리포트·수정한다.

- 형식은 자유다. `## ` 헤딩 하나가 룰 하나이고, 헤딩이 없으면 파일 전체가 룰 하나다. 룰 ID 는 `project/<경로>#<헤딩 번호 또는 헤딩>` 이다.
- 적용 대상은 frontmatter `paths`·`applies_to` 또는 본문의 적용 범위로 판정한다. 없으면 모든 `.kt`·`.kts` 에 적용한다.
- severity 는 frontmatter `severity` 가 없으면 `warning` 이다.
- 플러그인 룰과 반대되면 프로젝트 룰이 우선한다. 같은 코드를 같은 이유로 보고하면 한 항목으로 합친다.
- 규칙이 아닌 파일(충돌 기록·안내 문서)은 룰로 보지 않지만, 경로에서 제외하는 것이 확실하다.
- 룰 내용이 공개되지 않도록 프로젝트 룰의 결과는 `/kotlin-harness:issue` 로 등록하지 않는다.

</details>

<details>
<summary><strong>업데이트 · 개발 · 릴리스</strong></summary>

- 수동 업데이트: `claude plugin marketplace update kotlin-harness` 후 `claude plugin update kotlin-harness@kotlin-harness` 를 실행한다. `/reload-plugins` 로 현재 세션에 적용한다. 프롬프트 캐시 경고와 함께 적용되지 않으면 `/reload-plugins --force`.
- 로컬 개발: `claude --plugin-dir <이 리포 경로>`. 수정 후 세션을 다시 시작하면 반영된다.
- 릴리스: `.claude-plugin/plugin.json` 의 `version` 을 올리고 [CHANGELOG.md](CHANGELOG.md) 에 섹션을 추가한 뒤 푸시한다. `version` 이 바뀌지 않으면 업데이트가 전달되지 않는다.

</details>

## 룰

`rules/common/` (모든 platform) 또는 `rules/<platform>/` 아래에 룰마다 마크다운 파일 하나. `rules/` 기준 상대 경로가 룰 ID 다.

```markdown
---
severity: error          # error: 버그·누수·보안 | warning: 구조·API·생명주기·성능 | info: 표기 관례
applies_to: "**/*.kt"
source: https://...      # common 룰은 공식 문서만 허용
---

# 규칙 한 줄

## 이유
## 위반
## 수정
## 허용     # 위반으로 보지 않는 경우 (선택)
```

린터(ktlint·detekt)가 검사하는 네이밍·포맷팅은 룰로 추가하지 않는다. 새 platform 은 `rules/<platform>/` 을 만들고 설정의 `platform` 에 그 이름을 지정한다.