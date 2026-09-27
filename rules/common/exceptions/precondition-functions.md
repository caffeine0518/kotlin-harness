---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/exceptions.html#throw-exceptions-with-precondition-functions
---

# 인수·상태 검증은 `if (...) throw` 대신 `require()`·`check()` 계열 함수로 작성한다

## 이유

`require()` 는 조건이 거짓이면 `IllegalArgumentException` 이, `check()` 는 `IllegalStateException` 이 발생한다. 공식 문서는 입력 인수 검증에 `require()`·`requireNotNull()` 을, 객체·변수의 상태 검증에 `check()`·`checkNotNull()` 을 쓰라고 한다. 검증을 통과한 뒤에는 대상 변수에 스마트 캐스트가 적용된다.

## 위반

```kotlin
fun getIndices(count: Int): List<Int> {
    if (count < 0) throw IllegalArgumentException("count must be non-negative: $count")
    return List(count) { it + 1 }
}

fun currentState(): String {
    if (state == null) throw IllegalStateException("state must be set")
    return state!!
}
```

## 수정

```kotlin
fun getIndices(count: Int): List<Int> {
    require(count >= 0) { "count must be non-negative: $count" }
    return List(count) { it + 1 }
}

fun currentState(): String = checkNotNull(state) { "state must be set" }
```

## 허용

- `IllegalArgumentException`·`IllegalStateException` 이 아닌 예외(커스텀 예외 등)를 발생시키는 경우
- 예외에 `cause` 를 지정하는 경우
