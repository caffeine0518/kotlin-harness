---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#guard-conditions-in-when-expression
---

# `when` 의 가드 조건에서 불리언 식 여러 개를 결합하면 괄호로 감싼다

## 이유

코틀린 코딩 관례는 `when` 의 가드 조건(`if`)에서 불리언 식 여러 개를 결합할 때 괄호를 쓰라고 한다. 괄호로 감싸면 가드 조건이 어디서 시작해 어디서 끝나는지 분기 조건(`is Status.Ok`)과 구분된다.

## 위반

```kotlin
when (status) {
    is Status.Ok if status.info.isEmpty() || status.info.id == null -> "no information"
}
```

## 수정

```kotlin
when (status) {
    is Status.Ok if (status.info.isEmpty() || status.info.id == null) -> "no information"
}
```

## 허용

- 가드 조건이 불리언 식 하나인 경우
