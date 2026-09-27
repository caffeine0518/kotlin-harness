---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#nullable-boolean-values-in-conditions
---

# 널러블 `Boolean` 을 조건에 쓸 때는 `== true` 또는 `== false` 로 비교한다

## 이유

공식 코딩 컨벤션이 지정한 방식이다. `!!` 를 쓰면 `null` 일 때 NPE 가 발생하고, `?: false` 는 `null` 을 어떻게 처리하는지 한눈에 읽히지 않는다.

## 위반

```kotlin
if (user.isVerified!!) { ... }
if (user.isVerified ?: false) { ... }
```

## 수정

```kotlin
if (user.isVerified == true) { ... }
if (user.isVerified == false) { ... }  // null 은 포함하지 않는다
```
