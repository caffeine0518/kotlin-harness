---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#overload-layout
---

# 같은 이름의 오버로드는 클래스 안에서 연달아 선언한다

## 이유

코틀린 코딩 관례는 클래스의 오버로드를 항상 서로 옆에 두라고 한다. 오버로드가 떨어져 있으면 한 오버로드를 수정할 때 다른 오버로드가 있다는 것을 알기 어렵고, 기본값·동작이 서로 달라진다.

## 위반

같은 이름의 멤버 함수 사이에 다른 이름의 멤버가 선언되어 있다.

```kotlin
class Logger {
    fun send(message: String) { /* ... */ }
    fun flush() { /* ... */ }
    fun send(message: String, level: Level) { /* ... */ }
}
```

## 수정

```kotlin
class Logger {
    fun send(message: String) { /* ... */ }
    fun send(message: String, level: Level) { /* ... */ }
    fun flush() { /* ... */ }
}
```

## 허용

- 최상위 함수. 공식 문서는 클래스 안의 오버로드만 규정한다.
- 파라미터만 추가되는 오버로드는 이 룰이 아니라 `common/functions/default-parameter-over-overload` 가 보고한다.
