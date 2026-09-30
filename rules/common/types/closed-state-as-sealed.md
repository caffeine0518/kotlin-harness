---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/sealed-classes.html#state-management-in-ui-applications
---

# 정해진 개수의 상태는 `String`·`Int` 상수나 Boolean·널러블 필드의 조합 대신 sealed 클래스나 enum 으로 표현한다

## 이유

공식 문서는 하위 타입의 집합이 컴파일 시점에 정해져 있고 상태 관리처럼 타입 안전성이 중요한 경우에 sealed 클래스를 쓰라고 하고, UI 상태를 예로 든다. 상태를 `String`·`Int` 로 표현하면 정의하지 않은 값도 대입할 수 있고, `when` 에서 상태를 누락해도 컴파일러가 검출하지 못한다.

Boolean·널러블 필드 여러 개의 조합으로 상태를 표현해도 같다. 필드마다 따로 갱신하므로 의미 없는 조합(값이 있는데 로드가 끝나지 않은 상태 등)이 생길 수 있고, 조합에서 상태를 판별하는 `when` 은 분기 순서에 따라 결과가 달라진다.

## 위반

`String`·`Int` 상수로 상태를 표현한다.

```kotlin
const val STATE_LOADING = 0
const val STATE_SUCCESS = 1
const val STATE_ERROR = 2

class ScreenModel {
    var state: Int = STATE_LOADING
    var data: String? = null      // STATE_SUCCESS 일 때만 의미가 있다
}

fun render(model: ScreenModel) {
    when (model.state) {
        STATE_LOADING -> showLoading()
        STATE_SUCCESS -> showData(model.data)
    }
}
```

상태를 판별하는 조건이 같은 객체의 Boolean·널러블 필드 두 개 이상이고, 그 결과로 서로 배타적인 상태(sealed 하위 타입·enum 상수)를 반환하거나 분기한다.

```kotlin
data class ConfigState(
    val remoteConfig: RemoteConfig? = null,
    val cachedConfig: CachedConfig? = null,
    val isCacheRead: Boolean = false,
    val hasRemoteLoadEnded: Boolean = false,
)

fun ConfigState.toLoadStatus(): ConfigLoadStatus = when {
    remoteConfig != null -> ConfigLoadStatus.Loaded(remoteConfig)
    !isCacheRead -> ConfigLoadStatus.Initial
    hasRemoteLoadEnded -> ConfigLoadStatus.Failed(cachedConfig)
    else -> ConfigLoadStatus.Pending(cachedConfig)
}
```

## 수정

상태마다 필요한 데이터가 다르면 sealed 클래스로, 데이터 없이 상수만 필요하면 enum 으로 선언한다.

```kotlin
sealed interface ScreenState {
    data object Loading : ScreenState
    data class Success(val data: String) : ScreenState
    data class Error(val cause: Throwable) : ScreenState
}

fun render(state: ScreenState) = when (state) {
    ScreenState.Loading -> showLoading()
    is ScreenState.Success -> showData(state.data)
    is ScreenState.Error -> showError(state.cause)
}
```

필드 조합으로 표현한 상태는 원본을 sealed 클래스로 선언한다. 값이 여러 소스에서 오면 소스마다 sealed 클래스로 표현하고 `combine` 으로 합친다. 아직 값을 받지 않은 상태는 `stateIn` 의 초기값으로 표현한다.

```kotlin
sealed interface RemoteLoad {
    data object Loading : RemoteLoad
    data class Success(val config: RemoteConfig) : RemoteLoad
    data object Failure : RemoteLoad
}

val loadStatus: StateFlow<ConfigLoadStatus> = combine(cachedConfig, remoteLoad) { cached, remote ->
    when (remote) {
        is RemoteLoad.Success -> ConfigLoadStatus.Loaded(remote.config)
        RemoteLoad.Failure -> ConfigLoadStatus.Failed(cached)
        RemoteLoad.Loading -> ConfigLoadStatus.Pending(cached)
    }
}.stateIn(scope, SharingStarted.WhileSubscribed(5_000), ConfigLoadStatus.Initial)
```

## 허용

- 서버 응답·DB 컬럼처럼 외부 형식이 `String`·`Int` 인 값을 받는 경우. 경계에서 sealed 클래스나 enum 으로 변환하는 코드가 있으면 위반이 아니다.
- Android 프레임워크 API 가 `Int` 상수를 요구하는 경우(예: `View.VISIBLE`, `@IntDef` 로 정의한 값)
- 서로 독립적인 Boolean·널러블 필드. 모든 조합이 유효하고(`isSignedIn`·`isPremium` 등), 조합에서 배타적인 상태를 판별하는 코드가 없으면 위반이 아니다.
- 필드 하나만 조건으로 쓰는 분기(`if (isLoading) ... else ...`)
