---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/idioms.html#map-nullable-value-if-not-null
---

# `?.let { } ?: ...` 을 if-else 로 쓸 때 `let` 블록이 `null` 을 반환할 수 있으면 `if` 로 분기한다

## 이유

`value?.let { ... } ?: fallback` 에서 엘비스 연산자 오른쪽은 `value` 가 `null` 일 때뿐 아니라 `let` 블록의 마지막 식이 `null` 일 때도 실행된다. 공식 문서는 이 관용구에 대해 "value 또는 변환 결과가 `null` 이면 defaultValue 를 반환한다"고 적는다. `let` 블록이 부수 효과를 실행한 뒤 널러블 값을 반환하면 `let` 블록과 엘비스 오른쪽이 모두 실행된다.

## 위반

```kotlin
// cache.put 은 이전 값(없으면 null)을 반환하므로 새 키면 load() 도 실행된다
user?.let { cache.put(it.id, it) } ?: load()

// findSession() 이 null 을 반환하면 로그인한 사용자에게도 로그인 화면이 표시된다
currentUser?.let {
    analytics.track(it)
    findSession(it)
} ?: showLogin()
```

## 수정

```kotlin
if (user != null) cache.put(user.id, user) else load()

val user = currentUser
if (user != null) {
    analytics.track(user)
    findSession(user)
} else {
    showLogin()
}
```

## 허용

- `let` 블록의 마지막 식이 논널 타입인 경우 (`user?.let { it.name } ?: "guest"` 에서 `name` 이 `String`)
- 변환 결과가 `null` 일 때도 기본값을 쓰는 것이 의도인 값 변환 (`value?.let { parse(it) } ?: default`). 블록에 부수 효과가 없으면 위반이 아니다.
