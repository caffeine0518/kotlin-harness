---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/enum-classes.html#find-enum-constants
---

# 외부 입력으로 enum 상수를 찾을 때는 `null` 을 반환하는 함수를 쓴다

## 이유

enum 상수를 찾는 함수 중 일부는 일치하는 상수가 없으면 예외를 발생시킨다.

- `valueOf()`: 이름이 일치하는 상수가 없으면 `IllegalArgumentException`
- `entries.first { }`: 조건에 맞는 상수가 없으면 `NoSuchElementException`
- `entries[index]`: 인덱스가 범위를 벗어나면 `IndexOutOfBoundsException`

서버 응답·저장값·Intent extra 는 값이 enum 에 있다고 보장할 수 없다. 서버가 새 상수를 추가하거나, 이전 버전에서 저장한 값의 상수가 삭제·변경되면 앱이 종료된다.

## 위반

```kotlin
val status = Status.valueOf(response.status)
val color = Color.entries[prefs.getInt("color", 0)]
val type = Type.entries.first { it.code == json.getInt("type") }
```

## 수정

enum 의 companion object 에 `null` 을 반환하는 조회 함수를 두고, 호출하는 쪽은 그 함수를 호출한다.

```kotlin
enum class Type(val code: Int) {
    TEXT(1), IMAGE(2);

    companion object {
        fun fromCode(code: Int): Type? = entries.find { it.code == code }
    }
}

val status = Status.fromName(response.status) ?: Status.UNKNOWN
val color = Color.fromPosition(prefs.getInt("color", 0)) ?: Color.RED
val type = Type.fromCode(json.getInt("type"))
```

## 허용

- 상수 이름·인덱스를 코드에서 직접 지정해 존재가 보장되는 경우(예: `Color.valueOf("RED")`)
- `runCatching`·`try` 로 예외를 처리하는 경우
