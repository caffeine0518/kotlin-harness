---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/state-hoisting#screen-ui-state
---

# ViewModel 인스턴스를 하위 컴포저블에 전달하지 않는다

## 이유

공식 문서는 ViewModel 인스턴스를 다른 컴포저블에 전달하지 말라고 한다. ViewModel 은 화면 수준 컴포저블이나 Navigation 의 destination 에서만 사용하고, 재사용하는 UI 에서는 사용하지 않는다. ViewModel 을 받은 하위 컴포저블은 그 ViewModel 이 없으면 미리보기·테스트·재사용을 할 수 없고, ViewModel 의 모든 상태와 함수에 의존하게 된다.

## 위반

```kotlin
@Composable
fun HomeScreen(viewModel: HomeViewModel = hiltViewModel()) {
    Column {
        HomeHeader(viewModel)
        HomeFeed(viewModel = viewModel)
    }
}

@Composable
fun HomeHeader(viewModel: HomeViewModel) {
    val user by viewModel.user.collectAsStateWithLifecycle()
    Text(user.name, Modifier.clickable { viewModel.onProfileClick() })
}
```

## 수정

화면 수준 컴포저블에서 상태를 수집하고, 하위 컴포저블에는 필요한 상태와 이벤트 람다만 전달한다.

```kotlin
@Composable
fun HomeScreen(viewModel: HomeViewModel = hiltViewModel()) {
    val user by viewModel.user.collectAsStateWithLifecycle()
    Column {
        HomeHeader(user = user, onProfileClick = viewModel::onProfileClick)
    }
}

@Composable
fun HomeHeader(user: User, onProfileClick: () -> Unit) {
    Text(user.name, Modifier.clickable(onClick = onProfileClick))
}
```

## 허용

- 화면 수준 컴포저블이 ViewModel 을 파라미터로 받는 경우. `viewModel()`·`hiltViewModel()` 을 기본값으로 지정했거나, `NavHost` 의 destination·`setContent` 에서 호출하는 컴포저블
