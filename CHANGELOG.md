# Changelog

## 0.34.0
- gate 가 이번 변경의 맥락을 받는다. 세션 대화의 배경(고치려는 결함, 되돌린 접근, 정해진 동작·기획)을 요약하고, 범위 뒤에 적은 이슈·URL·파일·MCP 리소스 힌트를 읽는다 (예: `/kotlin-harness:gate branch #123 docs/spec.md`). 맥락은 영향·허용·구조 룰 대안을 판정하는 근거로만 쓰고, 새 위반을 찾는 데는 쓰지 않는다.
- 접근 방식을 다루는 `structure` 카테고리를 추가했다. 수정 에이전트는 구조 룰 위반을 먼저 판정하고, 그 코드 범위에는 다른 룰의 수정을 먼저 적용하지 않는다.
  - `android/ui/compose/structure/imperative-ui-after-state-transition`: `LaunchedEffect` 에서 상태 전이를 기다린 뒤 스크롤·포커스를 조작하는 코드를 판정하고, 상태 모델로 해결하는 대안으로 수정한다.
  - 설정 `review.structureAutoFix` (기본값 `true`). `false` 면 구조 룰 위반과 그 코드 범위의 위반을 수정하지 않고 리포트에 대안만 적는다.
- `android/ui/compose/performance/remember-expensive-calculation` 이 기존 식을 `remember` 로 감싸기만 한다. 키로만 쓰는 지역 변수를 추가하거나 식을 다시 쓰지 않는다.
- README 에서 자동 업데이트 안내를 삭제했다.

## 0.33.0
- `/kotlin-harness:update` 를 삭제했다. 업데이트는 `claude plugin marketplace update kotlin-harness` 후 `claude plugin update kotlin-harness@kotlin-harness` 로 실행한다.

## 0.32.1
- gate 의 판정·수정 에이전트 지침을 윤문했다. 동작은 바뀌지 않는다.
  - `reviewer.md`: 섹션마다 요약을 먼저 적고 세부 항목을 나열하도록 재구성하고, 긴 문장을 나눴다. 리포트 요약에 적을 설정 값을 템플릿에 넣었다.
  - `detector.md`: 반환 형식에 실제 값으로 채운 예시를 추가했다.

## 0.32.0
- `common/functions/named-arguments` 가 같은 기본 타입 파라미터가 둘 이상인 함수·생성자에 변수를 위치 인수로 전달한 호출도 보고한다. 리터럴만 보고해서, 같은 타입 변수 두 개의 순서가 바뀐 호출을 판정하지 못했다. 변수 이름이 다른 위치의 파라미터 이름과 같으면 순서가 바뀐 것으로 본다. `max(a, b)`·`Point(x, y)` 처럼 순서가 관례로 정해진 호출은 허용한다.
- gate 가 `방어용` 수정을 룰마다 커밋 하나로 묶고, 모듈이 다르면 커밋을 나눈다. 룰이 다른 수정이 한 커밋에 섞여 제목으로 구분할 수 없고 하나만 되돌릴 수 없었다.

## 0.31.0
- gate 의 검수·재검수 단계를 삭제했다. 룰이 늘면서 검수 에이전트 하나가 모든 룰을 변경된 줄에 대조하는 단계가 실행 시간의 대부분을 차지했다. 오탐은 수정 에이전트가 후보를 검증할 때 제외하고, 실제 문제는 red→green 테스트로 재현한다. 결과 출력에서 `검수:` 줄이 없어진다.
- `common/types/field-by-field-equality` 룰을 추가했다. 서로 다른 타입의 같은 이름 프로퍼티를 3개 이상 `&&` 로 이어 비교하는 함수를 판정하고, 비교 기준을 data class 로 선언해 `==` 로 비교하도록 수정한다.

## 0.30.0
- **설정 확인 필요.** `android/ui/compose` 룰 19개를 하위 카테고리 4개로 이동했다. 룰 ID 가 바뀌므로, 옛 ID 를 적은 `excludeRules` 는 없는 이름이 되어 gate 가 중단된다. 새 ID 로 바꾼다. `excludeCategories` 의 `ui/compose` 는 지금처럼 하위 카테고리 전체를 제외한다.
  - `android/ui/compose/api`: `composable-naming`, `emit-or-return`, `modifier-applied-once`, `modifier-parameter`, `remember-prefix`, `single-modifier-parameter`, `trailing-composable-lambda`
  - `android/ui/compose/side-effects`: `derived-state-of-captured-value`, `effect-captured-value`, `empty-on-dispose`, `launch-in-composition`, `lifecycle-effect`, `unnecessary-derived-state-of`
  - `android/ui/compose/performance`: `backwards-write`, `defer-state-read`, `lazy-item-key`, `remember-expensive-calculation`
  - `android/ui/compose/state`: `collect-as-state-with-lifecycle`, `viewmodel-parameter`
- `android/ui/compose/api/modifier-parameter` 가 마지막 파라미터인 `@Composable` 콘텐츠 람다를 `modifier` 뒤에 두는 코드를 위반으로 보고하지 않는다. `trailing-composable-lambda`·`single-modifier-parameter` 의 수정 예시와 충돌하던 판정을 바로잡았다.
- 룰 74개의 이유에서 "공식 문서는 ~라고 한다" 같은 출처 서술을 삭제했다. 근거는 frontmatter `source` 로 확인한다.
- `android/ui/compose` 룰 19개의 이유·예시를 다듬었다. 예시만 있던 위반 섹션에 위반 조건 문장을 추가하고, `lifecycle-effect` 에 `Activity` 콜백이 화면 단위 생명주기를 모르는 이유를, `unnecessary-derived-state-of` 에 `remember` 도 필요 없는 이유를 추가했다.

## 0.29.0
- **설정 확인 필요.** `android/coroutines/inject-test-dispatchers` 를 `android/test/inject-test-dispatchers` 로 이동했다. 옛 ID 를 적은 `excludeRules` 는 없는 이름이 되어 gate 가 중단되므로 새 ID 로 바꾼다. `excludeCategories` 의 `coroutines` 는 이 룰을 더 이상 제외하지 않고, `test` 가 제외한다.
- `android/coroutines/catch-exceptions-in-ui-scope` 가 `viewModelScope`·`lifecycleScope` 의 `launch` 호출을 감싼 `try`·`catch` 도 위반으로 보고한다. 같은 코드를 `common/coroutines/try-catch-around-launch` 로 중복 보고하지 않는다.
- `android/coroutines/main-safe-suspend-function` 이 ViewModel 에서 IO 디스패처로 전환하는 코드를 위반으로 보고한다. 블로킹 API 호출은 리포지토리 같은 데이터 레이어 클래스의 main-safe suspend 함수로 옮긴다. Default 디스패처로 CPU 작업을 하는 경우는 허용한다.
- `android/coroutines/unnecessary-dispatcher-switch` 가 `Dispatchers.*` 를 직접 지정한 불필요한 전환도 보고하고, `android/coroutines/inject-dispatchers` 는 이 코드를 보고하지 않는다. 두 룰이 같은 코드에 반대되는 수정(주입·삭제)을 제안하지 않는다.
- `android/data/immutable-exposed-model` 이 리포지토리의 `private set` 없는 `var` 프로퍼티와 `MutableStateFlow`·`MutableSharedFlow` 프로퍼티도 판정한다.
- `android/data/repository-naming` 이 데이터 소스를 조합하는 `Manager`·`Service`·`Helper` 클래스를 `data`·`repository` 패키지 밖에서도 판정한다.
- `android/test/state-flow-value-assertion` 이 빈 컬렉터를 요구하는 `stateIn` 을 `SharingStarted.WhileSubscribed()` 처럼 컬렉터가 있어야 시작하는 경우로 한정한다.
- `android` 룰 19개의 이유·예시를 다듬었다. 이유에서 출처 서술을 삭제하고, 위반 조건은 기준을 먼저 적은 뒤 예시를 나열한다. `use case` 표기를 `UseCase` 로 통일했다.
- README 를 개편했다. Before/after 예시와 사용·동작 요약을 앞에 두고, 설정·프로젝트 룰은 접어 두었다.

## 0.28.0
- `common/null-safety/not-null-assertion` 의 수정을 `null` 의 의미에 따라 나눴다. 정상적인 경우는 기본값·`if` 분기·조기 반환으로, 버그인 경우는 `checkNotNull`·`requireNotNull`·`getValue` 로 수정한다. 판정할 수 없으면 수정하지 않고 리포트에 사유와 수정 제안을 적는다.
- `common/functions/extension-visibility` 가 한 파일에서만 쓰는 익스텐션만 판정한다. 한 모듈에서만 쓰는 익스텐션에 `internal` 을 요구하지 않는다.
- `common/types/enum-lookup-or-null` 의 수정을 companion object 조회 함수(`fromName`·`fromPosition`·`fromCode`)로 바꿨다.
- `common` 룰 9개의 이유·예시를 사람과 판정 에이전트가 함께 읽기 쉽게 다듬었다: `closed-state-as-sealed`, `data-class-body-property`, `extract-long-receiver`, `if-else-over-let-elvis`, `let-elvis-null-result`, `mutating-function-name`, `property-over-function`, `value-class-over-typealias`, `when-else-on-sealed`.

## 0.27.0
- **설정 확인 필요.** 카테고리 2개를 Kotlin 문서 구성에 맞춰 이동했다. 룰 ID 가 바뀌므로, 옛 경로를 적은 `excludeCategories`·`excludeRules` 는 없는 이름이 되어 gate 가 중단된다. 새 경로로 바꾼다.
  - `common/flow` → `common/coroutines/flow`
  - `common/exceptions` → `common/control-flow/exceptions`
  - `excludeCategories` 에 `coroutines`·`control-flow` 를 적었으면 이동한 하위 카테고리도 함께 제외된다.
- `minSeverity` 기본값을 `warning` 에서 `info` 로 변경했다. 기본 설정에서 표기 관례 룰까지 모든 룰을 적용한다. 이전처럼 표기 관례 룰을 제외하려면 `"minSeverity": "warning"` 을 지정한다.
- gate 가 `방어용` 수정을 룰 카테고리마다가 아니라 실행 한 번에 커밋 하나로 묶는다. `실제 문제` 수정과 red 커밋은 지금처럼 분리한다.

## 0.26.0
- `common/exceptions/catch-order` 가 예외를 분기하는 `when` 의 `is` 분기 순서도 판정한다. `runCatching { }.onFailure { }`·예외 변환 함수에서 상위 타입의 분기가 하위 타입보다 앞에 있으면 보고한다. 같은 예외 계층을 여러 곳에서 분기하면 경계에서 sealed 타입으로 변환하는 방법을 수정에 선택지로 추가했다.
- `common/coroutines/cancel-custom-scope` 의 수정을 suspend 함수, 소유자 스코프 주입, 직접 생성 후 취소의 3단계로 나눴다. 기존 예시는 주입받은 스코프를 `close()` 에서 취소해 소유자의 스코프 전체를 취소했으므로 예시를 분리했다.
- `common/coroutines/cooperative-cancellation` 에 블로킹 I/O 를 `runInterruptible` 로 감싸는 수정과 `flow { }` 선택지를 추가했다. 취소를 확인하는 kotlinx.coroutines 함수를 호출하는 suspend 함수를 루프에서 호출하는 경우도 허용한다.
- `common/control-flow/guard-condition-parentheses` 에 긴 가드 조건을 이름 있는 프로퍼티·함수로 추출하는 수정을 추가했다.
- `common/coroutines/shared-mutable-state` 에서 `@Volatile` 이 읽기-수정-쓰기 연산에 효과가 없는 이유를 예시와 함께 설명했다.

## 0.25.0
- `common/collections/sequence-for-multi-step-chain` 이 중간 연산이 1개여도 끝의 연산과 함수 하나로 합칠 수 없으면 판정한다 (`map { }.first { }`·`filter { }.take(n)` 등). `filter { }.first()` 처럼 합칠 수 있는 체인은 지금처럼 허용하고 `filter-then-terminal` 룰로 수정한다.
- `common/collections/sorted-by-descending` 에 `sortedBy { }.reversed()` 와 `sortedByDescending { }` 은 정렬 키가 같은 요소의 순서가 다르다는 설명과, `thenBy { }` 로 두 번째 정렬 기준을 지정하는 방법을 추가했다. 키가 같은 요소의 순서가 원본의 역순이어야 하는 경우는 허용한다.
- `common/comments/history-comment` 가 테스트 함수·클래스에 붙은 주석이 그 테스트가 검출하는 회귀를 설명하면 이슈 링크 없이 허용한다. 이전 동작 서술이 섞인 주석은 삭제하지 않고 현재 보장하는 동작을 서술하는 문장으로 고친다. ([#10](https://github.com/caffeine0518/kotlin-harness/issues/10))
- gate 가 `방어용` 수정을 룰 카테고리마다 커밋 하나로 묶는다. `실제 문제` 수정과 red 커밋은 지금처럼 분리한다. 검수는 멤버 종류를 바꾼 수정을 멤버 배치 룰에도 대조한다. ([#9](https://github.com/caffeine0518/kotlin-harness/issues/9))

## 0.24.0
- severity 에 `info` 를 추가하고, 설정 `minSeverity`(기본값 `warning`)보다 낮은 룰은 판정하지 않는다. 기본 설정에서는 info 룰을 적용하지 않으므로, 이전처럼 모든 룰을 적용하려면 `"minSeverity": "info"` 를 지정한다.
- 표기 관례 룰 55개를 `warning` 에서 `info` 로 변경했다. `common` 의 `comments`·`control-flow`·`file-layout`·`functions`·`lambdas`·`naming`·`scope-functions`·`strings` 전체와, 다른 카테고리의 일부 룰(`android` 8개, `collections` 3개, `exceptions` 4개, `immutability` 3개, `null-safety` 2개)이다.
- 룰 3개를 `warning` 에서 `error` 로 변경했다: `android/security/store-user-password`, `common/exceptions/use-for-closeable`, `common/coroutines/run-blocking-in-suspend`.

## 0.23.0
- 룰 1개 추가. 기존 카테고리에 추가했으므로 `excludeCategories` 설정은 그대로 적용된다.
  - `common/scope-functions`: 리시버가 지역 `val`·파라미터인 `?.let { } ?: ...` 로 값을 고르는 경우. `if (x == null) a else f(x)` 로 작성한다.

## 0.22.0
- `common/types/closed-state-as-sealed` 가 Boolean·널러블 필드 여러 개의 조합으로 상태를 표현하는 코드도 판정한다. 같은 객체의 필드 두 개 이상을 조건으로 서로 배타적인 상태를 반환하거나 분기하는 `when`·`if` 가 대상이며, 서로 독립적인 필드는 허용한다.

## 0.21.0
- 룰 2개 추가. 모두 기존 카테고리에 추가했으므로 `excludeCategories` 설정은 그대로 적용된다.
  - `android/coroutines`: main-safe suspend 함수만 호출하면서 IO·Default 디스패처로 전환하는 경우 ([#8](https://github.com/caffeine0518/kotlin-harness/issues/8))
  - `android/ui/viewmodel`: ViewModel·상태 홀더의 `init` 블록·생성자에서 비동기 작업을 시작하는 경우. 함수로 추출해 `init` 에서 호출하는 경우도 포함한다. ([#7](https://github.com/caffeine0518/kotlin-harness/issues/7))
- `android/coroutines/inject-dispatchers` 의 예제를 새 룰에 해당하지 않도록 블로킹 파일 I/O 예제로 교체했다.

## 0.20.0
- 룰 2개 추가. 새 카테고리 `android/di` 는 기본으로 적용되므로, 원하지 않으면 `excludeCategories` 에 지정한다.
  - `android/di`: ViewModel·Repository·DataSource·use case 가 의존성을 직접 생성하는 경우
  - `android/test`: Fake 구현이 있는 타입을 mock·stub·spy 로 만드는 경우

## 0.19.0
- 룰 6개 추가. 모두 기존 카테고리에 추가했으므로 `excludeCategories` 설정은 그대로 적용된다.
  - `android/test`: `Dispatchers.setMain` 뒤 `resetMain` 복원 누락, 완료되지 않는 Flow 를 `backgroundScope` 밖에서 수집, `StateFlow` 를 수집한 값 목록으로 검증
  - `common/lambdas`: 마지막 인수인 람다를 괄호 안에 전달
  - `android/domain`: use case 에 공개 함수가 여러 개, use case 를 싱글턴 스코프로 제공
- README 의 룰 표를 `rules/` 디렉터리의 실제 카테고리·룰과 일치하도록 수정했다.

## 0.18.0
- `onWrite` 훅(`review.onWrite`)을 삭제했다. 이제 `python3` 가 필요하지 않다. 룰 확인은 `/kotlin-harness:gate` 로 실행한다.

## 0.17.0
- gate 실행 순서를 바꿨다. ([#6](https://github.com/caffeine0518/kotlin-harness/issues/6))
  - 판정: 룰 그룹 3개를 에이전트 3개가 병렬로 대조해 위반 후보만 반환한다 (새 지침 `detector.md`).
  - 수정: 에이전트 하나가 후보를 검증하고 영향 판정·테스트·수정·커밋·리포트 작성을 한다.
  - 검수: 룰 전체를 다시 대조하지 않고, 리포트 항목의 판정·처리가 맞는지와 gate 가 바꾼 줄에 새 위반이 없는지 확인한다.
  - 반영과 재검수: 검수가 문제를 찾으면 반영하고 바뀐 줄을 다시 검수한다. 최대 2회 반복하고, 같은 문제가 반복되면 멈춘다. 이전에는 반영한 수정을 검수하지 않았다.
- 0.16.0 의 검수 병렬화(#5)는 이 구조로 대체했다.

## 0.16.1
- 업데이트 후 Claude Code 를 다시 시작하지 않고 `/reload-plugins` 로 현재 세션에 적용하도록 안내를 바꿨다.

## 0.16.0
- 검수를 병렬로 실행한다. 누락 대조는 룰을 카테고리 단위로 룰 수가 비슷한 그룹 3개로 나눠 에이전트마다 하나씩 맡기고, 나머지 검수 항목은 에이전트 하나가 동시에 확인한다. 검수 결과는 gate 가 합쳐 리포트에 한 번 기록한다. 룰이 30개 미만이면 나누지 않는다. ([#5](https://github.com/caffeine0518/kotlin-harness/issues/5))

## 0.15.1
- `common/scope-functions/extract-long-receiver`: 람다가 `it`·`this` 를 한 번만 참조해도 위반으로 보고한다. `.let { println(it) }` 처럼 함수 하나에 전달하는 경우의 허용을 없애고, 메서드 참조만 허용한다. ([#3](https://github.com/caffeine0518/kotlin-harness/issues/3))
- 검수가 위반 조건에 해당하는데 위반 목록과 `허용으로 제외한 코드` 표 어디에도 없는 코드를 `허용 기록 누락` 으로 제기하고, 허용 표의 항목이 실제로 허용 조건에 해당하는지 확인한다. ([#4](https://github.com/caffeine0518/kotlin-harness/issues/4))

## 0.15.0
- `common/scope-functions/extract-long-receiver` 추가. 호출 체인 결과에 스코프 함수를 호출하고 람다에서 `it`·`this` 를 여러 번 쓰면, 결과를 이름 있는 지역 `val` 로 추출하도록 보고한다.

## 0.14.1
- 리뷰 시작 시 작업 중이던 파일을 수정하고 커밋하지 않았으면, 결과 출력에 파일과 건수를 `커밋하지 않은 수정` 으로 표시한다.

## 0.14.0
- `projectRules` 설정 추가. 프로젝트의 룰 파일(형식 자유)을 플러그인 룰과 함께 적용한다. 플러그인 룰과 반대되면 프로젝트 룰을 따르고, 같은 이유로 보고하면 한 항목으로 합친다. 프로젝트 룰의 결과는 `/kotlin-harness:issue` 로 등록하지 않는다.
- `excludeRules` 설정 추가. 카테고리 전체가 아니라 룰 하나만 제외한다.

## 0.13.0
- `comments` 룰 6개 추가: 코드를 반복하는 주석, 이름·타입으로 나타낼 수 있는 설명, 이름과 시그니처만 반복하는 KDoc, 주석 처리한 코드, 구분선 주석, 수정 이력·작성자·결함 배경 주석

## 0.12.0
- Kotlin 코딩 관례 룰 23개 추가. 새 카테고리 7개가 기본으로 적용되므로, 원하지 않으면 `excludeCategories` 에 지정한다.
  - `control-flow`: 단순 순회의 `forEach`, 두 갈래 `when`·세 갈래 이상 `if` 체인, 식 형태 `if`·`when`, 루프 대신 고차 함수, `..<` 범위, 가드 조건 괄호
  - `functions`: `Boolean`·같은 타입 인수의 이름, 오버로드 대신 기본값, 함수 대신 프로퍼티, 인픽스 함수, 팩토리 함수 이름, 익스텐션 가시성
  - `lambdas`: 라벨 반환
  - `naming`: 변경·복사 함수 이름, `Manager`·`Wrapper`, 약어 대소문자, 백킹 프로퍼티 이름
  - `strings`: 문자열 템플릿, 여러 줄 문자열
  - `file-layout`: 클래스 멤버 순서, 오버로드 위치, 익스텐션만 모은 파일
  - `comments`: `@param`·`@return` 태그

## 0.11.0
- 룰 13개 추가
  - `android/ui/compose`: `modifier` 파라미터(누락·기본값·위치, 적용 위치와 횟수, 여러 개), 컴포저블 이름, `remember` 접두사, UI 를 그리면서 값을 반환, 마지막 파라미터의 `@Composable` 이 아닌 람다, 컴포지션에서 코루틴 시작, 키 없는 `derivedStateOf` 에서 `State` 가 아닌 값 읽기
  - `android/domain` (새 카테고리): use case 이름, use case 의 가변 상태
  - `android/data`: 리포지토리·데이터 소스 이름, 노출하는 모델의 `var` 프로퍼티

## 0.10.0
- 룰 10개 추가
  - `common/flow` (새 카테고리): `flow { }` 에서 다른 컨텍스트로 `emit`, 컬렉터 예외 무시, `collect { }` 람다 예외를 `catch` 로 처리, `onCompletion` 으로 실패 복구, 터미널 연산자 누락
  - `common/coroutines`: `launch` 를 감싼 `try`·`catch`, 자식 코루틴·`async` 에 지정한 `CoroutineExceptionHandler`
  - `android/test` (새 카테고리): `minSdk` 30 미만 모듈의 계측 테스트 메서드 이름에 공백
  - `android/ui/strings` (새 카테고리): 화면 문구 하드코딩·조립, 개수에 따른 문구를 `if` 로 분기

## 0.9.0
- `review.redCommit` 기본값을 `true` 로 변경. 실제 문제를 수정할 때 실패하는 테스트를 먼저 커밋한다. 이전 동작(테스트와 수정을 한 커밋)을 원하면 `false` 로 지정한다.

## 0.8.0
- 실제 문제로 판정한 위반은 버그를 재현하는 단위 테스트를 작성해 실패(red)를 확인한 뒤 수정하고 통과(green)를 확인한다. 재현되지 않으면 실제 문제가 아닌 것으로 다시 판정한다.
- `review.redCommit` 설정 추가. `true` 이면 실패하는 테스트를 먼저 커밋한다.

## 0.7.0
- 위반마다 현재 코드에서 실제로 문제가 발생하는지 판정한다(`실제 문제`·`방어용`·`판정 불가`). 결과는 리포트의 `영향` 에 근거와 함께 적는다.
- 커밋 메시지가 영향 판정을 따른다. 방어용 수정은 현재 동작이 바뀌지 않는다고 적고, `fix` 타입을 쓰지 않는다.
- 검수가 영향 판정과 커밋 메시지의 과장 여부를 확인한다. ([#1](https://github.com/caffeine0518/kotlin-harness/issues/1))

## 0.6.0
- `/kotlin-harness:update` 추가. 플러그인을 최신 버전으로 업데이트하고 변경 내역을 보여 준다.

## 0.5.0
- `/kotlin-harness:issue` 추가. 오탐·누락·잘못된 수정을 이 리포에 GitHub 이슈로 등록한다.
- 검수를 한 번만 실행한다. 검수에서 나온 문제는 반영하고, 다시 검수하지 않는다.

## 0.4.0
- Android 룰 35개 추가: `ui/compose`, `ui/view`, `ui/viewmodel`, `data`, `coroutines`, `security`
- `excludeCategories` 에 하위 경로(`ui/view` 등)를 지정할 수 있다.

## 0.3.0
- 설정 파일 없이 실행할 수 있다. platform 은 `build.gradle(.kts)` 로 자동 판정한다.
- 리포트 디렉터리에 `.gitignore` 를 자동으로 만든다.
- `branch` 범위의 기본 base 를 리포의 기본 브랜치로 변경했다.

## 0.2.0
- GitHub marketplace 로 설치할 수 있다.
- `python3` 가 없으면 훅을 오류 없이 건너뛴다.

## 0.1.0
- `/kotlin-harness:gate`: 룰 기반 리뷰, 위반 수정·커밋, 리포트 작성, 별도 에이전트 검수
- 코틀린 공통 룰 39개: `null-safety`, `immutability`, `exceptions`, `coroutines`, `types`, `scope-functions`, `collections`
