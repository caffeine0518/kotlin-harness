---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/recommendations#layered-architecture
---

# UI 레이어는 데이터 소스에 직접 접근하지 않고 리포지토리를 통해 접근한다

## 이유

데이터 레이어의 진입점은 리포지토리다. 다른 레이어는 데이터 소스에 직접 접근하지 않고, 데이터 소스가 하나뿐이어도 리포지토리를 만든다.

UI 레이어가 데이터 소스를 직접 호출하면 캐시·동기화·오류 처리 같은 데이터 로직이 화면마다 중복된다. 데이터 소스를 교체할 때도 UI 코드까지 수정해야 한다.

## 위반

UI 레이어 코드가 데이터 소스를 생성자 파라미터·프로퍼티로 보유하거나, 직접 생성·조회한다.

- UI 레이어 코드: ViewModel, Activity·Fragment, `@Composable` 함수
- 데이터 소스: 앱이 쓰는 데이터를 제공하는 API. 예: Room DAO·`RoomDatabase`, Retrofit 서비스 인터페이스, `SharedPreferences`, `DataStore`, Firebase 클라이언트, `FusedLocationProviderClient`·`LocationManager`, `BluetoothAdapter`, `ConnectivityManager`
- 직접 생성·조회의 예: `getSharedPreferences(...)`, `context.dataStore`, `Room.databaseBuilder(...)`, `retrofit.create(...)`

```kotlin
class ProfileViewModel(
    private val userDao: UserDao,
    private val api: UserApi,  // Retrofit 서비스
) : ViewModel() {
    val user = userDao.observeUser()
    fun refresh() = viewModelScope.launch { userDao.insert(api.fetchUser()) }
}

@Composable
fun SettingsScreen() {
    val prefs = LocalContext.current.getSharedPreferences("settings", Context.MODE_PRIVATE)
    val darkMode = prefs.getBoolean("dark_mode", false)
}
```

## 수정

데이터 소스를 리포지토리 뒤로 옮기고, UI 레이어는 리포지토리(또는 도메인 레이어의 use case)만 의존한다.

```kotlin
class UserRepository(
    private val userDao: UserDao,
    private val api: UserApi,
) {
    val user: Flow<User> = userDao.observeUser().map { it.asExternalModel() }
    suspend fun refresh() = userDao.insert(api.fetchUser().asEntity())
}

class ProfileViewModel(private val userRepository: UserRepository) : ViewModel() {
    val user = userRepository.user
    fun refresh() = viewModelScope.launch { userRepository.refresh() }
}
```

## 허용

- 리포지토리·use case 를 의존하는 경우. 예: 이름이 `Repository`·`UseCase` 로 끝나는 타입과 그 구현 타입
- `SavedStateHandle`, 리소스 조회(`getString` 등), `Intent`·`Bundle` 인자 조회. 앱이 쓰는 데이터를 제공하는 데이터 소스가 아니다.
- `@Preview` 함수, 테스트 코드
- DI 모듈(`@Module`)과 `Application` 클래스에서 데이터 소스를 생성해 리포지토리에 주입하는 코드
