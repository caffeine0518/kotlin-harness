---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/data-classes.html#copying
---

# data class 프로퍼티는 가변 컬렉션 타입으로 선언하지 않는다

## 이유

data class 의 `copy()` 는 얕은 복사라서 프로퍼티가 참조하는 객체는 원본과 복사본이 공유한다. 프로퍼티가 `MutableList` 같은 가변 컬렉션이면, 복사본에 요소를 추가해도 원본이 함께 바뀐다. 공식 문서는 이 동작을 `MutableList<String>` 프로퍼티 예제로 설명한다.

## 위반

```kotlin
data class Employee(val name: String, val roles: MutableList<String>)

val original = Employee("Jamie", mutableListOf("developer"))
val duplicate = original.copy()
duplicate.roles.add("team lead")  // original.roles 도 바뀐다
```

## 수정

```kotlin
data class Employee(val name: String, val roles: List<String>)

val duplicate = original.copy(roles = original.roles + "team lead")
```

## 허용

- 클래스 밖으로 노출하지 않는 `private` data class 이고 `copy()` 를 호출하지 않는 경우
