---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coroutines-flow.html
---

# 실행해야 하는 Flow 에는 터미널 연산자를 호출한다

## 이유

콜드 Flow 는 지연 평가된다. 공식 문서에 따르면 콜드 Flow 빌더의 코드 블록은 컬렉터가 수집하기 전까지 실행되지 않는다. 중간 연산자(`map`·`onEach`·`filter`·`catch` 등)는 새 Flow 를 반환할 뿐이므로, `collect`·`launchIn`·`first`·`toList` 같은 터미널 연산자가 없으면 `onEach` 에 작성한 저장·전송 코드는 실행되지 않는다. 컴파일러는 이 코드를 오류로 보고하지 않는다.

## 위반

Flow 를 반환하는 호출의 결과를 변수에 대입하지도, 반환하지도, 터미널 연산자로 수집하지도 않는다.

```kotlin
fun syncAll() {
    viewModelScope.launch {
        repository.pendingOrders()
            .onEach { repository.upload(it) }  // 수집하지 않아 upload 가 호출되지 않는다
    }
}
```

## 수정

```kotlin
fun syncAll() {
    repository.pendingOrders()
        .onEach { repository.upload(it) }
        .launchIn(viewModelScope)
}
```

## 허용

- Flow 를 변수·프로퍼티에 대입하거나 함수에서 반환하는 경우
- 다른 함수의 인수로 전달하는 경우 (`combine(a, b)`·`emitAll(flow)` 등)
