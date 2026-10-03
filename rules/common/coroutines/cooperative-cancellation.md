---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coroutines-cancellation.html#cancellation-is-cooperative
---

# 일시 중단 없이 오래 실행되는 코루틴 루프는 취소를 확인한다

## 이유

코루틴 취소는 협력적이다. 코루틴은 일시 중단 지점에 도달하거나 취소를 명시적으로 확인할 때만 취소에 반응한다. suspend 함수를 호출하지 않는 CPU 집약 루프는 취소되어도 끝까지 실행되고, 같은 스레드의 다른 코루틴도 실행되지 못한다.

## 위반

```kotlin
scope.launch(Dispatchers.Default) {
    for (file in files) {
        hash(file)  // suspend 함수가 아니다
    }
}

scope.launch {
    while (true) {
        compute()
    }
}
```

## 수정

반복마다 `yield()` 를 호출하거나, 다른 코루틴에 스레드를 양보할 필요가 없으면 `ensureActive()`·`isActive` 로 확인한다.

```kotlin
scope.launch(Dispatchers.Default) {
    for (file in files) {
        ensureActive()
        hash(file)
    }
}

scope.launch {
    while (isActive) {
        compute()
    }
}
```

반복 본문이 파일·소켓 읽기 같은 블로킹 I/O 를 호출하면, 그 호출을 `runInterruptible` 로 감싼 suspend 함수로 바꾼다. 호출할 때마다 취소를 확인하고, 취소되면 실행 중인 스레드를 인터럽트해 블로킹 호출도 중단한다. 반복문에는 확인 코드를 추가하지 않는다.

```kotlin
suspend fun hash(file: File): Hash = runInterruptible(Dispatchers.IO) { blockingHash(file) }

scope.launch {
    for (file in files) {
        hash(file)
    }
}
```

결과를 하나씩 호출하는 쪽에 전달해야 하는 작업이면 `flow { }` 로 작성할 수 있다. `emit` 이 값마다 취소를 확인한다. 함수의 반환 타입이 바뀌어 호출하는 쪽도 수정해야 하므로, 기존 함수의 수정으로 적용하지 않고 설계를 바꿀 때 선택한다. `asFlow()` 는 취소를 확인하지 않으므로 `.cancellable()` 을 함께 쓴다.

```kotlin
fun hashes(files: List<File>): Flow<Hash> = flow {
    for (file in files) emit(hash(file))
}.flowOn(Dispatchers.Default)
```

## 허용

- 루프 본문에서 취소를 확인하는 suspend 함수를 호출하는 경우. `delay`·`receive`·`emit`·`runInterruptible` 등 kotlinx.coroutines 의 suspend 함수와, 그 함수를 호출하는 suspend 함수가 해당한다.
- 반복 횟수가 적어 짧게 끝나는 루프
