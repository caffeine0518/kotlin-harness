---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/scope-functions.html#return-value
---

# 람다 결과가 필요하면 `let`·`run`·`with` 를, 컨텍스트 객체가 필요하면 `apply`·`also` 를 쓴다

## 이유

`apply`·`also` 는 컨텍스트 객체(context object)를 반환하고 람다의 마지막 식은 무시한다. `let`·`run`·`with` 는 람다 결과를 반환한다. 반환값을 잘못 고르면 계산한 값이 무시되거나, 객체 대신 `Unit` 이나 다른 값이 대입된다.

## 위반

```kotlin
// apply 는 list 를 반환하므로 total 은 합계가 아니라 list 다
val total = items.apply { sumOf { it.price } }

// also 의 람다 결과(trim 한 문자열)는 무시되고 원래 input 이 반환된다
val name = input.also { it.trim() }

// run 은 람다 결과(Unit)를 반환하므로 user 는 User 가 아니다
val user = User().run {
    name = "kim"
    age = 20
}
```

## 수정

```kotlin
val total = items.sumOf { it.price }

val name = input.trim()

val user = User().apply {
    name = "kim"
    age = 20
}
```

## 허용

- 반환값을 사용하지 않는 호출. 반환값을 무시하는 스코프 함수는 임시 스코프로 쓰는 용도다 (`with(list) { println(first()) }`).
- `also`·`apply` 블록의 마지막 식이 부수 효과 호출이라 결과를 쓰지 않아도 되는 경우 (`also { log(it) }`, `apply { add(x) }`)
