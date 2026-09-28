---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/exception-handling.html#exception-propagation
---

# `launch` 에서 발생하는 예외는 `launch` 호출을 감싼 `try`·`catch` 가 아니라 코루틴 본문에서 처리한다

## 이유

`launch` 는 코루틴을 시작한 뒤 바로 반환한다. 코루틴 본문은 나중에, 다른 호출 스택에서 실행되므로 `launch` 호출을 감싼 `try`·`catch` 는 본문의 예외를 잡지 못한다. 공식 문서에 따르면 `launch` 는 예외를 자동으로 전파하는 빌더이고, 루트 코루틴이면 잡히지 않은 예외(uncaught exception)로 처리한다. Android 에서는 앱이 크래시한다.

## 위반

```kotlin
fun refresh() {
    try {
        viewModelScope.launch {
            repository.refresh()  // IOException 은 바깥 catch 로 전달되지 않는다
        }
    } catch (e: IOException) {
        _uiState.value = UiState.Error
    }
}
```

## 수정

```kotlin
fun refresh() {
    viewModelScope.launch {
        try {
            repository.refresh()
        } catch (e: IOException) {
            _uiState.value = UiState.Error
        }
    }
}
```

## 허용

- `try` 블록에 `launch` 외에 예외가 발생할 수 있는 동기 코드가 있고, `catch` 가 그 코드의 예외를 처리하는 경우
- `coroutineScope { }` 호출을 감싼 `try`·`catch`. `coroutineScope` 는 자식 코루틴이 끝날 때까지 기다리고, 자식의 예외를 호출한 쪽으로 전파한다.
