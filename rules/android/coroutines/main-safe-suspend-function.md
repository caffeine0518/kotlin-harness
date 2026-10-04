---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#main-safe
---

# 블로킹 작업을 하는 suspend 함수는 `withContext` 로 메인 스레드 밖에서 실행해 main-safe 하게 만든다

## 이유

`suspend` 키워드만 붙여서는 실행 스레드가 바뀌지 않는다. 메인 스레드에서 호출된 suspend 함수가 블로킹 API 를 호출하면 UI 갱신이 멈추고, ANR(Application Not Responding) 이 발생할 수 있다.

suspend 함수는 메인 스레드에서 호출해도 안전해야(main-safe) 한다. 메인 스레드 밖으로 실행을 옮기는 책임은 블로킹 작업을 하는 클래스가 진다. 그래야 호출하는 쪽이 디스패처를 지정하지 않고 메인 스레드에서 호출할 수 있다.

ViewModel 이 IO 디스패처로 전환해도 메인 스레드는 블로킹되지 않는다. 다만 데이터 처리는 데이터 레이어에 두므로, 블로킹 작업은 리포지토리 같은 데이터 레이어 클래스가 main-safe 하게 감싸고 ViewModel 은 그 suspend 함수를 호출하기만 하면 된다. 그래서 이 룰은 ViewModel 이 IO 디스패처로 전환하는 코드를 허용에 해당하지 않으면 위반으로 판정한다.

## 위반

다음 중 하나에 해당한다.

- suspend 함수 본문, 또는 디스패처를 지정하지 않은 `viewModelScope.launch { }`·`lifecycleScope.launch { }` 본문에서 `withContext` 없이 블로킹 API 를 호출한다.
- ViewModel(`ViewModel`·`AndroidViewModel` 을 상속한 클래스)에서 `withContext`·`launch`·`async` 에 IO 디스패처를 지정한다. 주입받은 `ioDispatcher` 도 포함한다. 블로킹 API 호출을 `withContext` 로 감싸도 위반이다.

블로킹 API 의 예는 다음과 같다.

- 네트워크: `HttpURLConnection`·`URL.openStream()`·OkHttp `Call.execute()`·Retrofit `Call.execute()`
- 파일 I/O: `File.readText()`·`File.writeText()`·`InputStream.read()`·`FileOutputStream`
- DB: `SQLiteDatabase.query()`·Room DAO 의 suspend 가 아닌 함수
- `Thread.sleep()`

```kotlin
class LoginRepository {
    suspend fun makeLoginRequest(jsonBody: String): LoginResponse {
        val connection = URL(loginUrl).openConnection() as HttpURLConnection
        connection.outputStream.write(jsonBody.toByteArray())
        return parse(connection.inputStream)
    }
}

class NoteViewModel(private val ioDispatcher: CoroutineDispatcher) : ViewModel() {
    fun load(file: File) {
        viewModelScope.launch { _text.value = file.readText() }
    }

    fun save(file: File, text: String) {
        viewModelScope.launch {
            withContext(ioDispatcher) { file.writeText(text) }  // ViewModel 에서 IO 디스패처로 전환한다
        }
    }
}
```

## 수정

블로킹 호출을 주입받은 디스패처의 `withContext` 로 감싼다. ViewModel 에서 블로킹 API 를 호출하거나 IO 디스패처로 전환하고 있으면, 그 호출을 리포지토리 같은 데이터 레이어 클래스의 main-safe 한 suspend 함수로 옮긴다.

```kotlin
class LoginRepository(private val ioDispatcher: CoroutineDispatcher) {
    suspend fun makeLoginRequest(jsonBody: String): LoginResponse = withContext(ioDispatcher) {
        val connection = URL(loginUrl).openConnection() as HttpURLConnection
        connection.outputStream.write(jsonBody.toByteArray())
        parse(connection.inputStream)
    }
}

class NoteRepository(private val ioDispatcher: CoroutineDispatcher) {
    suspend fun read(file: File): String = withContext(ioDispatcher) { file.readText() }

    suspend fun write(file: File, text: String) = withContext(ioDispatcher) { file.writeText(text) }
}

class NoteViewModel(private val noteRepository: NoteRepository) : ViewModel() {
    fun load(file: File) {
        viewModelScope.launch { _text.value = noteRepository.read(file) }
    }

    fun save(file: File, text: String) {
        viewModelScope.launch { noteRepository.write(file, text) }
    }
}
```

## 허용

- 이미 main-safe 한 suspend 함수만 호출하는 경우 (Retrofit·Room 의 suspend 함수, 다른 main-safe suspend 함수). 이 경우 IO·Default 디스패처로 전환한 코드는 `android/coroutines/unnecessary-dispatcher-switch` 가 보고한다.
- ViewModel 이 아닌 클래스에서 블로킹 호출이 다음 블록 안에 있는 경우. `Dispatchers.*` 를 하드코딩한 코드는 `android/coroutines/inject-dispatchers` 가 보고한다.
  - `withContext(Dispatchers.IO)`·`withContext(주입받은 디스패처)`
  - `Dispatchers.IO`·`Dispatchers.Default` 를 지정한 `launch`·`async`
- ViewModel 에서 Default 디스패처로 정렬·필터링·파싱처럼 CPU 를 많이 쓰는 작업을 하는 경우. 블로킹 호출이 아니므로 이 룰이 판정하지 않는다.
- 리스트 생성·매핑처럼 블로킹 호출이 없는 가벼운 작업만 하는 suspend 함수
- 테스트 코드
