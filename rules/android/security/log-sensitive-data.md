---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/privacy-and-security/risks/log-info-disclosure#general
---

# 토큰·비밀번호·개인정보를 `Log.*` 로 출력하지 않는다

## 이유

`Log.*` 는 logcat 에 출력하고, logcat 은 `READ_LOGS` 권한이 있는 앱이 읽을 수 있는 공유 리소스다. 사전 설치 앱이 이 권한을 가진 기기도 있어 로그에 출력한 자격 증명·개인정보가 다른 앱에 노출될 수 있다. 이 검사는 AGP 기본 Lint 에 포함되지 않는다(`LogInfoDisclosure` 는 별도 라이브러리 `com.android.security.lint` 의 검사다).

## 위반

`Log.v`·`d`·`i`·`w`·`e`·`wtf`, `println`, Timber 같은 로그 함수의 메시지·인수에 아래 값을 포함하는 코드가 위반이다.

- 액세스·리프레시 토큰, 세션 ID, 비밀번호, API 키, 인증 헤더, 인증 코드
- 이메일, 전화번호, 주소, 이름, 생년월일, 카드·계좌 번호, 위치 좌표 같은 개인정보
- 위 값을 프로퍼티로 가지는 객체 전체 (`toString()` 으로 모든 프로퍼티가 출력된다. `data class` 는 기본 `toString()` 이 모든 프로퍼티를 포함한다)
- 요청·응답 본문이나 헤더 전체

```kotlin
Log.d(TAG, "login success token=${response.accessToken}")
Log.i(TAG, "user signed in: $user")  // User(email=..., phone=...)
Log.e(TAG, "auth failed for ${credentials.email} / ${credentials.password}")
Timber.d("headers: ${request.headers}")
```

## 수정

민감한 값을 메시지에서 제외하고, 식별이 필요하면 마스킹한 값을 출력한다.

```kotlin
Log.d(TAG, "login success")
Log.i(TAG, "user signed in: id=${user.id}")
Log.e(TAG, "auth failed for ${credentials.email.mask()}")
```

민감한 값을 가진 타입은 `toString()` 을 오버라이드해 값을 가린다.

```kotlin
data class Credential(val token: String) {
    override fun toString() = "Credential(XX)"
}
```

## 허용

- 사용자 ID·주문 ID 처럼 그 자체로 개인을 식별하거나 인증에 쓸 수 없는 내부 식별자
- `if (BuildConfig.DEBUG)` 블록 안의 로그, 또는 debug 빌드 소스셋(`src/debug/`)의 로그
- 마스킹·해시한 값만 출력하는 경우, 또는 `toString()` 을 오버라이드해 민감한 프로퍼티를 가린 타입의 객체
- 테스트 코드
