---
severity: warning
applies_to: "**/src/{test,androidTest}/**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#test-coroutine-dispatcher
---

# 코루틴 테스트는 `runTest` 로 실행하고, 테스트 대상에 실제 디스패처 대신 `TestDispatcher` 를 주입한다

## 이유

Android 공식 문서는 테스트에서 클래스에 `TestDispatcher` 를 주입하고, 코루틴 테스트에는 `runTest` 를 쓰라고 한다. `runTest` 는 `TestCoroutineScheduler` 로 `delay` 를 건너뛰고 가상 시간을 제어한다. 테스트 대상이 `Dispatchers.IO`·`Dispatchers.Default` 에서 실행되면 `delay` 를 건너뛰지 못하고 코드가 여러 스레드에서 실행되어 테스트 결과가 실행할 때마다 달라질 수 있다(flaky). 같은 테스트의 `TestDispatcher` 는 모두 스케줄러 하나를 공유해야 한다.

## 위반

- 코루틴을 사용하는 테스트 함수를 `runBlocking` 으로 실행한다.
- 테스트 대상의 디스패처 파라미터에 `Dispatchers.IO`·`Dispatchers.Default`·`Dispatchers.Unconfined` 를 전달한다.
- `runTest` 안에서 `testScheduler` 를 전달하지 않고 `StandardTestDispatcher()`·`UnconfinedTestDispatcher()` 를 생성한다. 단, `Dispatchers.setMain` 으로 Main 을 `TestDispatcher` 로 교체한 뒤에 생성하면 Main 의 스케줄러를 공유하므로 위반이 아니다.

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
- `Dispatchers.setMain` 으로 Main 을 교체하는 `MainDispatcherRule` 같은 JUnit 룰에서 인자 없이 생성한 `TestDispatcher`
