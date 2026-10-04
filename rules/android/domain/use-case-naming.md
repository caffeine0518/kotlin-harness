---
severity: info
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/domain-layer
---

# UseCase 는 `현재형 동사 + 대상(선택) + UseCase` 로 이름 짓는다

## 이유

이름이 동작을 나타내야 그 클래스가 한 가지 기능만 담당하는지 판정할 수 있다. `NewsUseCase` 처럼 대상만 있는 이름은 뉴스에 관한 기능을 모두 한 클래스에 모으게 한다.

## 위반

- 이름이 `UseCase` 로 끝나는데 동사로 시작하지 않는다.
- UseCase 역할의 클래스인데 이름이 `UseCase` 로 끝나지 않는다. 예: 도메인 레이어 패키지(`domain`·`usecase`)에 있고 `operator fun invoke` 를 가진 클래스

```kotlin
class NewsUseCase(private val repository: NewsRepository)  // 동사가 없다
class LatestNewsUseCase(private val repository: NewsRepository)  // 동사가 없다
class GetLatestNews(private val repository: NewsRepository) {  // UseCase 로 끝나지 않는다
    operator fun invoke(): Flow<List<News>> = repository.latestNews()
}
```

## 수정

클래스가 담당하는 동작을 현재형 동사로 앞에 쓰고, `UseCase` 로 끝낸다. 예: `FormatDateUseCase`·`LogOutUserUseCase`·`GetLatestNewsWithAuthorsUseCase`

```kotlin
class GetLatestNewsUseCase(private val repository: NewsRepository) {
    operator fun invoke(): Flow<List<News>> = repository.latestNews()
}
```

## 허용

- 프로젝트가 다른 접미사를 일관되게 쓰는 경우. 같은 모듈의 UseCase 대부분이 그 접미사를 쓰면 위반으로 보고하지 않는다. 예: `Interactor`
