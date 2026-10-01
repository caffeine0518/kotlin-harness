---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#strings
---

# 여러 줄 문자열은 `\n` 대신 삼중따옴표로 작성하고, `trimIndent()`·`trimMargin()` 으로 소스 들여쓰기를 제거한다

## 이유

코틀린 코딩 관례는 일반 문자열 리터럴에 `\n` 을 넣는 것보다 여러 줄 문자열을 쓰라고 한다. 또 여러 줄 문자열의 들여쓰기를 유지하려면, 결과에 내부 들여쓰기가 필요 없으면 `trimIndent()` 를, 필요하면 `trimMargin()` 을 쓰라고 한다. 삼중따옴표 문자열은 소스 코드의 들여쓰기와 첫 줄·마지막 줄의 줄 바꿈을 그대로 값에 포함한다.

## 위반

- 문자열 리터럴 하나에 `\n` 이 두 번 이상 있다
- 줄 바꿈으로 시작하는 삼중따옴표 문자열에 `trimIndent()`·`trimMargin()` 이 없다

```kotlin
val body = "첫 줄\n둘째 줄\n셋째 줄"

val query = """
    SELECT *
    FROM user
"""
```

## 수정

```kotlin
val body = """
    첫 줄
    둘째 줄
    셋째 줄
""".trimIndent()

val query = """
    SELECT *
    FROM user
""".trimIndent()
```

## 허용

- 문자열 끝에 `\n` 하나만 붙이는 경우 (`"$line\n"`)
- 소스 들여쓰기와 앞뒤 줄 바꿈이 값에 포함되어도 되는 경우 (SQL·정규식에서 공백을 무시하는 경우 등). 판정할 수 없으면 판정 불가로 적는다.
