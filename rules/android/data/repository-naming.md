---
severity: info
applies_to: "**/*.kt"
source: https://developer.android.com/topic/architecture/data-layer
---

# 리포지토리는 `데이터 타입 + Repository`, 데이터 소스는 `데이터 타입 + 소스 종류 + DataSource` 로 이름 짓고, 구현 수단을 이름에 쓰지 않는다

## 이유

공식 문서는 리포지토리를 `데이터 타입 + Repository`(`NewsRepository`), 데이터 소스를 `데이터 타입 + 소스 종류 + DataSource` 로 이름 짓게 한다. 소스 종류는 구현이 바뀔 수 있으므로 `Remote`·`Local` 을 쓰고, 소스가 중요하면 `Network`·`Disk` 처럼 구체적으로 쓴다. `UserSharedPreferencesDataSource` 처럼 구현 수단으로 이름 지으면 안 된다고 명시한다. 데이터 소스를 쓰는 리포지토리는 데이터가 어떻게 저장되는지 몰라야 하고, 그래야 SharedPreferences 에서 DataStore 로 옮길 때 호출하는 레이어를 수정하지 않아도 된다.

## 위반

- 이름이 `DataSource` 로 끝나는데 `SharedPreferences`·`Prefs`·`DataStore`·`Room`·`Retrofit`·`Firebase`·`Sqlite` 같은 라이브러리·저장 방식 이름을 포함한다
- 데이터 레이어 패키지(`data`·`repository`)에서 데이터 소스를 조합해 앱에 데이터를 제공하는 클래스의 이름이 `Manager`·`Service`·`Helper` 로 끝난다

```kotlin
class UserSharedPreferencesDataSource(private val prefs: SharedPreferences)
class NewsRetrofitDataSource(private val api: NewsApi)
class NewsManager(private val remote: NewsRemoteDataSource, private val local: NewsLocalDataSource)
```

## 수정

```kotlin
class UserLocalDataSource(private val prefs: SharedPreferences)
class NewsRemoteDataSource(private val api: NewsApi)
class NewsRepository(private val remote: NewsRemoteDataSource, private val local: NewsLocalDataSource)
```

## 허용

- Retrofit 인터페이스(`NewsApi`·`NewsService`), Room DAO(`NewsDao`)처럼 라이브러리가 요구하는 선언. 이 룰은 그 선언을 감싸는 데이터 소스와 리포지토리의 이름만 판정한다.
- 여러 구현을 두는 인터페이스의 구현 클래스(`UserDataSource` 인터페이스의 `DataStoreUserDataSource`). 호출하는 쪽은 인터페이스 이름만 사용한다.
- Android `Service` 를 상속한 클래스
