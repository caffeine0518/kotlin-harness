---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/iterators.html#mutable-iterators
---

# 가변 컬렉션을 `for` 루프·`forEach` 로 순회하는 중에 그 컬렉션에 요소를 추가·삭제하지 않는다

## 이유

순회 중인 컬렉션의 `add()`·`remove()` 를 직접 호출하면 JVM 의 `ArrayList`·`HashMap` 등에서 다음 순회 단계에 `ConcurrentModificationException` 이 발생한다.

## 위반

```kotlin
for (item in cart) {
    if (item.isExpired) cart.remove(item)
}

users.forEach { if (it.isBlocked) users.remove(it) }

for ((key, session) in sessions) {
    if (session.isClosed) sessions.remove(key)
}
```

## 수정

```kotlin
cart.removeAll { it.isExpired }

val iterator = users.iterator()
while (iterator.hasNext()) {
    if (iterator.next().isBlocked) iterator.remove()
}

sessions.entries.removeAll { it.value.isClosed }
```

## 허용

- 순회 대상이 원본의 복사본인 경우 (`cart.toList()`, `ArrayList(cart)` 등을 순회하고 원본을 수정)
- 요소를 추가·삭제한 직후 `break`·`return` 으로 순회를 종료하는 경우
- `CopyOnWriteArrayList`·`ConcurrentHashMap` 처럼 순회 중 수정을 지원하는 컬렉션
- 인덱스 기반 루프(`for (i in list.indices.reversed())`)로 뒤에서부터 삭제하는 경우
