---
severity: warning
applies_to: "**/*.kt"
source: https://refactoring.com/catalog/extractVariable.html
---

# 호출 체인 결과에 스코프 함수를 호출하지 않고, 결과를 이름 있는 지역 `val` 로 추출한 뒤 사용한다

## 이유

스코프 함수의 리시버가 `a().b().c()` 같은 호출 체인이면, 람다 안의 `it`·`this` 가 무엇인지 알기 위해 체인의 마지막 호출과 인수까지 읽어야 한다. Martin Fowler 의 《Refactoring》은 복잡한 식을 설명하는 이름의 변수로 나누는 변수 추출(Extract Variable, Introduce Explaining Variable)을 제시한다. 결과를 `val token = ...` 으로 추출하면 바로 앞의 이름으로 `it` 이 무엇인지 알 수 있고, 지역 `val` 에는 스마트 캐스트가 적용되어 `?.let` 없이 `if (token != null)` 로 쓸 수도 있다.

## 위반

`let`·`also`·`run`·`takeIf`·`takeUnless` 의 리시버가 함수 호출이 두 개 이상 이어진 체인이고, 람다가 아래 중 하나에 해당한다.

- 여러 줄이다
- `it`·`this`(암시적 리시버 포함)를 두 번 이상 참조한다

```kotlin
InstrumentationRegistry.getArguments().getString(ARG_BYPASS_TOKEN)?.let {
    authenticator.authenticate(it)
    log("bypass token length=${it.length}")
}

repository.findUser(id)?.profiles?.firstOrNull()?.takeIf { it.isPublic && it.nickname.isNotBlank() }
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
```

## 허용

- 람다가 `it` 을 함수 하나에 그대로 전달하기만 하는 경우 (`numbers.map { it.length }.filter { it > 3 }.let { println(it) }`, `.let(::println)`). 공식 스코프 함수 문서의 `let` 예제가 이 형태다.
- 리시버가 변수·프로퍼티이거나, 함수 호출이 하나뿐인 경우 (`user?.let { }`, `findUser(id)?.let { }`)
- `?.` 로 이어진 프로퍼티 접근만 있는 경우 (`state.user?.profile?.let { }`)
- 변수 이름은 체인의 마지막 호출·인수 이름에서 정할 수 있을 때만 수정한다 (`getString(ARG_BYPASS_TOKEN)` → `token`). 정할 수 없으면 리포트에만 적고 수정하지 않는다.
