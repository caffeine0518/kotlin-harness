---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/enum-classes.html#find-enum-constants
---

# 외부 입력으로 enum 상수를 찾을 때는 `null` 을 반환하는 함수를 쓴다

## 이유

`valueOf()` 는 이름이 일치하는 상수가 없으면 `IllegalArgumentException` 이, `entries.first { }` 는 `NoSuchElementException` 이, `entries[index]` 는 `IndexOutOfBoundsException` 이 발생한다. 서버 응답·저장값·Intent extra 처럼 값을 보장할 수 없는 입력에서는 새 상수가 추가된 서버나 이전 버전의 저장값에서 앱이 종료된다. 공식 문서는 `null` 을 반환하는 `entries.getOrNull()`·`firstOrNull()` 과 companion object 조회 함수를 안내한다.

## 위반

```kotlin
val status = Status.valueOf(response.status)
val color = Color.entries[prefs.getInt("color", 0)]
val type = Type.entries.first { it.code == json.getInt("type") }
```

## 수정

```kotlin
val status = Status.entries.find { it.name == response.status } ?: Status.UNKNOWN
val color = Color.entries.getOrNull(prefs.getInt("color", 0)) ?: Color.RED
val type = Type.entries.firstOrNull { it.code == json.getInt("type") }
```

## 허용

- 상수 이름·인덱스를 코드에서 직접 지정해 존재가 보장되는 경우(예: `Color.valueOf("RED")`)
- `runCatching`·`try` 로 예외를 처리하는 경우
