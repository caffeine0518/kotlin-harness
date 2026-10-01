---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/collection-filtering.html#test-predicates
---

# `filter { }` 뒤에 요소 조회·개수·존재 확인을 호출하지 않고 조건을 받는 함수 하나로 쓴다

## 이유

`filter { }` 는 조건을 만족하는 요소 전체로 중간 컬렉션을 만든다. `any { }`·`none { }`·`first { }`·`firstOrNull { }`·`count { }` 는 같은 조건을 인자로 받아 중간 컬렉션 없이 결과를 반환하고, `any`·`none`·`first` 계열은 결과가 정해지는 시점에 순회를 중단한다.

## 위반

```kotlin
if (users.filter { it.isActive }.isNotEmpty()) { ... }
if (users.filter { it.isActive }.isEmpty()) { ... }
val admin = users.filter { it.isAdmin }.firstOrNull()
val activeCount = users.filter { it.isActive }.size
val activeCount = users.filter { it.isActive }.count()
```

## 수정

```kotlin
if (users.any { it.isActive }) { ... }
if (users.none { it.isActive }) { ... }
val admin = users.firstOrNull { it.isAdmin }
val activeCount = users.count { it.isActive }
```

## 허용

- `filter { }` 결과를 변수에 저장해 조회·개수 확인 외의 용도로도 쓰는 경우
- 시퀀스(`Sequence`)의 `filter { }` 뒤에 호출하는 경우. 중간 컬렉션을 만들지 않는다.
