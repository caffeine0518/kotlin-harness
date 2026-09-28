---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#loops-on-ranges
---

# 끝 값을 포함하지 않는 범위는 `0..n - 1` 대신 `..<` 로 작성한다

## 이유

코틀린 코딩 관례는 끝이 열린 범위를 순회할 때 `..<` 연산자를 쓰라고 한다. `0..n - 1` 은 끝 값에서 1 을 빼는 계산을 직접 작성하므로, `- 1` 을 빠뜨리면 인덱스 범위를 벗어나는 오류가 발생한다.

## 위반

```kotlin
for (i in 0..n - 1) { /* ... */ }
for (i in 0..list.size - 1) { /* ... */ }
```

## 수정

```kotlin
for (i in 0..<n) { /* ... */ }
for (i in list.indices) { /* ... */ }
```

## 허용

- 프로젝트의 Kotlin 버전이 1.9 미만이어서 `..<` 를 쓸 수 없는 경우. `until` 을 쓴다.
