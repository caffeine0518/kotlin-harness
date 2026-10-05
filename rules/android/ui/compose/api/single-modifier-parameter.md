---
severity: warning
applies_to: "**/*.kt"
source: https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/docs/compose-api-guidelines.md#elements-accept-and-respect-a-modifier-parameter
---

# 컴포저블은 `Modifier` 타입 파라미터를 하나만 받는다

## 이유

`modifier` 는 컴포저블 자체의 외부 동작을 지정하는 값이고, 하위 요소를 지정하는 값이 아니다. `contentModifier`·`iconModifier` 처럼 하위 요소마다 모디파이어를 받으면 다음 문제가 생긴다.

- 호출하는 쪽이 컴포저블의 내부 구조를 알아야 한다.
- 내부 구조를 바꿀 때 파라미터도 바꿔야 한다.

## 위반

UI 를 그리는 컴포저블이 `Modifier` 타입 파라미터를 두 개 이상 받는다.

```kotlin
@Composable
fun CheckboxRow(
    checked: Boolean,
    label: String,
    modifier: Modifier = Modifier,
    checkboxModifier: Modifier = Modifier,
    labelModifier: Modifier = Modifier,
) { /* ... */ }
```

## 수정

하위 요소는 `@Composable` 람다 슬롯으로 받는다.

```kotlin
@Composable
fun CheckboxRow(
    checked: Boolean,
    modifier: Modifier = Modifier,
    label: @Composable () -> Unit,
) {
    Row(modifier) {
        Checkbox(checked = checked, onCheckedChange = null)
        label()
    }
}
```

## 허용

- `private` 컴포저블
- `@Preview` 함수
