---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#immutability
---

# 변경하지 않는 컬렉션은 읽기 전용 인터페이스(`Collection`·`List`·`Set`·`Map`) 타입으로 선언한다

## 이유

공식 코딩 컨벤션은 변경하지 않는 컬렉션을 `Collection`·`List`·`Set`·`Map` 타입으로 선언하라고 한다. 파라미터·반환 타입·프로퍼티를 `MutableList`·`ArrayList`·`HashSet`·`HashMap` 같은 가변 타입으로 선언하면, 호출하는 쪽은 그 컬렉션이 변경될 수 있다고 가정해야 하고 다른 구현(`listOf()` 결과 등)을 전달할 수 없다. 읽기 전용 컬렉션은 공변이라 `List<Rectangle>` 을 `List<Shape>` 타입 파라미터에 전달할 수 있지만, 가변 컬렉션은 공변이 아니다.

읽기 전용 인터페이스는 불변을 보장하지 않는다. 쓰기 연산을 노출하지 않을 뿐, 같은 객체를 가변 타입으로 참조하는 코드가 있으면 내용은 바뀔 수 있다.

## 위반

```kotlin
// 함수 안에서 allowedValues 를 변경하지 않음
fun validateValue(actualValue: String, allowedValues: HashSet<String>) { ... }

// 호출하는 쪽이 결과를 변경할 필요가 없음
fun activeUsers(): MutableList<User> = users.filter { it.isActive }.toMutableList()
```

## 수정

```kotlin
fun validateValue(actualValue: String, allowedValues: Set<String>) { ... }

fun activeUsers(): List<User> = users.filter { it.isActive }
```

## 허용

- 함수 안에서 파라미터 컬렉션을 실제로 변경하는 경우(요소 추가·삭제가 함수의 목적인 경우)
- 호출하는 쪽이 결과를 변경하는 것이 API 의 의도인 경우
- `override` 함수처럼 상위 타입이 시그니처를 정한 경우
- Java API 가 가변 타입을 요구해 그대로 전달하는 경우
- 클래스 안에서 변경하는 public 가변 컬렉션 프로퍼티. `common/immutability/expose-read-only-view` 로 보고한다.
