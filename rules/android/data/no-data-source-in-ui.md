---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/recommendations#layered-architecture
---

# UI 레이어는 데이터 소스에 직접 접근하지 않고 리포지토리를 통해 접근한다

## 이유

공식 아키텍처 권장 사항은 리포지토리로 앱 데이터를 노출하고, 컴포저블·ViewModel 같은 UI 레이어 컴포넌트가 데이터 소스와 직접 상호작용하지 않게 하라고 한다(Strongly recommended). 데이터 레이어 가이드도 다른 레이어는 데이터 소스에 직접 접근하지 않으며, 데이터 레이어의 진입점은 항상 리포지토리 클래스라고 한다. 리포지토리가 한 개의 데이터 소스만 포함해도 리포지토리를 만든다.

UI 레이어가 데이터 소스를 직접 호출하면 캐시·동기화·오류 처리 같은 데이터 로직이 화면마다 중복되고, 데이터 소스를 교체할 때 UI 코드까지 수정해야 한다.

공식 문서가 예로 드는 데이터 소스는 데이터베이스, DataStore, SharedPreferences, Firebase API, GPS 위치 제공자, 블루투스, 네트워크 연결 상태 제공자다. 네트워크 API(Retrofit 서비스 등)도 데이터 소스다.

## 위반

아래 UI 레이어 코드에서 데이터 소스 타입을 생성자 파라미터·프로퍼티로 보유하거나, 데이터 소스를 직접 생성·조회한다.

- UI 레이어 코드: `ViewModel`·`AndroidViewModel` 을 상속한 클래스, `Activity`·`Fragment` 를 상속한 클래스, `@Composable` 함수
- 데이터 소스 타입: Room `@Dao`·`RoomDatabase` 하위 타입, `retrofit2` 의 `Retrofit.create` 로 만드는 서비스 인터페이스, `SharedPreferences`, `DataStore<*>`, `FirebaseFirestore`·`FirebaseDatabase` 등 Firebase 클라이언트, `FusedLocationProviderClient`·`LocationManager`, `BluetoothAdapter`, `ConnectivityManager`
- 직접 생성·조회: `getSharedPreferences(...)`, `context.dataStore`, `Room.databaseBuilder(...)`, `retrofit.create(...)`

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

- 리포지토리·use case 를 의존하는 경우. 타입 이름이 `Repository`·`UseCase` 로 끝나거나, 그 인터페이스를 구현한 타입이면 위반이 아니다.
- `SavedStateHandle`, 리소스 조회(`getString` 등), `Intent`·`Bundle` 인자 조회. 앱 데이터를 제공하는 데이터 소스가 아니다.
- `@Preview` 함수, 테스트 코드
- DI 모듈(`@Module`)과 `Application` 클래스에서 데이터 소스를 생성해 리포지토리에 주입하는 코드
