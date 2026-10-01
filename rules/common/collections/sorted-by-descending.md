---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/collection-ordering.html#custom-orders
---

# 내림차순 정렬은 `sorted().reversed()` 대신 `sortedDescending()`·`sortedByDescending { }` 로 쓴다

## 이유

`sortedBy { }.reversed()` 는 정렬한 리스트를 만든 뒤 요소를 복사한 리스트를 한 번 더 만든다. 공식 문서는 내림차순 정렬 함수로 `sortedDescending()` 과 `sortedByDescending { }` 을 제공한다.

## 위반

```kotlin
val latest = posts.sortedBy { it.createdAt }.reversed()
val scores = values.sorted().reversed()
```

## 수정

```kotlin
val latest = posts.sortedByDescending { it.createdAt }
val scores = values.sortedDescending()
```

## 허용

- 정렬 결과와 역순 결과를 모두 쓰는 경우
- `sortedWith(comparator).reversed()` 처럼 `Comparator` 를 쓰는 경우. `sortedWith(comparator.reversed())` 도 가능하지만 이 룰의 대상이 아니다.
