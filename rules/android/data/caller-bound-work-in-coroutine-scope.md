---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#create-coroutines-data-layer
---

# 데이터 레이어의 suspend 함수 안에서 데이터를 조회하는 코루틴은 클래스가 보유한 스코프가 아니라 `coroutineScope` 로 시작한다

## 이유

공식 문서는 데이터·비즈니스 레이어에서 코루틴을 만들 때 작업의 수명을 기준으로 스코프를 고르라고 한다.

- 사용자가 현재 화면에 있는 동안에만 필요한 작업은 호출하는 쪽의 생명주기를 따른다. `coroutineScope`·`supervisorScope` 로 시작하면, 호출하는 쪽(주로 ViewModel)이 취소될 때 작업도 함께 취소된다.
- 화면과 관계없이 앱이 실행되는 동안 완료되어야 하는 작업은 호출하는 쪽보다 오래 실행된다. `Application` 처럼 생명주기가 화면보다 긴 클래스가 관리하는 외부 `CoroutineScope` 를 주입받아 시작하면, 호출하는 쪽이 취소되어도 작업은 계속 실행된다.

데이터를 조회해 반환하기만 하는 작업은 첫 번째에 해당한다. 이 작업을 클래스가 보유한 스코프로 시작하면 다음 문제가 생긴다.

- 호출하는 쪽이 취소된 뒤에도 네트워크·DB 요청이 계속 실행된다. 아무도 사용하지 않을 결과를 만드는 데 리소스를 소모한다.
- `async` 에서 발생한 예외가 호출하는 쪽이 아니라 그 스코프로 전파된다.

## 위반

데이터·도메인 레이어의 suspend 함수가 클래스의 `CoroutineScope` 프로퍼티로, 데이터를 조회하기만 하는 `launch`·`async` 를 시작한다.

```kotlin
class ProfileRepository(
    private val userApi: UserApi,
    private val scope: CoroutineScope,
) {
    suspend fun getProfile(userId: String): Profile {
        val user = scope.async { userApi.getUser(userId) }
        val posts = scope.async { userApi.getPosts(userId) }
        return Profile(user.await(), posts.await())  // 사용자가 화면을 벗어나도 두 요청은 계속 실행된다
    }
}
```

## 수정

`coroutineScope` 블록 안에서 `launch`·`async` 를 호출한다. 호출하는 쪽이 취소되면 블록 안의 코루틴도 함께 취소되고, 예외는 호출하는 쪽으로 전파된다. 클래스가 보유한 스코프를 더 이상 쓰지 않으면 프로퍼티도 삭제한다.

```kotlin
class ProfileRepository(
    private val userApi: UserApi,
) {
    suspend fun getProfile(userId: String): Profile = coroutineScope {
        val user = async { userApi.getUser(userId) }
        val posts = async { userApi.getPosts(userId) }
        Profile(user.await(), posts.await())
    }
}
```

## 허용

- 블록이 캐시·DB 저장, 서버 전송처럼 사용자가 화면을 벗어나도 완료되어야 하는 쓰기를 포함하는 경우. 공식 문서의 `externalScope.launch { ... }.join()`, `externalScope.async { ... }.await()` 예시에 해당한다.
- `coroutineScope`·`supervisorScope`·`withContext` 블록 안에서 그 블록의 리시버로 `launch`·`async` 를 호출하는 경우
- 직접 생성한 스코프를 취소하지 않는 코드는 `common/coroutines/cancel-custom-scope` 가, `GlobalScope` 는 `common/coroutines/global-scope` 가 보고한다. 이 룰은 호출하는 쪽의 생명주기를 따라야 하는 작업의 스코프 선택만 보고한다.
- suspend 가 아닌 함수에서 코루틴을 시작하는 코드는 `android/data/expose-suspend-and-flow` 가 보고한다.
