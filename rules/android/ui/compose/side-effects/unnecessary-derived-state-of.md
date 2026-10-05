---
severity: info
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/side-effects#incorrect-usage
---

# 입력 상태가 바뀔 때마다 결과도 바뀌는 계산에는 `derivedStateOf` 를 쓰지 않는다

## 이유

`derivedStateOf` 는 입력 상태가 결과보다 자주 바뀔 때, 결과가 실제로 바뀐 경우에만 리컴포지션하도록 하는 API 다. 스크롤 위치가 바뀔 때마다가 아니라 임계값을 넘을 때만 버튼 표시 여부가 바뀌는 경우가 대표적이다.

입력이 바뀔 때마다 결과도 바뀌는 계산(단순 산술, 길이 계산)에 쓰면 리컴포지션 횟수는 줄지 않고 파생 상태 객체의 오버헤드만 추가된다.

## 위반

입력이 바뀔 때마다 결과도 바뀌는 계산을 `derivedStateOf` 로 감싼다. 예: 단순 산술, 길이 계산

```kotlin
@Composable
fun MemoField() {
    var memo by remember { mutableStateOf("") }
    val remaining by remember { derivedStateOf { MaxMemoLength - memo.length } }  // memo 가 바뀔 때마다 결과도 바뀐다

    OutlinedTextField(
        value = memo,
        onValueChange = { memo = it },
        supportingText = { Text(stringResource(R.string.memo_remaining, remaining)) },
    )
}
```

## 수정

`remember { derivedStateOf { } }` 없이 바로 계산한다. 단순 산술은 리컴포지션마다 다시 계산해도 비용이 작으므로 `remember` 도 쓰지 않는다.

```kotlin
@Composable
fun MemoField() {
    var memo by remember { mutableStateOf("") }
    val remaining = MaxMemoLength - memo.length

    OutlinedTextField(
        value = memo,
        onValueChange = { memo = it },
        supportingText = { Text(stringResource(R.string.memo_remaining, remaining)) },
    )
}
```

## 허용

- 결과가 입력보다 드물게 바뀌는 계산. 예: 비교·임계값 판정(`listState.firstVisibleItemIndex > 0`), `isNotEmpty()`, 조건에 맞는 요소가 있는지 확인하는 `any { }`
- 계산 비용이 커서 `remember(key) { derivedStateOf { } }` 로 입력 `State` 의 변경만 추적하려는 경우. 예: `State` 로 보관한 목록의 정렬. 계산 비용 문제는 `android/ui/compose/performance/remember-expensive-calculation` 이 판정한다.
