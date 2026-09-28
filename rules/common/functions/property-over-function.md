---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#functions-vs-properties
---

# 예외가 발생하지 않고 계산이 가벼우며 상태가 같으면 같은 값을 반환하는 인수 없는 함수는 읽기 전용 프로퍼티로 선언한다

## 이유

코틀린 코딩 관례는 인수 없는 함수의 알고리즘이 예외를 발생시키지 않고, 계산이 가볍거나 첫 실행에서 캐시되며, 객체 상태가 바뀌지 않으면 같은 결과를 반환할 때 함수보다 프로퍼티를 쓰라고 한다. 호출하는 쪽은 프로퍼티를 읽을 때 부수 효과나 비용이 없다고 기대하고, 함수를 호출할 때는 그렇지 않다고 기대한다.

## 위반

인수 없는 함수의 본문이 아래를 모두 만족한다.

- 같은 객체의 프로퍼티만 읽어 비교·조합한다
- 예외를 발생시키지 않고, 반복문·I/O·suspend 호출이 없다

```kotlin
class Cart(private val items: List<Item>) {
    fun isEmpty(): Boolean = items.isEmpty()
    fun itemCount(): Int = items.size
}
```

## 수정

```kotlin
class Cart(private val items: List<Item>) {
    val isEmpty: Boolean get() = items.isEmpty()
    val itemCount: Int get() = items.size
}
```

## 허용

- 인터페이스를 구현하거나 오버라이드하는 함수
- Java 에서 `isXxx()`·`getXxx()` 로 호출해야 하는 경우처럼 이미 공개된 API
- 호출할 때마다 새 객체를 반환하는 함수 (`toList()`, `copy()` 등)
