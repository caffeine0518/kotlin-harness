---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/performance/bestpractices#use-remember
---

# 컴포지션에서 실행하는 정렬·필터링 등 비용이 큰 계산은 `remember` 로 캐시한다

## 이유

컴포저블 본문의 코드는 리컴포지션마다 다시 실행된다. 애니메이션 중에는 매 프레임 실행될 수도 있다.

컴포저블 본문이나 `LazyColumn` 의 콘텐츠 람다에서 목록을 정렬·필터링하면 입력이 바뀌지 않아도 리컴포지션마다 전체 목록을 다시 계산한다.

## 위반

컴포저블 본문이나 Lazy 레이아웃의 콘텐츠 람다에서, 목록 전체를 순회하는 계산을 `remember` 없이 실행한다. 예: 정렬·필터링·그룹화

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

기존 식은 고쳐 쓰지 않고 `remember { }` 블록으로 감싸기만 한다. 키에는 계산에 사용하는 값을 식 그대로 지정한다. 키로만 쓰는 지역 변수를 추가하지 않는다.

```kotlin
// 수정 전
val key = status.filter.let { filter -> filter.sort to filter.items.filter { it.isSelected }.map { it.id } }

// 수정 후
val key = remember(status.filter) {
    status.filter.let { filter -> filter.sort to filter.items.filter { it.isSelected }.map { it.id } }
}
```

가능하면 계산을 ViewModel 등 컴포지션 밖으로 이동해, UI 가 계산 결과만 받게 한다.

## 허용

- 리컴포지션마다 실행되지 않는 블록 안의 계산. 예: `remember { }`·`derivedStateOf { }` 블록, `onClick` 같은 이벤트 람다, `LaunchedEffect` 블록
- 목록 전체를 순회하지 않는 연산. 예: `size`·`isEmpty()`·`first()`·`getOrNull()`
- 요소 수가 코드에 고정된 작은 목록에 대한 연산. 예: `listOf(...)` 리터럴, enum 의 `entries`
