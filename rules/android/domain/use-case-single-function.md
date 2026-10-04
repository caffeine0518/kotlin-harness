---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/domain-layer
---

# UseCase 는 공개 함수를 하나만 가진다

## 이유

UseCase 하나는 한 가지 기능만 담당해야 단순하고 가볍게 유지된다. 공개 함수가 여러 개인 UseCase 는 여러 기능을 담당하므로, 한 기능만 쓰는 쪽도 나머지 기능의 의존성까지 주입받는다.

## 위반

UseCase 에 이름이 다른 `public`·`internal` 함수가 두 개 이상 있다.

```kotlin
class NewsUseCase(
    private val newsRepository: NewsRepository,
    private val bookmarkRepository: BookmarkRepository,
) {
    suspend fun getLatestNews(): List<News> = newsRepository.latestNews()
    suspend fun bookmark(news: News) = bookmarkRepository.add(news)
}
```

## 수정

기능마다 UseCase 를 나누고, 각 UseCase 에 `operator fun invoke` 를 정의한다. 호출하는 쪽은 UseCase 인스턴스를 함수처럼 호출한다.

```kotlin
class GetLatestNewsUseCase(private val newsRepository: NewsRepository) {
    suspend operator fun invoke(): List<News> = newsRepository.latestNews()
}

class BookmarkNewsUseCase(private val bookmarkRepository: BookmarkRepository) {
    suspend operator fun invoke(news: News) = bookmarkRepository.add(news)
}
```

## 허용

- 같은 이름의 오버로드. 예: `invoke(id: String)`·`invoke(ids: List<String>)`
- `private` 함수
