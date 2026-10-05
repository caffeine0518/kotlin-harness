---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/develop/ui/compose/performance/bestpractices#defer-reads
---

# 스크롤 위치·애니메이션 값은 컴포지션에서 읽지 않고 람다 버전 모디파이어에서 읽는다

## 이유

스크롤 위치나 애니메이션 값은 매 프레임 바뀐다. 이 값을 컴포지션에서 읽어 `Modifier.offset(x, y)`·`Modifier.background(color)` 등에 전달하면 값이 바뀔 때마다 리컴포지션이 발생한다.

`offset { }`·`graphicsLayer { }`·`drawBehind { }` 같은 람다 버전 모디파이어 안에서 읽으면 레이아웃·그리기 단계에서만 읽으므로 컴포지션 단계를 건너뛴다.

## 위반

매 프레임 바뀌는 값을 컴포지션에서 읽어 모디파이어에 전달한다. 예: 스크롤 위치, `animate*AsState` 의 값

```kotlin
@Composable
fun SnackDetail(snack: Snack) {
    val scroll = rememberScrollState(0)
    Title(snack, scroll.value)
}

@Composable
private fun Title(snack: Snack, scroll: Int) {
    val offset = with(LocalDensity.current) { scroll.toDp() }
    Column(Modifier.offset(y = offset)) { /* ... */ }
}

val color by animateColorAsState(if (selected) Color.Cyan else Color.Magenta)
Box(Modifier.fillMaxSize().background(color))

val alpha by animateFloatAsState(if (visible) 1f else 0f)
Box(Modifier.alpha(alpha))
```

## 수정

값 대신 값을 반환하는 람다를 전달하고, 람다 버전 모디파이어 안에서 호출한다.

```kotlin
@Composable
fun SnackDetail(snack: Snack) {
    val scroll = rememberScrollState(0)
    Title(snack) { scroll.value }
}

@Composable
private fun Title(snack: Snack, scrollProvider: () -> Int) {
    Column(Modifier.offset { IntOffset(x = 0, y = scrollProvider()) }) { /* ... */ }
}

Box(Modifier.fillMaxSize().drawBehind { drawRect(color) })
Box(Modifier.graphicsLayer { this.alpha = alpha })
```

## 허용

- 값을 컴포지션에서 사용해야 하는 경우. 예: `Text` 로 표시
- 람다 버전이 없는 모디파이어에 전달하는 경우. 예: `padding`·`size`
- `derivedStateOf` 로 임계값 판정 결과만 읽는 경우
- 드물게 바뀌는 상태. 예: 사용자 입력, 데이터 변경
