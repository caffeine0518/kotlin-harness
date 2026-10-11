---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/exceptions.html#throw-exceptions-with-precondition-functions
---

# 값이 지켜야 할 조건은 주석 대신 `require()`·`check()` 로 작성한다

## 이유

"~여야 한다"·"~이면 안 된다"고 요구하는 주석은 아무것도 강제하지 않는다. 조건을 어긴 값이 들어와도 그대로 실행되고, 문제는 그 값을 사용하는 다른 곳에서 발생한다. `require()`(인수)·`check()`(상태)로 옮기면 조건을 어기는 순간 예외가 발생하고, 조건이 코드와 함께 바뀐다.

## 위반

프로퍼티·파라미터·함수의 주석이 값이나 상태가 지켜야 할 조건을 요구하고, 그 조건을 검사하는 코드가 없다.

- 값의 범위: "0보다 커야 한다", "1~100 사이"
- 비어 있으면 안 된다
- 호출 전 상태: "`connect()` 를 호출한 뒤에 호출해야 한다"

```kotlin
data class Order(
    /** 0보다 커야 한다. */
    val amount: Money,
    /** 비어 있으면 안 된다. */
    val idempotencyKey: String,
)

/** connect() 를 호출한 뒤에 호출해야 한다. */
fun send(message: Message) {
    socket!!.write(message)
}
```

## 수정

```kotlin
data class Order(val amount: Money, val idempotencyKey: String) {
    init {
        require(amount.isPositive) { "amount must be positive, got $amount" }
        require(idempotencyKey.isNotBlank()) { "idempotencyKey cannot be blank" }
    }
}

fun send(message: Message) {
    val socket = checkNotNull(socket) { "connect() must be called before send()" }
    socket.write(message)
}
```

## 허용

- 조건을 검사하는 코드가 이미 있거나, 타입이 이미 보장하는 조건(논널 타입에 "null 이면 안 된다")을 반복한 주석. `common/comments/redundant-comment` 가 보고한다.
- 조건을 어긴 값을 예외가 아닌 다른 방식(기본값 대체, 무시)으로 처리해야 하는 경우
- 조건을 어긴 기존 호출이 예외로 실패하도록 동작이 바뀌므로, 리포트의 수정 제안에 `require()`·`check()` 코드를 적고 수정하지 않는다.
