---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#viewmodel-coroutines
---

# ViewModel 은 UI 에 suspend 함수를 노출하지 않고 `viewModelScope` 에서 코루틴을 시작한다

## 이유

공식 문서는 ViewModel 이 비즈니스 로직을 수행하는 suspend 함수를 노출하지 말고 코루틴을 직접 생성하라고 한다. UI 가 ViewModel 의 suspend 함수를 호출하면 코루틴이 UI 의 스코프(`lifecycleScope`·`rememberCoroutineScope` 등)에서 실행되어, 화면 회전처럼 구성이 변경될 때 작업이 취소되고 결과가 UI 상태에 반영되지 않는다. `viewModelScope` 에서 시작한 코루틴은 ViewModel 이 해제될 때까지 유지되고, 결과는 UI 상태로 노출된다. 공식 문서는 UI 가 비즈니스 로직을 수행하는 코루틴을 직접 시작하지 않아야 한다고도 한다.

`ViewModel` 을 상속한 클래스에 적용한다.

## 위반

`ViewModel` 을 상속한 클래스의 `public`·`internal`(기본 가시성 포함) `suspend fun` 이 데이터를 조회·저장·갱신하는 경우

```kotlin
class LatestNewsViewModel(
    private val getLatestNewsWithAuthors: GetLatestNewsWithAuthorsUseCase,
) : ViewModel() {
    suspend fun loadNews() = getLatestNewsWithAuthors()
    suspend fun bookmark(articleId: String) = repository.bookmark(articleId)
}
```

## 수정

suspend 가 아닌 함수에서 `viewModelScope.launch` 로 코루틴을 시작하고, 결과를 UI 상태에 반영한다.

```kotlin
class LatestNewsViewModel(
    private val getLatestNewsWithAuthors: GetLatestNewsWithAuthorsUseCase,
) : ViewModel() {
    private val _uiState = MutableStateFlow<LatestNewsUiState>(LatestNewsUiState.Loading)
    val uiState: StateFlow<LatestNewsUiState> = _uiState.asStateFlow()

    fun loadNews() {
        viewModelScope.launch {
            _uiState.value = LatestNewsUiState.Success(getLatestNewsWithAuthors())
        }
    }
}
```

## 허용

- `private`·`protected` suspend 함수
- 상위 타입이 suspend 로 정의한 함수를 오버라이드한 경우
- 화면 상태로 표시하지 않고 호출한 쪽이 한 번만 사용하는 값 하나를 반환하는 경우(예: 공유할 텍스트를 생성해 반환). 공식 문서는 스트림 대신 값 하나만 반환하면 되는 경우 suspend 함수가 유용할 수 있다고 한다. 반환값을 화면에 표시하거나 새로 고침이 필요한 데이터는 이 허용에 해당하지 않는다.
- `ViewModel` 을 상속하지 않은 클래스(Repository·UseCase 는 suspend 함수를 노출하는 것이 권장 방식이다)
