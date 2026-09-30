---
severity: warning
applies_to: "**/src/{test,androidTest}/**/*.kt"
source: https://developer.android.com/kotlin/flow/test#stateflows
---

# `StateFlow` 는 수집한 값 목록 대신 `value` 프로퍼티로 검증한다

## 이유

Android 공식 문서는 `StateFlow` 를 데이터 홀더로 다루고 `value` 프로퍼티를 검증하라고 권장한다. `StateFlow` 는 값을 합치므로(conflation) 연달아 바뀐 중간 값은 컬렉터가 받지 못할 수 있다. 수집한 값의 개수·순서를 검증하면 결과가 합치기가 일어났는지에 따라 달라지고, `value` 를 검증하면 그 시점의 상태만 확인하므로 합치기와 관계없이 결과가 같다.

## 위반

테스트에서 `StateFlow` 타입 프로퍼티를 `toList`·`collect`·Turbine `test { }` 로 수집하고, 수집한 값의 개수·순서·특정 인덱스를 검증한다.

```kotlin
@Test
fun updatesScore() = runTest {
    val viewModel = MyViewModel(fakeRepository)
    val values = mutableListOf<Int>()
    backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
        viewModel.score.toList(values)
    }

    fakeRepository.emit(1)
    fakeRepository.emit(2)
    assertEquals(listOf(0, 1, 2), values)
}
```

## 수정

```kotlin
@Test
fun updatesScore() = runTest {
    val viewModel = MyViewModel(fakeRepository)
    assertEquals(0, viewModel.score.value)

    fakeRepository.emit(1)
    assertEquals(1, viewModel.score.value)

    fakeRepository.emit(2)
    assertEquals(2, viewModel.score.value)
}
```

`stateIn` 으로 만든 `StateFlow` 는 컬렉터가 있어야 업스트림 수집을 시작하므로, 빈 컬렉터를 `backgroundScope` 에서 시작한 뒤 `value` 를 검증한다.

```kotlin
backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
    viewModel.score.collect {}
}
```

## 허용

- 로딩 상태처럼 `value` 로 확인할 수 없는 중간 상태의 전이 자체가 검증 대상인 경우
- `StateFlow` 가 아닌 Flow 를 수집해 검증하는 경우
