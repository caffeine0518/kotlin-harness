---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/topic/libraries/architecture/viewmodel#best-practices
---

# ViewModel 은 `Context`·`Activity`·`Fragment`·`View`·`Resources`·`Lifecycle` 참조를 보관하지 않는다

## 이유

ViewModel 은 자신을 생성한 `ViewModelStoreOwner`(Activity·Fragment·내비게이션 대상)보다 오래 유지될 수 있다. 화면 회전처럼 구성이 변경되면 Activity 는 다시 생성되지만 ViewModel 은 그대로 남는다. ViewModel 이 `Activity`·`Context`·`Resources` 같은 생명주기 관련 API 의 참조를 보관하면 메모리 누수가 된다. 이미 파괴된 Activity 와 그 View 계층 전체가 ViewModel 이 해제될 때까지 메모리에 남는다.

`ViewModel` 을 상속한 클래스(`AndroidViewModel` 포함)에 적용한다. 클래스 이름이 `*ViewModel` 이 아니어도 상속 관계로 판정한다.

## 위반

아래 타입을 생성자 파라미터(`val`·`var`)·프로퍼티·`lateinit var` 로 보관하거나, 함수 파라미터로 받아 프로퍼티에 저장하는 경우

- `Context`, `Activity`·`AppCompatActivity`·`ComponentActivity` 등 Activity 하위 타입, `Fragment`
- `View` 와 그 하위 타입(`TextView`·`RecyclerView` 등), 뷰 바인딩 객체
- `Resources`
- `Lifecycle`, `LifecycleOwner`

```kotlin
class ProfileViewModel(
    private val context: Context,
) : ViewModel() {
    private var activity: Activity? = null
    private lateinit var nameView: TextView

    fun bind(activity: Activity) {
        this.activity = activity
    }

    fun title() = context.getString(R.string.profile_title)
}
```

## 수정

문자열·리소스가 필요하면 리소스 ID 를 UI 상태에 포함해 UI 에서 해석한다. `Context` 가 필요한 작업(파일·시스템 서비스 접근 등)은 데이터 레이어의 클래스로 옮기고, ViewModel 은 그 클래스를 주입받는다.

```kotlin
data class ProfileUiState(@StringRes val titleRes: Int = R.string.profile_title)

class ProfileViewModel(
    private val profileRepository: ProfileRepository,  // Context 는 Repository 가 보관한다
) : ViewModel() {
    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()
}
```

## 허용

- `Application` 이나 `@ApplicationContext` 를 지정한 `Context` 를 보관하는 경우. 앱 수명 동안 유지되므로 누수는 아니다. `android/ui/viewmodel/android-view-model` 로 보고한다.
- 프로퍼티에 저장하지 않고 함수 안에서만 사용하는 파라미터
- `ViewModel` 을 상속하지 않은 클래스
