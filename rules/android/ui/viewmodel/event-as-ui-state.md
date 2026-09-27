---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/ui-layer/events#handle-viewmodel-events
---

# ViewModel 은 일회성 이벤트를 `Channel`·`SharedFlow` 로 UI 에 보내지 않고 UI 상태를 갱신한다

## 이유

아키텍처 권장 사항은 ViewModel 에서 UI 로 이벤트를 보내지 말고, ViewModel 에서 이벤트를 즉시 처리한 결과로 상태를 갱신하라고 한다(Strongly recommended). 공식 문서는 `Channel` 이나 다른 반응형 스트림으로 이벤트를 UI 에 노출하면, 생산자(ViewModel)가 소비자(UI)보다 오래 유지될 때 이벤트의 전달과 처리가 보장되지 않는다고 한다. 구성 변경 중이나 UI 가 수집을 멈춘 동안 보낸 이벤트는 유실되고, 앱이 일관되지 않은 상태로 남거나 사용자가 중요한 정보를 보지 못할 수 있다. UI 상태로 표현하면 구성 변경 뒤에도 재현되고 유실되지 않는다.

`ViewModel` 을 상속한 클래스에 적용한다.

## 위반

UI 가 수집하도록 노출한 프로퍼티가 스낵바 표시·화면 이동·토스트 같은 일회성 이벤트를 전달하는 `Channel`(`receiveAsFlow()`·`consumeAsFlow()` 포함)·`SharedFlow`·`MutableSharedFlow` 인 경우. LiveData 기반 `SingleLiveEvent` 도 포함한다.

```kotlin
class LoginViewModel : ViewModel() {
    private val _events = Channel<LoginEvent>()
    val events = _events.receiveAsFlow()

    fun tryLogin(username: String, password: String) {
        viewModelScope.launch {
            if (login(username, password)) _events.send(LoginEvent.NavigateToHome)
            else _events.send(LoginEvent.ShowError("Login failed"))
        }
    }
}
```

## 수정

이벤트의 결과를 UI 상태의 필드로 표현한다. UI 는 상태를 보고 동작하고, 메시지처럼 소비 후 없애야 하는 값은 UI 가 ViewModel 에 알려 상태에서 제거한다.

```kotlin
data class LoginUiState(
    val isLoginInProgress: Boolean = false,
    val errorMessage: String? = null,
    val isUserLoggedIn: Boolean = false,
)

class LoginViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(LoginUiState())
    val uiState: StateFlow<LoginUiState> = _uiState.asStateFlow()

    fun tryLogin(username: String, password: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoginInProgress = true) }
            _uiState.update {
                if (login(username, password)) it.copy(isLoginInProgress = false, isUserLoggedIn = true)
                else it.copy(isLoginInProgress = false, errorMessage = "Login failed")
            }
        }
    }

    fun errorMessageShown() {
        _uiState.update { it.copy(errorMessage = null) }
    }
}
```

## 허용

- `private` 이고 ViewModel 안에서만 수집하는 `Channel`·`SharedFlow`(예: 검색어 입력을 `debounce` 해 처리하는 내부 스트림)
- 이벤트가 아니라 데이터 레이어에서 받은 데이터 스트림을 그대로 노출하는 `SharedFlow`
- `ViewModel` 을 상속하지 않은 클래스
