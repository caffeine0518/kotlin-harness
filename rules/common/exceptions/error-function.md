---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/exceptions.html#error-function
---

# 도달하면 안 되는 분기에서는 `throw IllegalStateException(...)` 대신 `error()` 를 호출한다

## 이유

`error()` 는 메시지를 받아 `IllegalStateException` 을 발생시킨다. 공식 문서는 논리적으로 발생하면 안 되는 상태를 나타낼 때, 특히 `when` 식의 `else` 분기에서 `error()` 를 쓰라고 한다.

## 위반

```kotlin
val label = when (user.role) {
    "admin" -> "관리자"
    "viewer" -> "뷰어"
    else -> throw IllegalStateException("Undefined role: ${user.role}")
}
```

## 수정

```kotlin
val label = when (user.role) {
    "admin" -> "관리자"
    "viewer" -> "뷰어"
    else -> error("Undefined role: ${user.role}")
}
```

## 허용

- 예외에 `cause` 를 지정하는 경우 (`error()` 는 메시지만 받는다)
- 조건 검사 뒤에 발생시키는 경우는 `common/exceptions/precondition-functions` 룰에서 다룬다
