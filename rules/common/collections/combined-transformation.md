---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/collection-transformations.html#map
---

# `map { }` 뒤에 결과를 다시 가공하지 않고 두 단계를 합친 함수를 쓴다

## 이유

아래 함수는 변환과 후처리를 한 번에 수행해 중간 컬렉션을 만들지 않는다.

| 위반 | 수정 |
|---|---|
| `map { }.filterNotNull()` | `mapNotNull { }` |
| `mapIndexed { }.filterNotNull()` | `mapIndexedNotNull { }` |
| `map { }.flatten()` | `flatMap { }` |
| `map { it.id to it }.toMap()` | `associateBy { it.id }` |
| `map { it to f(it) }.toMap()` | `associateWith { f(it) }` |
| `map { }.sum()` | `sumOf { }` |

## 위반

```kotlin
val ids = items.map { it.id?.toLongOrNull() }.filterNotNull()
val tags = posts.map { it.tags }.flatten()
val usersById = users.map { it.id to it }.toMap()
val total = orders.map { it.price }.sum()
```

## 수정

```kotlin
val ids = items.mapNotNull { it.id?.toLongOrNull() }
val tags = posts.flatMap { it.tags }
val usersById = users.associateBy { it.id }
val total = orders.sumOf { it.price }
```

## 허용

- `map { }` 결과를 변수에 저장해 다른 용도로도 쓰는 경우
- `filter { it != null }` 로 `null` 을 제외하는 경우는 `common/null-safety/filter-not-null` 룰이 다룬다. 이 룰로 중복 보고하지 않는다.
