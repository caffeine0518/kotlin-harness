---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#conditional-statements
---

# 모든 분기에서 같은 변수에 대입하거나 반환하는 `if`·`when` 은 식으로 작성한다

## 이유

코틀린 코딩 관례는 `try`·`if`·`when` 을 식 형태로 쓰라고 한다. 모든 분기가 같은 변수에 대입하거나 `return` 하면, 식으로 쓸 때 대입·반환이 한 번만 나타나 `val` 로 선언할 수 있고 분기를 빠뜨리면 컴파일 오류가 발생한다.

## 위반

```kotlin
val label: String
if (count > 0) label = "$count" else label = "-"

when (x) {
    0 -> return "zero"
    else -> return "nonzero"
}
```

## 수정

```kotlin
val label = if (count > 0) "$count" else "-"

return when (x) {
    0 -> "zero"
    else -> "nonzero"
}
```

## 허용

- 분기마다 다른 변수에 대입하거나, 일부 분기만 반환하는 경우
- 분기 안에 여러 문장이 있어 식으로 쓰면 오히려 읽기 어려운 경우
- `try` 는 이 룰이 아니라 `common/control-flow/exceptions/try-expression` 이 보고한다.
