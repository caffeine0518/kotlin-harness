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

`null` 의 의미에 따라 고른다.

- 정상적인 경우(값이 없을 수 있다): 기본값, 로컬 `val` 로 받아 `if` 로 분기, 조기 반환
- 버그인 경우: 상태는 `checkNotNull`, 인자는 `requireNotNull`, 필수 키는 `getValue` 로 원인을 남기고 실패한다. 이 예외는 잡아서 처리하지 않는다.
- 판정할 수 없으면 수정하지 않는다. 처리 결과에 `수정하지 않음: null 이 정상적인 경우인지 버그인지 판정할 수 없음` 을 적고, `수정 제안` 에 두 경우의 수정안과 확인할 내용(값을 채우는 위치, 널러블로 선언한 이유)을 적는다.
- 널 체크 뒤의 `!!`: 로컬 `val` 로 받아 스마트 캐스트를 적용한다.

```kotlin
val length = user.nickname?.length ?: 0
val parent = node.parent ?: return

val nickname = user.nickname
if (nickname != null) show(nickname)

val config = checkNotNull(cachedConfig) { "init() 전에 사용했다" }
val id = requireNotNull(args.id) { "id 인자가 필요하다" }
val name = map.getValue("name")
```

## 허용

- 직전 코드가 논널을 보장하지만 컴파일러가 판정하지 못하는 경우. 그 근거를 주석으로 적었으면 위반이 아니다.
- 테스트 코드
