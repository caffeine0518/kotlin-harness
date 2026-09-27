---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/recommendations#lifecycle
---

# 생명주기 콜백을 오버라이드해 코루틴을 시작·취소하지 않고 `repeatOnLifecycle` 을 쓴다

## 이유

공식 아키텍처 권장 사항(Strongly recommended)은 `onResume` 같은 액티비티 생명주기 메서드를 오버라이드해 UI 작업을 실행하지 말고, 생명주기 이벤트에 따라 실행하는 비동기 작업에는 `repeatOnLifecycle` 을 쓰라고 한다. `onStart` 에서 `Job` 을 시작하고 `onStop` 에서 취소하는 코드는 `repeatOnLifecycle(Lifecycle.State.STARTED)` 가 제공하는 동작을 직접 구현한 것이다. 취소를 빠뜨리거나 `Job` 을 여러 번 시작하는 실수가 생기기 쉽다.

## 위반

```kotlin
class NewsActivity : AppCompatActivity() {
    private var job: Job? = null

    override fun onStart() {
        super.onStart()
        job = lifecycleScope.launch { viewModel.uiState.collect { render(it) } }
    }

    override fun onStop() {
        job?.cancel()
        super.onStop()
    }
}
```

프래그먼트의 `onStart`·`onResume`·`onPause`·`onStop` 도 같다.

## 수정

```kotlin
class NewsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { render(it) }
            }
        }
    }
}
```

## 허용

- 생명주기 콜백에서 코루틴을 시작하지 않는 동기 코드(리스너 등록·해제, 로그 등)
- 이 룰이 보고한 코드는 `android/ui/view/collect-with-lifecycle` 로 중복 보고하지 않는다.
