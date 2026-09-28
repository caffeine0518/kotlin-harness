---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#loops
---

# 단순 순회는 `forEach` 대신 `for` 루프로 작성한다

## 이유

코틀린 코딩 관례는 `forEach` 대신 일반 `for` 루프를 쓰라고 한다. 예외는 `forEach` 의 리시버가 널러블이거나, `forEach` 가 긴 호출 체인의 일부인 경우다. `forEach` 안에서는 `break` 를 쓸 수 없고, `continue` 대신 `return@forEach` 를 써야 한다. 라벨 없는 `return` 은 `forEach` 가 인라인 함수이므로 람다가 아니라 바깥 함수를 종료한다. `for` 루프는 이 흐름 제어를 그대로 쓸 수 있다.

## 위반

리시버가 논널 컬렉션·범위이고, 호출 체인 없이 `forEach` 만 호출한다.

```kotlin
items.forEach { send(it) }

users.forEach { user ->
    if (user.blocked) return@forEach
    notify(user)
}
```

## 수정

```kotlin
for (item in items) send(item)

for (user in users) {
    if (user.blocked) continue
    notify(user)
}
```

## 허용

- 리시버가 널러블인 경우 (`items?.forEach { }`)
- 긴 호출 체인의 일부인 경우 (`items.filter { }.map { }.forEach { }`)
- `Map.forEach { (key, value) -> }` 처럼 구조 분해로 가독성이 높아지는 경우
