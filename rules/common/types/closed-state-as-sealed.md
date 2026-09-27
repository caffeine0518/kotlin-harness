---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/sealed-classes.html#state-management-in-ui-applications
---

# 정해진 개수의 상태는 `String`·`Int` 상수 대신 sealed 클래스나 enum 으로 표현한다

## 이유

공식 문서는 하위 타입의 집합이 컴파일 시점에 정해져 있고 상태 관리처럼 타입 안전성이 중요한 경우에 sealed 클래스를 쓰라고 하고, UI 상태를 예로 든다. 상태를 `String`·`Int` 로 표현하면 정의하지 않은 값도 대입할 수 있고, `when` 에서 상태를 누락해도 컴파일러가 검출하지 못한다.

## 위반

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

## 허용

- 서버 응답·DB 컬럼처럼 외부 형식이 `String`·`Int` 인 값을 받는 경우. 경계에서 sealed 클래스나 enum 으로 변환하는 코드가 있으면 위반이 아니다.
- Android 프레임워크 API 가 `Int` 상수를 요구하는 경우(예: `View.VISIBLE`, `@IntDef` 로 정의한 값)
