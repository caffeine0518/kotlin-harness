---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/collection-elements.html#retrieve-by-condition
---

# 비어 있을 수 있는 컬렉션에서 요소를 조회할 때는 `*OrNull` 함수를 쓴다

## 이유

`first()`·`last()` 는 컬렉션이 비어 있으면, `first { }`·`last { }` 는 조건을 만족하는 요소가 없으면 `NoSuchElementException` 이 발생한다. `elementAt()` 은 범위를 벗어난 위치에서, `firstNotNullOf { }` 는 논널 결과가 없을 때 예외가 발생한다. `firstOrNull()`·`lastOrNull()`·`elementAtOrNull()`·`firstNotNullOfOrNull()` 은 같은 경우에 예외 대신 `null` 을 반환한다.

## 위반

```kotlin
val mainEmail = user.emails.first()
val admin = members.first { it.role == Role.ADMIN }
val third = items.elementAt(2)
```

## 수정

```kotlin
val mainEmail = user.emails.firstOrNull() ?: ""
val admin = members.firstOrNull { it.role == Role.ADMIN } ?: return
val admin = members.find { it.role == Role.ADMIN }  // firstOrNull { } 과 같다
val third = items.elementAtOrNull(2)
```

## 허용

- 같은 함수 안에서 `isNotEmpty()`·`isEmpty()` 확인이나 `size` 비교로 요소가 있음을 확인한 뒤 호출하는 경우
- 요소가 있는 `listOf(...)` 리터럴에 직접 호출하는 경우. `filter { }` 등을 거친 결과에 호출하면 요소가 있음이 보장되지 않으므로 허용하지 않는다.
- 요소가 없는 것이 프로그래밍 오류이고, 예외를 발생시켜 즉시 실패하는 것이 의도인 경우. 그 의도를 주석으로 적었으면 위반이 아니다.
- 테스트 코드
