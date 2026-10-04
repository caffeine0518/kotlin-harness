---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/data-layer
---

# 리포지토리가 노출하는 모델과 프로퍼티는 불변으로 선언한다

## 이유

다른 클래스가 값을 바꿀 수 있으면 데이터가 일관되지 않은 상태가 될 수 있다. 불변 데이터는 여러 스레드에서 안전하게 다룰 수 있다. 데이터 변경은 리포지토리가 맡고, 다른 클래스는 리포지토리의 함수를 호출해 변경한다.

- 리포지토리는 캐시한 객체를 그대로 반환하는 경우가 많다. 그 객체에 `var` 가 있으면 한 화면에서 바꾼 값이 캐시와, 같은 객체를 받은 다른 화면에도 반영된다.
- 리포지토리의 프로퍼티를 밖에서 바꿀 수 있으면, 리포지토리의 함수를 거치지 않은 변경이 생긴다. 리포지토리가 그 변경을 저장소에 반영하지 못해 캐시와 저장소의 값이 달라진다.

## 위반

리포지토리의 public·internal 멤버가 다음 중 하나에 해당한다.

- 반환하는 모델에 `var` 프로퍼티가 있다. `Flow<T>`·`List<T>`·`Result<T>` 처럼 감싼 타입이면 `T` 를 판정한다.
- `private set` 이 없는 `var` 프로퍼티다.
- 프로퍼티 타입이 `MutableStateFlow`·`MutableSharedFlow` 처럼 밖에서 값을 바꿀 수 있는 타입이다.

```kotlin
data class News(val id: String, var title: String, var isBookmarked: Boolean)

class NewsRepository(private val newsApi: NewsApi) {
    var lastRefreshed: Instant? = null  // 밖에서 값을 바꿀 수 있다
    val bookmarks = MutableStateFlow<List<News>>(emptyList())  // 밖에서 value 를 바꿀 수 있다

    fun observeNews(): Flow<List<News>> = newsApi.observeNews()
}
```

## 수정

- 모델의 `var` 를 `val` 로 바꾼다. 값을 바꿔야 하는 쪽은 `copy` 로 새 객체를 만든다.
- 리포지토리의 `var` 프로퍼티에는 `private set` 을 지정한다.
- 가변 상태 타입은 `private` 프로퍼티로 두고, 읽기 전용 타입(`StateFlow`·`SharedFlow`)으로 노출한다. 값은 리포지토리의 함수로 바꾼다.

```kotlin
data class News(val id: String, val title: String, val isBookmarked: Boolean)

class NewsRepository(private val newsApi: NewsApi) {
    var lastRefreshed: Instant? = null
        private set

    private val _bookmarks = MutableStateFlow<List<News>>(emptyList())
    val bookmarks: StateFlow<List<News>> = _bookmarks.asStateFlow()

    fun observeNews(): Flow<List<News>> = newsApi.observeNews()

    fun bookmark(news: News) {
        _bookmarks.update { it + news.copy(isBookmarked = true) }
    }
}
```

## 허용

- Room 엔티티·네트워크 응답 모델처럼 리포지토리 밖으로 노출하지 않는 모델. 이런 모델을 리포지토리가 그대로 노출하는 코드는 `android/data/separate-data-source-models` 가 보고한다.
- 명시적 백킹 필드(explicit backing field)로 `val bookmarks: StateFlow<List<News>>` + `field = MutableStateFlow(...)` 처럼 선언한 경우
- 가변 컬렉션 타입의 프로퍼티. 리포지토리의 프로퍼티는 `common/immutability/expose-read-only-view` 가, data class 의 프로퍼티는 `common/immutability/data-class-mutable-collection` 이 보고한다.
