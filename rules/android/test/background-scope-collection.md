---
severity: warning
applies_to: "**/src/{test,androidTest}/**/*.kt"
source: https://developer.android.com/kotlin/flow/test#continuous-collection
---

# `runTest` 에서 완료되지 않는 Flow 를 수집하는 코루틴은 `backgroundScope` 에서 시작한다

## 이유

`runTest` 는 그 스코프에서 `launch` 한 코루틴이 모두 끝날 때까지 기다린다. `StateFlow`·`SharedFlow` 처럼 완료되지 않는 Flow 를 수집하는 코루틴은 끝나지 않으므로, 테스트가 제한 시간까지 끝나지 않는다.

`backgroundScope` 의 코루틴은 테스트 본문이 끝나면 자동으로 취소된다. 테스트마다 `job.cancel()` 을 호출할 필요가 없고, 빠뜨려서 테스트가 끝나지 않는 일도 없다.

## 위반

`runTest` 블록에서 `backgroundScope` 가 아닌 스코프로 `launch` 한 코루틴이 완료되지 않는 Flow 를 수집한다. 예: `collect`·`toList`·`collectLatest`

```kotlin
@Test
fun continuouslyCollect() = runTest {
    val values = mutableListOf<Int>()
    val job = launch(UnconfinedTestDispatcher(testScheduler)) {
        repository.scores().toList(values)
    }

    dataSource.emit(1)
    assertEquals(10, values[0])

    job.cancel()  // 빠뜨리면 테스트가 끝나지 않는다
}
```

## 수정

`backgroundScope.launch` 로 시작하고, `job.cancel()` 호출을 삭제한다.

```kotlin
@Test
fun continuouslyCollect() = runTest {
    val values = mutableListOf<Int>()
    backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
        repository.scores().toList(values)
    }

    dataSource.emit(1)
    assertEquals(10, values[0])
}
```

## 허용

- 완료되는 Flow 를 수집하는 경우. 예: `flowOf(...)`, `take(n)` 을 적용한 Flow
- Flow 의 완료 자체를 검증하기 위해 `job.join()` 으로 기다리는 경우
