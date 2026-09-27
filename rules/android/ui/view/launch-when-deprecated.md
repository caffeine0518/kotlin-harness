---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/libraries/architecture/views/coroutines-views#suspend-lifecycle-aware
---

# `launchWhenCreated`·`launchWhenStarted`·`launchWhenResumed` 와 `whenCreated`·`whenStarted`·`whenResumed` 대신 `repeatOnLifecycle` 을 쓴다

## 이유

`LifecycleCoroutineScope` 의 `launchWhenX` 와 `Lifecycle` 의 `whenX` 는 deprecated 다. API 레퍼런스는 리소스를 낭비할 수 있다는 이유를 든다. 두 API 는 `Lifecycle` 이 지정한 상태보다 낮아지면(예: `STOPPED`) 코루틴을 취소하지 않고 일시 중단하므로, 안에서 수집하는 Flow 의 업스트림은 백그라운드에서도 활성 상태로 남아 계속 값을 방출할 수 있다. `repeatOnLifecycle` 은 지정한 상태보다 낮아지면 블록을 취소하고, 다시 그 상태가 되면 블록을 새로 실행한다.

## 위반

```kotlin
lifecycleScope.launchWhenStarted {
    viewModel.uiState.collect { render(it) }
}

viewLifecycleOwner.lifecycleScope.launchWhenResumed {
    showDialog()
}

// Lifecycle 익스텐션 함수 형태도 위반이다
lifecycle.whenStarted { loadData() }
```

## 수정

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { render(it) }
    }
}
```

한 번만 실행하면 되는 일시 중단 없는 작업은 `withStarted { }` 를 쓴다.

```kotlin
lifecycleScope.launch {
    lifecycle.withStarted { showDialog() }
}
```

## 허용

- 이 룰이 보고한 코드는 `android/ui/view/collect-with-lifecycle` 로 중복 보고하지 않는다.
