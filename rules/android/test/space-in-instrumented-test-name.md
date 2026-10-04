---
severity: error
applies_to: "**/src/androidTest/**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#names-for-test-methods
---

# `minSdk` 가 30 미만인 모듈의 계측 테스트 메서드 이름에는 공백을 쓰지 않는다

## 이유

테스트 코드에서는 메서드 이름을 백틱으로 감싸 공백을 쓸 수 있다. 하지만 공백이 있는 이름은 DEX 040 형식부터 허용되어, Android 런타임은 API 30 부터 지원한다. `minSdk` 가 30 미만이면 D8 이 계측 테스트 APK 를 dex 로 변환할 때 빌드 오류가 발생한다.

`src/test` 의 로컬 단위 테스트는 JVM 에서 실행되므로 공백을 써도 된다.

## 위반

모듈의 `build.gradle(.kts)` 에서 `minSdk`(또는 `minSdkVersion`)가 30 미만이고, `src/androidTest` 의 메서드 이름에 공백이 있다.

```kotlin
@Test
fun `로그인하면 홈으로 이동한다`() { }

@Test
fun `login navigates to home`() { }
```

## 수정

공백 대신 밑줄을 쓰거나, 카멜 케이스로 이름 짓는다.

```kotlin
@Test
fun `로그인하면_홈으로_이동한다`() { }

@Test
fun loginNavigatesToHome() { }
```

## 허용

- 모듈의 `minSdk` 가 30 이상인 경우
- `minSdk` 를 확인할 수 없는 경우. 리포트에 판정 불가로 적는다.
