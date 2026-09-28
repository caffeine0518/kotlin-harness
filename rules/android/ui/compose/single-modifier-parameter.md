---
severity: warning
applies_to: "**/*.kt"
source: https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/docs/compose-api-guidelines.md#elements-accept-and-respect-a-modifier-parameter
---

# 컴포저블은 `Modifier` 타입 파라미터를 하나만 받는다

## 이유

Compose API 가이드라인은 UI 를 그리는 컴포저블이 `Modifier` 파라미터를 여러 개 받으면 안 된다고 한다(MUST NOT). `modifier` 는 컴포저블 자체의 외부 동작을 지정하는 값이고, 하위 요소를 지정하는 값이 아니다. 컴포넌트 가이드라인은 `contentModifier`·`iconModifier` 처럼 하위 요소마다 모디파이어를 받지 말고, 그 요소를 `@Composable` 람다 슬롯으로 받으라고 한다. 하위 요소마다 모디파이어를 받으면 호출하는 쪽이 컴포저블의 내부 구조를 알아야 하고, 내부 구조를 바꿀 때 파라미터도 바꿔야 한다.

## 위반

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

하위 요소를 슬롯으로 받는다.

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
