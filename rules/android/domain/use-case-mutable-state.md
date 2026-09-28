---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/domain-layer
---

# use case 는 가변 상태를 보관하지 않는다

## 이유

공식 문서는 use case 를 단순하고 가볍게 유지하기 위해 한 가지 기능만 담당하게 하고, 가변 데이터를 포함하지 않게 하라고 한다. 가변 데이터는 UI 레이어나 데이터 레이어에서 처리한다. use case 는 여러 ViewModel 에서 재사용되고 DI 스코프에 따라 인스턴스가 공유될 수 있어, 상태를 보관하면 한 화면의 호출 결과가 다른 화면의 호출에 영향을 준다.

## 위반

이름이 `UseCase` 로 끝나는 클래스가 아래 중 하나를 가진다.

- `var` 프로퍼티
- `MutableList`·`MutableMap`·`MutableStateFlow` 등 가변 타입 프로퍼티

```kotlin
class GetNewsPageUseCase(private val repository: NewsRepository) {
    private var lastPage = 0

    suspend operator fun invoke(): List<News> = repository.news(page = ++lastPage)
}
```

## 수정

진행 상태는 호출하는 쪽이 보관하고 파라미터로 전달한다.

```kotlin
class GetNewsPageUseCase(private val repository: NewsRepository) {
    suspend operator fun invoke(page: Int): List<News> = repository.news(page)
}
```

## 허용

- 생성자로 주입받은 의존성을 보관하는 `val` 프로퍼티
- `Mutex` 처럼 동시 실행을 제어하기 위한 객체
