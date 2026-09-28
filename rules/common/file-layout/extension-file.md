---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#source-file-organization
---

# 한 클래스의 익스텐션만 모은 파일을 만들지 않는다

## 이유

코틀린 코딩 관례는 클래스를 쓰는 모든 코드에 필요한 익스텐션 함수는 그 클래스와 같은 파일에 두고, 특정 코드에서만 의미 있는 익스텐션 함수는 그 코드 옆에 두라고 한다. 어떤 클래스의 익스텐션을 모두 모으기 위한 파일은 만들지 않는다. `UserExtensions.kt` 에 익스텐션을 모으면 각 익스텐션을 어디서 쓰는지 파일 이름으로 알 수 없고, 한 곳에서만 쓰는 익스텐션도 public 으로 남는다.

## 위반

파일 이름이 `<타입>Extensions.kt`·`<타입>Ext.kt`·`<타입>Ktx.kt` 형식이고, 파일의 최상위 선언이 모두 그 타입의 익스텐션이며, 그 타입이 같은 모듈에 선언되어 있다.

```kotlin
// UserExtensions.kt
fun User.displayName(): String = "$firstName $lastName"
fun User.isAdult(): Boolean = age >= 19
```

## 수정

모든 호출하는 쪽에 필요한 익스텐션은 `User.kt` 로 옮기고, 한 화면에서만 쓰는 익스텐션은 그 화면 파일에 `private` 으로 선언한다.

```kotlin
// User.kt
data class User(val firstName: String, val lastName: String, val age: Int)

fun User.displayName(): String = "$firstName $lastName"
```

## 허용

- 다른 모듈·라이브러리의 타입(`String`·`Context`·`Flow` 등)에 대한 익스텐션. 그 타입의 파일에 둘 수 없다.
- 파일을 옮기면 import 가 바뀌어 여러 모듈을 수정해야 하므로, 이 룰의 위반은 리포트에만 적고 수정하지 않는다.
