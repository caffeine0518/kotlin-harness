---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/scope-functions.html#function-selection
---

# 지역 `val`·파라미터의 널 여부로 값을 고르는 `?.let { } ?: ...` 은 `if`-`else` 로 작성한다

## 이유

`x?.let(::b) ?: a` 를 읽으려면 메서드 참조·`it`·엘비스 연산자를 머릿속에서 `if`-`else` 로 바꿔야 한다. 또 `b(x)` 가 `null` 을 반환할 때도 엘비스 오른쪽의 `a` 가 실행되는지 따로 확인해야 한다.

리시버가 지역 `val`·파라미터이면 스마트 캐스트가 적용되므로, 같은 분기를 `if (x == null) a else b(x)` 로 쓸 수 있다. 두 분기가 나란히 놓여 어떤 조건에서 어떤 값이 되는지 바로 읽힌다.

## 위반

리시버가 지역 `val`·함수 파라미터이고, `?.let { }`·`?.let(::f)` 결과에 엘비스 연산자로 대체 값을 지정한다.

```kotlin
return when (regionConfig) {
    is RegionConfig.Loaded -> LoadStatus.Loaded(mapper.mapFrom(regionConfig.config))
    RegionConfig.Loading -> storedFilter?.let(LoadStatus::Pending) ?: LoadStatus.Initial
    RegionConfig.Failed -> storedFilter?.let(LoadStatus::Failed) ?: LoadStatus.Initial
}

fun greeting(name: String?): String = name?.let { "Hello, $it" } ?: "Hello, guest"
```

## 수정

```kotlin
return when (regionConfig) {
    is RegionConfig.Loaded -> LoadStatus.Loaded(mapper.mapFrom(regionConfig.config))
    RegionConfig.Loading -> if (storedFilter == null) LoadStatus.Initial else LoadStatus.Pending(storedFilter)
    RegionConfig.Failed -> if (storedFilter == null) LoadStatus.Initial else LoadStatus.Failed(storedFilter)
}

fun greeting(name: String?): String = if (name == null) "Hello, guest" else "Hello, $name"
```

## 허용

- 리시버가 호출 체인·`?.` 체인·다른 객체의 프로퍼티·`var` 여서 스마트 캐스트가 적용되지 않는 경우 (`findUser(id)?.let { } ?: ...`, `state.user?.let { } ?: ...`). 호출 체인은 `common/scope-functions/extract-long-receiver` 가 보고한다.
- 엘비스 오른쪽이 `return`·`throw`·`continue`·`break` 인 조기 종료 (`val user = id?.let(::findUser) ?: return`)
- `let` 블록이 `null` 을 반환할 수 있는 경우. 이 룰이 아니라 `common/scope-functions/let-elvis-null-result` 가 보고한다.
