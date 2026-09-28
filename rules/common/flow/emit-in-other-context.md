---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coroutines-flow.html
---

# `flow { }` 빌더에서 `withContext`·`launch` 블록 안에서 `emit` 을 호출하지 않는다

## 이유

`flow { }` 빌더는 빌더가 실행되는 코루틴 컨텍스트에서만 값을 방출해야 한다. 공식 문서는 빌더 안에서 `withContext()` 로 컨텍스트를 바꾸거나, 다른 코루틴을 시작해 그 블록에서 `emit()` 을 호출할 수 없다고 한다. 이 규칙을 어기면 수집할 때 `IllegalStateException`(`Flow invariant is violated`)이 발생한다. 업스트림을 다른 디스패처에서 실행하려면 `flowOn()` 을 쓴다.

## 위반

```kotlin
fun items(): Flow<Item> = flow {
    withContext(Dispatchers.IO) {
        emit(api.load())
    }
}

fun events(): Flow<Event> = flow {
    coroutineScope {
        launch { emit(Event.Started) }
    }
}
```

## 수정

```kotlin
fun items(): Flow<Item> = flow {
    emit(api.load())
}.flowOn(Dispatchers.IO)

// withContext 는 값을 계산하는 데만 쓰고, emit 은 블록 밖에서 호출한다
fun items(): Flow<Item> = flow {
    val item = withContext(Dispatchers.IO) { api.load() }
    emit(item)
}

// 여러 코루틴에서 값을 보내야 하면 channelFlow 를 쓴다
fun events(): Flow<Event> = channelFlow {
    launch { send(Event.Started) }
}
```

## 허용

- `withContext` 블록 안에 `emit` 호출이 없는 경우
- `channelFlow { }`·`callbackFlow { }` 에서 `send` 를 호출하는 경우
- 디스패처 하드코딩은 이 룰이 아니라 `android/coroutines/inject-dispatchers` 가 보고한다.
