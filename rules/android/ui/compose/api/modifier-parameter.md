---
severity: warning
applies_to: "**/*.kt"
source: https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/docs/compose-api-guidelines.md#elements-accept-and-respect-a-modifier-parameter
---

# UI 를 그리는 컴포저블은 기본값이 `Modifier` 인 `modifier` 파라미터를 첫 번째 선택 파라미터로 받는다

## 이유

`modifier` 를 받지 않으면 호출하는 쪽이 크기·여백·배치·클릭 처리를 지정할 수 없어, 컴포저블을 감싸는 `Box` 를 추가하게 된다.

기본값에 `Modifier.padding(8.dp)` 같은 값을 넣으면, 호출하는 쪽이 `modifier` 를 전달할 때 그 값이 사라진다.

## 위반

`public`·`internal`(기본 가시성 포함) 이고 `Unit` 을 반환하는 `@Composable` 함수가 레이아웃·다른 UI 컴포저블을 호출하는데, 아래 중 하나에 해당한다.

- `Modifier` 타입 파라미터가 없다.
- 파라미터 이름이 `modifier` 가 아니다.
- 기본값이 없거나 `Modifier` 가 아니다.
- 필수 파라미터 앞에 있거나, 다른 선택 파라미터 뒤에 있다.

```kotlin
@Composable
fun UserBadge(name: String) {
    Text(name)
}

@Composable
fun Badge(text: String, modifier: Modifier = Modifier.padding(8.dp)) { /* ... */ }

@Composable
fun Tag(label: String, color: Color = Color.Gray, modifier: Modifier = Modifier) { /* ... */ }
```

## 수정

기본 여백 같은 값은 기본값이 아니라 컴포저블 안에서 받은 `modifier` 뒤에 연결한다.

```kotlin
@Composable
fun UserBadge(name: String, modifier: Modifier = Modifier) {
    Text(name, modifier = modifier)
}

@Composable
fun Badge(text: String, modifier: Modifier = Modifier) {
    Text(text, modifier = modifier.padding(8.dp))
}

@Composable
fun Tag(label: String, modifier: Modifier = Modifier, color: Color = Color.Gray) { /* ... */ }
```

## 허용

- `private` 컴포저블, `@Preview` 함수
- UI 를 그리지 않는 컴포저블. 예: `LaunchedEffect` 만 호출하는 함수, 값을 반환하는 함수
- 호출하는 쪽이 하나이고 배치를 지정할 필요가 없는 화면 단위 컴포저블. 예: `NavHost` 의 `composable { }` 에서만 호출하는 컴포저블. 판단할 수 없으면 판정 불가로 적는다.
