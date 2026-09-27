---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/performance/bestpractices#use-remember
---

# 컴포지션에서 실행하는 정렬·필터링 등 비용이 큰 계산은 `remember` 로 캐시한다

## 이유

컴포저블 본문의 코드는 리컴포지션마다 다시 실행된다. 애니메이션 중에는 매 프레임 실행될 수도 있다. 컴포저블 본문이나 `LazyColumn` 의 콘텐츠 람다에서 목록을 정렬·필터링하면 입력이 바뀌지 않아도 리컴포지션마다 전체 목록을 다시 계산한다. 공식 문서는 `remember` 로 결과를 저장해 입력이 바뀔 때만 다시 계산하라고 한다.

## 위반

```kotlin
@Composable
fun ContactList(contacts: List<Contact>, comparator: Comparator<Contact>) {
    LazyColumn {
        items(contacts.sortedWith(comparator)) { contact -> ContactRow(contact) }
    }
}

@Composable
fun OrderSummary(orders: List<Order>) {
    val byDate = orders.filter { it.isPaid }.groupBy { it.date }
    // ...
}
```

## 수정

계산에 사용하는 값을 모두 `remember` 의 키로 지정한다.

```kotlin
@Composable
fun ContactList(contacts: List<Contact>, comparator: Comparator<Contact>) {
    val sortedContacts = remember(contacts, comparator) { contacts.sortedWith(comparator) }
    LazyColumn {
        items(sortedContacts) { contact -> ContactRow(contact) }
    }
}
```

가능하면 계산을 ViewModel 등 컴포지션 밖으로 이동해, UI 가 계산 결과만 받게 한다.

## 허용

- `remember { }`·`derivedStateOf { }` 블록 안, `onClick` 등 이벤트 람다 안, `LaunchedEffect` 블록 안의 계산
- `size`·`isEmpty()`·`first()`·`getOrNull()` 처럼 목록 전체를 순회하지 않는 연산
- 요소 수가 코드에 고정된 작은 목록(예: `listOf(...)` 리터럴, enum 의 `entries`)에 대한 연산
