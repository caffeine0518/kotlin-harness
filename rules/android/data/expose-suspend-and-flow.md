---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#coroutines-data-layer
---

# 리포지토리·데이터 소스는 일회성 작업을 suspend 함수로, 데이터 변경을 `Flow` 로 노출한다

## 이유

공식 문서는 데이터 레이어 클래스가 일회성 호출에는 suspend 함수를, 시간에 따른 데이터 변경 알림에는 `Flow` 를 노출하라고 한다. 그래야 호출하는 쪽(주로 ViewModel)이 작업의 실행과 생명주기를 제어하고 필요할 때 취소할 수 있다.

콜백을 받는 함수나, 내부에서 코루틴을 시작하고 바로 반환하는 suspend 가 아닌 함수는 호출하는 쪽이 작업의 완료를 기다리거나 취소할 수 없고, 작업에서 발생한 예외도 호출하는 쪽으로 전파되지 않는다. `LiveData` 는 Android 생명주기에 연결된 UI 레이어용 타입이라, 데이터 레이어가 노출하면 코루틴·`Flow` 의 연산자와 취소를 적용할 수 없다.

## 위반

리포지토리·데이터 소스(이름이 `Repository`·`DataSource` 로 끝나는 클래스와 그 구현 클래스)의 public·internal 멤버가 아래에 해당한다.

- 결과를 전달하는 함수 타입 파라미터(`onSuccess`·`onError`·`callback` 등)나 콜백 인터페이스를 받는다
- `LiveData`·`MutableLiveData` 를 반환하거나 프로퍼티로 노출한다
- suspend 가 아닌 함수에서 `launch`·`async` 로 코루틴을 시작하고 반환한다

```kotlin
class NewsRepository(private val api: NewsApi, private val scope: CoroutineScope) {
    fun fetchNews(onSuccess: (List<News>) -> Unit, onError: (Throwable) -> Unit) {
        scope.launch {
            runCatching { api.fetchNews() }.fold(onSuccess, onError)
        }
    }

    val bookmarks: LiveData<List<News>> = MutableLiveData()

    fun refresh() {
        scope.launch { api.refresh() }
    }
}
```

## 수정

```kotlin
class NewsRepository(private val api: NewsApi, private val dao: NewsDao) {
    suspend fun fetchNews(): List<News> = api.fetchNews()

    val bookmarks: Flow<List<News>> = dao.observeBookmarks()

    suspend fun refresh() = api.refresh()
}
```

## 허용

- Room `@Dao` 인터페이스의 반환 타입. 데이터 레이어의 진입점인 리포지토리에서 판정한다.
- 콜백 기반 라이브러리를 감싸는 데이터 소스 내부의 `private` 함수, `suspendCancellableCoroutine`·`callbackFlow` 로 콜백을 suspend 함수·`Flow` 로 변환하는 코드
- 결과 전달이 아닌 동작을 지정하는 함수 타입 파라미터(`transform: (T) -> R`, `predicate` 등)
- 직접 생성한 스코프를 취소하지 않는 코드는 `common/coroutines/cancel-custom-scope` 가 보고한다. 이 룰은 suspend 가 아닌 함수에서 코루틴을 시작하는 API 형태만 보고한다.
