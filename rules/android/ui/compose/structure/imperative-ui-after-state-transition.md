---
severity: warning
applies_to: "**/*.kt"
source: https://github.com/caffeine0518/kotlin-harness/issues/15
---

# 상태 전이를 기다려 명령형으로 UI 를 조작하는 이펙트는 상태 모델로 해결할 수 있는지 검토한다

## 이유

Compose 의 UI 는 상태로 결정된다. 이펙트에서 상태가 특정 값으로 바뀌기를 기다린 뒤 스크롤·포커스를 조작하면, 결과가 상태가 아니라 이벤트가 도착하는 순서에 따라 달라진다.

이런 코드는 대부분 상태 모델이 UI 에 필요한 정보를 표현하지 못해서 생긴다. 상태 모델을 바꾸면 이펙트 없이 한 줄로 해결되는 경우가 많다. 이펙트를 다듬는 수정(키 캐시, 조건 추가)은 코드만 늘린다.

## 위반

`LaunchedEffect` 안에서 `snapshotFlow` 등으로 상태 전이를 기다린 뒤(`first`·`dropWhile`·`filter` 등) 명령형 UI 조작을 실행한다. 예: `scrollToItem`·`animateScrollToItem`·`requestFocus`

```kotlin
val condition = state.filter.let { f -> f.sort to f.items.filter { it.isSelected }.map { it.id } }
LaunchedEffect(condition) {
    snapshotFlow { items.loadState.refresh }
        .dropWhile { it !is LoadState.Loading }
        .first { it is LoadState.NotLoading }
    listState.scrollToItem(0)
}
```

## 수정

상태 모델만 바꿔 같은 결과를 내도록 수정한다. 대안은 상태 모델에 따라 다르므로, 리포 안의 상태 모델과 상태를 만드는 코드를 확인해 정한다.

예: 조건을 바꿔 다시 조회하면 목록이 처음으로 스크롤되어야 하는 경우. 이펙트와 키를 계산하는 코드를 삭제하고 아래 중 하나로 수정한다.

- 조건을 키로 `LazyListState` 를 새로 만든다. 조건이 바뀔 때만 위치가 초기화되고, 같은 조건으로 다시 조회할 때(당겨서 새로고침 등)는 LazyColumn 의 key 로 보던 아이템 위치가 유지된다. 어느 쪽이 맞는지 코드로 판정할 수 없으면 이 대안을 쓴다.
- 다시 조회하는 동안 목록을 비운다. 목록이 다시 생성되어 위치가 초기화된다. 같은 조건으로 다시 조회할 때도 위치가 초기화되므로, 위치를 유지할 필요가 없을 때만 쓴다.

```kotlin
// 조건을 키로 LazyListState 를 새로 만든다
val listState = remember(state.filter) { LazyListState() }

// 다시 조회하는 동안 목록을 비운다
// 수정 전
refresh is LoadState.Loading && itemCount == 0 -> Loading
// 수정 후
refresh is LoadState.Loading -> Loading
```

## 허용

- 사용자 이벤트에 대한 응답으로 스크롤·포커스를 조작하는 경우. 예: `onClick` 에서 `animateScrollToItem(0)`
- 상태 전이를 기다리지 않고, 키가 바뀔 때 바로 UI 를 조작하는 경우. 예: `LaunchedEffect(selectedIndex) { listState.animateScrollToItem(selectedIndex) }`
- 위 대안으로는 기획상 필요한 위치 유지를 구현할 수 없고, 그 이유를 주석으로 적은 경우
