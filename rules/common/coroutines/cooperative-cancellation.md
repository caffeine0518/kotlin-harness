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

## 허용

- 루프 본문에서 `delay`·`receive`·`emit` 등 kotlinx.coroutines 의 suspend 함수를 호출하는 경우
- 반복 횟수가 적어 짧게 끝나는 루프
