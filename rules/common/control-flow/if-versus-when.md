---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#if-versus-when
---

# 두 갈래 조건은 `if` 로, 세 갈래 이상은 `when` 으로 작성한다

## 이유

코틀린 코딩 관례는 두 갈래 조건에는 `when` 대신 `if` 를 쓰고, 세 갈래 이상이면 `when` 을 쓰라고 한다. 두 갈래인 `when` 은 `if` 보다 길고, 세 갈래 이상인 `if`-`else if` 체인은 비교 대상을 매번 반복해 어떤 값으로 분기하는지 파악하기 어렵다.

## 위반

- `else` 를 포함해 분기가 둘뿐인 `when`
- `else if` 가 두 번 이상 이어지는 `if` 체인 (분기 셋 이상)

```kotlin
when (x) {
    null -> showEmpty()
    else -> show(x)
}

if (status == Status.Loading) showProgress()
else if (status == Status.Error) showError()
else if (status == Status.Empty) showEmpty()
else showContent()
```

## 수정

```kotlin
if (x == null) showEmpty() else show(x)

when (status) {
    Status.Loading -> showProgress()
    Status.Error -> showError()
    Status.Empty -> showEmpty()
    else -> showContent()
}
```

## 허용

- sealed·enum 타입 subject 의 두 갈래 `when`. 나중에 하위 타입이 추가되면 컴파일러가 누락된 분기를 보고한다.
- `if` 체인의 조건이 서로 다른 값을 비교해 하나의 subject 로 정리되지 않는 경우
- `is` 검사로 스마트 캐스트를 적용하는 두 갈래 `when`
