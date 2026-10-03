---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#extension-functions
---

# 한 파일에서만 쓰는 익스텐션 함수는 `private` 으로 선언한다

## 이유

코틀린 코딩 관례는 익스텐션 함수를 적극적으로 쓰되, API 오염을 줄이기 위해 가시성을 가능한 한 좁히라고 한다. 필요에 따라 로컬 익스텐션 함수, 멤버 익스텐션 함수, `private` 최상위 익스텐션 함수를 쓴다. `String.toSlug()` 같은 public 익스텐션은 그 타입을 쓰는 모든 코드의 자동 완성에 노출된다.

## 위반

public(기본 가시성) 최상위 익스텐션 함수·프로퍼티를 선언한 파일 밖에서 호출하는 코드가 없다.

```kotlin
// ProfileScreen.kt
fun String.toDisplayName(): String = replaceFirstChar { it.uppercase() }  // 이 파일에서만 호출한다
```

## 수정

```kotlin
private fun String.toDisplayName(): String = replaceFirstChar { it.uppercase() }
```

다른 모듈이 의존하는 모듈에서는, 그 모듈 안에서만 쓰는 익스텐션을 `internal` 로 좁힐 수 있다. 앱 모듈처럼 다른 모듈이 의존하지 않는 모듈에서는 public 과 차이가 없으므로 이 룰은 `internal` 을 요구하지 않는다.

## 허용

- 라이브러리 모듈의 공개 API
- 리뷰 범위에서 다른 파일의 호출을 확인할 수 없는 경우 (`file`·`diff` 범위). 프로젝트 전체를 검색해 호출이 없을 때만 보고한다.
- 테스트 소스셋에서 호출하는 익스텐션. `private` 으로 좁히면 테스트에서 호출할 수 없다.
