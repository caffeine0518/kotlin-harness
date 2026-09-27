---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/null-safety.html#collections-of-a-nullable-type
---

# 널러블 요소 컬렉션에서 `null` 을 제외할 때는 `filterNotNull()` 을 쓴다

## 이유

`filter { it != null }` 는 결과 타입이 여전히 `List<T?>` 라서 이후에 `!!` 가 필요해진다. `filterNotNull()` 은 `List<T>` 를 반환한다.

## 위반

```kotlin
val ids = items.filter { it != null }.map { it!!.id }
```

## 수정

```kotlin
val ids = items.filterNotNull().map { it.id }
// 변환 결과에서 null 을 제외하는 경우
val ids = items.mapNotNull { it?.id }
```
