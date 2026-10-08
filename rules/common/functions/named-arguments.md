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
- 같은 기본 타입(`Int`·`Long`·`Float`·`Double`·`String` 등) 파라미터가 둘 이상인 함수·생성자에 그 타입의 인수를 위치 인수로 전달한다. 리터럴이든 변수든 위반이다. 변수 이름이 명확해도 두 값의 순서가 바뀐 것은 컴파일러가 검출하지 못한다.

인수로 전달한 변수 이름이 그 위치가 아닌 다른 같은 타입 파라미터의 이름과 같으면(`sourceId` 파라미터에 `requestKey` 를 전달) 순서가 이미 바뀐 것이다.

```kotlin
show(true)
resize(10, 20)
drawSquare(10, 10, 100, 100, true)
Route(event.requestKey, event.target, event.amount, event.sourceId)
```

## 수정

순서가 바뀐 호출은 위치 그대로 이름을 붙이지 않고, 변수 이름과 같은 파라미터에 전달한다.

```kotlin
show(animated = true)
resize(width = 10, height = 20)
drawSquare(x = 10, y = 10, width = 100, height = 100, fill = true)
Route(sourceId = event.sourceId, target = event.target, amount = event.amount, requestKey = event.requestKey)
```

## 허용

- 같은 타입 파라미터가 하나뿐이고, 함수 이름이나 전달하는 변수 이름으로 의미가 명확한 경우 (`setEnabled(isEnabled)`)
- 순서가 바뀌어도 결과가 같거나, 인수 순서가 관례로 정해진 경우 (`max(a, b)`, `Point(x, y)`)
- 파라미터가 하나이고 함수 이름이 그 의미를 나타내는 경우 (`setVisible(true)`)
- Java 메서드 호출. Java 파라미터에는 이름 있는 인수를 쓸 수 없다.
