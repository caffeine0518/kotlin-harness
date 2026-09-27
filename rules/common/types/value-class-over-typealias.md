---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/inline-classes.html#inline-classes-vs-type-aliases
---

# 같은 기반 타입의 값을 서로 구분해야 하면 타입 별칭 대신 value class 를 쓴다

## 이유

타입 별칭은 기존 타입에 다른 이름을 지정할 뿐이라 기반 타입, 그리고 기반 타입이 같은 다른 타입 별칭과 대입 호환된다. `UserId` 파라미터에 `OrderId` 나 임의의 `String` 을 전달해도 컴파일 오류가 발생하지 않는다. value class 는 새로운 타입을 정의하므로 기반 타입과 대입 호환되지 않고, 런타임에는 대부분 기반 타입으로 표현된다.

## 위반

```kotlin
typealias UserId = String
typealias OrderId = String

fun cancel(userId: UserId, orderId: OrderId) { ... }

cancel(order.id, user.id)  // 인수 순서가 바뀌어도 컴파일된다
```

## 수정

```kotlin
@JvmInline
value class UserId(val value: String)

@JvmInline
value class OrderId(val value: String)

fun cancel(userId: UserId, orderId: OrderId) { ... }
```

## 허용

- 함수 타입이나 타입 파라미터가 있는 긴 타입에 이름을 지정하는 타입 별칭(예: `typealias ClickHandler = (View) -> Unit`, `typealias PersonIndex = Map<String, Person>`). 공식 코딩 컨벤션이 권장하는 사용법이다.
- 서로 구분할 필요가 없고 가독성만을 위한 타입 별칭
