---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#named-arguments
---

# `Boolean` 인수와 같은 기본 타입 인수 여러 개는 이름을 붙여 전달한다

## 이유

코틀린 코딩 관례는 같은 기본 타입 파라미터를 여러 개 받거나 `Boolean` 타입 파라미터를 받는 함수를 호출할 때, 모든 파라미터의 의미가 문맥상 명확하지 않으면 이름 있는 인수를 쓰라고 한다. `show(true)`·`resize(10, 20)` 은 호출 코드만으로 각 값이 무엇인지 알 수 없고, 같은 타입 인수의 순서가 바뀌어도 컴파일 오류가 발생하지 않는다.

## 위반

- `Boolean` 리터럴(`true`·`false`)을 위치 인수로 전달한다
- 같은 기본 타입(`Int`·`Long`·`Float`·`Double`·`String` 등) 파라미터가 둘 이상인 함수에 리터럴을 위치 인수로 전달한다

```kotlin
show(true)
resize(10, 20)
drawSquare(10, 10, 100, 100, true)
```

## 수정

```kotlin
show(animated = true)
resize(width = 10, height = 20)
drawSquare(x = 10, y = 10, width = 100, height = 100, fill = true)
```

## 허용

- 함수 이름이나 전달하는 변수 이름으로 의미가 명확한 경우 (`setEnabled(isEnabled)`, `max(a, b)`, `Point(x, y)`)
- 파라미터가 하나이고 함수 이름이 그 의미를 나타내는 경우 (`setVisible(true)`)
- Java 메서드 호출. Java 파라미터에는 이름 있는 인수를 쓸 수 없다.
