---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/data-layer/offline-first#exposing-resources
---

# 리포지토리는 Room 엔티티·네트워크 모델을 그대로 노출하지 않고 별도 모델로 변환해 노출한다

## 이유

Room 엔티티와 네트워크 모델은 DB 스키마와 서버 응답의 형태를 따른다. 리포지토리가 이 타입을 그대로 노출하면, 앱 동작과 관계없는 작은 변경(컬럼 추가, JSON 필드 이름 변경 등)도 UI 레이어까지 전파된다.

별도 모델로 변환해 노출하면 이런 변경이 데이터 레이어 안에서 끝난다. 다른 레이어에는 필요한 데이터만 노출할 수 있다.

## 위반

리포지토리의 public 멤버가 Room 엔티티나 네트워크 모델을 반환하거나 파라미터로 받는다. `List<T>`·`Flow<T>`·`Result<T>` 처럼 감싼 타입이면 `T` 를 판정한다.

- Room 엔티티: `@Entity` 를 적용한 클래스
- 네트워크 모델: 직렬화 어노테이션(`@Serializable`·`@JsonClass`·`@SerializedName`)을 적용했고, 이름에 `Network`·`Dto`·`Response`·`Request` 가 들어간 클래스

```kotlin
@Entity(tableName = "authors")
data class AuthorEntity(@PrimaryKey val id: String, val name: String, val imageUrl: String)

@Serializable
data class NetworkAuthor(val id: String, val name: String, val imageUrl: String)

class AuthorsRepository(private val dao: AuthorDao, private val api: AuthorApi) {
    fun getAuthorStream(id: String): Flow<AuthorEntity> = dao.observe(id)
    suspend fun fetchAuthor(id: String): NetworkAuthor = api.getAuthor(id)
}
```

## 수정

외부 레이어용 모델을 선언하고, 리포지토리 안에서 변환한다.

```kotlin
data class Author(val id: String, val name: String, val imageUrl: String)

fun AuthorEntity.asExternalModel() = Author(id = id, name = name, imageUrl = imageUrl)
fun NetworkAuthor.asExternalModel() = Author(id = id, name = name, imageUrl = imageUrl)

class AuthorsRepository(private val dao: AuthorDao, private val api: AuthorApi) {
    fun getAuthorStream(id: String): Flow<Author> = dao.observe(id).map { it.asExternalModel() }
    suspend fun fetchAuthor(id: String): Author = api.getAuthor(id).asExternalModel()
}
```

## 허용

- 데이터 소스가 자신의 엔티티·네트워크 모델을 반환하는 경우. 데이터 레이어 안에서만 쓰는 타입이다. 예: `@Dao`, Retrofit 서비스, 이름이 `DataSource` 로 끝나는 클래스
- 리포지토리의 `private`·`internal` 멤버
- 모델 변환 함수. 예: `asEntity`·`asExternalModel`
- 어노테이션이 없는 일반 `data class` 를 노출하는 경우. 이름만으로는 데이터 소스 모델인지 판정할 수 없다.
