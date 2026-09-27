---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#main-safe
---

# 블로킹 작업을 하는 suspend 함수는 `withContext` 로 메인 스레드 밖에서 실행해 메인 스레드 안전(main-safe)하게 만든다

## 이유

Android 공식 문서는 suspend 함수가 메인 스레드에서 호출해도 안전해야 한다고 한다. 코루틴 안에서 오래 걸리는 블로킹 작업을 하는 클래스가 `withContext` 로 실행을 메인 스레드 밖으로 옮길 책임을 진다. `suspend` 키워드만 붙인다고 스레드가 바뀌지 않는다. 메인 스레드에서 호출되면 블로킹 호출이 UI 갱신을 막아 화면이 멈추고 ANR(Application Not Responding) 이 발생할 수 있다.

## 위반

suspend 함수, 또는 디스패처를 지정하지 않은 `viewModelScope.launch { }`·`lifecycleScope.launch { }` 본문에서 `withContext` 없이 블로킹 API 를 호출한다. 블로킹 API 의 예는 다음과 같다.

- `HttpURLConnection`·`URL.openStream()`·OkHttp `Call.execute()`·Retrofit `Call.execute()`
- `File.readText()`·`File.writeText()`·`InputStream.read()`·`FileOutputStream` 등 파일 I/O
- `SQLiteDatabase.query()`·Room DAO 의 suspend 가 아닌 함수
- `Thread.sleep()`

```kotlin
class LoginRepository {
    suspend fun makeLoginRequest(jsonBody: String): LoginResponse {
        val connection = URL(loginUrl).openConnection() as HttpURLConnection
        connection.outputStream.write(jsonBody.toByteArray())
        return parse(connection.inputStream)
    }
}

class NoteViewModel : ViewModel() {
    fun load(file: File) {
        viewModelScope.launch { _text.value = file.readText() }
    }
}
```

## 수정

블로킹 호출을 주입받은 디스패처의 `withContext` 로 감싼다. 호출하는 쪽은 디스패처를 신경 쓰지 않고 메인 스레드에서 호출한다.

```kotlin
class LoginRepository(private val ioDispatcher: CoroutineDispatcher) {
    suspend fun makeLoginRequest(jsonBody: String): LoginResponse = withContext(ioDispatcher) {
        val connection = URL(loginUrl).openConnection() as HttpURLConnection
        connection.outputStream.write(jsonBody.toByteArray())
        parse(connection.inputStream)
    }
}

class NoteViewModel(private val noteRepository: NoteRepository) : ViewModel() {
    fun load(file: File) {
        viewModelScope.launch { _text.value = noteRepository.read(file) }  // read 는 main-safe
    }
}
```

## 허용

- 이미 main-safe 한 suspend 함수만 호출하는 경우 (Retrofit·Room 의 suspend 함수, 다른 main-safe suspend 함수)
- 블로킹 호출이 `withContext(Dispatchers.IO)`·`withContext(주입받은 디스패처)` 블록이나 `Dispatchers.IO`·`Dispatchers.Default` 를 지정한 `launch`·`async` 블록 안에 있는 경우 (`Dispatchers.*` 를 하드코딩했다면 `android/coroutines/inject-dispatchers` 가 보고한다)
- 리스트 생성·매핑처럼 블로킹이 없는 가벼운 작업만 하는 suspend 함수
- 테스트 코드
