---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/properties.html#backing-properties
---

# 클래스 안에서 변경하는 컬렉션은 private 가변 프로퍼티로 두고 public 에는 읽기 전용 타입으로 노출한다

## 이유

`MutableList`·`MutableMap` 같은 가변 타입을 public 프로퍼티로 노출하면, 클래스 밖의 코드가 클래스의 메서드를 거치지 않고 요소를 추가·삭제할 수 있어 클래스가 상태 변경을 통제하지 못한다. 공식 문서는 실제 컬렉션을 `_` 로 시작하는 private 백킹 프로퍼티로 두고, public 프로퍼티는 읽기 전용 타입으로 선언하는 방식을 소개한다.

## 위반

```kotlin
class UserDirectory {
    val users = mutableListOf<String>()  // 타입이 MutableList<String> 으로 노출됨

    fun addUser(username: String) {
        users.add(username)
    }
}

// 호출하는 쪽에서 addUser 를 거치지 않고 변경할 수 있다
directory.users.clear()
```

## 수정

```kotlin
class UserDirectory {
    private val _users = mutableListOf<String>()
    val users: List<String> get() = _users

    fun addUser(username: String) {
        _users.add(username)
    }
}
```

public 프로퍼티가 반환하는 값은 `_users` 와 같은 객체의 읽기 전용 참조다. 이후 변경이 그대로 반영되고, 호출하는 쪽이 `MutableList` 로 캐스트하면 변경할 수도 있다. 시점의 스냅샷이 필요하면 `get() = _users.toList()` 로 복사해 반환한다.

## 허용

- `private` 프로퍼티와 로컬 변수
- 명시적 백킹 필드(explicit backing field) `val items: List<String>` + `field = mutableListOf()` 로 선언한 경우. 외부에는 이미 읽기 전용 타입으로 노출된다.
- 호출하는 쪽이 컬렉션을 직접 변경하는 것이 클래스의 의도인 경우(빌더, 설정 객체 등)
