---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/domain-layer
---

# UseCase 를 싱글턴 스코프로 제공하지 않는다

## 이유

UseCase 는 자체 생명주기가 없고, UseCase 를 사용하는 클래스의 스코프를 따른다. 가변 데이터를 보관하지 않으므로 의존성으로 전달할 때마다 새 인스턴스를 생성해도 된다.

싱글턴으로 제공하면 앱 프로세스가 끝날 때까지 UseCase 와 그 의존성이 메모리에 남는다.

## 위반

UseCase 를 싱글턴으로 제공한다. DI 라이브러리별로 다음과 같다.

- UseCase 클래스에 `@Singleton` 이 있다.
- Hilt·Dagger 의 `@Provides`·`@Binds` 함수에 `@Singleton` 이 있고, UseCase 를 반환한다.
- Koin 에서 UseCase 를 `single { }`·`singleOf(::)` 로 등록한다.

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

`@Singleton` 을 삭제한다. Koin 에서는 `factory { }`·`factoryOf(::)` 로 등록한다.

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

- UseCase 를 사용하는 클래스의 스코프를 따르는 경우. 예: `@ViewModelScoped`
