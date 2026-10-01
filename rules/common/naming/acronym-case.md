---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#choose-good-names
---

# 이름에 쓰는 약어는 두 글자면 모두 대문자로, 세 글자 이상이면 첫 글자만 대문자로 쓴다

## 이유

코틀린 코딩 관례는 선언 이름에 약어를 쓸 때, 두 글자 약어는 두 글자 모두 대문자로(`IOStream`), 세 글자 이상 약어는 첫 글자만 대문자로(`XmlFormatter`·`HttpInputStream`) 쓰라고 한다. `HTTPURLParser` 처럼 약어를 모두 대문자로 이어 쓰면 단어 경계가 구분되지 않는다.

## 위반

클래스·함수·프로퍼티 이름에 세 글자 이상 약어가 모두 대문자로 들어 있다.

```kotlin
class HTTPClient
class XMLParser
fun parseJSON(raw: String): Map<String, Any>
```

## 수정

```kotlin
class HttpClient
class XmlParser
fun parseJson(raw: String): Map<String, Any>
```

## 허용

- 상수(`const val`·SCREAMING_SNAKE_CASE)
- Java·라이브러리 API 를 오버라이드하거나 그 이름을 그대로 따르는 경우 (`getURL()` 오버라이드 등)
- 직렬화 키·DB 컬럼 이름과 일치시켜야 하는 프로퍼티. `@SerialName`·`@ColumnInfo` 로 지정할 수 있으면 위반이다.
