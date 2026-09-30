---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/domain-layer
---

# use case 를 싱글턴 스코프로 제공하지 않는다

## 이유

공식 문서는 use case 에 자체 생명주기가 없고, use case 를 사용하는 클래스의 스코프를 따른다고 한다. use case 는 가변 데이터를 포함하지 않으므로, 의존성으로 전달할 때마다 새 인스턴스를 생성하라고 한다. 싱글턴으로 제공하면 앱 프로세스가 끝날 때까지 use case 와 그 의존성이 메모리에 남는다.

## 위반

- 이름이 `UseCase` 로 끝나는 클래스에 `@Singleton` 이 있다.
- Hilt·Dagger 의 `@Provides`·`@Binds` 함수가 `@Singleton` 이고 `UseCase` 로 끝나는 타입을 반환한다.
- Koin 에서 `UseCase` 로 끝나는 타입을 `single { }`·`singleOf(::)` 로 등록한다.

```kotlin
@Singleton
class GetLatestNewsUseCase @Inject constructor(
    private val newsRepository: NewsRepository,
) {
    suspend operator fun invoke(): List<News> = newsRepository.latestNews()
}

val domainModule = module {
    single { GetLatestNewsUseCase(get()) }
}
```

## 수정

스코프 어노테이션을 제거하고, Koin 에서는 `factory { }`·`factoryOf(::)` 로 등록한다.

```kotlin
class GetLatestNewsUseCase @Inject constructor(
    private val newsRepository: NewsRepository,
) {
    suspend operator fun invoke(): List<News> = newsRepository.latestNews()
}

val domainModule = module {
    factory { GetLatestNewsUseCase(get()) }
}
```

## 허용

- `@ViewModelScoped` 처럼 use case 를 사용하는 클래스의 스코프를 따르는 경우
