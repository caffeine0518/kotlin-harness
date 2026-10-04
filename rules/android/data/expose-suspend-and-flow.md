---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#coroutines-data-layer
---

# 리포지토리·데이터 소스는 일회성 작업을 suspend 함수로, 데이터 변경을 `Flow` 로 노출한다

## 이유

데이터 레이어 클래스가 일회성 호출을 suspend 함수로, 시간에 따른 데이터 변경을 `Flow` 로 노출하면 호출하는 쪽(주로 ViewModel)이 작업의 실행과 생명주기를 제어하고, 필요할 때 취소할 수 있다.

## 위반

리포지토리·데이터 소스의 public·internal 멤버가 다음 중 하나에 해당한다.

- 결과를 콜백으로 전달한다. 호출하는 쪽이 완료를 기다리거나 취소할 수 없다. 예: `onSuccess`·`onError` 같은 함수 타입 파라미터, 콜백 인터페이스
- `LiveData` 를 반환하거나 프로퍼티로 노출한다. `LiveData` 는 UI 레이어용 타입이라, 호출하는 쪽에서 `Flow` 연산자와 코루틴 취소를 적용할 수 없다.
- suspend 가 아닌 함수에서 `launch`·`async` 로 코루틴을 시작하고 바로 반환한다. 호출하는 쪽이 완료를 기다리거나 취소할 수 없고, 예외도 호출하는 쪽이 아니라 그 스코프로 전파된다.

```kotlin
class NewsRepository(private val api: NewsApi, private val scope: CoroutineScope) {
    fun fetchNews(onSuccess: (List<News>) -> Unit, onError: (Throwable) -> Unit) {
        scope.launch {
            runCatching { api.fetchNews() }.fold(onSuccess, onError)  // 결과를 콜백으로 전달한다
        }
    }

    val bookmarks: LiveData<List<News>> = MutableLiveData()  // LiveData 로 노출한다

    fun refresh() {
        scope.launch { api.refresh() }  // 호출하는 쪽이 완료를 기다릴 수 없다
    }
}
```

## 수정

일회성 작업은 결과를 반환하는 suspend 함수로, 변경을 관찰하는 데이터는 `Flow` 로 노출한다. 코루틴을 시작하던 스코프를 더 이상 쓰지 않으면 프로퍼티도 삭제한다.

```kotlin
class NewsRepository(private val api: NewsApi, private val dao: NewsDao) {
    suspend fun fetchNews(): List<News> = api.fetchNews()

    val bookmarks: Flow<List<News>> = dao.observeBookmarks()

    suspend fun refresh() = api.refresh()
}
```

## 허용

- Room `@Dao` 인터페이스의 반환 타입. 데이터 레이어의 진입점인 리포지토리에서 판정한다.
- 콜백 기반 라이브러리를 감싸는 데이터 소스 내부의 `private` 함수
- `suspendCancellableCoroutine`·`callbackFlow` 로 콜백을 suspend 함수·`Flow` 로 변환하는 코드
- 결과를 전달하지 않고 동작을 지정하는 함수 타입 파라미터. 예: `transform: (T) -> R`, `predicate`
- 직접 생성한 스코프를 취소하지 않는 코드는 `common/coroutines/cancel-custom-scope` 가 보고한다. 이 룰은 suspend 가 아닌 함수에서 코루틴을 시작하는 API 형태만 보고한다.
