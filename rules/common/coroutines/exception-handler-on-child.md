---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/exception-handling.html#coroutineexceptionhandler
---

# `CoroutineExceptionHandler` 는 자식 코루틴이나 `async` 가 아니라 루트 코루틴에 지정한다

## 이유

`CoroutineExceptionHandler` 는 잡히지 않은 예외에만 호출된다. 자식 코루틴(다른 `Job` 의 컨텍스트에서 생성한 코루틴)은 예외 처리를 부모에게 위임하므로, 자식의 컨텍스트에 지정한 핸들러는 호출되지 않는다. `async` 는 모든 예외를 잡아 `Deferred` 에 보관하므로 `async` 에 지정한 핸들러도 효과가 없다. 핸들러로 예외를 처리했다고 판단한 코드에서 앱이 크래시한다.

## 위반

```kotlin
val handler = CoroutineExceptionHandler { _, e -> log(e) }

viewModelScope.launch {
    launch(handler) { repository.sync() }  // 자식이라 handler 가 호출되지 않는다
}

coroutineScope {
    launch(handler) { repository.sync() }  // coroutineScope 의 자식이다
}

val deferred = scope.async(handler) { repository.load() }  // async 에는 효과가 없다
```

## 수정

```kotlin
viewModelScope.launch(handler) {
    launch { repository.sync() }
}

val deferred = scope.async { repository.load() }
try {
    deferred.await()
} catch (e: IOException) {
    log(e)
}
```

## 허용

- `CoroutineScope` 인스턴스(`viewModelScope`·`lifecycleScope`·주입받은 스코프)에서 직접 호출한 `launch` 에 지정한 경우. 스코프의 `Job` 은 코루틴이 아니므로 그 `launch` 는 루트 코루틴이다.
- `CoroutineScope(SupervisorJob() + handler)` 처럼 스코프를 생성할 때 컨텍스트에 지정한 경우
- `supervisorScope { }` 안에서 직접 시작한 `launch` 에 지정한 경우. `supervisorScope` 의 자식은 예외를 부모에게 위임하지 않는다.
