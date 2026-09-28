---
severity: warning
applies_to: "**/*.kt"
source: https://kotlinlang.org/docs/coding-conventions.html#names-for-backing-properties
---

# public 프로퍼티와 짝을 이루는 private 백킹 프로퍼티는 이름을 `_` 로 시작한다

## 이유

코틀린 코딩 관례는 개념적으로 같은 두 프로퍼티 중 하나가 public API 이고 다른 하나가 구현 세부 사항이면, private 프로퍼티 이름 앞에 밑줄을 붙이라고 한다. 이름이 `elementList`·`mutableElements` 처럼 다르면 두 프로퍼티가 같은 값이라는 것을 선언을 모두 읽어야 알 수 있다.

## 위반

public 프로퍼티의 게터나 초기화 식이 private 프로퍼티를 그대로 반환·변환(`asStateFlow()`·`asSharedFlow()`·`toList()`)하는데, private 프로퍼티 이름이 `_<public 이름>` 이 아니다.

```kotlin
private val elementList = mutableListOf<Element>()
val elements: List<Element> get() = elementList

private val mutableState = MutableStateFlow(UiState())
val state: StateFlow<UiState> = mutableState.asStateFlow()
```

## 수정

```kotlin
private val _elements = mutableListOf<Element>()
val elements: List<Element> get() = _elements

private val _state = MutableStateFlow(UiState())
val state: StateFlow<UiState> = _state.asStateFlow()
```

## 허용

- 명시적 백킹 필드(explicit backing field, `field = ...`)를 쓰는 경우
- private 프로퍼티를 여러 public 프로퍼티가 조합해 사용하는 경우. 짝을 이루는 프로퍼티가 하나가 아니다.
