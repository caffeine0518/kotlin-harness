---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/recommendations#viewmodel
---

# 서로 관련된 화면 상태는 여러 스트림으로 나누지 않고 `uiState` 하나로 노출한다

## 이유

단일 스트림과 여러 스트림 중 하나를 고르는 기준은 방출하는 값 사이의 관계다. 로딩 여부·오류·데이터처럼 서로 관련된 값을 별도 스트림으로 노출하면, UI 가 두 스트림을 각각 수집하는 동안 한쪽만 갱신된 상태(로딩이 끝났는데 목록은 이전 값인 상태 등)를 표시할 수 있다. 하나의 상태 객체로 노출하면 UI 는 항상 일관된 최신 상태를 받는다.

`ViewModel` 을 상속한 클래스에 적용한다.

## 위반

한 ViewModel 이 public `StateFlow`·`LiveData`·`State` 프로퍼티를 두 개 이상 노출하고, 그중 하나가 다른 프로퍼티가 가진 데이터의 로딩·오류·빈 상태를 나타내는 경우(`isLoading`·`error`·`isEmpty` 와 `items` 등)

```kotlin
class NewsViewModel(private val repository: NewsRepository) : ViewModel() {
    private val _articles = MutableStateFlow<List<Article>>(emptyList())
    val articles: StateFlow<List<Article>> = _articles.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage: StateFlow<String?> = _errorMessage.asStateFlow()
}
```

## 수정

관련된 값을 하나의 UI 상태 클래스로 묶는다. 상태가 서로 배타적이면 sealed 클래스로 선언한다. 데이터 레이어에서 스트림으로 받는 데이터는 `stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), 초기값)` 으로 `StateFlow` 를 만든다.

```kotlin
data class NewsUiState(
    val articles: List<Article> = emptyList(),
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
)

class NewsViewModel(private val repository: NewsRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(NewsUiState())
    val uiState: StateFlow<NewsUiState> = _uiState.asStateFlow()
}
```

## 허용

- 서로 관련 없는 데이터를 각각 노출하는 경우. 권장 사항은 UI 가 관련 없는 데이터 여러 개를 표시하면 UI 상태 프로퍼티를 여러 개 노출해도 된다고 한다(예: 화면의 사용자 프로필과, 그와 독립적으로 갱신되는 알림 개수).
- 한 값이 다른 값보다 훨씬 자주 갱신되어(예: 입력 중인 검색어, 재생 위치) 별도 스트림으로 분리한 경우
- UI 상태 프로퍼티가 하나이고 이름이 `uiState` 가 아닌 경우. 이름은 이 룰의 위반으로 보고하지 않는다.
- 로딩·오류 상태를 나타내는 프로퍼티 없이 데이터 스트림만 여러 개 노출하는 경우는 값 사이의 관계를 코드만으로 판정할 수 없으므로 보고하지 않는다.
- `ViewModel` 을 상속하지 않은 클래스
