---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coroutines-flow.html
---

# `flow { }` 빌더에서 `emit` 을 감싼 `try`·`catch` 로 잡은 예외는 다시 전파한다

## 이유

`emit()` 은 `collect()` 에 전달한 람다를 호출한다. 따라서 `emit` 을 감싼 `try` 는 컬렉터에서 발생한 예외도 잡는다. 공식 문서는 빌더에서 컬렉터의 예외를 잡았으면 다시 전파하라고 한다. 다시 전파해야 예외 투명성(exception transparency)이 유지되고, `collect()` 를 호출한 쪽이 그 예외를 처리할 수 있다. 예외를 무시하면 컬렉터가 실패한 뒤에도 빌더가 다음 값을 계속 방출한다.

## 위반

```kotlin
fun prices(): Flow<Price> = flow {
    for (id in ids) {
        try {
            emit(api.price(id))
        } catch (e: IOException) {
            log(e)  // 컬렉터에서 발생한 IOException 도 여기서 무시된다
        }
    }
}
```

## 수정

업스트림 예외만 처리하려면 `emit` 을 `try` 밖으로 옮기거나 `catch` 연산자를 쓴다. `emit` 을 감싸야 하면 잡은 예외를 다시 전파한다.

```kotlin
fun prices(): Flow<Price> = flow {
    for (id in ids) {
        val price = try {
            api.price(id)
        } catch (e: IOException) {
            log(e)
            continue
        }
        emit(price)
    }
}

fun prices(): Flow<Price> = flow {
    for (id in ids) emit(api.price(id))
}.catch { e -> if (e is IOException) log(e) else throw e }
```

## 허용

- `catch` 블록에서 잡은 예외를 다시 전파하는 경우
- `try` 블록에 `emit`·`emitAll` 호출이 없는 경우
- `finally` 만 있고 `catch` 가 없는 경우
