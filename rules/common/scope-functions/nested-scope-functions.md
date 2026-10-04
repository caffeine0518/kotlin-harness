---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/scope-functions.html#function-selection
---

# 스코프 함수 안에서 스코프 함수를 중첩하지 않는다

## 이유

스코프 함수(scope function)를 중첩하면 안쪽 람다의 `this`·`it` 이 어느 컨텍스트 객체(context object)를 가리키는지 코드만으로 구분되지 않는다. `this` 를 생략한 멤버 접근은 가장 안쪽 리시버에 우선 해석되므로, 바깥 객체의 멤버를 쓰려던 코드가 안쪽 객체의 멤버를 호출해도 컴파일 오류가 발생하지 않는다.

## 위반

```kotlin
user?.let {
    it.address?.let {
        send(it.zipCode)          // it 은 address
    }
}

binding.apply {
    viewModel.state.run {
        title.text = name         // title·name 이 binding 과 state 중 어느 쪽 멤버인지 구분되지 않는다
    }
}
```

## 수정

```kotlin
val zipCode = user?.address?.zipCode
if (zipCode != null) send(zipCode)

val state = viewModel.state
binding.apply {
    title.text = state.name
}
```

## 허용

- 안쪽 스코프 함수가 람다 파라미터에 이름을 지정해 `this`·`it` 을 쓰지 않는 경우 (`user?.let { u -> u.address?.let { address -> ... } }`)
- 바깥 스코프 함수 안에서 호출한 `forEach`·`map` 같은 컬렉션 함수. 스코프 함수 중첩이 아니다 (암시적 `it` 은 `common/scope-functions/nested-lambda-implicit-it` 에 해당한다).
- `apply`·`also` 를 같은 객체에 이어서 호출하는 체이닝 (`list.also { log(it) }.apply { sort() }`). 컨텍스트 객체가 바뀌지 않는다.
