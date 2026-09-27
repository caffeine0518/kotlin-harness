---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/recommendations#lifecycle
---

# 생명주기에 맞춰 실행하는 UI 작업은 `Activity` 콜백 오버라이드나 `LaunchedEffect` 대신 Lifecycle 이펙트로 실행한다

## 이유

공식 아키텍처 권장 사항은 UI 관련 작업을 실행하려고 `onResume` 등 `Activity` 의 생명주기 메서드를 오버라이드하지 말고, 컴포저블에서 `LifecycleStartEffect`·`LifecycleResumeEffect` 등 Lifecycle 이펙트를 쓰라고 강력히 권장한다. 작업이 그 작업을 사용하는 컴포저블과 함께 선언되어, 컴포저블이 컴포지션에서 제외될 때 정리 블록도 실행된다.

`LaunchedEffect` 는 컴포지션에 연결되어 있어, `HorizontalPager` 가 미리 컴포지션한 옆 페이지처럼 사용자에게 보이지 않을 때도 실행된다. 공식 문서는 화면 조회 기록처럼 사용자가 실제로 화면을 보는지에 따라 달라지는 작업은 `LaunchedEffect` 대신 `LifecycleEventEffect` 를 쓰라고 한다.

## 위반

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { CameraScreen(cameraController) }
    }

    override fun onResume() {
        super.onResume()
        cameraController.startPreview()
    }

    override fun onPause() {
        super.onPause()
        cameraController.stopPreview()
    }
}

@Composable
fun ProductScreen(productId: String) {
    LaunchedEffect(productId) {
        analytics.logScreenView("product", productId)
    }
}
```

## 수정

시작·중지가 짝을 이루는 작업은 `LifecycleStartEffect`(`onStopOrDispose`), 재개·일시 중지가 짝을 이루는 작업은 `LifecycleResumeEffect`(`onPauseOrDispose`)를 쓴다. 정리할 작업이 없는 일회성 작업은 `LifecycleEventEffect` 를 쓴다.

```kotlin
@Composable
fun CameraScreen(cameraController: CameraController) {
    LifecycleResumeEffect(cameraController) {
        cameraController.startPreview()
        onPauseOrDispose { cameraController.stopPreview() }
    }
}

@Composable
fun ProductScreen(productId: String) {
    LifecycleEventEffect(Lifecycle.Event.ON_RESUME) {
        analytics.logScreenView("product", productId)
    }
}
```

## 허용

- `setContent` 를 호출하지 않는 View 기반 `Activity`
- 오버라이드한 메서드에서 `super` 호출 외에 UI 와 관계없는 작업(예: 앱 전체 상태 저장)만 실행하는 경우
- 사용자에게 보이는지와 관계없이 실행해야 하는 `LaunchedEffect` 작업 (예: 데이터 로드, 스크롤 위치 이동)
