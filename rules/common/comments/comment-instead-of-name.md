---
severity: info
applies_to: "**/*.kt"
source: https://testing.googleblog.com/2017/07/code-health-to-comment-or-not-to-comment.html
---

# 이름이나 타입으로 나타낼 수 있는 설명은 주석 대신 이름·타입으로 작성한다

## 이유

이름과 타입은 코드와 함께 바뀌지만, 주석은 코드가 바뀌어도 그대로 남아 틀린 설명이 된다. 타입은 규칙을 컴파일러가 확인하게 한다. 형식·생성 규칙을 지킨 값만 만들 수 있는 타입을 쓰면, 호출부마다 규칙을 지킬 필요가 없다.

## 위반

- 변수·파라미터·프로퍼티의 뜻이나 단위를 설명하는 주석
- 값의 형식이나 생성 규칙을 설명하는 주석. 정규화 규칙(숫자만 남긴다 등)이나 경우에 따라 다른 값을 쓰는 규칙이다.
- 조건식의 뜻을 설명하는 주석. KDoc 이 조건을 불릿으로 나열하는 경우도 포함한다.
- 함수 본문의 코드 블록 앞에서 그 블록이 하는 일을 요약하는 주석

```kotlin
// 만료까지 남은 일수
val d = ChronoUnit.DAYS.between(today, expiry)

val timeout = 30  // 초 단위

data class Contact(
    /** 하이픈을 포함해도 된다. 비교할 때 숫자만 남긴다. */
    val phone: String,
    /** 내부 연락처는 사용자 id 를, 외부 연락처는 "ext-" 로 시작하는 값을 쓴다. */
    val id: String,
)

// 구독 중이고 플랜 변경을 예약하지 않은 경우
if (sub.isActive && sub.nextPlanId == sub.planId) { /* ... */ }

fun checkout(cart: Cart) {
    // 재고 확인
    for (item in cart.items) {
        require(stock.available(item.id) >= item.quantity)
    }
    // 결제
    payment.charge(cart.total)
}
```

## 수정

- 뜻·단위: 이름에 포함한다(`daysUntilExpiry`, `timeoutMillis`). `Duration` 같은 전용 타입이 있으면 그 타입을 쓴다.
- 형식·생성 규칙: 생성자를 `private` 으로 두고, 규칙을 적용하는 팩토리로만 값을 만드는 value class 를 도입한다.
- 조건식: 조건을 지역 변수로 추출하고, 주석 내용을 변수 이름으로 쓴다. 불릿으로 나열한 조건은 항목마다 변수 하나가 된다.
- 코드 블록 요약: 블록을 함수로 추출하고, 주석 내용을 함수 이름으로 쓴다.

```kotlin
val daysUntilExpiry = ChronoUnit.DAYS.between(today, expiry)

val timeout = 30.seconds

@JvmInline
value class PhoneDigits private constructor(val value: String) {
    companion object {
        fun of(phone: String) = PhoneDigits(phone.filter(Char::isDigit))
    }
}

@JvmInline
value class ContactId private constructor(val value: String) {
    companion object {
        fun internal(user: User) = ContactId(user.id)
        fun external(phone: PhoneDigits) = ContactId("ext-${phone.value}")
    }
}

data class Contact(val phone: PhoneDigits, val id: ContactId)

val hasNoPlanChangeScheduled = sub.nextPlanId == sub.planId
if (sub.isActive && hasNoPlanChangeScheduled) { /* ... */ }

fun checkout(cart: Cart) {
    verifyStock(cart)
    payment.charge(cart.total)
}
```

형식·생성 규칙은 타입을 도입하면서 리포 안의 호출부도 함께 수정한다. 값을 만들던 호출부는 팩토리를 호출하고, 값을 읽던 호출부는 `value` 를 읽는다. 아래 경우는 수정하지 않고, 수정 제안에 도입할 타입과 팩토리를 적는다.

- 호출부에서 어느 팩토리를 호출할지 코드만으로 판정할 수 없다.
- 선언이 리포 밖에서도 쓰이는 모듈에 있다. 예: `maven-publish` 를 적용한 라이브러리 모듈

코드 블록 요약은 리포트의 수정 제안에만 적고 수정하지 않는다. 함수를 어디까지 추출할지 하나로 정해지지 않는다.

## 허용

- 이름으로 옮기면 지나치게 길어지는 이유 설명
- 코드로 강제할 수 없는 제약 설명. 코드로 강제할 수 있는 전제 조건은 `common/comments/precondition-comment` 가 보고한다.
- 외부 API·프로토콜이 정한 이름이어서 바꿀 수 없는 식별자의 설명
