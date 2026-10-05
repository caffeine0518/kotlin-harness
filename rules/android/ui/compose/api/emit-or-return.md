줘---
severity: warning
applies_to: "**/*.kt"
source: https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/docs/compose-api-guidelines.md#emit-xor-return-a-value
---

# UI 를 그리는 컴포저블은 값을 반환하지 않는다

## 이유

컴포저블이 UI 를 그리면서 입력값·선택 상태를 반환하면 다음 문제가 생긴다.

- 호출하는 쪽이 상태를 소유하지 못해, 상태를 호이스팅할 수 없다.
- 반환값은 리컴포지션할 때만 갱신된다.

## 위반

`Unit` 이 아닌 타입을 반환하는 `@Composable` 함수가 레이아웃·UI 컴포저블을 호출한다.

```kotlin
@Composable
fun SearchBar(): String {
    var query by remember { mutableStateOf("") }
    TextField(value = query, onValueChange = { query = it })
    return query
}
```

## 수정

상태를 파라미터로 받고, 변경은 콜백으로 전달한다.

```kotlin
@Composable
fun SearchBar(query: String, onQueryChange: (String) -> Unit, modifier: Modifier = Modifier) {
    TextField(value = query, onValueChange = onQueryChange, modifier = modifier)
}
```

## 허용

- UI 를 그리지 않고 값만 반환하는 컴포저블. 예: `rememberXxxState()`·`stringResource()`
