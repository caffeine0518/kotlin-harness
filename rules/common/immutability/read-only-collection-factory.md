---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#immutability
---

# 변경하지 않는 컬렉션은 `listOf`·`setOf`·`mapOf` 로 생성한다

## 이유

공식 코딩 컨벤션은 팩토리 함수로 컬렉션을 생성할 때 가능하면 읽기 전용 타입을 반환하는 함수를 쓰라고 한다. `arrayListOf()`·`mutableListOf()`·`hashMapOf()`·`ArrayList()` 는 가변 타입을 반환하므로, 선언 이후 요소를 추가·삭제하지 않으면 가변 타입일 이유가 없다.

## 위반

```kotlin
val allowedValues = arrayListOf("a", "b", "c")      // 이후 add·remove 없음
val headers = hashMapOf("Accept" to "application/json")  // 이후 put·remove 없음
val empty = ArrayList<String>()                      // 비어 있는 채로 반환만 함
```

## 수정

```kotlin
val allowedValues = listOf("a", "b", "c")
val headers = mapOf("Accept" to "application/json")
val empty = emptyList<String>()
```

## 허용

- 생성 뒤 같은 스코프에서 요소를 추가·삭제·수정하는 경우. 구성 과정만 가변이면 `buildList`·`buildMap` 도 쓸 수 있다.
- 변수나 프로퍼티의 선언 타입이 가변 타입이고, 그 타입이 필요한 API 에 전달하는 경우
- 선언한 파일 밖에서 요소를 변경할 수 있는 `public`·`internal`·`protected` 프로퍼티. 변경 여부를 리뷰 대상 파일만으로 판정할 수 없다. 클래스 안에서 변경하는 경우는 `common/immutability/expose-read-only-view` 로 보고한다.
