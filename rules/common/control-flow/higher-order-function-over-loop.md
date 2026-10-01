---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#loops
---

# 거르기·변환·합계를 계산하는 루프는 `filter`·`map`·`sumOf` 같은 고차 함수로 작성한다

## 이유

코틀린 코딩 관례는 루프보다 `filter`·`map` 같은 고차 함수를 쓰라고 한다. 빈 가변 컬렉션을 만들고 루프에서 `add` 하는 코드는 무엇을 계산하는지 루프 본문을 읽어야 알 수 있고, 결과가 가변 컬렉션으로 남는다. 고차 함수는 연산의 이름이 목적을 나타내고, 읽기 전용 컬렉션을 반환한다.

## 위반

루프 앞에서 빈 가변 컬렉션·누적 변수를 선언하고, 루프 본문이 조건에 따라 `add`·`put`·`+=` 만 한다.

```kotlin
val names = mutableListOf<String>()
for (user in users) {
    if (user.active) names.add(user.name)
}

var total = 0
for (item in cart) total += item.price
```

## 수정

```kotlin
val names = users.filter { it.active }.map { it.name }

val total = cart.sumOf { it.price }
```

## 허용

- 루프 안에서 `break`·`return` 으로 일찍 종료하는 경우
- 한 번의 순회로 여러 결과를 계산하는 경우
- 고차 함수 여러 개를 연결하면 중간 컬렉션이 여러 번 생성되어 성능이 문제가 되는 경우. 공식 문서도 연산 비용을 고려하라고 한다.
- 루프 본문에서 suspend 함수·I/O 등 부수 효과가 있는 호출을 하는 경우
