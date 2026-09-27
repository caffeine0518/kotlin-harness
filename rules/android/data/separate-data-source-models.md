---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/data-layer/offline-first#exposing-resources
---

# 리포지토리는 Room 엔티티·네트워크 모델을 그대로 노출하지 않고 별도 모델로 변환해 노출한다

## 이유

공식 문서는 로컬 데이터 소스의 엔티티(`AuthorEntity`)와 네트워크 데이터 소스의 모델(`NetworkAuthor`)을 데이터 레이어 내부에 두고, 외부 레이어에는 세 번째 타입(`Author`)을 노출하는 것이 좋은 관행이라고 한다. 앱 동작과 관계없는 로컬·네트워크 데이터 소스의 작은 변경(컬럼 추가, JSON 필드 이름 변경 등)이 UI 레이어까지 전파되지 않는다.

데이터 레이어 가이드도 리포지토리가 다른 레이어에 필요한 데이터만 노출하도록 모델 클래스를 분리하라고 하고, 최소한 데이터 소스가 받는 데이터가 앱의 다른 코드가 기대하는 형태와 다를 때는 새 모델을 만들라고 한다(https://developer.android.com/topic/architecture/data-layer#business-models).

## 위반

리포지토리(이름이 `Repository` 로 끝나는 클래스·인터페이스와 그 구현 클래스)의 public 함수·프로퍼티의 반환 타입이나 파라미터 타입에 아래 타입이 포함된다. `List<T>`·`Flow<T>`·`Result<T>` 등의 타입 인자도 포함한다.

- Room `@Entity` 로 선언된 클래스
- 네트워크 응답·요청 모델: `@Serializable`·`@JsonClass`·`@SerializedName` 을 적용했고, 이름에 `Network`·`Dto`·`Response`·`Request` 가 포함된 클래스

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

class AuthorsRepository(private val dao: AuthorDao, private val api: AuthorApi) {
    fun getAuthorStream(id: String): Flow<Author> = dao.observe(id).map { it.asExternalModel() }
    suspend fun fetchAuthor(id: String): Author = api.getAuthor(id).asEntity().asExternalModel()
}
```

## 허용

- 데이터 소스(`@Dao`, Retrofit 서비스, `DataSource` 로 끝나는 클래스)가 자신의 엔티티·네트워크 모델을 반환하는 경우. 데이터 레이어 내부 타입이다.
- 리포지토리의 `private`·`internal` 멤버, 모델 변환 함수(`asEntity`·`asExternalModel` 등)
- 어노테이션이 없는 일반 `data class` 를 노출하는 경우. 이름만으로는 데이터 소스 모델인지 판정할 수 없다.
