---
severity: warning
applies_to: "**/*.kt"
source: https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/docs/compose-component-api-guidelines.md#parameters-order
---

# 컴포저블의 마지막 파라미터에는 `@Composable` 이 아닌 람다를 두지 않는다

## 이유

Compose 컴포넌트 API 가이드라인은 파라미터 순서를 필수 파라미터, `modifier`, 선택 파라미터, 트레일링 `@Composable` 람다(주요 콘텐츠) 순으로 정한다. `onClick` 처럼 `@Composable` 이 아닌 람다를 마지막에 두면 호출하는 쪽이 트레일링 람다로 작성할 수 있는데, 사용자는 컴포넌트의 트레일링 람다를 `@Composable` 콘텐츠로 예상하므로 오해를 부른다고 한다. `Chip("태그") { onTagClick() }` 은 클릭 처리인지 콘텐츠인지 호출 코드만으로 구분되지 않는다.

## 위반

UI 를 그리는 `public`·`internal` 컴포저블의 마지막 파라미터가 `@Composable` 이 아닌 함수 타입이다.

```kotlin
@Composable
fun Chip(label: String, modifier: Modifier = Modifier, onClick: () -> Unit) { /* ... */ }

// 호출하는 쪽
Chip("태그") { onTagClick() }
```

## 수정

`@Composable` 콘텐츠 슬롯이 있으면 마지막에 두고, 없으면 콜백을 필수 파라미터로 `modifier` 앞에 둔다.

```kotlin
@Composable
fun Chip(onClick: () -> Unit, modifier: Modifier = Modifier, content: @Composable () -> Unit) { /* ... */ }

@Composable
fun Chip(label: String, onClick: () -> Unit, modifier: Modifier = Modifier) { /* ... */ }
```

## 허용

- `private` 컴포저블
- 이미 널리 호출되는 공개 API 여서 파라미터 순서를 바꾸면 호출하는 쪽을 모두 수정해야 하는 경우. 리포트에만 적고 수정하지 않는다.
