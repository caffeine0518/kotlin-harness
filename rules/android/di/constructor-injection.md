---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/training/dependency-injection#what-is-di
---

# ViewModel·Repository·DataSource·use case 는 의존성을 직접 생성하지 않고 생성자로 주입받는다

## 이유

Android 아키텍처 권장사항은 의존성 주입, 특히 생성자 주입을 쓰라고 강력히 권장한다. 공식 문서에 따르면 클래스가 의존성을 직접 생성하면 두 클래스가 강하게 결합되어 다른 구현으로 교체할 수 없고, 테스트에서 실제 인스턴스를 쓰게 되어 테스트 더블로 바꿀 수 없다. 생성자로 주입받으면 의존성이 API 의 일부가 되어 객체를 생성할 때나 컴파일 시점에 확인된다.

## 위반

이름이 `ViewModel`·`Repository`·`DataSource`·`UseCase` 로 끝나는 클래스가 프로퍼티 초기화식이나 본문에서 아래 타입의 인스턴스를 직접 생성한다.

- 이름이 `Repository`·`DataSource`·`UseCase`·`Api`·`Service`·`Dao` 로 끝나는 타입
- `Retrofit.Builder()`·`Room.databaseBuilder()`·`OkHttpClient()` 로 만드는 네트워크·DB 클라이언트

```kotlin
class NewsViewModel : ViewModel() {
    private val repository = NewsRepository(NewsRemoteDataSource())
}

class NewsRepository {
    private val api = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .build()
        .create(NewsApi::class.java)
}
```

## 수정

생성자 파라미터로 받고, 생성은 Hilt·Koin 모듈이나 수동 DI 컨테이너에서 한다.

```kotlin
@HiltViewModel
class NewsViewModel @Inject constructor(
    private val repository: NewsRepository,
) : ViewModel()

class NewsRepository @Inject constructor(
    private val api: NewsApi,
)
```

## 허용

- 생성자 파라미터의 기본값으로 생성하는 경우 (`class NewsRepository(private val api: NewsApi = NewsApi.create())`). 호출하는 쪽이 다른 구현을 전달할 수 있다.
- Hilt·Koin 모듈, 수동 DI 컨테이너(`AppContainer`), `ViewModelProvider.Factory` 처럼 의존성을 생성하는 역할의 코드
- 매퍼·포매터처럼 상태와 I/O 가 없는 값 객체
