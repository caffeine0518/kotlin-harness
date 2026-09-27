---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/exceptions.html#create-custom-exceptions
---

# 예외를 `object` 선언으로 만들지 않는다

## 이유

예외는 생성된 시점의 스택 트레이스를 상태로 가진다. `object` 로 선언한 예외는 인스턴스가 하나뿐이라 어디서 발생시켜도 처음 생성된 시점의 스택 트레이스가 표시되고, 실제 발생 위치를 추적할 수 없다. 공식 문서는 `object` 선언으로 예외를 만들지 말고 필요할 때마다 새 인스턴스를 생성하라고 한다.

## 위반

```kotlin
object SessionExpiredException : Exception("Session expired")

sealed class AccountException(message: String) : Exception(message) {
    object InvalidCredentials : AccountException("Invalid credentials")
}

fun refresh() {
    if (expired) throw SessionExpiredException
}
```

## 수정

```kotlin
class SessionExpiredException : Exception("Session expired")

sealed class AccountException(message: String) : Exception(message) {
    class InvalidCredentials : AccountException("Invalid credentials")
}

fun refresh() {
    if (expired) throw SessionExpiredException()
}
```
