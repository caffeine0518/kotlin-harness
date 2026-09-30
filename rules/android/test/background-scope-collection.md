---
severity: warning
applies_to: "**/src/{test,androidTest}/**/*.kt"
source: https://developer.android.com/kotlin/flow/test#continuous-collection
---

# `runTest` 에서 완료되지 않는 Flow 를 수집하는 코루틴은 `backgroundScope` 에서 시작한다

## 이유

Android 공식 문서는 테스트 중에 Flow 를 계속 수집하는 코루틴을 `TestScope.backgroundScope` 에서 시작하라고 한다. `backgroundScope` 의 코루틴은 테스트가 끝나기 전에 취소되지만, `runTest` 의 스코프에서 `launch` 한 코루틴은 `runTest` 가 완료될 때까지 기다린다. `StateFlow`·`SharedFlow` 처럼 완료되지 않는 Flow 를 수집하면 테스트가 제한 시간까지 끝나지 않는다. `job.cancel()` 을 테스트 끝에 호출해도, 앞의 단언이 실패하면 호출되지 않아 같은 문제가 발생한다.

## 위반

`runTest` 블록에서 `backgroundScope` 가 아닌 스코프로 `launch` 하고, 그 안에서 완료되지 않는 Flow 를 `collect`·`toList`·`collectLatest` 로 수집한다.

```kotlin
@Test
fun continuouslyCollect() = runTest {
    val values = mutableListOf<Int>()
    val job = launch(UnconfinedTestDispatcher(testScheduler)) {
        repository.scores().toList(values)
    }

    dataSource.emit(1)
    assertEquals(10, values[0])

    job.cancel()
}
```

## 수정

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

- `flowOf`·`take(n)`·`first()` 처럼 완료되는 Flow 를 수집하는 경우
- Flow 의 완료 자체를 검증하기 위해 `job.join()` 으로 기다리는 경우
