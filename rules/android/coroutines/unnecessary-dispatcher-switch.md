---
severity: info
applies_to: "**/*.kt"
source: https://developer.android.com/kotlin/coroutines/coroutines-best-practices#main-safe
---

# main-safe suspend 함수만 호출하는 코드는 다른 디스패처로 전환하지 않는다

## 이유

Android 공식 문서는 suspend 함수가 메인 스레드에서 호출해도 안전해야 하고, 블로킹 작업을 하는 클래스가 `withContext` 로 실행을 메인 스레드 밖으로 옮길 책임을 진다고 한다. 이 책임은 아키텍처의 어느 레이어에 있는 클래스든 같다. 공식 예제의 use case 는 main-safe 한 Repository 를 호출하므로 스레드를 옮기지 않는다. 호출하는 쪽에서 IO 나 Default 디스패처로 다시 전환해도 얻는 것이 없고, 생성자·DI 모듈·테스트에 디스패처 파라미터만 추가된다.

호출 대상이 main-safe 하지 않을 경우에 대비해 호출하는 쪽에서 Default 로 전환하는 것도 같다. 고칠 곳은 `withContext` 를 빠뜨린 호출 대상이며, `android/coroutines/main-safe-suspend-function` 이 그쪽을 보고한다. 호출하는 쪽에서 전환해 두면 ANR 이 발생하지 않아 그 위반이 드러나지 않고, 같은 함수를 호출하는 다른 코드는 여전히 메인 스레드에서 블로킹된다. Default 는 CPU 코어 수만큼의 스레드만 쓰므로, 그 위에서 블로킹 호출이 실행되면 CPU 작업까지 대기한다. 또 블록 안의 상태 갱신이 메인 스레드 밖에서 실행된다. `LiveData.setValue` 는 백그라운드 스레드에서 호출하면 `IllegalStateException` 이 발생한다.

## 위반

IO·Default 디스패처를 지정한 `launch`·`async`·`withContext` 블록 안에 main-safe suspend 함수 호출과 가벼운 작업(상태 갱신·매핑·리스트 생성)만 있다. 디스패처는 주입받은 파라미터(`ioDispatcher`·`defaultDispatcher` 등)와 `Dispatchers.IO`·`Dispatchers.Default` 를 모두 판정한다. `Dispatchers.*` 를 직접 지정했다면 `android/coroutines/inject-dispatchers` 도 보고하며, 이 룰의 수정으로 두 위반이 함께 해소된다.

호출 대상은 구현을 프로젝트에서 찾을 수 있고 다음 중 하나에 해당할 때만 main-safe 로 판정한다.

- 본문이 `withContext(디스패처)` 로 감싸져 있다
- Retrofit 인터페이스의 suspend 함수, Room DAO 의 suspend 함수
- 위 두 가지에 해당하는 함수만 호출하고 블로킹 호출이 없는 suspend 함수

```kotlin
class ProfileViewModel(
    private val ioDispatcher: CoroutineDispatcher,
    private val profileRepository: ProfileRepository,  // fetch·save 는 withContext 로 main-safe
) : ViewModel() {
    fun load() {
        viewModelScope.launch(ioDispatcher) {
            val profile = profileRepository.fetch()
            _uiState.update { it.copy(profile = profile) }
        }
    }

    fun save(profile: Profile) {
        viewModelScope.launch(ioDispatcher) { profileRepository.save(profile) }
    }
}

// Repository 가 main-safe 하지 않을 경우에 대비해 방어적으로 Default 로 전환한다
class SettingsViewModel(
    private val defaultDispatcher: CoroutineDispatcher,
    private val settingsRepository: SettingsRepository,  // 구현이 withContext(ioDispatcher) 로 main-safe
) : ViewModel() {
    fun load() {
        viewModelScope.launch(defaultDispatcher) {
            val settings = settingsRepository.read()
            _uiState.update { it.copy(settings = settings) }
        }
    }
}
```

## 수정

디스패처 전환을 삭제한다. 디스패처 파라미터를 더 이상 쓰지 않으면 파라미터도 삭제하고, 생성자를 호출하는 DI 모듈과 테스트를 함께 수정한다.

```kotlin
class ProfileViewModel(
    private val profileRepository: ProfileRepository,
) : ViewModel() {
    fun load() {
        viewModelScope.launch {
            val profile = profileRepository.fetch()
            _uiState.update { it.copy(profile = profile) }
        }
    }

    fun save(profile: Profile) {
        viewModelScope.launch { profileRepository.save(profile) }
    }
}
```

블록 안에 정렬·파싱처럼 CPU 를 많이 쓰는 작업이 있으면, 블록 전체가 아니라 그 계산만 `Dispatchers.Default` 에 해당하는 주입 디스패처의 `withContext` 로 감싼다.

```kotlin
fun load() {
    viewModelScope.launch {
        val articles = articleRepository.fetch()
        val sorted = withContext(defaultDispatcher) { articles.sortedWith(relevanceComparator) }
        _uiState.update { it.copy(articles = sorted) }
    }
}
```

## 허용

- 블록 안에 블로킹 호출이 있는 경우. 블로킹 API 의 목록은 `android/coroutines/main-safe-suspend-function` 과 같다.
- 호출 대상의 구현을 프로젝트에서 찾을 수 없는 경우(라이브러리 함수 등). main-safe 인지 판정할 수 없으므로 위반이 아니라 판정 불가로 보고한다.
- 블록 안에 정렬·필터링·파싱처럼 CPU 를 많이 쓰는 작업이 있고 Default 디스패처로 전환한 경우. 블록 안에 main-safe 호출과 가벼운 작업만 있다면 Default 로 전환했더라도 위반이다.
- `flowOn`. Flow 의 업스트림에서 블로킹·CPU 집약 작업을 하는지는 이 룰이 판정하지 않는다.
- 테스트 코드
