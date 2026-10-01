---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#choose-good-names
---

# 리시버를 변경하는 함수는 동사 원형으로, 새 객체를 반환하는 함수는 과거분사형으로 이름 짓는다

## 이유

코틀린 코딩 관례는 메서드 이름이 객체를 변경하는지 새 객체를 반환하는지 나타내야 한다고 한다. `sort` 는 컬렉션을 제자리에서 정렬하고, `sorted` 는 정렬된 복사본을 반환한다. 표준 라이브러리도 `reverse`/`reversed`, `shuffle`/`shuffled` 를 같은 규칙으로 구분한다. 제자리에서 변경하는 함수를 `sorted()` 로 이름 지으면 호출하는 쪽은 원본이 바뀌지 않는다고 생각하고, 복사본을 반환하는 함수를 `sort()` 로 이름 지으면 반환값을 사용하지 않아 결과가 사라진다.

## 위반

- 이름이 `-ed` 로 끝나는 과거분사형(`sorted`·`filtered`·`reversed`·`normalized`)인데, 리시버·프로퍼티를 변경하고 `Unit` 을 반환한다
- 이름이 동사 원형(`sort`·`filter`·`normalize`)인데, 리시버를 변경하지 않고 새 객체를 반환한다

```kotlin
class Playlist {
    private val songs = mutableListOf<Song>()
    fun sorted() { songs.sortBy { it.title } }  // 제자리 변경
}

fun MutableList<Song>.sortByTitle(): List<Song> = sortedBy { it.title }  // 가변 리시버인데 복사본을 반환
```

## 수정

```kotlin
class Playlist {
    private val songs = mutableListOf<Song>()
    fun sort() { songs.sortBy { it.title } }
}

fun MutableList<Song>.sortedByTitle(): List<Song> = sortedBy { it.title }
```

## 허용

- `String`·data class 처럼 불변 타입의 함수. 리시버를 변경할 수 없으므로 동사 원형이어도 새 객체를 반환한다는 것이 명확하다. 단, 같은 타입에 변경 함수와 복사 함수가 함께 있으면 위반이다.
- `toXxx()`·`asXxx()`·`withXxx()` 처럼 변환을 나타내는 관례 접두사
