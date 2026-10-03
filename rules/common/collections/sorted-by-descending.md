---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/collection-ordering.html#custom-orders
---

# 내림차순 정렬은 `sorted().reversed()` 대신 `sortedDescending()`·`sortedByDescending { }` 로 쓴다

## 이유

`sortedBy { }.reversed()` 는 정렬한 리스트를 만든 뒤 요소를 복사한 리스트를 한 번 더 만든다. 공식 문서는 내림차순 정렬 함수로 `sortedDescending()` 과 `sortedByDescending { }` 을 제공한다.

두 방식은 정렬 키가 같은 요소의 순서가 다르다. `sorted` 계열은 안정 정렬이라 키가 같은 요소의 원본 순서를 유지하는데, `reversed()` 는 정렬 결과를 통째로 뒤집어 그 순서까지 역순으로 만든다. 따라서 수정하면 키가 같은 요소의 순서가 바뀔 수 있다. 그 순서가 중요하면 `thenBy { }`·`thenByDescending { }` 으로 두 번째 정렬 기준을 지정한다.

```kotlin
// 원본: [가(3), 나(1), 다(3), 라(1)]
posts.sortedBy { it.likes }.reversed()   // [다, 가, 라, 나]
posts.sortedByDescending { it.likes }    // [가, 다, 나, 라]
posts.sortedWith(compareByDescending<Post> { it.likes }.thenByDescending { it.createdAt })
```

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
- 키가 같은 요소의 순서가 원본의 역순이어야 하는 경우
- `sortedWith(comparator).reversed()` 처럼 `Comparator` 를 쓰는 경우. `sortedWith(comparator.reversed())` 도 가능하지만 이 룰의 대상이 아니다.
