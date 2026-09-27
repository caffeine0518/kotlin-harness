---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#create-coroutines-data-layer
---

# 데이터 레이어의 suspend 함수에서 결과만 반환하는 동시 작업은 `coroutineScope` 로 시작한다

## 이유

공식 문서는 데이터·비즈니스 레이어에서 코루틴을 만들 때 작업의 수명을 기준으로 스코프를 고르라고 한다.

- 사용자가 현재 화면에 있을 때만 의미 있는 작업은 호출하는 쪽의 생명주기를 따라야 한다. 이때는 `coroutineScope`·`supervisorScope` 를 쓴다. 호출하는 쪽(주로 ViewModel)이 취소되면 작업도 취소된다.
- 앱이 열려 있는 동안 완료되어야 하고 특정 화면에 묶이지 않는 작업은 호출하는 쪽보다 오래 실행되어야 한다. 이때는 `Application` 등 화면보다 오래 사는 클래스가 관리하는 외부 `CoroutineScope` 를 주입받아 쓴다.

결과를 반환하기만 하는 작업을 클래스가 보유한 스코프로 시작하면, 호출하는 쪽이 취소된 뒤에도 네트워크·DB 요청이 계속 실행되어 결과를 사용하지 않는 작업에 리소스를 소모한다. 또 `async` 에서 발생한 예외가 호출하는 쪽이 아닌 그 스코프로 전파된다.

## 위반

리포지토리·데이터 소스·use case(이름이 `Repository`·`DataSource`·`UseCase` 로 끝나는 클래스)의 suspend 함수가 아래를 모두 만족한다.

- 클래스가 보유한 `CoroutineScope` 프로퍼티(주입받았거나 직접 생성했거나)로 `launch`·`async` 를 호출한다
- 시작한 코루틴의 블록이 데이터를 조회해 반환하기만 하고, 캐시·DB·서버에 쓰는 코드를 포함하지 않는다

```kotlin
class BookAndAuthorsRepository(
    private val booksDataSource: BooksDataSource,
    private val authorsDataSource: AuthorsDataSource,
    private val externalScope: CoroutineScope,
) {
    suspend fun getBookAndAuthors(): BookAndAuthors {
        val books = externalScope.async { booksDataSource.getAllBooks() }
        val authors = externalScope.async { authorsDataSource.getAllAuthors() }
        return BookAndAuthors(books.await(), authors.await())
    }
}
```

## 수정

```kotlin
suspend fun getBookAndAuthors(): BookAndAuthors = coroutineScope {
    val books = async { booksDataSource.getAllBooks() }
    val authors = async { authorsDataSource.getAllAuthors() }
    BookAndAuthors(books.await(), authors.await())
}
```

## 허용

- 블록이 캐시·DB 저장, 서버 전송 등 사용자가 화면을 벗어나도 완료되어야 하는 쓰기를 포함하는 경우. 공식 문서의 `externalScope.launch { ... }.join()`, `externalScope.async { ... }.await()` 예시에 해당한다.
- `coroutineScope`·`supervisorScope`·`withContext` 블록 안에서 그 블록의 리시버로 `launch`·`async` 를 호출하는 경우
- 직접 생성한 스코프를 취소하지 않는 코드는 `common/coroutines/cancel-custom-scope` 가, `GlobalScope` 는 `common/coroutines/global-scope` 가 보고한다. 이 룰은 호출하는 쪽의 생명주기를 따라야 하는 작업의 스코프 선택만 보고한다.
- suspend 가 아닌 함수에서 코루틴을 시작하는 코드는 `android/data/expose-suspend-and-flow` 가 보고한다.
