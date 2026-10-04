---
severity: warning
applies_to: "**/src/{test,androidTest}/**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#test-coroutine-dispatcher
---

# 코루틴 테스트는 `runTest` 로 실행하고, 테스트 대상에 실제 디스패처 대신 `TestDispatcher` 를 주입한다

## 이유

`runTest` 와 `TestDispatcher` 는 코루틴을 가상 시간과 하나의 스케줄러로 실행한다. 그래야 `delay` 를 기다리지 않고, 테스트 결과가 실행할 때마다 같다.

## 위반

- 코루틴을 사용하는 테스트 함수를 `runBlocking` 으로 실행한다. `delay` 만큼 실제로 기다린다.
- 테스트 대상의 디스패처 파라미터에 실제 디스패처를 전달한다. `runTest` 로 실행해도 `delay` 를 건너뛰지 못하고, 코드가 여러 스레드에서 실행되어 테스트 결과가 실행할 때마다 달라질 수 있다. 예: `Dispatchers.IO`·`Dispatchers.Default`·`Dispatchers.Unconfined`
- `runTest` 안에서 `testScheduler` 를 전달하지 않고 `TestDispatcher` 를 생성한다. 스케줄러가 달라서, `runTest` 의 시간을 진행해도 그 디스패처의 코루틴은 실행되지 않는다. 예: `StandardTestDispatcher()`·`UnconfinedTestDispatcher()`

```kotlin
@Test
fun bookmarkArticle() = runBlocking {
    val repository = ArticlesRepository(dataSource, defaultDispatcher = Dispatchers.IO)
    repository.bookmarkArticle(article)
    assertTrue(dataSource.isBookmarked(article))
}

@Test
fun fetchData() = runTest {
    val repository = Repository(StandardTestDispatcher())  // runTest 와 다른 스케줄러를 쓴다
    assertEquals("Hello world", repository.fetchData())
}
```

## 수정

`runTest` 로 실행하고, `testScheduler` 를 전달해 생성한 `TestDispatcher` 를 테스트 대상에 주입한다.

```kotlin
@Test
fun bookmarkArticle() = runTest {
    val testDispatcher = UnconfinedTestDispatcher(testScheduler)
    val repository = ArticlesRepository(dataSource, defaultDispatcher = testDispatcher)
    repository.bookmarkArticle(article)
    assertTrue(dataSource.isBookmarked(article))
}

@Test
fun fetchData() = runTest {
    val repository = Repository(StandardTestDispatcher(testScheduler))
    assertEquals("Hello world", repository.fetchData())
}
```

## 허용

- 코루틴을 사용하지 않는 테스트
- `Dispatchers.setMain` 으로 Main 을 `TestDispatcher` 로 교체한 뒤, 인자 없이 `TestDispatcher` 를 생성하는 경우. 새 `TestDispatcher` 는 Main 의 스케줄러를 쓴다.
- `Dispatchers.setMain` 으로 Main 을 교체하는 JUnit 룰에서 인자 없이 생성한 `TestDispatcher`. 예: `MainDispatcherRule`
