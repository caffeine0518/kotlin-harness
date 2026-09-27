---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/privacy-and-security/risks/sql-injection#replaceable_parameters
---

# SQL 문과 selection 절에 외부 값을 문자열 연결·템플릿으로 넣지 않고 `?` 파라미터로 전달한다

## 이유

외부 값을 연결해 만든 SQL 문은 값에 포함된 `'`·`OR 1=1` 같은 문자열이 SQL 로 해석되어 SQL 인젝션이 발생한다. 공식 문서는 SQL 인젝션으로 개인정보가 노출되거나 인증·권한 제한이 우회되고 데이터베이스가 손상·삭제될 수 있다고 한다. `?` 파라미터와 별도의 인수 배열을 쓰면 값이 SQL 문의 일부로 해석되지 않고 쿼리에 바인딩된다. 공식 문서는 `query()`·`update()`·`delete()` 같은 파라미터 메서드를 쓰더라도 selection 인수를 사용자 데이터와 연결해 만들면 SQL 인젝션을 막지 못한다고 명시한다.

## 위반

파라미터·프로퍼티·인텐트 extra·네트워크 응답 등 상수가 아닌 값을 SQL 문자열에 연결하거나 문자열 템플릿으로 넣고, 그 문자열을 아래 API 에 전달하는 코드가 위반이다.

- `SQLiteDatabase.rawQuery()`·`execSQL()`·`compileStatement()` 의 SQL 문
- `SQLiteDatabase.query()`·`update()`·`delete()`, `ContentResolver.query()`·`update()`·`delete()` 의 selection(`where`) 인수
- Room `SimpleSQLiteQuery(...)` 의 SQL 문, `SupportSQLiteDatabase.query()`·`execSQL()` 의 SQL 문

```kotlin
fun findOrder(email: String, orderNumber: String): Cursor =
    db.rawQuery("SELECT * FROM purchases WHERE email = '$email' AND order_number = '$orderNumber'", null)

fun deleteByName(name: String) {
    db.execSQL("DELETE FROM users WHERE name = '" + name + "'")
}

val cursor = contentResolver.query(
    ContactsContract.Contacts.CONTENT_URI,
    null,
    "${ContactsContract.Contacts.DISPLAY_NAME} = '$query'",
    null,
    null,
)

dao.search(SimpleSQLiteQuery("SELECT * FROM notes WHERE title LIKE '%$keyword%'"))
```

## 수정

```kotlin
fun findOrder(email: String, orderNumber: String): Cursor =
    db.rawQuery(
        "SELECT * FROM purchases WHERE email = ? AND order_number = ?",
        arrayOf(email, orderNumber),
    )

fun deleteByName(name: String) {
    db.execSQL("DELETE FROM users WHERE name = ?", arrayOf(name))
}

val cursor = contentResolver.query(
    ContactsContract.Contacts.CONTENT_URI,
    null,
    "${ContactsContract.Contacts.DISPLAY_NAME} = ?",
    arrayOf(query),
    null,
)

dao.search(SimpleSQLiteQuery("SELECT * FROM notes WHERE title LIKE ?", arrayOf("%$keyword%")))
```

Room DAO 로 바꿀 수 있으면 `@Query("SELECT * FROM notes WHERE title LIKE :pattern")` 처럼 바인딩 파라미터를 쓴다.

## 허용

- 연결하는 값이 모두 컴파일 타임 상수(`const val`, 컬럼명 상수 `ContactsContract.Contacts.DISPLAY_NAME`, 테이블명 상수 등)인 SQL 문. 위 수정 예시처럼 컬럼명 상수와 `?` 만 연결하는 selection 도 해당한다.
- 테이블명·컬럼명·정렬 방향처럼 `?` 로 바인딩할 수 없는 식별자를 코드에 정의한 고정 목록(`enum`, `setOf(...)` 등)에서 선택해 연결하는 경우
- `?` 개수를 맞추기 위해 `List(n) { "?" }.joinToString()` 처럼 플레이스홀더만 생성해 연결하는 경우
- Room `@Query` 애너테이션의 SQL 문 (컴파일 타임에 검증되고 `:name` 파라미터로 바인딩된다)
- 테스트 코드
