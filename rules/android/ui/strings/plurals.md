---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/guide/topics/resources/string-resource#Plurals
---

# 개수에 따라 달라지는 문구는 `if` 로 분기하지 않고 `plurals` 리소스로 선언한다

## 이유

복수형 규칙은 언어마다 다르다. 공식 문서에 따르면 영어는 `one`·`other` 를 구분하고, 폴란드어는 `few` 를 추가로 구분하며, 한국어는 `other` 만 쓴다. 코드에서 `count == 1` 로 분기하면 영어 규칙만 적용되어 다른 언어의 복수형을 표현할 수 없다. `plurals` 리소스로 선언하면 언어마다 필요한 형태를 번역 파일에서 지정한다.

## 위반

개수 변수를 `1`·`0` 과 비교해 서로 다른 문자열 리소스나 문구를 선택한다.

```kotlin
Text(if (count == 1) stringResource(R.string.song_one) else stringResource(R.string.songs, count))

val label = when (count) {
    1 -> "1 item"
    else -> "$count items"
}
```

## 수정

```kotlin
// <plurals name="songs_found">
//     <item quantity="one">%d song found.</item>
//     <item quantity="other">%d songs found.</item>
// </plurals>
Text(pluralStringResource(R.plurals.songs_found, count, count))

val label = resources.getQuantityString(R.plurals.items, count, count)
```

`pluralStringResource()`·`getQuantityString()` 의 첫 번째 `count` 는 복수형을 선택하고, 두 번째 `count` 는 `%d` 에 들어간다.

## 허용

- `count == 0` 일 때 "항목 없음" 처럼 개수가 문구에 표시되지 않는 다른 상태를 보여 주는 경우. 공식 문서는 문법상 복수형이 아닌 분기에 `plurals` 를 쓰지 말라고 한다.
- 앱이 지원하는 모든 언어가 복수형을 구분하지 않는 경우(`res/values-*` 에 해당 언어만 있음). 판정할 수 없으면 판정 불가로 적는다.
