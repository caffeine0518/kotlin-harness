---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/ui-layer/state-production#initializing-state-production
---

# ViewModel·상태 홀더의 `init` 블록과 생성자에서 비동기 작업을 시작하지 않는다

## 이유

UI 상태 생성 가이드는 ViewModel 의 `init` 블록이나 생성자에서 비동기 작업을 시작하지 말라고 한다. 객체를 생성하는 도중 시작한 코루틴은 초기화가 끝나지 않은 객체를 읽거나 쓸 수 있다. 이를 객체 누출(leaking the object)이라고 하며, 원인을 찾기 어려운 오류로 이어진다. ViewModel 이 Compose State 를 가지고 있으면 `init` 에서 시작한 코루틴이 그 State 를 갱신할 때 `IllegalStateException` 이 발생할 수 있다.

이 문제는 코루틴을 시작하는 코드가 `init` 블록 안에 직접 있든, `init` 에서 호출한 함수 안에 있든 같다. 함수로 추출해도 생성 도중 실행된다는 점은 달라지지 않는다.

`ViewModel` 을 상속한 클래스와, `CoroutineScope` 를 생성자로 받아 화면 상태를 관리하는 상태 홀더 클래스에 적용한다.

## 위반

`init` 블록, 프로퍼티 초기화 식, 또는 이들에서 호출한 같은 클래스의 함수에서 다음을 실행한다.

- `launch`·`async`
- Flow 의 `collect`·`launchIn`
- `stateIn`·`shareIn` 에 `SharingStarted.Eagerly` 지정

```kotlin
class ProfileViewModel(private val profileRepository: ProfileRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            val profile = profileRepository.fetch()
            _uiState.update { it.copy(profile = profile) }
        }
    }
}

class ProfileStateHolder(
    private val scope: CoroutineScope,
    private val profileRepository: ProfileRepository,
) {
    init {
        loadProfile()  // 함수로 추출해도 생성 도중 코루틴을 시작한다
    }

    private fun loadProfile() {
        scope.launch { /* ... */ }
    }
}
```

## 수정

가이드는 가능하면 상태 생성을 지연해, 결과를 수집하는 쪽이 생길 때 시작하라고 한다. `stateIn` 에 `SharingStarted.WhileSubscribed` 를 지정하면 UI 가 구독을 시작할 때 실행된다. 값을 한 번 반환하는 suspend 함수도 `flow { }` 로 감싸 같은 방법을 쓴다.

```kotlin
class ProfileViewModel(profileRepository: ProfileRepository) : ViewModel() {
    val uiState: StateFlow<ProfileUiState> = profileRepository.profile
        .map { ProfileUiState(profile = it) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ProfileUiState())
}

class ArticleViewModel(articleRepository: ArticleRepository) : ViewModel() {
    val uiState: StateFlow<ArticleUiState> = flow { emit(articleRepository.fetch()) }
        .map { ArticleUiState(article = it) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ArticleUiState())
}
```

`WhileSubscribed(5_000)` 는 구독이 5초 넘게 없으면 업스트림을 중단하고, 다시 구독하면 처음부터 실행한다. 재구독할 때 다시 실행하면 안 되는 작업처럼 이 방법을 쓸 수 없는 경우에만, 가이드의 예제처럼 멱등인 `initialize` 함수로 추출하고 UI 에서 호출한다. 플래그가 원자적 타입이 아니므로 멱등성은 메인 스레드에서 호출할 때만 보장된다. `@MainThread` 를 지정한다.

```kotlin
class ProfileViewModel(private val profileRepository: ProfileRepository) : ViewModel() {
    private var initializeCalled = false

    @MainThread
    fun initialize() {
        if (initializeCalled) return
        initializeCalled = true

        viewModelScope.launch {
            val profile = profileRepository.fetch()
            _uiState.update { it.copy(profile = profile) }
        }
    }
}
```

## 허용

- `SharingStarted.WhileSubscribed`·`SharingStarted.Lazily` 를 지정한 `stateIn`·`shareIn`
- 코루틴을 시작하지 않는 동기 초기화(프로퍼티 계산, `SavedStateHandle` 에서 값 읽기)
- `ViewModel` 을 상속하지 않고, `CoroutineScope` 를 받지 않는 클래스
- 테스트 코드
