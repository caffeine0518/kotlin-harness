---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/sequences.html#sequence-processing-example
---

# 크기가 제한되지 않은 컬렉션에서 중간 연산 뒤에 일부 요소만 사용하면 `asSequence()` 로 처리한다

## 이유

`Iterable` 의 연산 체인은 즉시 평가된다. 단계마다 모든 요소를 처리하고 중간 컬렉션을 만든 뒤 다음 단계로 넘어간다. 시퀀스는 지연 평가되어 요소 하나씩 모든 단계를 수행하고, 결과가 필요한 만큼만 계산한다. 공식 문서의 예시에서 `filter` → `map` → `take(4)` 체인은 `Iterable` 로는 모든 요소를 `filter`·`map` 하지만 시퀀스로는 4개를 얻는 데 필요한 요소만 처리한다.

반면 문서는 시퀀스의 지연 평가에 오버헤드가 있어, 작은 컬렉션이나 단순한 계산에서는 오히려 불리할 수 있으니 두 방식을 비교해 선택하라고 한다. 그래서 이 룰은 아래 조건을 모두 만족할 때만 적용한다.

1. 중간 연산(`filter`·`map`·`mapNotNull`·`flatMap` 등)이 2개 이상 이어지거나, 1개이지만 끝의 연산과 함수 하나로 합칠 수 없다 — `map { }` 뒤의 `first { }`, `filter { }` 뒤의 `take(n)` 등.
2. 체인이 일부 요소만 사용하는 연산으로 끝난다 — `take(n)`·`first { }`·`firstOrNull { }`·`find { }`·`any { }`·`none { }`.
3. 리시버의 크기가 코드에서 제한되지 않는다 — DB·네트워크·파일에서 읽은 목록, 함수 파라미터로 받은 목록 등.

## 위반

```kotlin
fun findFirstLongTitles(articles: List<Article>): List<String> =
    articles
        .filter { it.isPublished }
        .map { it.title.trim() }
        .filter { it.length > 50 }
        .take(3)

fun findFirstValid(articles: List<Article>): Rendered =
    articles.map { render(it) }.first { it.isValid }
```

## 수정

```kotlin
fun findFirstLongTitles(articles: List<Article>): List<String> =
    articles.asSequence()
        .filter { it.isPublished }
        .map { it.title.trim() }
        .filter { it.length > 50 }
        .take(3)
        .toList()

fun findFirstValid(articles: List<Article>): Rendered =
    articles.asSequence().map { render(it) }.first { it.isValid }
```

## 허용

- 중간 연산이 1개이고 끝의 연산과 함수 하나로 합칠 수 있는 체인 — `filter { }.first()`·`filter { }.any()` 등은 `filter-then-terminal` 룰로 수정한다.
- 체인 끝에서 모든 요소를 사용하는 경우 (`toList()`·`sum()`·`joinToString()` 등으로 끝나고 `take` 가 없는 경우)
- `listOf(...)` 리터럴, `enum` 의 `entries` 처럼 크기가 작고 고정된 컬렉션
- 체인 중간에 `sorted`·`groupBy` 처럼 모든 요소가 필요한 연산이 있는 경우
