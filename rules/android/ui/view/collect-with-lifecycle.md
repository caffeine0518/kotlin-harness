---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/flow/stateflow-and-sharedflow#stateflow
---

# 액티비티·프래그먼트에서 UI 를 갱신하는 Flow 는 `repeatOnLifecycle` 또는 `flowWithLifecycle` 안에서 수집한다

## 이유

`lifecycleScope` 는 `Lifecycle` 이 `DESTROYED` 가 될 때만 코루틴을 취소한다. `lifecycleScope.launch { flow.collect { } }` 나 `flow.launchIn(lifecycleScope)` 로 수집하면 화면이 보이지 않는 동안(`STOPPED`)에도 수집을 계속해 이벤트를 처리한다. `STOPPED` 상태에서 이벤트를 처리해 UI 를 갱신하면 앱 크래시로 이어질 수 있다. `LiveData.observe()` 와 달리 `StateFlow` 를 포함한 Flow 는 `STOPPED` 에서 수집을 자동으로 중단하지 않는다.

## 위반

```kotlin
class NewsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        lifecycleScope.launch {
            viewModel.uiState.collect { render(it) }
        }
        viewModel.events.onEach { showToast(it) }.launchIn(lifecycleScope)
    }
}

// 프래그먼트에서 viewLifecycleOwner 를 써도 repeatOnLifecycle 이 없으면 위반이다
viewLifecycleOwner.lifecycleScope.launch {
    viewModel.uiState.collect { binding.title.text = it.title }
}
```

## 수정

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        launch { viewModel.uiState.collect { render(it) } }
        launch { viewModel.events.collect { showToast(it) } }
    }
}

// Flow 가 하나면 flowWithLifecycle 도 쓸 수 있다
viewLifecycleOwner.lifecycleScope.launch {
    viewModel.uiState
        .flowWithLifecycle(viewLifecycleOwner.lifecycle, Lifecycle.State.STARTED)
        .collect { binding.title.text = it.title }
}
```

## 허용

- `first()`·`firstOrNull()`·`single()` 처럼 값 하나를 받고 끝나는 터미널 연산자
- Flow 수집 없이 suspend 함수만 호출하는 `lifecycleScope.launch { }`
- `ViewModel` 의 `viewModelScope` 등 UI 가 아닌 클래스에서의 수집
- `launchWhenStarted` 등 안에서의 수집은 `android/ui/view/launch-when-deprecated` 로 보고한다.
- `onStart` 에서 시작하고 `onStop` 에서 취소하는 수집은 `android/ui/view/lifecycle-callback-collection` 으로 보고한다.
- 프래그먼트에서 `repeatOnLifecycle` 의 리시버로 `viewLifecycleOwner` 대신 `this` 를 쓰는 코드는 Android Lint(`UnsafeRepeatOnLifecycleDetector`)가 검사하므로 보고하지 않는다.
