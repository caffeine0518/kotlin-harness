---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#documentation-comments
---

# KDoc 에서 짧은 파라미터·반환값 설명은 `@param`·`@return` 대신 본문 문장에 작성한다

## 이유

코틀린 코딩 관례는 일반적으로 `@param`·`@return` 태그를 피하고, 파라미터와 반환값 설명을 문서 주석 본문에 포함하며, 파라미터를 언급하는 곳마다 `[파라미터]` 링크를 추가하라고 한다. `@param`·`@return` 은 본문 흐름에 들어가지 않는 긴 설명이 필요할 때만 쓴다. 태그로 나누면 본문과 같은 내용이 반복된다.

## 위반

`@param`·`@return` 태그의 설명이 한 줄이고, 본문 문장에 포함할 수 있다.

```kotlin
/**
 * Returns the absolute value of the given number.
 * @param number The number to return the absolute value for.
 * @return The absolute value.
 */
fun abs(number: Int): Int { /* ... */ }
```

## 수정

```kotlin
/**
 * Returns the absolute value of the given [number].
 */
fun abs(number: Int): Int { /* ... */ }
```

## 허용

- 파라미터·반환값 설명이 여러 문장이거나 조건별 설명이 있어 본문에 넣으면 읽기 어려운 경우
- 라이브러리 공개 API 에서 Dokka 문서의 파라미터 표가 필요한 경우
- `@throws`·`@see`·`@sample` 등 다른 태그
