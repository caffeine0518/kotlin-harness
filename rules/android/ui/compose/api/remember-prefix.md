---
severity: info
applies_to: "**/*.kt"
source: https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/docs/compose-api-guidelines.md#naming-composable-functions-that-remember-the-objects-they-return
---

# 내부에서 `remember` 한 가변 객체를 반환하는 컴포저블은 이름을 `remember` 로 시작한다

## 이유

`remember` 로 시작하는 이름을 보면, 반환된 객체가 리컴포지션 사이에 유지된다는 것을 알 수 있다. `createScrollState()` 처럼 이름을 지으면 호출하는 쪽이 동작을 잘못 예상한다.

- 매번 새 객체가 생성된다고 생각해 다시 `remember` 로 감싼다.
- 반대로 `remember` 가 없는 일반 팩토리를 같은 방식으로 이름 지으면, 컴포저블 안에서 그대로 호출해 리컴포지션마다 상태를 잃는다.

## 위반

내부에서 `remember` 한 가변 객체를 반환하는 컴포저블의 이름이 `remember` 로 시작하지 않는다.

```kotlin
@Composable
fun createSearchState(): SearchState {
    return remember { SearchState() }
}

@Composable
fun scrollState(): ScrollState = remember { ScrollState(0) }
```

## 수정

```kotlin
@Composable
fun rememberSearchState(): SearchState {
    return remember { SearchState() }
}

@Composable
fun rememberScrollState(): ScrollState = remember { ScrollState(0) }
```

## 허용

- `remember` 하지 않고 매번 새 객체를 반환하는 함수
- 불변 값을 반환하는 함수
