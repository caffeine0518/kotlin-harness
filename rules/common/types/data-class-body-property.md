---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/data-classes.html#properties-declared-in-the-class-body
---

# data class 의 상태를 나타내는 프로퍼티는 주 생성자에 선언한다

## 이유

data class 에서 컴파일러가 자동으로 생성하는 함수(`equals()`·`hashCode()`·`toString()`·`copy()`·`componentN()`)는 주 생성자에 선언한 프로퍼티만 사용한다. 그래서 클래스 본문에 선언한 프로퍼티는 아래처럼 동작한다.

- 값이 달라도 `equals()` 가 두 객체를 같다고 판정한다.
- `toString()` 결과에 나타나지 않는다.
- `copy()` 로 만든 객체에 값이 복사되지 않고, 선언한 초기값을 갖는다.

## 위반

```kotlin
data class Person(val name: String) {
    var age: Int = 0
}

val a = Person("John").apply { age = 10 }
val b = Person("John").apply { age = 20 }
a == b          // true
a.copy().age    // 0
```

## 수정

```kotlin
data class Person(val name: String, val age: Int = 0)
```

## 허용

- 게터만 있고 backing field 가 없는 프로퍼티(예: `val fullName get() = "$first $last"`)
- 주 생성자 프로퍼티로 계산한 값을 초기화하는 `val` 프로퍼티(예: `val fullName = "$first $last"`). 비교 결과가 달라지지 않는다.
- 캐시·로그용 값처럼 `equals()`·`copy()` 에서 제외하는 것이 의도인 경우. 그 의도를 주석으로 적었으면 위반이 아니다.
