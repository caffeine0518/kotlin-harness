---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#conditional-statements
---

# `try`·`catch` 의 각 블록에서 같은 변수에 대입하거나 반환할 때는 `try` 를 식으로 쓴다

## 이유

`try` 는 식이고, `try` 블록 또는 실행된 `catch` 블록의 마지막 식이 값이 된다. 공식 코딩 컨벤션은 `try`·`if`·`when` 의 식 형태를 선호하라고 한다. 식으로 쓰면 결과를 `var` 대신 `val` 로 받을 수 있다.

## 위반

```kotlin
var settings: String
try {
    settings = File("user-settings.json").readText()
} catch (e: IOException) {
    settings = "{}"
}

fun parse(text: String): Int {
    try {
        return text.toInt()
    } catch (e: NumberFormatException) {
        return -1
    }
}
```

## 수정

```kotlin
val settings = try {
    File("user-settings.json").readText()
} catch (_: IOException) {
    "{}"
}

fun parse(text: String): Int = try {
    text.toInt()
} catch (_: NumberFormatException) {
    -1
}
```

## 허용

- `catch` 블록이 값을 만들지 않고 예외를 다시 전파하거나 로그만 출력하는 경우
- `try` 블록 안에서 대입 외에 여러 부수 효과를 실행하고, 대입이 그중 하나일 뿐인 경우
