---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#lambda-parameters
---

# 중첩된 람다에서는 파라미터 이름을 명시하고 암시적 `it` 을 쓰지 않는다

## 이유

람다 안의 람다에서 `it` 을 쓰면 바깥 람다의 `it` 이 가려져, 읽는 사람이 `it` 이 어느 람다의 파라미터인지 확인해야 한다. 바깥 `it` 을 쓰려던 코드가 안쪽 `it` 을 참조해도 타입이 같으면 컴파일 오류가 발생하지 않는다. 공식 코딩 컨벤션은 짧고 중첩되지 않은 람다에서만 `it` 을 쓰고, 파라미터가 있는 중첩 람다에서는 항상 파라미터를 명시하라고 한다.

## 위반

```kotlin
orders.forEach {
    it.items.filter { it.price > 0 }.forEach {
        println(it.name)
    }
}
```

## 수정

```kotlin
orders.forEach { order ->
    order.items.filter { item -> item.price > 0 }.forEach { item ->
        println(item.name)
    }
}
```

## 허용

- 바깥 람다가 파라미터에 이름을 지정했고, 가장 안쪽 한 개의 람다만 `it` 을 쓰는 경우 (`orders.forEach { order -> order.items.map { it.id } }`). `it` 이 가리키는 대상이 하나뿐이다.
- 바깥 람다가 파라미터가 없거나 리시버(`this`)만 있는 람다인 경우 (`apply`·`run`·`with`·`buildList` 안의 `map { it.id }`)
- 중첩된 두 람다가 모두 스코프 함수면 `common/scope-functions/nested-scope-functions` 로만 보고한다.
