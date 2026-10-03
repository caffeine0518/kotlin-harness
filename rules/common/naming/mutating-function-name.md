---
severity: info
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#choose-good-names
---

# 리시버를 변경하는 함수는 동사 원형으로, 새 객체를 반환하는 함수는 과거분사형으로 이름 짓는다

## 이유

코틀린 코딩 관례는 메서드 이름에서 객체를 변경하는지, 새 객체를 반환하는지 알 수 있어야 한다고 한다. `sort` 는 컬렉션 자체를 정렬하고, `sorted` 는 원본을 그대로 두고 정렬된 복사본을 반환한다. 표준 라이브러리의 `reverse`/`reversed`, `shuffle`/`shuffled` 도 같은 규칙으로 구분한다.

이름이 실제 동작과 반대이면 호출하는 쪽이 결과를 잘못 판단한다.

- 원본을 변경하는 함수의 이름이 `sorted()` 이면, 호출하는 쪽은 원본이 그대로라고 생각해 바뀐 원본을 그대로 사용한다.
- 복사본을 반환하는 함수의 이름이 `sort()` 이면, 호출하는 쪽은 원본이 정렬됐다고 생각해 반환값을 받지 않고, 정렬 결과가 사라진다.

## 위반

- 이름이 `-ed` 로 끝나는 과거분사형(`sorted`·`filtered`·`reversed`·`normalized`)인데, 리시버·프로퍼티를 변경하고 `Unit` 을 반환한다
- 이름이 동사 원형(`sort`·`filter`·`normalize`)인데, 리시버를 변경하지 않고 새 객체를 반환한다

```kotlin
class Playlist {
    private val songs = mutableListOf<Song>()
    fun sorted() { songs.sortBy { it.title } }  // 이름은 sorted 인데 songs 자체를 정렬한다
}

fun MutableList<Song>.sortByTitle(): List<Song> = sortedBy { it.title }  // 이름은 sort 인데 원본을 그대로 두고 정렬된 복사본을 반환한다
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
