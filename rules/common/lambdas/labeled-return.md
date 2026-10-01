---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#returns-in-a-lambda
---

# 람다 하나에 라벨 반환을 여러 번 쓰지 않고, 람다의 마지막 문에는 라벨 반환을 쓰지 않는다

## 이유

코틀린 코딩 관례는 람다 하나에 라벨 반환(`return@label`)을 여러 번 쓰지 말고, 출구가 하나가 되도록 람다를 다시 작성하라고 한다. 그렇게 할 수 없거나 명확하지 않으면 람다를 익명 함수로 바꾼다. 익명 함수에서는 라벨 없는 `return` 이 그 함수만 종료한다. 람다의 마지막 문에는 라벨 반환을 쓰지 않는다. 람다의 마지막 식이 그대로 반환값이다.

## 위반

```kotlin
items.forEach {
    if (it.hidden) return@forEach
    if (it.expired) return@forEach
    send(it)
}

val ids = users.map { user ->
    val id = user.id.trim()
    return@map id
}
```

## 수정

```kotlin
items.filter { !it.hidden && !it.expired }.forEach { send(it) }

val ids = users.map { user -> user.id.trim() }
```

## 허용

- 라벨 반환이 한 번이고 마지막 문이 아닌 경우
- 람다를 익명 함수로 바꾸면 호출 형태가 오히려 읽기 어려워지는 DSL 블록
