---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/recommendations#viewmodel
---

# ViewModel 은 `AndroidViewModel` 을 상속하지 않고, `Application` 을 사용하지 않는다

## 이유

ViewModel 이 `Context` 에 의존하면 ViewModel 이 데이터 레이어의 일을 맡게 되고, 단위 테스트에서 `Application` 을 준비해야 한다. `Application` 이 필요한 의존성은 UI 레이어나 데이터 레이어로 옮긴다.

## 위반

- `AndroidViewModel` 을 상속한 클래스
- `ViewModel` 을 상속한 클래스가 `Application` 이나 `@ApplicationContext` 를 지정한 `Context` 를 생성자 파라미터·프로퍼티로 보관하는 경우

```kotlin
class SettingsViewModel(application: Application) : AndroidViewModel(application) {
    fun cacheSize() = getApplication<Application>().cacheDir.length()
}

@HiltViewModel
class DownloadViewModel @Inject constructor(
    @ApplicationContext private val context: Context,
) : ViewModel() {
    fun start(url: String) {
        WorkManager.getInstance(context).enqueue(DownloadWorker.request(url))
    }
}
```

## 수정

`Context` 를 사용하는 코드를 데이터 레이어의 클래스로 옮기고, ViewModel 은 그 클래스를 주입받는다.

```kotlin
class DownloadRepository @Inject constructor(
    @ApplicationContext private val context: Context,
) {
    fun start(url: String) {
        WorkManager.getInstance(context).enqueue(DownloadWorker.request(url))
    }
}

@HiltViewModel
class DownloadViewModel @Inject constructor(
    private val downloadRepository: DownloadRepository,
) : ViewModel() {
    fun start(url: String) = downloadRepository.start(url)
}
```

## 허용

- Activity·Fragment 등 `Application` 이 아닌 `Context` 를 보관하는 경우. 누수로 이어지므로 `android/ui/viewmodel/lifecycle-reference` 로 보고한다.
- `ViewModel` 을 상속하지 않은 클래스(Repository·데이터 소스 등)가 `Application`·`@ApplicationContext` 를 보관하는 경우
