---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/recommendations#lifecycle
---

# 생명주기에 맞춰 실행하는 UI 작업은 Lifecycle 이펙트로 실행한다

## 이유

Compose 앱은 보통 `Activity` 하나 안에서 여러 화면을 전환한다. `Activity` 의 생명주기 메서드는 지금 어떤 화면이 보이는지 모르므로, 다른 화면으로 이동해도 그 화면의 작업이 계속 실행된다.

Lifecycle 이펙트는 생명주기 이벤트에 맞춰 실행되고, 작업을 그 작업을 사용하는 컴포저블과 함께 선언한다. 그래서 컴포저블을 다른 화면이나 `Activity` 로 옮겨도 생명주기 처리가 함께 옮겨진다.

컴포저블이 컴포지션에서 제외되면 정리 블록도 함께 실행된다.

## 위반

다음 중 하나에 해당한다.

- `setContent` 를 호출하는 `Activity` 가 UI 작업을 실행하려고 생명주기 메서드를 오버라이드한다. 작업이 그 작업을 사용하는 컴포저블과 떨어진 곳에 선언된다.
- 사용자가 화면을 보는지에 따라 달라지는 작업을 `LaunchedEffect` 에서 실행한다. `LaunchedEffect` 는 컴포지션에 연결되어 있어, 사용자에게 보이지 않을 때도 실행된다. 예: `HorizontalPager` 가 미리 컴포지션한 옆 페이지에서 화면 조회가 기록된다.

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

작업 종류에 맞는 Lifecycle 이펙트를 쓴다.

- 시작·중지가 짝을 이루는 작업: `LifecycleStartEffect`. 정리는 `onStopOrDispose` 에 작성한다.
- 재개·일시 중지가 짝을 이루는 작업: `LifecycleResumeEffect`. 정리는 `onPauseOrDispose` 에 작성한다.
- 정리할 작업이 없는 일회성 작업: `LifecycleEventEffect`

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
- 오버라이드한 메서드에서 `super` 호출 외에 UI 와 관계없는 작업만 실행하는 경우. 예: 앱 전체 상태 저장
- 사용자에게 보이는지와 관계없이 실행해야 하는 `LaunchedEffect` 작업. 예: 데이터 로드, 스크롤 위치 이동
