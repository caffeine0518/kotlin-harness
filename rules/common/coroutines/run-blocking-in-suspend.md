---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/run-blocking.html
---

# suspend 함수와 코루틴 안에서 `runBlocking` 을 호출하지 않는다

## 이유

`runBlocking` 은 일반 블로킹 코드에서 suspend 함수를 호출하기 위한 브리지다. suspend 함수 안에서 호출하면 불필요할 뿐 아니라, 블록 안에서 호출한 suspend 함수가 일시 중단될 때 스레드를 해제하지 않고 블로킹한다. 스레드 고갈로 이어질 수 있고, 현재 코루틴 컨텍스트를 무시하고 새 컨텍스트에서 실행되므로 호출한 코루틴의 취소도 적용되지 않는다.

## 위반

```kotlin
suspend fun loadConfiguration() {
    val data = runBlocking { fetchConfigurationData() }
}

scope.launch {
    val user = runBlocking { api.fetchUser() }
}
```

## 수정

```kotlin
suspend fun loadConfiguration() {
    val data = fetchConfigurationData()
}
```

## 허용

- `main` 함수, 테스트 코드
- suspend 가 아닌 콜백(예: Java 인터페이스 구현)에서 suspend 함수를 호출해야 하는 경우
