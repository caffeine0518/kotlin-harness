---
severity: error
applies_to: "**/src/{test,androidTest}/**/*.kt"
source: https://developer.android.com/kotlin/coroutines/test#setting-main-dispatcher
---

# `Dispatchers.setMain` 으로 교체한 Main 디스패처는 테스트가 끝날 때 `Dispatchers.resetMain` 으로 복원한다

## 이유

`setMain` 으로 바꾼 `Dispatchers.Main` 은 그 테스트에만 적용되지 않는다. 테스트가 끝나도 그대로 남아서, 복원하지 않으면 다음에 실행되는 테스트도 이전 테스트의 `TestDispatcher` 를 Main 으로 쓴다.

Main 이 `TestDispatcher` 이면 새로 생성한 `TestDispatcher` 와 `runTest` 도 Main 의 스케줄러를 쓴다. 이전 테스트의 스케줄러에 남은 코루틴이 다음 테스트에서 실행되어, 테스트 결과가 실행 순서에 따라 달라진다.

## 위반

- `Dispatchers.setMain` 을 호출하는 테스트 클래스·JUnit 룰에 대응하는 `Dispatchers.resetMain` 호출이 없다.
- `resetMain` 을 테스트가 실패해도 실행되는 위치가 아니라 테스트 본문 끝에서 호출한다. 앞의 단언이 실패하면 호출되지 않는다. 실패해도 실행되는 위치의 예: `finally`·`@After`·`@AfterEach`·JUnit 룰의 `finished`

```kotlin
class HomeViewModelTest {
    @Before
    fun setUp() {
        Dispatchers.setMain(UnconfinedTestDispatcher())
    }

    @Test
    fun loadMessage() = runTest {
        val viewModel = HomeViewModel()
        viewModel.loadMessage()
        assertEquals("Greetings!", viewModel.message.value)
        Dispatchers.resetMain()  // 단언이 실패하면 호출되지 않는다
    }
}
```

## 수정

JUnit 룰로 교체와 복원을 함께 처리한다.

```kotlin
class MainDispatcherRule(
    val testDispatcher: TestDispatcher = UnconfinedTestDispatcher(),
) : TestWatcher() {
    override fun starting(description: Description) {
        Dispatchers.setMain(testDispatcher)
    }

    override fun finished(description: Description) {
        Dispatchers.resetMain()
    }
}

class HomeViewModelTest {
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    @Test
    fun loadMessage() = runTest {
        val viewModel = HomeViewModel()
        viewModel.loadMessage()
        assertEquals("Greetings!", viewModel.message.value)
    }
}
```

## 허용

- 부모 테스트 클래스의 `@After` 나 JUnit 5 익스텐션의 `afterEach` 에서 `resetMain` 을 호출하는 경우
