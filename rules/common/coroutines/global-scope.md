---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-global-scope/
---

# `GlobalScope` 로 코루틴을 시작하지 않는다

## 이유

`GlobalScope` 는 `@DelicateCoroutinesApi` 로 표시된 API 다. 구조화된 동시성이 적용되지 않아 다음 문제가 생긴다.

- 결과가 더 이상 필요 없어도 계산이 계속 실행된다. 화면이 파괴된 뒤 UI 를 갱신하면 앱이 크래시할 수 있다.
- 취소되지 않거나 재개되지 않는 코루틴은 리소스 누수가 된다.
- `CoroutineExceptionHandler` 가 없어서 `launch` 에서 발생한 예외가 플랫폼 기본 처리로 전파된다. Android 에서는 앱이 크래시한다.

## 위반

```kotlin
fun refresh() {
    GlobalScope.launch {
        val record = withContext(Dispatchers.IO) { fetchLastRecord() }
        component.display(record)
    }
}
```

## 수정

코루틴이 하나면 suspend 함수로 호출하고, 동시 실행이 필요하면 `coroutineScope` 를 쓴다. 호출하는 쪽의 수명보다 오래 실행되어야 하면 수명이 정해진 `CoroutineScope` 를 주입받는다.

```kotlin
suspend fun loadConfigurationAndData() = coroutineScope {
    launch { loadConfiguration() }
    launch { loadData() }
}

class Refresher(private val scope: CoroutineScope) {
    fun refresh() = scope.launch { /* ... */ }
}
```

## 허용

- 앱 전체 수명 동안 실행되어야 하는 최상위 백그라운드 작업에 `@OptIn(DelicateCoroutinesApi::class)` 를 명시하고 `CoroutineExceptionHandler` 를 지정한 경우
