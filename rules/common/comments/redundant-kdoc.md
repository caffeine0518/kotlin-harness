---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/style-guide#exception-self-explanatory
---

# 이름과 시그니처를 반복하기만 하는 KDoc 을 작성하지 않는다

## 이유

Android Kotlin 스타일 가이드는 `getFoo` 같은 단순하고 자명한 함수와 `foo` 같은 프로퍼티에는, "foo 를 반환한다" 외에 적을 내용이 없으면 KDoc 을 생략해도 된다고 한다. Google 코드 리뷰 가이드도 주석은 코드가 무엇을 하는지가 아니라 왜 있는지 설명해야 한다고 한다. 이름·파라미터·반환 타입을 문장으로 옮긴 KDoc 은 정보를 더하지 않고, 시그니처가 바뀔 때 함께 수정되지 않는다.

## 위반

KDoc 의 모든 문장이 선언 이름, 파라미터 이름, 반환 타입을 문장으로 바꾼 것이다.

```kotlin
/** 사용자 이름 */
val userName: String

/**
 * 섹션 제목을 찾는다. 찾으면 true 를 반환한다.
 */
fun findSectionTitle(): Boolean

/** [id] 로 주문을 조회한다. */
suspend fun getOrder(id: String): Order
```

## 수정

KDoc 을 삭제한다. 호출하는 쪽이 알아야 할 동작(예외, 스레드, null 을 반환하는 조건, 부수 효과)이 있으면 그것만 적는다.

```kotlin
val userName: String

fun findSectionTitle(): Boolean

/** 캐시에 없으면 서버에서 조회한다. 주문이 없으면 [OrderNotFoundException] 이 발생한다. */
suspend fun getOrder(id: String): Order
```

## 허용

- 용어 자체를 설명해야 하는 경우. 스타일 가이드는 `canonicalName` 처럼 독자가 용어의 뜻을 모를 수 있으면 생략하지 말라고 한다.
- 라이브러리 모듈의 공개 API. 스타일 가이드는 public 멤버에 KDoc 을 작성하라고 한다.
- 프로젝트가 Dokka·detekt `UndocumentedPublicFunction` 등으로 KDoc 작성을 강제하는 경우
