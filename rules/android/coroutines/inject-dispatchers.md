---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#inject-dispatchers
---

# 코루틴을 시작하거나 `withContext` 를 호출할 때 `Dispatchers` 를 하드코딩하지 않고 주입한다

## 이유

Android 공식 권장 사항이다. 디스패처를 생성자로 주입받으면 단위 테스트와 계측 테스트에서 `TestDispatcher` 로 교체할 수 있어 테스트가 결정적으로 실행된다. 클래스 안에서 `Dispatchers.IO`·`Dispatchers.Default` 를 직접 지정하면 테스트에서 교체할 방법이 없어, 코드가 여러 스레드에서 실행되고 `delay` 도 건너뛰지 못한다.

## 위반

클래스 본문에서 `withContext`·`launch`·`async`·`flowOn`·`CoroutineScope(...)` 에 `Dispatchers.IO`·`Dispatchers.Default`·`Dispatchers.Unconfined` 를 직접 지정한다.

```kotlin
class NewsRepository {
    suspend fun loadNews() = withContext(Dispatchers.Default) { /* ... */ }
}

class LogWriter(private val scope: CoroutineScope, private val file: File) {
    fun write(line: String) {
        scope.launch(Dispatchers.IO) { file.appendText(line) }
    }
}
```

## 수정

`CoroutineDispatcher` 를 생성자 파라미터로 받는다. 공식 문서의 예시처럼 기본값으로 `Dispatchers.*` 를 지정해도 된다.

```kotlin
class NewsRepository(
    private val defaultDispatcher: CoroutineDispatcher = Dispatchers.Default,
) {
    suspend fun loadNews() = withContext(defaultDispatcher) { /* ... */ }
}

class LogWriter(
    private val scope: CoroutineScope,
    private val file: File,
    private val ioDispatcher: CoroutineDispatcher,
) {
    fun write(line: String) {
        scope.launch(ioDispatcher) { file.appendText(line) }
    }
}
```

## 허용

- 생성자·함수 파라미터의 기본값으로 지정한 `Dispatchers.*`
- 디스패처를 제공하는 DI 모듈 (Hilt `@Provides`·Koin `single { Dispatchers.IO }` 등)
- 최상위 `main` 함수
- 테스트 코드 (테스트의 디스패처는 `android/coroutines/inject-test-dispatchers` 가 보고한다)
- `Dispatchers.Main`·`Dispatchers.Main.immediate`. 테스트에서 `Dispatchers.setMain` 으로 교체할 수 있다.
- 디스패처를 지정하지 않은 `viewModelScope.launch { }`·`lifecycleScope.launch { }`
- 주입받은 디스패처로 불필요하게 전환하는 경우. main-safe 함수만 호출하면서 IO·Default 디스패처로 전환하는 코드는 `android/coroutines/unnecessary-dispatcher-switch` 가 보고한다.
