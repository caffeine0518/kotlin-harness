---
severity: warning
applies_to: "**/*.kt"
source: https://testing.googleblog.com/2017/07/code-health-to-comment-or-not-to-comment.html
---

# 이름이나 타입으로 나타낼 수 있는 설명은 주석 대신 이름·타입으로 작성한다

## 이유

Google Testing Blog 의 Code Health 글은 주석 대신 이름과 타입으로 정보를 나타내라고 한다. 단위는 `widthInPixels`·`timeoutMillis` 처럼 이름에 포함하고, 가능하면 `Duration` 같은 전용 타입을 쓴다. Martin Fowler 의 《Refactoring》은 설명 주석을 코드 스멜로 분류하고, 복잡한 식은 변수 추출(Extract Variable)로, 주석으로 설명한 코드 블록은 함수 추출(Extract Method)로 바꾸고 주석 내용을 이름으로 쓰라고 한다. 이름은 코드와 함께 바뀌지만 주석은 코드가 바뀌어도 그대로 남는다.

## 위반

- 변수·파라미터·프로퍼티의 뜻이나 단위를 설명하는 주석
- 조건식의 뜻을 설명하는 주석
- 함수 본문의 코드 블록 앞에서 그 블록이 하는 일을 요약하는 주석
- KDoc 이 조건을 불릿으로 나열하는 경우. 각 항목이 지역 변수 이름이 된다.

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
```

## 허용

- 이름으로 옮기면 지나치게 길어지는 이유·제약 설명
- 외부 API·프로토콜이 정한 이름이어서 바꿀 수 없는 식별자의 설명
- 함수 추출은 수정 방법이 하나로 정해지지 않으므로, 코드 블록 요약 주석은 리포트에만 적고 수정하지 않는다.
