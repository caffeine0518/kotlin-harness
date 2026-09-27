---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/side-effects#restarting-effects
---

# 이펙트 블록에서 사용하는 값은 키로 지정하거나 `rememberUpdatedState` 로 감싼다

## 이유

`LaunchedEffect`·`DisposableEffect`·`produceState` 의 블록은 키가 바뀔 때만 다시 실행된다. 키로 지정하지 않은 파라미터·로컬 값을 블록에서 사용하면, 리컴포지션으로 값이 바뀌어도 블록은 처음 실행될 때 캡처한 값을 계속 사용한다. 공식 문서는 이펙트에서 사용하는 변수를 이펙트 컴포저블의 파라미터(키)로 추가하거나 `rememberUpdatedState` 로 감싸라고 한다.

키로 `Unit`·`true` 같은 상수를 지정하면 블록이 호출 지점의 수명 동안 한 번만 실행된다. 공식 문서는 이 방식이 정말 필요한지 다시 확인하라고 한다. 상수 키 이펙트에서 바뀔 수 있는 값을 사용하는 경우도 이 룰에 해당한다.

## 위반

```kotlin
@Composable
fun LandingScreen(onTimeout: () -> Unit) {
    LaunchedEffect(Unit) {
        delay(SplashWaitTimeMillis)
        onTimeout()  // 리컴포지션 뒤에도 처음 전달받은 onTimeout 을 호출한다
    }
}

@Composable
fun SearchResult(query: String, sort: SortOrder, repository: SearchRepository) {
    val result by produceState<List<Item>>(emptyList(), query) {
        value = repository.search(query, sort)  // sort 가 바뀌어도 다시 검색하지 않는다
    }
}
```

## 수정

값이 바뀔 때 이펙트를 다시 시작해야 하면 키로 지정한다. 다시 시작하지 않고 최신 값만 사용해야 하면 `rememberUpdatedState` 로 감싸고, 이펙트에서는 반환된 `State` 를 사용한다.

```kotlin
@Composable
fun LandingScreen(onTimeout: () -> Unit) {
    val currentOnTimeout by rememberUpdatedState(onTimeout)
    LaunchedEffect(Unit) {
        delay(SplashWaitTimeMillis)
        currentOnTimeout()
    }
}

@Composable
fun SearchResult(query: String, sort: SortOrder, repository: SearchRepository) {
    val result by produceState<List<Item>>(emptyList(), query, sort, repository) {
        value = repository.search(query, sort)
    }
}
```

## 허용

아래 값은 컴포저블의 수명 동안 바뀌지 않거나, 읽을 때마다 최신 값을 반환하므로 키로 지정하지 않아도 된다.

- `rememberUpdatedState` 가 반환한 `State`, `remember { mutableStateOf(...) }` 로 만든 `State` 와 그 `by` 위임 프로퍼티. 블록 안에서 읽는 시점의 값을 반환한다.
- 키 없는 `remember { }` 로 만든 객체, `rememberCoroutineScope()`, `rememberLazyListState()` 등 `remember*` 로 만든 상태 객체
- `viewModel()`·`hiltViewModel()` 로 얻은 ViewModel 인스턴스
- `const val`, `object` 의 프로퍼티, 최상위 `val` 등 상수
- `LaunchedEffect` 블록 안에서 선언한 로컬 값, 블록 람다의 파라미터
