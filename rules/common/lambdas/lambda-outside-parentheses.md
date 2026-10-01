---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#lambdas
---

# 마지막 인수인 람다는 괄호 밖에 트레일링 람다로 전달한다

## 이유

코틀린 코딩 관례는 호출이 람다 하나를 받으면 가능한 한 괄호 밖으로 전달하라고 한다. 함수의 마지막 파라미터가 함수 타입이면 그 인수로 전달하는 람다를 괄호 밖에 둘 수 있고, 람다가 유일한 인수이면 괄호를 생략할 수 있다. 괄호 안에 두면 `({ ... })` 처럼 괄호가 겹쳐 람다의 범위를 확인하기 어렵다.

## 위반

마지막 인수가 람다 리터럴인데 괄호 안에 있다.

```kotlin
val adults = users.filter({ it.age >= 18 })
val total = items.fold(0, { acc, item -> acc + item.price })
```

## 수정

```kotlin
val adults = users.filter { it.age >= 18 }
val total = items.fold(0) { acc, item -> acc + item.price }
```

## 허용

- 람다를 여러 개 전달하며 `onSuccess = { }`, `onFailure = { }` 처럼 이름 붙인 인수로 역할을 구분하는 경우
- 함수 참조(`::process`)나 람다를 저장한 변수를 전달하는 경우. 람다 리터럴이 아니므로 이 룰의 대상이 아니다.
