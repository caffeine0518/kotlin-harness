---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#platform-types
---

# 플랫폼 타입 값을 반환·보관하는 public 함수와 프로퍼티는 코틀린 타입을 명시한다

## 이유

Java 에서 온 값은 플랫폼 타입이라 컴파일러가 널 체크를 하지 않는다. 타입을 명시하지 않으면 플랫폼 타입이 API 밖으로 전파되고, 호출하는 쪽에서 `null` 로 인한 NPE 가 발생할 수 있다. 공식 문서는 플랫폼 타입 표현식을 반환하는 public 함수와, 플랫폼 타입 표현식으로 초기화하는 프로퍼티에 코틀린 타입을 명시하라고 한다.

## 위반

```kotlin
fun apiCall() = MyJavaApi.getProperty("name")

class Person {
    val name = MyJavaApi.getProperty("name")
}
```

## 수정

`null` 이 될 수 있으면 널러블 타입으로 명시한다. 논널 타입으로 명시하면 값이 `null` 일 때 대입 시점에 NPE 가 발생한다.

```kotlin
fun apiCall(): String? = MyJavaApi.getProperty("name")

class Person {
    val name: String = requireNotNull(MyJavaApi.getProperty("name"))
}
```

## 허용

- 로컬 변수
- `@Nullable`·`@NonNull` 등 널 허용성 어노테이션이 있는 Java API. 플랫폼 타입이 아니라 실제 코틀린 타입으로 처리된다.
