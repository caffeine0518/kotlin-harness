---
severity: error
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/performance/bestpractices#avoid-backwards
---

# 컴포지션에서 읽은 상태를 같은 컴포지션에서 변경하지 않는다

## 이유

컴포저블 본문에서 이미 읽은 `State` 에 값을 쓰는 것을 역방향 쓰기(backwards write)라고 한다. 값이 바뀌면 그 상태를 읽은 컴포저블이 다시 리컴포지션되고, 리컴포지션에서 다시 값을 쓰므로 프레임마다 리컴포지션이 반복된다.

## 위반

```kotlin
@Composable
fun BadComposable() {
    var count by remember { mutableIntStateOf(0) }

    Button(onClick = { count++ }) { Text("Recompose") }
    Text("$count")
    count++
}

@Composable
fun Cart(items: List<Item>) {
    var total by remember { mutableIntStateOf(0) }
    Text("합계: $total")
    total = items.sumOf { it.price }
}
```

## 수정

상태 변경은 `onClick` 등 이벤트 람다에서만 실행한다. 다른 값에서 계산되는 값은 상태로 보관하지 않고 계산 결과를 그대로 사용한다.

```kotlin
@Composable
fun GoodComposable() {
    var count by remember { mutableIntStateOf(0) }

    Button(onClick = { count++ }) { Text("Increment") }
    Text("$count")
}

@Composable
fun Cart(items: List<Item>) {
    val total = remember(items) { items.sumOf { it.price } }
    Text("합계: $total")
}
```

## 허용

- `onClick` 등 이벤트 람다, `LaunchedEffect`·`DisposableEffect` 블록, 콜백 안에서의 쓰기
- `State` 가 아닌 일반 변수(`var`)에 대한 쓰기
