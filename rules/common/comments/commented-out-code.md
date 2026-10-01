---
severity: info
applies_to: "**/*.kt"
source: https://www.oreilly.com/library/view/clean-code-a/9780136083238/
---

# 주석 처리한 코드를 남기지 않는다

## 이유

Robert C. Martin 의 《Clean Code》 4장은 주석 처리한 코드를 남기지 말라고 한다. 다른 사람은 그 코드가 중요해서 남겼다고 생각해 삭제하지 못하고, 주석 처리한 코드는 계속 쌓인다. 주석 처리한 코드는 컴파일되지 않으므로 주변 코드가 바뀌면 더 이상 동작하지 않는 코드가 된다. 삭제한 코드는 버전 관리 이력에 남는다.

## 위반

주석 안에 컴파일 가능한 형태의 코틀린 문장·선언이 두 줄 이상 있거나, 한 줄이어도 함수 호출·대입·선언이다.

```kotlin
// suspend fun refund(id: String) {
//     gateway.refund(id)
// }

fun load() {
    // cache.clear()
    repository.load()
}
```

## 수정

주석을 삭제한다.

```kotlin
fun load() {
    repository.load()
}
```

## 허용

- KDoc 의 사용 예시 코드 (`/** ```kotlin ... ``` */`, `@sample`)
- 코드가 아닌 이유를 설명하는 문장 안에 식별자·식을 인용한 경우 (`// cache.clear() 를 먼저 호출하면 ...`)
- 라이선스 헤더, 자동 생성 코드
