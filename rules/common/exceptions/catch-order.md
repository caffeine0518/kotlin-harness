---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/exceptions.html#handle-exceptions-using-try-catch-blocks
---

# 여러 `catch` 블록은 구체적인 예외부터 일반적인 예외 순서로 작성한다

## 이유

`catch` 블록은 위에서부터 순서대로 확인되고, 처음 해당하는 블록 하나만 실행된다. 상위 타입의 `catch` 가 먼저 있으면 그 아래 하위 타입의 `catch` 는 실행되지 않는다. 공식 문서는 가장 구체적인 예외부터 가장 일반적인 예외 순서로 작성하라고 한다.

## 위반

```kotlin
try {
    processWithdrawal(amount, funds)
} catch (e: WithdrawalException) {
    showGenericError()
} catch (e: InsufficientFundsException) {  // InsufficientFundsException : WithdrawalException — 실행되지 않는다
    showInsufficientFunds()
}

try {
    file.readText()
} catch (e: Exception) {
    log(e)
} catch (e: IOException) {  // 실행되지 않는다
    retry()
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
```

## 허용

- 두 예외 타입 사이에 상속 관계가 없는 경우. 이때는 순서가 결과에 영향을 주지 않는다.
- 상속 관계를 코드에서 확인할 수 없는 경우는 보고하지 않는다.
