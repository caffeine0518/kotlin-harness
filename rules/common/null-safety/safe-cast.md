---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/null-safety.html#safe-casts
---

# 타입이 보장되지 않는 값은 `as` 대신 `as?` 로 캐스트한다

## 이유

`as` 는 대상 타입이 아니면 `ClassCastException` 이 발생한다. `as?` 는 대상 타입이 아니면 `null` 을 반환한다.

## 위반

```kotlin
val id = bundle.get("id") as String
val listener = context as OnClickListener
```

## 수정

```kotlin
val id = bundle.get("id") as? String ?: return
val listener = context as? OnClickListener
    ?: throw IllegalStateException("$context must implement OnClickListener")
```

## 허용

- 직전의 `is` 체크나 `when` 분기처럼 타입이 보장되는 경우 (이때는 스마트 캐스트로 `as` 자체가 필요 없다)
- 캐스트 실패가 프로그래밍 오류이고, 예외를 발생시켜 즉시 실패하는 것이 의도인 경우. 그 의도를 주석으로 적었으면 위반이 아니다.
