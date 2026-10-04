---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/privacy-and-security/risks/implicit-intent-hijacking#implicit-intent-hijacking-mitigations
---

# 토큰·개인정보를 포함한 인텐트는 암시적 인텐트로 보내지 않고 `setPackage()`·컴포넌트를 지정한다

## 이유

패키지나 컴포넌트를 지정하지 않은 암시적 인텐트는 같은 인텐트 필터를 등록한 다른 앱도 수신할 수 있다. 그 앱이 인텐트를 가로채 세션 토큰 같은 민감한 정보를 읽을 수 있다. 수신 권한을 지정하지 않은 브로드캐스트도 같다.

## 위반

아래 조건을 모두 만족하는 코드가 위반이다.

1. 인텐트에 액세스·세션 토큰, 비밀번호, 인증 코드, 개인정보(이메일·전화번호·주소 등)를 extra·data URI 로 포함한다.
2. 인텐트에 `setPackage()`·`setComponent()`·`setClass()`·`Intent(context, Foo::class.java)` 중 어느 것도 지정하지 않았다.
3. `startActivity()`·`startService()`·`sendBroadcast()`·`sendOrderedBroadcast()` 로 보낸다. `sendBroadcast()`·`sendOrderedBroadcast()` 는 수신 권한(`receiverPermission`) 인수를 지정하지 않은 경우만 위반이다.

```kotlin
val intent = Intent("com.example.action.OPEN_WEB").apply {
    putExtra("url", "https://example.com/home?session=$sessionToken")
}
startActivity(intent)

sendBroadcast(Intent("com.example.action.LOGIN_COMPLETED").putExtra("access_token", token))
```

## 수정

```kotlin
val intent = Intent("com.example.action.OPEN_WEB").apply {
    setPackage(context.packageName)
    putExtra("url", "https://example.com/home?session=$sessionToken")
}
startActivity(intent)

sendBroadcast(
    Intent("com.example.action.LOGIN_COMPLETED")
        .setPackage(context.packageName)
        .putExtra("access_token", token),
)
```

수신할 앱이 자기 앱이 아니면 대상 패키지를 코드만으로 정할 수 없으므로 자동으로 수정하지 않는다. 앱 내부 이벤트 알림이면 브로드캐스트 대신 콜백·Flow 로 전달하는 방법도 있다.

## 허용

- 이메일 작성·공유·카메라처럼 수신 앱을 알 수 없어 암시적 인텐트가 필요하고, 사용자가 직접 입력·선택한 내용만 포함하는 경우 (예: `ACTION_SEND` 로 사용자가 작성한 텍스트를 공유)
- 민감한 정보를 포함하지 않는 암시적 인텐트
- `sendBroadcast(intent, "com.example.permission.X")` 처럼 수신 권한을 지정한 브로드캐스트
- `PendingIntent` 의 가변성·암시적 인텐트 문제 — Android Lint `UnspecifiedImmutableFlag`·`MutableImplicitPendingIntent` 가 검사한다
- 암시적 인텐트가 자기 앱의 export 되지 않은 컴포넌트와 일치하는 경우 — Android Lint `UnsafeImplicitIntentLaunch` 가 검사한다
