---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/exceptions.html#handle-exceptions-using-try-catch-blocks
---

# 여러 `catch` 블록과 예외를 분기하는 `when` 의 `is` 분기는 구체적인 예외부터 일반적인 예외 순서로 작성한다

## 이유

`catch` 블록은 위에서부터 순서대로 확인되고, 처음 해당하는 블록 하나만 실행된다. 상위 타입의 `catch` 가 먼저 있으면 그 아래 하위 타입의 `catch` 는 실행되지 않는다. 공식 문서는 가장 구체적인 예외부터 가장 일반적인 예외 순서로 작성하라고 한다.

예외를 `when` 의 `is` 분기로 나누는 경우도 같다. `when` 도 분기를 위에서부터 순서대로 확인해 처음 해당하는 분기 하나만 실행하므로, 상위 타입의 `is` 분기 아래에 있는 하위 타입의 분기는 실행되지 않는다. `catch (e: Exception)` 블록 안, `runCatching { }.onFailure { }`, 예외를 다른 타입으로 변환하는 함수에서 이렇게 작성한다.

## 위반

```kotlin
try {
    processWithdrawal(amount, funds)
} catch (e: WithdrawalException) {
    showGenericError()
} catch (e: InsufficientFundsException) {  // WithdrawalException 의 하위 타입이라 위 catch 가 먼저 처리한다. 실행되지 않는다
    showInsufficientFunds()
}

try {
    file.readText()
} catch (e: Exception) {
    log(e)
} catch (e: IOException) {  // Exception 의 하위 타입이라 위 catch 가 먼저 처리한다. 실행되지 않는다
    retry()
}

runCatching { processWithdrawal(amount, funds) }
    .onFailure { e ->
        when (e) {
            is WithdrawalException -> showGenericError()
            is InsufficientFundsException -> showInsufficientFunds()  // WithdrawalException 의 하위 타입이라 위 분기가 먼저 해당한다. 실행되지 않는다
        }
    }
```

## 수정

```kotlin
try {
    processWithdrawal(amount, funds)
} catch (e: InsufficientFundsException) {
    showInsufficientFunds()
} catch (e: WithdrawalException) {
    showGenericError()
}

runCatching { processWithdrawal(amount, funds) }
    .onFailure { e ->
        when (e) {
            is InsufficientFundsException -> showInsufficientFunds()
            is WithdrawalException -> showGenericError()
        }
    }
```

같은 예외 계층을 여러 곳에서 분기하면, 데이터를 가져오는 계층의 경계에서 sealed 타입으로 한 번 변환해 이후의 분기가 순서와 무관하게 할 수 있다. sealed 의 하위 타입끼리는 상속 관계가 없어 순서가 결과에 영향을 주지 않고, `else` 없이 작성하면 처리하지 않은 타입이 컴파일 오류가 된다.

```kotlin
sealed interface WithdrawalError {
    data object InsufficientFunds : WithdrawalError
    data class Unknown(val cause: Throwable) : WithdrawalError
}

fun Throwable.toWithdrawalError(): WithdrawalError = when (this) {
    is InsufficientFundsException -> WithdrawalError.InsufficientFunds
    else -> WithdrawalError.Unknown(this)
}
```

## 허용

- 두 예외 타입 사이에 상속 관계가 없는 경우. 이때는 순서가 결과에 영향을 주지 않는다. `when` 의 `is` 분기도 같다.
- 상속 관계를 코드에서 확인할 수 없는 경우는 보고하지 않는다.
