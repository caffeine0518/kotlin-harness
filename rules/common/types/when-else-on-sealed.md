---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/sealed-classes.html#use-sealed-classes-with-when-expression
---

# sealed·enum 타입을 subject 로 하는 `when` 에 `else` 분기를 두지 않는다

## 이유

subject 가 sealed 클래스·인터페이스나 enum 이면 컴파일러가 모든 하위 타입·상수를 다루었는지 검사하므로 `else` 가 필요 없다. `else` 를 두면 이 검사가 적용되지 않아, 이후 하위 타입이나 상수를 추가해도 컴파일 오류가 발생하지 않고 새 값이 `else` 분기로 처리된다.

## 위반

```kotlin
sealed interface UiState {
    data object Loading : UiState
    data class Success(val data: String) : UiState
    data class Error(val cause: Throwable) : UiState
}

fun render(state: UiState) = when (state) {
    is UiState.Loading -> showLoading()
    is UiState.Success -> showData(state.data)
    else -> showError()
}
```

## 수정

```kotlin
fun render(state: UiState) = when (state) {
    is UiState.Loading -> showLoading()
    is UiState.Success -> showData(state.data)
    is UiState.Error -> showError()
}
```

## 허용

- 일부 값만 처리하고 나머지를 같은 방식으로 처리하는 것이 의도인 경우(예: `Color.RED -> ...; else -> ...`). 그 의도를 주석으로 적었으면 위반이 아니다.
- subject 가 없는 `when`, 또는 subject 가 `String`·`Int` 처럼 값이 닫혀 있지 않은 타입인 경우. 이때 `else` 는 필수다.
- 멀티플랫폼 공통 코드에서 `expect` 로 선언한 sealed 클래스를 subject 로 하는 경우. 공식 문서는 이때 `else` 가 필요하다고 한다.
