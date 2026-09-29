# Changelog

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
