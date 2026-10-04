---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/privacy-and-security/security-tips#key-generation-storage
---

# API 키·암호화 키·비밀번호 같은 비밀 값을 소스 코드에 리터럴로 작성하지 않는다

## 이유

소스 코드에 포함된 API 키는 앱을 디컴파일하면 추출할 수 있다. 문자열이나 바이트 배열로 코드에 작성한 암호화 키도 리버스 엔지니어링 도구로 쉽게 추출되고, 그 경우 보안 모델이 유효하지 않다.

## 위반

아래 값을 문자열·바이트 배열 리터럴로 작성해 변수·상수·인수로 쓰는 코드가 위반이다.

- 서비스 API 키, 클라이언트 시크릿, 액세스 토큰 (예: `sk_live_...`, `AIza...`, `ghp_...` 형식, 또는 이름이 `apiKey`·`secret`·`token`·`password` 인 변수·인수에 전달하는 긴 무작위 문자열)
- `SecretKeySpec`·`IvParameterSpec`·`PBEKeySpec` 에 전달하는 키·IV·비밀번호
- 서버 인증에 쓰는 비밀번호·Basic 인증 문자열

```kotlin
private const val PAYMENT_API_KEY = "sk_live_51H8xYzAbCdEfGhIjKlMnOp"

val request = Request.Builder()
    .url(url)
    .header("Authorization", "Bearer eyJhbGciOiJIUzI1NiJ9.c2VjcmV0.abc123")
    .build()

val key = SecretKeySpec("0123456789abcdef".toByteArray(), "AES")
val aesKey = SecretKeySpec(byteArrayOf(0x1f, 0x2e, 0x3d, 0x4c, 0x5b, 0x6a, 0x79, 0x08), "AES")
```

## 수정

어디에 저장할지는 키의 용도에 따라 달라서 코드만으로 정할 수 없다. 저장 위치가 정해져 있지 않으면 자동으로 수정하지 않고 리포트에만 남긴다. 리터럴을 다른 소스 파일·`strings.xml`·커밋되는 `gradle.properties` 로 옮기는 것은 수정이 아니다.

- 빌드 시점에 필요한 API 키: `local.properties` 등 커밋하지 않는 파일에 두고 secrets-gradle-plugin 으로 `BuildConfig` 필드를 생성해 참조한다.
- 앱이 만드는 암호화 키: 리터럴 대신 Android Keystore 에서 생성·조회한다.
- 서버 호출에 필요한 비밀: 사용자 인증 뒤 서버가 발급한 단기 토큰을 사용한다.

```kotlin
val apiKey = BuildConfig.PAYMENT_API_KEY  // local.properties 에서 secrets-gradle-plugin 이 생성

val keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
keyGenerator.init(
    KeyGenParameterSpec.Builder("app_key", KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        .build(),
)
val key = keyGenerator.generateKey()
```

## 허용

- `BuildConfig` 필드·`System.getenv()`·Keystore·서버 응답에서 조회한 값 (이 룰은 리터럴만 검사한다)
- `"AndroidKeyStore"` 같은 provider 이름, Keystore 별칭, 헤더 이름, 설정 키 이름처럼 비밀이 아닌 식별자 문자열
- Google Maps·Firebase 처럼 서비스가 앱 패키지·서명으로 사용을 제한하도록 설계한 공개 식별자를 서비스 문서가 지정한 위치(`google-services.json` 등)에서 참조하는 경우
- `GenerativeModel` 생성자에 전달하는 API 키 — Android Lint `SecretInSource` 가 검사한다
- 빈 문자열, 또는 값 전체가 `"YOUR_API_KEY"`·`"<api-key>"` 처럼 키를 입력하라는 안내 문구인 플레이스홀더. `sk_live_`·`AIza` 같은 키 형식 접두사가 있으면 플레이스홀더로 보지 않는다.
- 테스트 코드 (`src/test/`·`src/androidTest/` 아래 파일)
