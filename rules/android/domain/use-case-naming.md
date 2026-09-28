---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/domain-layer
---

# use case 클래스는 `현재형 동사 + 대상(선택) + UseCase` 로 이름 짓는다

## 이유

공식 문서는 use case 를 그 클래스가 담당하는 단일 동작의 이름으로 짓고, `현재형 동사 + 명사(선택) + UseCase` 형식을 쓰라고 한다. 예: `FormatDateUseCase`·`LogOutUserUseCase`·`GetLatestNewsWithAuthorsUseCase`. 이름이 동작을 나타내야 클래스가 한 가지 기능만 담당하는지 판정할 수 있다. `NewsUseCase` 처럼 대상만 있는 이름은 여러 기능이 한 클래스에 모이게 한다.

## 위반

- 이름이 `UseCase` 로 끝나는데 동사로 시작하지 않는다
- 도메인 레이어 패키지(`domain`·`usecase`)에 있고 `operator fun invoke` 를 가진 클래스인데 이름이 `UseCase` 로 끝나지 않는다

```kotlin
class NewsUseCase(private val repository: NewsRepository)
class LatestNewsUseCase(private val repository: NewsRepository)
class GetLatestNews(private val repository: NewsRepository) {
    operator fun invoke(): Flow<List<News>> = repository.latestNews()
}
```

## 수정

```kotlin
class GetLatestNewsUseCase(private val repository: NewsRepository)
```

## 허용

- 프로젝트가 다른 접미사(`Interactor` 등)를 일관되게 쓰는 경우. 같은 모듈의 use case 대부분이 그 접미사를 쓰면 위반으로 보고하지 않는다.
