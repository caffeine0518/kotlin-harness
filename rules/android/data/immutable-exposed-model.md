---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/data-layer
---

# 리포지토리가 노출하는 모델은 `var` 프로퍼티 없이 불변으로 선언한다

## 이유

다른 클래스가 값을 바꿀 수 있으면 데이터가 일관되지 않은 상태가 될 수 있다. 불변 데이터는 여러 스레드에서 안전하게 다룰 수 있다.

리포지토리는 캐시한 객체를 그대로 반환하는 경우가 많다. 그 객체에 `var` 가 있으면 한 화면에서 바꾼 값이 캐시와, 같은 객체를 받은 다른 화면에도 반영된다.

## 위반

리포지토리의 public 함수·프로퍼티가 반환하는 모델에 `var` 프로퍼티가 있다. `Flow<T>`·`List<T>`·`Result<T>` 처럼 감싼 타입이면 `T` 를 판정한다.

```kotlin
data class News(val id: String, var title: String, var isBookmarked: Boolean)

interface NewsRepository {
    fun observeNews(): Flow<List<News>>
}
```

## 수정

`var` 를 `val` 로 바꾼다. 값을 바꿔야 하는 쪽은 `copy` 로 새 객체를 만든다.

```kotlin
data class News(val id: String, val title: String, val isBookmarked: Boolean)

val bookmarked = news.copy(isBookmarked = true)
```

## 허용

- Room 엔티티·네트워크 응답 모델처럼 리포지토리 밖으로 노출하지 않는 모델. 이런 모델을 리포지토리가 그대로 노출하는 코드는 `android/data/separate-data-source-models` 가 보고한다.
- `private set` 이 있는 `var` 프로퍼티
- data class 의 가변 컬렉션 프로퍼티는 이 룰이 아니라 `common/immutability/data-class-mutable-collection` 이 보고한다.
