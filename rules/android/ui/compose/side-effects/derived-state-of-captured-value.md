---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/side-effects
---

# 키 없는 `remember { derivedStateOf { } }` 에서 `State` 가 아닌 파라미터·값을 읽지 않는다

## 이유

`derivedStateOf` 는 계산 블록에서 읽은 Compose `State` 객체가 바뀔 때만 다시 계산한다. 일반 파라미터나 data class 같은 `State` 가 아닌 값은 변경을 감지하지 못한다. 키 없는 `remember { }` 로 감싸면 `derivedStateOf` 객체가 처음 컴포지션에서 한 번만 생성되고, 계산 블록은 그때 캡처한 파라미터 값을 계속 사용한다. 호출하는 쪽이 다른 값을 전달해도 결과가 갱신되지 않는다.

`derivedStateOf` 는 하나 이상의 `State` 객체를 다른 `State` 로 변환하는 API 다. `State` 가 아닌 값을 읽지 말라는 명시적인 규칙은 없고, 이 룰은 그 동작 방식과 `remember` 의 키 동작에서 도출했다.

## 위반

키 없는 `remember { derivedStateOf { } }` 의 계산 블록에서 컴포저블 파라미터, 또는 `State` 가 아닌 로컬 값을 읽는다.

```kotlin
@Composable
fun MembershipBanner(state: ScreenState) {
    val visible by remember { derivedStateOf { state.target == Target.MEMBERSHIP } }  // state 변경을 감지하지 못한다
    /* ... */
}

@Composable
fun TaskList(tasks: SnapshotStateList<Task>, keyword: String) {
    val filtered by remember { derivedStateOf { tasks.filter { keyword in it.title } } }  // keyword 가 바뀌어도 갱신되지 않는다
}
```

## 수정

`State` 를 읽지 않는 계산은 `derivedStateOf` 없이 `remember(key)` 로 계산한다. `State` 와 일반 값을 함께 읽으면 일반 값을 `remember` 의 키로 지정한다.

```kotlin
@Composable
fun MembershipBanner(state: ScreenState) {
    val visible = remember(state.target) { state.target == Target.MEMBERSHIP }
}

@Composable
fun TaskList(tasks: SnapshotStateList<Task>, keyword: String) {
    val filtered by remember(keyword) { derivedStateOf { tasks.filter { keyword in it.title } } }
}
```

## 허용

- 계산 블록에서 읽는 값이 모두 `State` 객체이거나, `remember` 로 만든 상태 객체(`rememberLazyListState()` 등)의 프로퍼티인 경우
- `rememberUpdatedState` 가 반환한 `State` 를 읽는 경우
- 읽는 값을 모두 `remember` 의 키로 지정한 경우
- `derivedStateOf` 가 불필요한 계산은 `android/ui/compose/side-effects/unnecessary-derived-state-of` 가 보고한다.
