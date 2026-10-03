---
severity: info
applies_to: "**/*.kt"
source: https://refactoring.com/catalog/extractVariable.html
---

# 호출 체인 결과에 스코프 함수를 호출하지 않고, 결과를 이름 있는 지역 `val` 로 추출한 뒤 사용한다

## 이유

스코프 함수의 리시버가 `a().b().c()` 같은 호출 체인이면, 람다 안의 `it`·`this` 가 무엇인지 알려면 체인의 마지막 호출과 인수까지 읽어야 한다. 체인 결과를 `val token = ...` 으로 추출하면 이름만 보고 값이 무엇인지 알 수 있다. 또 지역 `val` 에는 스마트 캐스트가 적용되므로 `?.let` 대신 `if (token != null)` 로 분기할 수 있다.

참고: Martin Fowler 의 《Refactoring》은 복잡한 식을 설명하는 이름의 변수로 추출하는 방법을 변수 추출(Extract Variable)로 소개한다.

## 위반

`let`·`also`·`run`·`takeIf`·`takeUnless` 의 리시버가 함수 호출이 두 개 이상 이어진 체인이고, 람다가 `it`·`this`(암시적 리시버 포함)를 참조한다. 참조 횟수와 람다의 줄 수는 판정에 영향을 주지 않는다. `it` 을 한 번만 전달해도 그 값이 무엇인지는 체인을 끝까지 읽어야 알 수 있다.

```kotlin
InstrumentationRegistry.getArguments().getString(ARG_BYPASS_TOKEN)?.let {
    authenticator.authenticate(it)
    log("bypass token length=${it.length}")
}

repository.findUser(id)?.profiles?.firstOrNull()?.takeIf { it.isPublic && it.nickname.isNotBlank() }

Registry.getArguments().getString(ARG_KEY)?.let {
    System.setProperty(PROPERTY_NAME, it)
}
```

## 수정

리시버를 지역 `val` 로 추출한다. 널 체크만 하는 `?.let` 이면 `if` 와 스마트 캐스트로 바꾼다.

```kotlin
val token = InstrumentationRegistry.getArguments().getString(ARG_BYPASS_TOKEN)
if (token != null) {
    authenticator.authenticate(token)
    log("bypass token length=${token.length}")
}

val profile = repository.findUser(id)?.profiles?.firstOrNull()
profile?.takeIf { it.isPublic && it.nickname.isNotBlank() }

val key = Registry.getArguments().getString(ARG_KEY)
if (key != null) System.setProperty(PROPERTY_NAME, key)
```

## 허용

- 람다 대신 메서드 참조를 전달하는 경우 (`.let(::println)`), 람다가 `it`·`this` 를 참조하지 않는 경우. 공식 스코프 함수 문서에는 호출 체인 결과에 `let { println(it) }` 을 호출하는 예제가 있지만, 이 룰은 `it` 을 참조하면 위반으로 본다.
- 리시버가 변수·프로퍼티이거나, 함수 호출이 하나뿐인 경우 (`user?.let { }`, `findUser(id)?.let { }`)
- `?.` 로 이어진 프로퍼티 접근만 있는 경우 (`state.user?.profile?.let { }`)
- 변수 이름은 체인의 마지막 호출·인수 이름에서 정할 수 있을 때만 수정한다 (`getString(ARG_BYPASS_TOKEN)` → `token`). 정할 수 없으면 리포트에만 적고 수정하지 않는다.
