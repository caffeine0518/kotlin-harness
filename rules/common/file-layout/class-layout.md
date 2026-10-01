---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#class-layout
---

# 클래스 멤버는 프로퍼티·초기화 블록, 부 생성자, 메서드, companion object 순서로 선언한다

## 이유

코틀린 코딩 관례는 클래스 내용을 프로퍼티 선언과 초기화 블록, 부 생성자, 메서드 선언, companion object 순서로 두라고 한다. 메서드를 알파벳순이나 가시성순으로 정렬하지 말고, 위에서 아래로 읽으며 흐름을 따라갈 수 있게 관련된 것끼리 모은다. 순서가 정해져 있으면 클래스를 열었을 때 상태와 동작을 찾는 위치가 일정하다.

## 위반

- companion object 가 메서드보다 앞에 있다
- 프로퍼티 선언이 메서드 선언 사이나 뒤에 있다
- 부 생성자가 메서드 뒤에 있다

```kotlin
class Player(private val source: Source) {
    companion object {
        const val MAX_VOLUME = 100
    }

    fun play() { /* ... */ }

    private var volume = 50
}
```

## 수정

```kotlin
class Player(private val source: Source) {
    private var volume = 50

    fun play() { /* ... */ }

    companion object {
        const val MAX_VOLUME = 100
    }
}
```

## 허용

- 중첩 클래스. 공식 문서는 사용하는 코드 옆에 두고, 외부에서만 쓰는 중첩 클래스는 companion object 뒤에 두라고 한다.
- 메서드 사이의 순서. 관련된 것끼리 모았는지는 판단이 필요하므로 이 룰은 보고하지 않는다.
