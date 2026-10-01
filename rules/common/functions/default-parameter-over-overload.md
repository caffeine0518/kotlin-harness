---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#default-parameter-values
---

# 파라미터만 추가되는 오버로드 대신 기본값이 있는 파라미터 하나로 선언한다

## 이유

코틀린 코딩 관례는 오버로드 함수를 여러 개 선언하는 것보다 파라미터 기본값을 쓰라고 한다. 파라미터가 적은 오버로드가 고정 값을 넣어 다른 오버로드를 호출하기만 하면, 기본값이 두 곳에 나뉘어 한쪽만 수정될 수 있다.

## 위반

한 오버로드가 다른 오버로드를 호출하면서 누락된 파라미터에 상수를 전달하기만 한다.

```kotlin
fun load() = load(force = false)
fun load(force: Boolean) { /* ... */ }
```

## 수정

```kotlin
fun load(force: Boolean = false) { /* ... */ }
```

## 허용

- Java 에서 호출하는 API. `@JvmOverloads` 를 붙이거나 오버로드를 유지한다.
- 오버로드가 서로 다른 타입을 받는 경우
- 이미 배포된 라이브러리의 공개 API 여서 바이너리 호환성을 유지해야 하는 경우
