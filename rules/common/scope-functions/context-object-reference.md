---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/scope-functions.html#context-object-this-or-it
---

# 컨텍스트 객체의 멤버를 주로 호출하면 `this` 를 쓰는 스코프 함수를, 인자로 주로 전달하면 `it` 을 쓰는 스코프 함수를 쓴다

## 이유

객체의 함수를 호출하거나 프로퍼티에 값을 대입하는 람다에 `it` 으로 참조하는 `let`·`also` 를 쓰면 `it.` 이 줄마다 반복된다. 객체를 함수 호출의 인자로 주로 쓰는 람다에 리시버(`this`)로 참조하는 `run`·`with`·`apply` 를 쓰면, `this` 를 인자로 전달하느라 바깥 스코프의 `this` 가 가려진다.

## 위반

```kotlin
val view = TextView(context).also {
    it.text = title
    it.textSize = 16f
    it.gravity = Gravity.CENTER
}

val request = Request().apply {
    validator.validate(this)
    logger.log(this)
}
```

## 수정

```kotlin
val view = TextView(context).apply {
    text = title
    textSize = 16f
    gravity = Gravity.CENTER
}

val request = Request().also {
    validator.validate(it)
    logger.log(it)
}
```

## 허용

- 멤버 접근과 인자 전달이 섞여 있어 어느 쪽이 주된 용도인지 판정할 수 없는 경우
- 블록 안의 멤버 접근이 두 개 이하인 경우
- 바깥 스코프의 `this`(Activity·Fragment 등)를 가리지 않으려고 `also`·`let` 을 쓴 경우. 공식 문서가 `also` 의 용도로 명시한다.
- `?.let` 으로 널러블 값을 논널로 다루는 경우
