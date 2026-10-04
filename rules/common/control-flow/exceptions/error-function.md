---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/exceptions.html#error-function
---

# 도달하면 안 되는 분기에서는 `throw IllegalStateException(...)` 대신 `error()` 를 호출한다

## 이유

`error()` 는 메시지를 받아 `IllegalStateException` 을 발생시킨다. `throw IllegalStateException(...)` 과 같은 예외를 더 짧게 발생시키고, 함수 이름으로 도달하면 안 되는 상태라는 의도를 드러낸다.

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
- 조건 검사 뒤에 발생시키는 경우는 `common/control-flow/exceptions/precondition-functions` 룰에서 다룬다
