---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coroutines-flow.html
---

# `catch` 연산자로 처리하려는 코드는 `collect { }` 람다가 아니라 `catch` 앞의 `onEach { }` 에 둔다

## 이유

`catch` 연산자는 업스트림에서 발생한 예외만 처리한다. `collect { }` 람다에서 예외가 발생하면 `catch` 를 지정했어도 수집한 코루틴으로 예외가 전파되고, `viewModelScope`·`lifecycleScope` 에서는 앱이 크래시할 수 있다.

## 위반

`.catch { }` 뒤에 호출한 `collect { }` 람다에서 네트워크·파싱·DB 작업처럼 예외가 발생할 수 있는 함수를 호출한다.

```kotlin
viewModelScope.launch {
    repository.observeOrders()
        .catch { _uiState.value = UiState.Error }
        .collect { order -> repository.saveReceipt(order) }  // 여기서 발생한 예외는 catch 가 처리하지 않는다
}
```

## 수정

```kotlin
viewModelScope.launch {
    repository.observeOrders()
        .onEach { order -> repository.saveReceipt(order) }
        .catch { _uiState.value = UiState.Error }
        .collect()
}

// 또는 collect() 를 try·catch 로 감싼다
viewModelScope.launch {
    try {
        repository.observeOrders().collect { order -> repository.saveReceipt(order) }
    } catch (e: IOException) {
        _uiState.value = UiState.Error
    }
}
```

## 허용

- `collect { }` 람다가 상태 갱신·`emit`·UI 갱신처럼 예외가 발생하지 않는 작업만 하는 경우
- `collect()` 호출을 `try`·`catch` 로 감싼 경우
- `.catch { }` 없이 수집하는 코드의 예외 처리 여부는 `android/coroutines/catch-exceptions-in-ui-scope` 가 보고한다.
