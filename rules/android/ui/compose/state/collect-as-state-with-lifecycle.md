---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/recommendations#ui-layer
---

# 컴포저블에서 UI 상태 `Flow` 는 `collectAsState()` 대신 `collectAsStateWithLifecycle()` 로 수집한다

## 이유

`collectAsState()` 는 컴포저블이 컴포지션에 있는 동안 계속 수집한다. 앱이 백그라운드로 이동해도 수집이 중단되지 않아, 업스트림 `Flow` 가 위치 업데이트·데이터베이스 조회 같은 작업을 계속 실행한다.

`collectAsStateWithLifecycle()` 은 기본적으로 생명주기가 `STARTED` 일 때 수집을 시작하고 `STOPPED` 일 때 중단한다.

## 위반

컴포저블에서 UI 상태 `Flow` 를 `collectAsState()` 로 수집한다.

```kotlin
@Composable
fun ConversationScreen(viewModel: ConversationViewModel = viewModel()) {
    val messages by viewModel.messages.collectAsState()
    val draft by viewModel.draft.collectAsState(initial = "")
}
```

## 수정

`androidx.lifecycle:lifecycle-runtime-compose` 의 `collectAsStateWithLifecycle()` 을 사용한다. 수집 기준 상태를 바꾸려면 `minActiveState` 를 지정한다.

```kotlin
@Composable
fun ConversationScreen(viewModel: ConversationViewModel = viewModel()) {
    val messages by viewModel.messages.collectAsStateWithLifecycle()
    val draft by viewModel.draft.collectAsStateWithLifecycle(initialValue = "")
}
```

## 허용

- `lifecycle-runtime-compose` 를 사용할 수 없는 모듈. 예: Android 생명주기 의존성이 없는 Compose Multiplatform 공통 코드
