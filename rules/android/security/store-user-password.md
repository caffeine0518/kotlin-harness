---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/privacy-and-security/security-tips#credential-exposure
---

# 사용자 비밀번호를 기기에 저장하지 않고 서버가 발급한 토큰을 저장한다

## 이유

공식 문서는 비밀번호 인증을 써야 한다면 사용자 ID 와 비밀번호를 기기에 저장하지 말고, 사용자가 입력한 비밀번호로 최초 인증한 뒤 수명이 짧은 서비스 전용 인가 토큰을 사용하라고 한다. 토큰은 만료·폐기할 수 있지만 기기에 저장한 비밀번호는 사용자가 바꾸기 전까지 유효하다.

## 위반

사용자가 입력한 비밀번호를 `SharedPreferences`·DataStore·Room·파일에 저장하는 코드가 위반이다. 암호화해 저장하는 경우(`EncryptedSharedPreferences` 등)도 포함한다.

```kotlin
fun onLoginSuccess(email: String, password: String) {
    prefs.edit()
        .putString("email", email)
        .putString("password", password)
        .apply()
}

dataStore.edit { it[PASSWORD_KEY] = password }
```

## 수정

로그인 응답의 토큰을 저장하고, 자동 로그인은 토큰 갱신으로 처리한다.

```kotlin
fun onLoginSuccess(response: LoginResponse) {
    tokenStore.save(response.accessToken, response.refreshToken)
}
```

비밀번호 저장을 대체하려면 로그인 API 가 토큰을 반환해야 하고 자동 로그인 흐름도 바뀌므로 자동으로 수정하지 않는다. 비밀번호 없이 인증하려면 Credential Manager(패스키, Google 로그인)를 사용한다.

## 허용

- 서버가 발급한 액세스·리프레시 토큰을 저장하는 경우
- 비밀번호를 저장하지 않고 입력 화면의 상태(`rememberSaveable`·`SavedStateHandle`)로만 보관하는 경우
- 사용자가 설정한 앱 잠금 PIN 을 해시해 저장하는 경우
- 테스트 코드
