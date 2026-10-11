---
severity: info
applies_to: "**/*.kt"
source: https://testing.googleblog.com/2017/07/code-health-to-comment-or-not-to-comment.html
---

# 이름이나 타입으로 나타낼 수 있는 설명은 주석 대신 이름·타입으로 작성한다

## 이유

단위는 `widthInPixels`·`timeoutMillis` 처럼 이름에 포함하고, 가능하면 `Duration` 같은 전용 타입을 쓴다. 복잡한 식은 변수로, 주석으로 설명한 코드 블록은 함수로 추출하고 주석 내용을 이름으로 쓴다. 값의 형식·생성 규칙은 그 규칙을 지킨 값만 만들 수 있는 타입으로 옮기면, 호출부마다 규칙을 지킬 필요가 없다. 이름과 타입은 코드와 함께 바뀌지만 주석은 코드가 바뀌어도 그대로 남는다.

## 위반

- 변수·파라미터·프로퍼티의 뜻이나 단위를 설명하는 주석
- 조건식의 뜻을 설명하는 주석
- 함수 본문의 코드 블록 앞에서 그 블록이 하는 일을 요약하는 주석
- KDoc 이 조건을 불릿으로 나열하는 경우. 각 항목이 지역 변수 이름이 된다.
- 값의 형식이나 생성 규칙을 설명하는 주석. 정규화 규칙(숫자만 남긴다 등)이나 경우에 따라 다른 값을 쓰는 규칙이다.

```kotlin
// 만료까지 남은 일수
val d = ChronoUnit.DAYS.between(today, expiry)

val timeout = 30  // 초 단위

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

data class Contact(
    /** 하이픈을 포함해도 된다. 비교할 때 숫자만 남긴다. */
    val phone: String,
    /** 내부 연락처는 사용자 id 를, 외부 연락처는 "ext-" 로 시작하는 값을 쓴다. */
    val id: String,
)
```

## 수정

```kotlin
val daysUntilExpiry = ChronoUnit.DAYS.between(today, expiry)

val timeout = 30.seconds

val hasNoPlanChangeScheduled = sub.nextPlanId == sub.planId
if (sub.isActive && hasNoPlanChangeScheduled) { /* ... */ }

fun checkout(cart: Cart) {
    verifyStock(cart)
    payment.charge(cart.total)
}

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
```

## 허용

- 이름으로 옮기면 지나치게 길어지는 이유 설명, 코드로 강제할 수 없는 제약 설명. 코드로 강제할 수 있는 전제 조건은 `common/comments/precondition-comment` 가 보고한다.
- 외부 API·프로토콜이 정한 이름이어서 바꿀 수 없는 식별자의 설명
- 함수 추출은 수정 방법이 하나로 정해지지 않으므로, 코드 블록 요약 주석은 리포트에만 적고 수정하지 않는다.
- 형식·생성 규칙을 타입으로 옮기면 호출부도 함께 수정해야 하므로, 리포트의 수정 제안에 도입할 타입과 팩토리를 적고 수정하지 않는다.
