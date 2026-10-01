---
severity: error
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/exceptions.html#the-finally-block
---

# `AutoCloseable`·`Closeable` 리소스는 직접 `close()` 를 호출하지 않고 `use()` 로 닫는다

## 이유

`use()` 는 블록이 정상 종료되든 예외로 종료되든 리소스를 닫는다. 공식 문서는 `AutoCloseable` 리소스를 `try`-`finally` 로 닫는 대신 `use()` 를 쓰는 것을 이디오매틱한 방식으로 소개한다. `finally` 없이 `try` 블록 끝에서 `close()` 를 호출하면 예외가 발생했을 때 리소스가 닫히지 않는다.

## 위반

```kotlin
val writer = FileWriter("test.txt")
try {
    writer.write("some text")
} finally {
    writer.close()
}

val reader = BufferedReader(FileReader(path))
val firstLine = reader.readLine()
reader.close()  // readLine() 에서 예외가 발생하면 닫히지 않는다
```

## 수정

```kotlin
FileWriter("test.txt").use { writer ->
    writer.write("some text")
}

val firstLine = BufferedReader(FileReader(path)).use { it.readLine() }
```

## 허용

- 리소스를 생성한 함수가 아닌 다른 곳(예: `onDestroy()`)에서 수명에 맞춰 닫는 경우
- `AutoCloseable`·`Closeable` 을 구현하지 않는 타입
