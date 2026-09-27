---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/lists#item-keys
---

# 항목이 추가·삭제·이동될 수 있는 Lazy 레이아웃의 `items` 에는 `key` 를 지정한다

## 이유

`key` 를 지정하지 않으면 각 항목의 상태가 목록에서의 위치를 기준으로 저장된다. 데이터가 바뀌어 항목의 위치가 바뀌면 그 항목에서 `remember`·`rememberSaveable` 로 저장한 상태(입력값, 펼침 여부, 중첩 `LazyRow` 의 스크롤 위치)가 다른 항목에 연결되고, Compose 는 이동한 항목을 모두 리컴포지션한다. 안정적이고 고유한 키를 지정하면 위치가 바뀌어도 상태가 항목과 함께 이동한다.

## 위반

```kotlin
@Composable
fun NotesList(notes: List<Note>) {
    LazyColumn {
        items(notes) { note -> NoteRow(note) }
    }
}

LazyColumn {
    itemsIndexed(messages, key = { index, _ -> index }) { _, message -> MessageRow(message) }  // 위치를 키로 지정하면 기본값과 같다
}
```

## 수정

항목을 식별하는 값을 키로 지정한다. 키의 타입은 `Bundle` 에 저장할 수 있는 타입(기본 타입, enum, `Parcelable` 등)이어야 한다.

```kotlin
@Composable
fun NotesList(notes: List<Note>) {
    LazyColumn {
        items(notes, key = { note -> note.id }) { note -> NoteRow(note) }
    }
}
```

## 허용

- 코드에 고정된 목록(`listOf(...)` 리터럴, enum 의 `entries`, 상수 범위)처럼 실행 중에 항목이 추가·삭제·이동되지 않는 목록
- `items(count: Int)` 로 개수만 지정하고 항목에 상태가 없는 목록 (예: 로딩 플레이스홀더)
- `LazyPagingItems` 에 `itemKey { }` 로 키를 지정한 경우
