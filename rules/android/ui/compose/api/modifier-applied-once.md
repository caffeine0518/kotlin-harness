---
severity: warning
applies_to: "**/*.kt"
source: https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/docs/compose-api-guidelines.md#elements-accept-and-respect-a-modifier-parameter
---

# 전달받은 `modifier` 는 가장 바깥 레이아웃에 한 번, 체인의 처음에 적용한다

## 이유

Compose 가이드라인에 따르면 `modifier` 는 컴포저블의 가장 바깥 레이아웃에 체인의 첫 번째 모디파이어로 한 번 적용한다. 추가 모디파이어는 받은 `modifier` 의 뒤에만 연결할 수 있고, 앞에 연결하면 안 된다(MUST NOT). `modifier` 는 컴포저블 전체의 외부 동작을 지정하는 값이다.

- 자식에 적용하면 호출하는 쪽이 지정한 크기·배경·클릭 영역이 컴포저블 전체가 아니라 일부에만 적용된다.
- 두 곳에 적용하면 `padding`·`clickable` 이 중복 적용된다.
- 앞에 모디파이어를 연결하면(`Modifier.padding(8.dp).then(modifier)`) 호출하는 쪽의 `size`·`background` 가 내부 여백 안쪽에 적용된다.

## 위반

```kotlin
@Composable
fun ProfileCard(name: String, modifier: Modifier = Modifier) {
    Column {
        Text(name, modifier = modifier)  // 가장 바깥 레이아웃이 아니라 자식에 적용
    }
}

@Composable
fun Chip(label: String, modifier: Modifier = Modifier) {
    Row(modifier = modifier) {
        Text(label, modifier = modifier.padding(4.dp))  // 두 번 적용
    }
}

@Composable
fun Tag(label: String, modifier: Modifier = Modifier) {
    Box(Modifier.padding(8.dp).then(modifier)) { Text(label) }  // 앞에 연결
}
```

## 수정

```kotlin
@Composable
fun ProfileCard(name: String, modifier: Modifier = Modifier) {
    Column(modifier = modifier) {
        Text(name)
    }
}

@Composable
fun Chip(label: String, modifier: Modifier = Modifier) {
    Row(modifier = modifier) {
        Text(label, modifier = Modifier.padding(4.dp))
    }
}

@Composable
fun Tag(label: String, modifier: Modifier = Modifier) {
    Box(modifier.padding(8.dp)) { Text(label) }
}
```

## 허용

- `if` 분기마다 다른 레이아웃을 그리고, 각 분기의 가장 바깥 레이아웃에 한 번씩 적용하는 경우
- 받은 `modifier` 를 그대로 다른 컴포저블의 `modifier` 로 전달하는 래퍼 컴포저블
