---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#strings
---

# 문자열 연결은 `+` 대신 문자열 템플릿으로 작성한다

## 이유

코틀린 코딩 관례는 문자열 연결보다 문자열 템플릿을 쓰라고 한다. `"id=" + id + ", name=" + name` 은 따옴표와 `+` 가 반복되어 완성된 문자열의 형태를 읽기 어렵고, 공백을 빠뜨리기 쉽다.

## 위반

문자열 리터럴과 값을 `+` 로 연결한다.

```kotlin
val message = "User " + user.id + " not found"
log("count=" + count)
```

## 수정

```kotlin
val message = "User ${user.id} not found"
log("count=$count")
```

## 허용

- 여러 줄에 걸친 긴 리터럴을 줄마다 나누어 `+` 로 연결하는 경우
- 문자열 변수끼리만 연결하는 경우 (`prefix + name`)
- 화면에 표시하는 문구는 템플릿도 코드에 작성한 리터럴이므로 이 룰이 아니라 `android/ui/strings/hardcoded-ui-text` 가 보고한다.
