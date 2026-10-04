---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/privacy-and-security/risks/unsafe-use-of-deeplinks#unsafe-use-of-deep-links-implement-robust-data-validation
---

# 딥 링크 URI 의 값은 허용 목록으로 검증한 뒤 WebView 로드·화면 이동·파일 접근에 사용한다

## 이유

딥 링크는 다른 앱이나 웹 페이지가 임의의 값으로 호출할 수 있다. 딥 링크 검증이 없으면 호스트 검증 우회, 크로스 앱 스크립팅, 원격 코드 실행 같은 공격에 악용될 수 있다.

## 위반

`intent.data`, `Uri.getQueryParameter()`·`pathSegments`·`host`·`lastPathSegment`, Navigation 의 딥 링크 인수(`navArgs()`·`SavedStateHandle` 로 받은 딥 링크 값)를 허용 목록 검증 없이 아래에 전달하는 코드가 위반이다.

- `WebView.loadUrl()`·`loadDataWithBaseURL()` 의 URL
- `File`·`openFileInput()`·`ContentResolver.openInputStream()` 등 파일 경로·URI
- `startActivity()`·`Intent.parseUri()`·`NavController.navigate()` 의 이동 대상
- 결제·보상 지급·계정 변경처럼 권한이나 선행 조건이 필요한 동작의 인수

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    val uri = intent.data ?: return
    webView.loadUrl(uri.getQueryParameter("url") ?: return)

    val fileName = uri.lastPathSegment ?: return
    val content = File(filesDir, fileName).readText()

    val levelId = uri.getQueryParameter("level_id") ?: return
    rewardRepository.grant(levelId)
}
```

## 수정

```kotlin
private val allowedHosts = setOf("example.com", "www.example.com")

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    val uri = intent.data ?: return

    val url = uri.getQueryParameter("url")?.toUri()
    if (url != null && url.scheme == "https" && url.host in allowedHosts) {
        webView.loadUrl(url.toString())
    }

    val fileName = uri.lastPathSegment?.takeIf { it in setOf("terms.txt", "privacy.txt") } ?: return
    val content = File(filesDir, fileName).readText()

    val levelId = uri.getQueryParameter("level_id") ?: return
    if (levelRepository.hasCompleted(levelId)) {
        rewardRepository.grant(levelId)
    } else {
        navigateToMain()
    }
}
```

허용 목록과 선행 조건은 앱의 요구 사항에 따라 달라서 코드만으로 정할 수 없으므로 자동으로 수정하지 않는다.

## 허용

- 값을 `toIntOrNull()`·`enum` 조회 등으로 기대한 형식으로 변환하고, 변환에 실패하면 사용하지 않는 경우 (ID 를 화면 조회 키로만 쓰는 경우 등)
- 값을 화면에 텍스트로 표시하거나 검색어로만 사용하는 경우
- 딥 링크가 아닌 자기 앱 내부에서 만든 인텐트의 값
- 인텐트 extra 에 포함된 `Intent` 를 그대로 실행하는 경우 — Android Lint `UnsafeIntentLaunch` 가 검사한다
- `setJavaScriptEnabled`·`addJavascriptInterface` 사용 자체 — Android Lint 가 검사한다
