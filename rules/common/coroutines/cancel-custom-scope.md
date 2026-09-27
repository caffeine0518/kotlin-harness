---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/
---

# 직접 생성한 `CoroutineScope` 는 소유자의 수명이 끝날 때 취소한다

## 이유

공식 문서는 직접 생성한 `CoroutineScope` 를 사용할 때 핵심이 수명 종료 시점에 취소하는 것이라고 한다. 취소하지 않으면 코루틴을 시작한 객체가 더 이상 필요 없어도 코루틴이 계속 실행되어 리소스 누수가 된다. 함수 안에서 매번 `CoroutineScope(...)` 를 생성하면 취소할 방법 자체가 없다.

## 위반

```kotlin
fun upload(file: File) {
    CoroutineScope(Dispatchers.IO).launch { api.upload(file) }
}

class Poller {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
    fun start() = scope.launch { while (isActive) { poll(); delay(1_000) } }
    // scope.cancel() 을 호출하는 곳이 없다
}
```

## 수정

수명이 호출 범위 안에 있으면 `coroutineScope { }`·`supervisorScope { }` 를 쓴다. 객체의 수명을 따라야 하면 프로퍼티로 보관하고 `close()` 등 수명 종료 지점에서 `cancel()` 을 호출한다.

```kotlin
suspend fun upload(file: File) = withContext(Dispatchers.IO) { api.upload(file) }

class Poller(
    private val scope: CoroutineScope = CoroutineScope(SupervisorJob() + Dispatchers.Default),
) : AutoCloseable {
    fun start() = scope.launch { while (isActive) { poll(); delay(1_000) } }
    override fun close() = scope.cancel()
}
```

## 허용

- 외부에서 주입받은 스코프(취소 책임이 주입한 쪽에 있다)
- 앱 전체 수명 동안 유지되는 싱글턴 스코프임을 주석으로 적은 경우
