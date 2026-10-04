---
severity: info
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/data-layer
---

# 리포지토리·데이터 소스의 이름에는 구현 수단 대신 데이터 타입과 소스 종류를 쓴다

## 이유

데이터 소스를 쓰는 쪽은 데이터가 어떻게 저장되는지 몰라야 한다. `UserSharedPreferencesDataSource` 처럼 구현 수단을 이름에 쓰면, SharedPreferences 에서 DataStore 로 옮길 때 이름이 실제 구현과 달라진다. 이름을 바꾸면 호출하는 코드까지 수정해야 한다.

리포지토리를 `Manager`·`Helper` 로 이름 지으면, 그 클래스가 데이터 레이어의 진입점인지 이름으로 알 수 없다.

## 위반

- 데이터 소스 이름에 라이브러리·저장 방식 이름이 들어 있다. 예: `SharedPreferences`·`Prefs`·`DataStore`·`Room`·`Retrofit`·`Firebase`·`Sqlite`
- 데이터 소스를 조합해 앱에 데이터를 제공하는 클래스의 이름이 `Repository` 가 아니라 `Manager`·`Service`·`Helper` 로 끝난다.

```kotlin
class UserSharedPreferencesDataSource(private val prefs: SharedPreferences)
class NewsRetrofitDataSource(private val api: NewsApi)
class NewsManager(private val remote: NewsRemoteDataSource, private val local: NewsLocalDataSource)
```

## 수정

- 리포지토리: `데이터 타입 + Repository`. 예: `NewsRepository`
- 데이터 소스: `데이터 타입 + 소스 종류 + DataSource`. 소스 종류는 `Remote`·`Local` 로 쓰고, 소스를 구분해야 하면 `Network`·`Disk` 처럼 구체적으로 쓴다. 예: `NewsRemoteDataSource`

```kotlin
class UserLocalDataSource(private val prefs: SharedPreferences)
class NewsRemoteDataSource(private val api: NewsApi)
class NewsRepository(private val remote: NewsRemoteDataSource, private val local: NewsLocalDataSource)
```

## 허용

- 라이브러리가 요구하는 선언. 예: Retrofit 인터페이스(`NewsApi`·`NewsService`), Room DAO(`NewsDao`). 이 룰은 그 선언을 감싸는 데이터 소스와 리포지토리의 이름만 판정한다.
- 여러 구현을 두는 인터페이스의 구현 클래스. 예: `UserDataSource` 인터페이스의 `DataStoreUserDataSource`. 호출하는 쪽은 인터페이스 이름만 사용한다.
- Android `Service` 를 상속한 클래스
