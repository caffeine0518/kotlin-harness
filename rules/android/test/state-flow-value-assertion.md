---
severity: warning
applies_to: "**/src/{test,androidTest}/**/*.kt"
source: https://developer.android.com/kotlin/flow/test#stateflows
---

# `StateFlow` 는 수집한 값 목록 대신 `value` 프로퍼티로 검증한다

## 이유

`StateFlow` 는 값이 연달아 바뀌면 중간 값을 건너뛰고 최신 값만 컬렉터에 전달한다(conflation). 수집한 값의 개수·순서를 검증하면, 결과가 중간 값을 건너뛰었는지에 따라 달라진다.

`value` 는 그 시점의 상태만 확인하므로 결과가 항상 같다.

## 위반

테스트에서 `StateFlow` 를 수집하고, 수집한 값의 개수·순서·특정 인덱스를 검증한다. 수집 방법의 예: `toList`·`collect`·Turbine `test { }`

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

상태를 바꿀 때마다 `value` 를 검증한다.

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

`stateIn(scope, SharingStarted.WhileSubscribed(), ...)` 처럼 컬렉터가 있어야 업스트림 수집을 시작하는 `StateFlow` 는, `backgroundScope` 에서 빈 컬렉터를 시작한 뒤 `value` 를 검증한다.

```kotlin
backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
    viewModel.score.collect {}
}
```

## 허용

- `value` 로 확인할 수 없는 중간 상태의 전이 자체가 검증 대상인 경우. 예: 로딩 상태
- `StateFlow` 가 아닌 Flow 를 수집해 검증하는 경우
