---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#infix-functions
---

# 인픽스 함수는 비슷한 역할의 두 객체를 다룰 때만 선언하고, 리시버를 변경하는 함수는 인픽스로 선언하지 않는다

## 이유

코틀린 코딩 관례는 비슷한 역할을 하는 두 객체를 다루는 함수만 `infix` 로 선언하라고 한다. 좋은 예로 `and`·`to`·`zip`, 나쁜 예로 `add` 를 든다. 리시버를 변경하는 메서드는 `infix` 로 선언하지 않는다. `list append item` 처럼 쓰면 연산자처럼 읽혀 값을 반환하는 식으로 오해하기 쉽다.

## 위반

- `infix` 함수 본문이 리시버의 상태를 변경한다 (`add`·`put`·프로퍼티 대입 등)
- `infix` 함수의 리시버와 파라미터가 대등한 역할이 아니다 (컨테이너와 요소, 대상과 설정값)

```kotlin
infix fun <T> MutableList<T>.append(item: T) { add(item) }
infix fun View.visibleIf(condition: Boolean) { isVisible = condition }
```

## 수정

```kotlin
fun <T> MutableList<T>.append(item: T) { add(item) }
fun View.visibleIf(condition: Boolean) { isVisible = condition }
```

## 허용

- 테스트 DSL(`shouldBe`·`shouldContain` 등) 처럼 라이브러리가 인픽스 형태를 관례로 쓰는 경우
