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

`null` 이 무엇을 뜻하는지에 따라 고른다.

1. `null` 이 정상적인 경우(값이 없을 수 있다)면, 그때 할 일을 코드로 적는다. 기본값을 쓰거나, 값이 있을 때만 실행하거나, 함수를 끝낸다. 공식 문서는 엘비스 연산자 오른쪽에 `return` 을 쓰는 예를 든다.

```kotlin
val length = user.nickname?.length ?: 0
user.nickname?.let { show(it) }
val parent = node.parent ?: return
```

2. `null` 이면 버그(초기화 순서 오류, 잘못된 인자, 있어야 할 키 누락)라면, 무엇이 없는지 메시지와 함께 실패한다. `!!` 는 메시지 없는 NPE 만 남기지만, 아래 함수는 원인을 메시지와 예외 타입으로 남긴다. 상태는 `checkNotNull`(`IllegalStateException`), 인자는 `requireNotNull`(`IllegalArgumentException`) 로 검증하고, 맵에 반드시 있어야 하는 키는 `getValue`(`NoSuchElementException`, 메시지에 키 포함) 로 조회한다. 이 예외는 호출하는 쪽에서 잡아 처리할 대상이 아니라 버그를 드러내기 위한 것이다.

```kotlin
val config = checkNotNull(cachedConfig) { "init() 을 호출하기 전에 사용했다" }
val id = requireNotNull(args.id) { "id 인자가 필요하다" }
val name = map.getValue("name")
```

`null` 의 의미를 코드에서 판정할 수 없으면 2를 쓴다. `null` 일 때 실패하는 것은 `!!` 와 같고, 예외 타입이 NPE 에서 바뀌고 원인이 메시지로 남는 것만 다르다.

3. 널 체크 뒤의 `!!` 는 값을 로컬 `val` 로 받아 스마트 캐스트를 적용한다.

```kotlin
val nickname = user.nickname
if (nickname != null) show(nickname)
```

## 허용

- 직전 코드가 논널을 보장하지만 컴파일러가 판정하지 못하는 경우. 그 근거를 주석으로 적었으면 위반이 아니다.
- 테스트 코드
