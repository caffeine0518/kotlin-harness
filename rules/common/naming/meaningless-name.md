---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#choose-good-names
---

# 클래스 이름에 `Manager`·`Wrapper` 처럼 의미 없는 단어를 쓰지 않는다

## 이유

코틀린 코딩 관례는 이름으로 그 요소의 목적을 알 수 있어야 하므로 `Manager`·`Wrapper` 같은 의미 없는 단어를 피하라고 한다. 클래스 이름은 그 클래스가 무엇인지 설명하는 명사다(`List`·`PersonReader`). `UserManager` 는 사용자에 대해 무엇을 하는지 알 수 없어, 관련 없는 기능이 한 클래스에 모이게 한다.

## 위반

클래스·인터페이스·object 이름이 `Manager`·`Wrapper` 로 끝나거나, 그 단어 외에 역할을 나타내는 단어가 없다.

```kotlin
class UserManager(private val api: UserApi, private val prefs: SharedPreferences)
class ResponseWrapper<T>(val data: T?, val error: String?)
```

## 수정

클래스가 실제로 하는 일을 이름으로 쓴다. 이름을 정할 수 없을 만큼 역할이 많으면 클래스를 나눈다.

```kotlin
class UserRepository(private val api: UserApi, private val prefs: SharedPreferences)
class ApiResult<T>(val data: T?, val error: String?)
```

## 허용

- Android `WindowManager`·`FragmentManager`·`WorkManager` 처럼 프레임워크·라이브러리 타입을 상속하거나 구현하는 경우, 그 타입의 이름을 따르는 경우
- 수정 방법이 하나로 정해지지 않으므로 리포트에만 적고 수정하지 않는다.
