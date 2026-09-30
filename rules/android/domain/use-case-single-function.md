---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/domain-layer
---

# use case 는 공개 함수를 하나만 가진다

## 이유

공식 문서는 use case 를 단순하고 가볍게 유지하기 위해 use case 하나가 한 가지 기능만 담당하게 하라고 한다. 코틀린에서는 `operator fun invoke` 를 정의해 use case 인스턴스를 함수처럼 호출한다. 공개 함수가 여러 개인 use case 는 여러 기능을 담당하므로, 한 기능만 쓰는 호출하는 쪽도 나머지 기능의 의존성까지 주입받는다.

## 위반

이름이 `UseCase` 로 끝나는 클래스에 이름이 다른 `public`·`internal` 함수가 두 개 이상 있다.

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

기능마다 use case 를 나누고 `operator fun invoke` 로 호출한다.

```kotlin
class GetLatestNewsUseCase(private val newsRepository: NewsRepository) {
    suspend operator fun invoke(): List<News> = newsRepository.latestNews()
}

class BookmarkNewsUseCase(private val bookmarkRepository: BookmarkRepository) {
    suspend operator fun invoke(news: News) = bookmarkRepository.add(news)
}
```

## 허용

- 같은 이름의 오버로드(`invoke(id: String)`·`invoke(ids: List<String>)`)
- `private` 함수
