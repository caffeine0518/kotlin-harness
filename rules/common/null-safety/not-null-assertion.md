---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/null-safety.html#not-null-assertion-operator
---

# 널이 될 수 있는 값에 `!!` 를 쓰지 않는다

## 이유

값이 `null` 이면 `!!` 에서 NPE 가 발생한다. 공식 문서는 `!!` 를 NPE 의 원인 중 하나로 들고, 값이 `null` 이 아님을 확신하지만 컴파일러가 보장하지 못하는 경우에만 쓰라고 한다.

## 위반

```kotlin
val name = map["name"]!!
val length = user.nickname!!.length
```

널 체크 뒤에 `!!` 를 쓰는 경우도 위반이다. 체크 대상이 `var` 프로퍼티면 체크와 사용 사이에 값이 바뀔 수 있어 스마트 캐스트가 적용되지 않는다.

```kotlin
if (user.nickname != null) {
    show(user.nickname!!)
}
```

## 수정

```kotlin
val name = map["name"] ?: throw IllegalStateException("name is missing")
val length = user.nickname?.length ?: 0

user.nickname?.let { show(it) }
// 또는 로컬 val 로 받아 스마트 캐스트를 적용한다
val nickname = user.nickname
if (nickname != null) show(nickname)
```

## 허용

- 직전 코드가 논널을 보장하지만 컴파일러가 판정하지 못하는 경우. 그 근거를 주석으로 적었으면 위반이 아니다.
- 테스트 코드
