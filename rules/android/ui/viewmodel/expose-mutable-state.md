---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#mutable-types
---

# ViewModel 은 `MutableStateFlow`·`MutableSharedFlow`·`MutableLiveData` 를 public 으로 노출하지 않는다

## 이유

공식 문서는 ViewModel 이 가변 타입을 노출하지 말고 불변 타입을 노출하라고 한다. 상태 변경이 ViewModel 한 곳에서만 일어나야 문제가 생겼을 때 추적하기 쉽다. `MutableStateFlow` 를 public 으로 노출하면 UI 가 ViewModel 의 함수를 거치지 않고 `value` 를 바꿀 수 있어, UI 는 상태를 소비하고 ViewModel 은 상태를 생성한다는 단방향 데이터 흐름(UDF)이 적용되지 않는다.

`ViewModel` 을 상속한 클래스에 적용한다.

## 위반

- `public`·`internal`(기본 가시성 포함) 프로퍼티의 타입이 `MutableStateFlow`·`MutableSharedFlow`·`MutableLiveData`·`MutableState` 인 경우. 타입을 생략하고 `MutableStateFlow(...)` 등으로 초기화한 경우도 포함한다.
- `var uiState by mutableStateOf(...)` 에 `private set` 이 없는 경우

```kotlin
class LatestNewsViewModel : ViewModel() {
    val uiState = MutableStateFlow(LatestNewsUiState.Loading)
    val isRefreshing: MutableLiveData<Boolean> = MutableLiveData(false)
    var query by mutableStateOf("")
}
```

## 수정

가변 타입은 `_` 로 시작하는 private 백킹 프로퍼티로 두고, public 프로퍼티는 읽기 전용 타입으로 선언한다. `asStateFlow()`·`asSharedFlow()` 를 쓰면 UI 가 `MutableStateFlow` 로 캐스트해 값을 바꿀 수도 없다.

```kotlin
class LatestNewsViewModel : ViewModel() {
    private val _uiState = MutableStateFlow<LatestNewsUiState>(LatestNewsUiState.Loading)
    val uiState: StateFlow<LatestNewsUiState> = _uiState.asStateFlow()

    private val _isRefreshing = MutableLiveData(false)
    val isRefreshing: LiveData<Boolean> = _isRefreshing

    var query by mutableStateOf("")
        private set
}
```

## 허용

- `private` 프로퍼티
- 명시적 백킹 필드(explicit backing field) `val uiState: StateFlow<UiState>` + `field = MutableStateFlow(...)` 로 선언한 경우
- 읽기 전용 타입(`StateFlow`·`LiveData`)으로 선언하고 `_state` 를 그대로 할당한 경우. `asStateFlow()` 를 쓰지 않아도 이 룰의 위반으로 보고하지 않는다. 공식 문서의 수정 예제도 이 형태다.
- `MutableList`·`MutableMap` 같은 가변 컬렉션을 public 으로 노출하는 경우. `common/immutability/expose-read-only-view` 로 보고한다.
- `ViewModel` 을 상속하지 않은 클래스
