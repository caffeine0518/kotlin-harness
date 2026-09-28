---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/on-completion.html
---

# 실패를 복구하려면 `onCompletion` 이 아니라 `catch` 연산자를 쓴다

## 이유

`onCompletion` 은 수집 전체를 `finally` 로 감싼 것과 같다. 공식 문서에 따르면 `onCompletion` 은 예외를 관찰할 뿐 처리하지 않으므로, `cause` 가 있어도 예외는 계속 전파된다. 추가 값은 Flow 가 정상 완료된 경우에만 방출할 수 있고, 실패나 취소 시 예외를 억제하고 값을 방출하려면 `catch` 를 쓰라고 한다. `onCompletion { cause -> if (cause != null) emit(...) }` 은 실패를 복구하지 못한다.

`onCompletion` 은 `catch` 와 달리 업스트림·다운스트림 예외와 취소 예외를 모두 관찰한다. 따라서 `cause != null` 을 업스트림 실패로 간주하면 컬렉터의 예외나 화면 이탈로 인한 취소에도 오류 처리 코드가 실행된다.

## 위반

```kotlin
repository.observeOrders()
    .onCompletion { cause -> if (cause != null) emit(emptyList()) }  // 예외가 계속 전파된다

repository.observeOrders()
    .onCompletion { cause -> if (cause != null) _uiState.value = UiState.Error }  // 취소에도 오류 상태가 된다
    .collect { render(it) }
```

## 수정

```kotlin
repository.observeOrders()
    .catch { emit(emptyList()) }

repository.observeOrders()
    .catch { _uiState.value = UiState.Error }
    .onCompletion { hideProgress() }
    .collect { render(it) }
```

## 허용

- 정상 완료·실패·취소와 관계없이 실행할 정리 작업(진행 표시 해제, 리소스 해제, 로그 출력)
- `cause` 로 분기하되 `cause is CancellationException` 을 구분하고, 예외를 복구하지 않는 경우
- `cause == null` 일 때만 값을 방출하는 경우
