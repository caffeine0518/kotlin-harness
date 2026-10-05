---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/data-classes.html
---

# 다른 타입끼리 필드를 하나씩 비교하지 않고, 비교 기준을 data class 로 선언해 `==` 로 비교한다

## 이유

필드를 `&&` 로 하나씩 이어 비교하면 무엇을 기준으로 같다고 판정하는지가 그 식에만 있다. 같은 기준으로 비교하는 함수가 여러 개면 기준을 바꿀 때 모두 찾아 수정해야 하고, 하나를 빠뜨려도 컴파일러가 검출하지 못한다.

비교 기준을 data class 로 선언하면 기준에 이름이 생기고, 비교는 그 타입의 `==` 하나가 된다. data class 의 `equals()` 는 주 생성자의 프로퍼티를 모두 비교하므로, 기준에 필드를 추가하면 그 타입을 생성하는 코드마다 컴파일 오류가 발생해 수정할 위치를 컴파일러가 알려 준다.

## 위반

아래 조건을 모두 만족하는 함수.

- 서로 다른 타입 두 개에서 같은 이름의 프로퍼티끼리 `==` 로 비교하는 식이 3개 이상 `&&` 로 이어진다.
- 그 식이 `Boolean` 을 반환하는 함수의 본문 전체다.

```kotlin
data class Result(val id: String, val sourceId: String, val targetId: String, val targetCode: String, val amount: String)

data class Command(val sourceId: String, val targetId: String, val targetCode: String, val amount: String, val note: String?)

private fun Result.isSameRequest(command: Command): Boolean =
    sourceId == command.sourceId &&
        targetId == command.targetId &&
        targetCode == command.targetCode &&
        amount == command.amount
```

## 수정

비교 기준이 되는 필드로 data class 를 선언하고, 양쪽 타입에서 그 타입을 생성하는 익스텐션 함수를 추가해 `==` 로 비교한다. 같은 파일 안에서만 쓰면 `private` 으로 선언한다.

```kotlin
private data class RequestKey(val sourceId: String, val targetId: String, val targetCode: String, val amount: String)

private fun Result.requestKey() = RequestKey(sourceId, targetId, targetCode, amount)

private fun Command.requestKey() = RequestKey(sourceId, targetId, targetCode, amount)

private fun Result.isSameRequest(command: Command) = requestKey() == command.requestKey()
```

## 허용

- 같은 타입 두 개를 비교하면서 일부 필드만 의도적으로 비교하는 경우. 그 의도를 주석으로 적었으면 위반이 아니다.
- `equals()` 오버라이드 구현
