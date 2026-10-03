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

작업의 수명에 따라 아래 순서로 고른다.

1. 수명이 호출 범위 안에 있으면 스코프를 만들지 않고 `suspend` 함수로 작성해 `withContext`·`coroutineScope { }`·`supervisorScope { }` 를 쓴다.
2. 객체의 수명을 따라야 하면 소유자의 스코프(`viewModelScope` 등)를 주입받는다. 소유자가 취소되면 함께 취소되므로 직접 취소하지 않는다. 그 객체의 작업만 멈춰야 하면 스코프가 아니라 `launch` 가 반환한 `Job` 을 취소한다.
3. 주입받을 스코프가 없을 때만 직접 생성하고, `close()` 등 수명 종료 지점에서 `cancel()` 을 호출한다.

```kotlin
// 1
suspend fun upload(file: File) = withContext(Dispatchers.IO) { api.upload(file) }

// 2
class Poller(private val scope: CoroutineScope) {
    private var job: Job? = null
    fun start() { job = scope.launch { while (isActive) { poll(); delay(1_000) } } }
    fun stop() { job?.cancel() }
}

// 3
class Poller : AutoCloseable {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
    fun start() = scope.launch { while (isActive) { poll(); delay(1_000) } }
    override fun close() = scope.cancel()
}
```

3의 `AutoCloseable` 은 `close()` 하나를 가진 표준 인터페이스다. 구현하면 `use { }` 로 `close()` 를 빠뜨리지 않게 할 수 있고, AndroidX `ViewModel` 에 전달하면 ViewModel 이 정리될 때 `close()` 를 호출한다.

## 허용

- 외부에서 주입받은 스코프(취소 책임이 주입한 쪽에 있다)
- 앱 전체 수명 동안 유지되는 싱글턴 스코프임을 주석으로 적은 경우
