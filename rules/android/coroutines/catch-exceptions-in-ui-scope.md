---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#exceptions
---

# `viewModelScope`·`lifecycleScope` 로 시작한 코루틴에서 발생할 수 있는 예외는 코루틴 본문에서 처리한다

## 이유

코루틴에서 처리되지 않은 예외가 발생하면 앱이 크래시할 수 있다. 네트워크·디스크 I/O 는 사용자 환경에 따라 실패하므로, 처리하지 않으면 로그인 실패 같은 일반적인 오류가 앱 크래시로 이어진다.

## 위반

`viewModelScope.launch { }`·`lifecycleScope.launch { }` 본문에서 네트워크·파일·DB 작업처럼 실패할 수 있는 함수를 호출하는데, 다음 중 하나에 해당한다.

- 본문에 `try`/`catch`·`runCatching` 이 없고, `launch` 에 `CoroutineExceptionHandler` 도 지정하지 않았다.
- `launch` 호출을 감싼 `try`/`catch` 로 예외를 처리한다. `launch` 는 코루틴을 시작한 뒤 바로 반환하므로, 바깥 `catch` 는 본문의 예외를 잡지 못한다.

```kotlin
class LoginViewModel(private val loginRepository: LoginRepository) : ViewModel() {
    fun login(username: String, token: String) {
        viewModelScope.launch {
            loginRepository.login(username, token)  // IOException 이 발생하면 앱이 크래시한다
            _uiState.value = LoginUiState.LoggedIn
        }
    }

    fun logout() {
        try {
            viewModelScope.launch {
                loginRepository.logout()  // IOException 은 바깥 catch 로 전달되지 않는다
                _uiState.value = LoginUiState.LoggedOut
            }
        } catch (exception: IOException) {
            _uiState.value = LoginUiState.Error
        }
    }
}
```

## 수정

`try`/`catch` 는 `launch` 호출 바깥이 아니라 코루틴 본문 안에 작성한다. 예외 타입은 `Exception`·`Throwable` 대신 `IOException` 처럼 구체적인 타입을 잡는다.

```kotlin
class LoginViewModel(private val loginRepository: LoginRepository) : ViewModel() {
    fun login(username: String, token: String) {
        viewModelScope.launch {
            try {
                loginRepository.login(username, token)
                _uiState.value = LoginUiState.LoggedIn
            } catch (exception: IOException) {
                _uiState.value = LoginUiState.Error
            }
        }
    }

    fun logout() {
        viewModelScope.launch {
            try {
                loginRepository.logout()
                _uiState.value = LoginUiState.LoggedOut
            } catch (exception: IOException) {
                _uiState.value = LoginUiState.Error
            }
        }
    }
}
```

## 허용

- 호출하는 함수가 예외를 내부에서 처리하고 `Result`·sealed 타입으로 실패를 반환하는 경우 (같은 파일에서 판정할 수 있을 때)
- `launch` 에 `CoroutineExceptionHandler` 를 지정한 경우, Flow 에 `.catch { }` 를 적용하고 `launchIn`·`collect` 하는 경우
- 코루틴 본문이 상태 갱신·`delay`·`emit` 처럼 예외가 발생하지 않는 작업만 하는 경우
- `catch (e: Exception)` 으로 잡았지만 `CancellationException` 을 다시 전파하지 않는 코드는 이 룰이 아니라 `common/coroutines/rethrow-cancellation-exception` 이 보고한다.
- 이 룰이 보고한 코드는 `common/coroutines/try-catch-around-launch` 로 중복 보고하지 않는다.
