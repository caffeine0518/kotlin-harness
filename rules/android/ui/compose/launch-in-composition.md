---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/side-effects
---

# 컴포저블 본문에서 코루틴을 시작하지 않고 `LaunchedEffect` 나 이벤트 콜백에서 시작한다

## 이유

공식 문서에 따르면 컴포저블은 예측할 수 없는 시점에 리컴포지션되고, 순서가 바뀌거나 결과가 폐기될 수 있으므로 사이드 이펙트가 없어야 한다. 컴포저블 본문에서 `scope.launch { }` 를 호출하면 리컴포지션할 때마다 코루틴이 새로 시작되고, 폐기된 컴포지션에서도 실행된다. 컴포지션에 진입할 때 실행할 작업은 `LaunchedEffect` 로, 사용자 이벤트에 대한 작업은 `rememberCoroutineScope()` 로 얻은 스코프를 이벤트 콜백에서 호출한다.

## 위반

`@Composable` 함수 본문(람다 파라미터·이펙트 블록 밖)에서 `launch`·`async` 를 호출한다.

```kotlin
@Composable
fun ProfileScreen(userId: String, viewModel: ProfileViewModel) {
    val scope = rememberCoroutineScope()
    scope.launch { viewModel.load(userId) }  // 리컴포지션마다 다시 시작된다
    /* ... */
}
```

## 수정

```kotlin
@Composable
fun ProfileScreen(userId: String, viewModel: ProfileViewModel) {
    LaunchedEffect(userId) { viewModel.load(userId) }
    /* ... */
}

@Composable
fun SaveButton(onSave: suspend () -> Unit) {
    val scope = rememberCoroutineScope()
    Button(onClick = { scope.launch { onSave() } }) { Text("저장") }
}
```

## 허용

- `onClick` 등 이벤트 콜백 람다, `LaunchedEffect`·`DisposableEffect`·`SideEffect` 블록 안에서 호출하는 경우
- 컴포저블 안에 선언한 로컬 함수·람다 안에서 호출하고, 그 함수를 이벤트 콜백에서만 호출하는 경우
