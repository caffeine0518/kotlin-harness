---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/shared-mutable-state-and-concurrency.html#the-problem
---

# 여러 코루틴이 동시에 변경하는 가변 상태는 동기화한다

## 이유

`Dispatchers.Default`·`Dispatchers.IO` 처럼 멀티스레드 디스패처에서 실행되는 코루틴이 같은 `var`·가변 컬렉션을 동기화 없이 변경하면 갱신이 유실된다. `@Volatile` 은 변수를 읽는 연산 하나, 쓰는 연산 하나가 각각 원자적으로 실행되고 다른 스레드에 바로 보이게 할 뿐, 여러 연산을 묶어 원자적으로 실행하지는 않는다. `counter++` 는 읽기·더하기·쓰기 세 연산이고, 읽기와 쓰기 사이에 다른 코루틴이 끼어들 수 있으므로 `@Volatile` 을 지정해도 갱신이 유실된다.

```
counter = 0
A: 읽기 → 0
B: 읽기 → 0          // A 가 쓰기 전이라 B 도 0 을 읽는다
A: 0 + 1 → 쓰기 1
B: 0 + 1 → 쓰기 1    // A 의 갱신을 덮어쓴다. 결과는 2 가 아니라 1
```

## 위반

```kotlin
var counter = 0
withContext(Dispatchers.Default) {
    repeat(100) { launch { counter++ } }
}

@Volatile var total = 0
val results = mutableListOf<Item>()
items.forEach { scope.launch(Dispatchers.IO) { results += load(it); total++ } }
```

## 수정

단순한 값은 스레드 안전 자료 구조를, 복잡한 상태는 `Mutex` 나 단일 스레드 한정(thread confinement)을 쓴다. `Mutex.withLock` 은 스레드를 블로킹하지 않는다.

```kotlin
val counter = AtomicInteger()
withContext(Dispatchers.Default) {
    repeat(100) { launch { counter.incrementAndGet() } }
}

val mutex = Mutex()
val results = mutableListOf<Item>()
items.forEach { scope.launch(Dispatchers.IO) { val item = load(it); mutex.withLock { results += item } } }

// 결과를 모으기만 하면 async 로 반환한다
val results = coroutineScope { items.map { async(Dispatchers.IO) { load(it) } }.awaitAll() }
```

## 허용

- 모든 접근이 단일 스레드 디스패처(`Dispatchers.Main`, `runBlocking` 스레드 등)에서만 실행되는 경우
