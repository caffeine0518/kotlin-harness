---
severity: info
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/side-effects#disposableeffect-effects-that-require-cleanup
---

# 정리할 작업이 없으면 `DisposableEffect` 대신 다른 이펙트를 쓴다

## 이유

`DisposableEffect` 는 키가 바뀌거나 컴포지션에서 제외될 때 정리가 필요한 이펙트를 위한 API 다. 공식 문서는 `onDispose` 블록을 비워 두는 것이 좋은 방법이 아니며, 용도에 더 맞는 이펙트가 있는지 다시 확인하라고 한다.

## 위반

```kotlin
DisposableEffect(user) {
    analytics.setUserProperty("userType", user.userType)
    onDispose { }
}

DisposableEffect(Unit) {
    scope.launch { repository.refresh() }
    onDispose {}
}
```

## 수정

리컴포지션이 완료될 때마다 Compose 상태를 Compose 가 아닌 코드에 전달하면 `SideEffect`, suspend 함수를 실행하면 `LaunchedEffect` 를 쓴다.

```kotlin
SideEffect {
    analytics.setUserProperty("userType", user.userType)
}

LaunchedEffect(Unit) {
    repository.refresh()
}
```
