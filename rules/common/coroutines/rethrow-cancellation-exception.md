---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coroutines-cancellation.html#cancel-coroutines
---

# 코루틴 안에서 잡은 `CancellationException` 은 다시 전파한다

## 이유

코루틴은 취소를 `CancellationException` 으로 전달한다. 이 예외를 잡으면 취소 전파가 끊어질 수 있다. 다시 전파하지 않으면 취소된 코루틴이 이후 코드를 계속 실행하고, 부모 스코프가 취소를 기다리는 동안 작업이 끝나지 않을 수 있다.

`CancellationException` 은 `IllegalStateException` 의 하위 타입이다. 따라서 suspend 함수 호출을 감싼 `catch (e: Exception)`·`catch (e: Throwable)`·`runCatching` 도 이 예외를 잡는다.

## 위반

```kotlin
suspend fun sync() {
    try {
        repository.fetch()
    } catch (e: Exception) {
        log(e)  // CancellationException 도 여기서 무시된다
    }
}

val result = runCatching { repository.fetch() }  // suspend 함수 안에서
```

## 수정

```kotlin
suspend fun sync() {
    try {
        repository.fetch()
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        log(e)
    }
}

val result = runCatching { repository.fetch() }
    .onFailure { if (it is CancellationException) throw it }
```

## 허용

- `catch` 블록 안에서 `CancellationException` 이면 다시 전파하거나 `ensureActive()` 를 호출하는 경우
- `try` 블록 안에 suspend 함수 호출이 없는 경우
- 구체적인 예외 타입(`IOException` 등)만 잡는 경우
