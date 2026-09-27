---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/exceptions.html#the-nothing-type
---

# 항상 예외를 발생시키는 함수는 반환 타입을 `Nothing` 으로 선언한다

## 이유

`Nothing` 은 모든 타입의 하위 타입이고, 정상적으로 반환하지 않는 함수를 나타낸다. 반환 타입이 `Unit` 이면 컴파일러는 호출 뒤에도 실행이 이어진다고 판단하므로 엘비스 연산자 오른쪽에 쓸 수 없고, 호출 뒤에 스마트 캐스트도 적용되지 않는다. `Nothing` 으로 선언하면 `val s: String = name ?: fail("...")` 처럼 쓸 수 있고, 호출 뒤의 코드는 도달할 수 없는 코드로 경고된다.

## 위반

```kotlin
fun fail(message: String) {
    throw IllegalArgumentException(message)
}

fun showUser(name: String?) {
    if (name == null) fail("name required")
    println(name!!.length)
}
```

## 수정

```kotlin
fun fail(message: String): Nothing {
    throw IllegalArgumentException(message)
}

fun showUser(name: String?) {
    val nonNullName = name ?: fail("name required")
    println(nonNullName.length)
}
```

## 허용

- 오버라이드한 함수 (상위 타입의 반환 타입을 따른다)
- `TODO()` 만 호출하는 함수 (구현 전인 함수다)
