---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#immutability
---

# 초기화 뒤 재할당하지 않는 로컬 변수와 프로퍼티는 `var` 대신 `val` 로 선언한다

## 이유

`val` 은 재할당을 컴파일 오류로 만들어, 의도하지 않은 재할당을 막는다. `var` 프로퍼티는 체크와 사용 사이에 값이 바뀔 수 있어 스마트 캐스트도 적용되지 않는다.

## 위반

```kotlin
fun total(items: List<Item>): Int {
    var sum = items.sumOf { it.price }  // 이후 재할당 없음
    return sum
}

class Session(token: String) {
    var token = token  // 클래스 안팎 어디서도 재할당하지 않음
}
```

## 수정

```kotlin
fun total(items: List<Item>): Int {
    val sum = items.sumOf { it.price }
    return sum
}

class Session(val token: String)
```

## 허용

- 선언한 파일 밖에서 재할당할 수 있는 `public`·`internal`·`protected` `var` 프로퍼티. 재할당 여부를 리뷰 대상 파일만으로 판정할 수 없다.
- `lateinit var`, 위임 프로퍼티(`by`), `open`·`override` 프로퍼티
- 가변 컬렉션을 `val` 에 할당한 경우. 요소 추가·삭제는 재할당이 아니다.
