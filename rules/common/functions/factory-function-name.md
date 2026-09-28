---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#factory-functions
---

# 특별한 동작을 하는 팩토리 함수에는 클래스와 다른 이름을 붙인다

## 이유

코틀린 코딩 관례는 팩토리 함수에 클래스와 같은 이름을 붙이지 말고, 팩토리 함수의 동작이 왜 특별한지 나타내는 이름을 쓰라고 한다. 특별한 의미가 없을 때만 클래스와 같은 이름을 쓸 수 있다. `Point(angle, radius)` 는 생성자 호출처럼 보여, 인수가 좌표가 아니라 극좌표라는 것을 호출 코드에서 알 수 없다.

## 위반

클래스와 같은 이름의 최상위 함수·companion 의 `invoke` 가, 인수를 변환·검증하거나 캐시된 인스턴스를 반환하는 등 생성자와 다른 동작을 한다.

```kotlin
fun Point(angle: Double, radius: Double): Point =
    Point(radius * cos(angle), radius * sin(angle))
```

## 수정

```kotlin
class Point(val x: Double, val y: Double) {
    companion object {
        fun fromPolar(angle: Double, radius: Double) = Point(radius * cos(angle), radius * sin(angle))
    }
}
```

## 허용

- 인터페이스와 같은 이름으로 기본 구현을 생성하는 함수(`fun CoroutineScope(context)`, `fun MutableStateFlow(value)`)처럼 특별한 의미 없이 인스턴스를 생성하는 경우
