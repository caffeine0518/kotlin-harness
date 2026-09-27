---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/side-effects#incorrect-usage
---

# 입력 상태가 바뀔 때마다 결과도 바뀌는 계산에는 `derivedStateOf` 를 쓰지 않는다

## 이유

`derivedStateOf` 는 입력 상태가 결과보다 자주 바뀔 때, 결과가 실제로 바뀐 경우에만 리컴포지션하도록 하는 API 다. 스크롤 위치가 바뀔 때마다가 아니라 임계값을 넘을 때만 버튼 표시 여부가 바뀌는 경우가 대표적이다. 입력이 바뀔 때마다 결과도 바뀌는 계산(문자열 조합, 단순 산술)에 쓰면 리컴포지션 횟수는 줄지 않고 파생 상태 객체의 오버헤드만 추가된다. 공식 문서는 이름과 성을 합치는 예제를 잘못된 사용법으로 제시한다.

## 위반

```kotlin
var firstName by remember { mutableStateOf("") }
var lastName by remember { mutableStateOf("") }

val fullName by remember { derivedStateOf { "$firstName $lastName" } }
val total by remember { derivedStateOf { price * quantity } }
```

## 수정

```kotlin
val fullName = "$firstName $lastName"
val total = price * quantity
```

## 허용

- 결과가 입력보다 드물게 바뀌는 계산. 비교·임계값 판정(`listState.firstVisibleItemIndex > 0`), `isNotEmpty()`, 조건에 맞는 요소가 있는지 확인하는 `any { }` 등
- 계산 비용이 커서 `remember(key) { derivedStateOf { } }` 로 입력 `State` 의 변경만 추적하려는 경우 (예: `State` 로 보관한 목록의 정렬). 계산 비용 문제는 `android/ui/compose/remember-expensive-calculation` 이 판정한다.
