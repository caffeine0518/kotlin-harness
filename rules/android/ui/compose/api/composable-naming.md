---
severity: info
applies_to: "**/*.kt"
source: https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/docs/compose-api-guidelines.md#naming-unit-composable-functions-as-entities
---

# `Unit` 을 반환하는 컴포저블은 PascalCase 명사로, 값을 반환하는 컴포저블은 camelCase 로 이름 짓는다

## 이유

`Unit` 을 반환하는 컴포저블은 명령을 실행하는 것이 아니라 UI 에 존재하는 요소를 선언한다. 그래서 이름은 PascalCase 명사로 짓는다. 앞에 형용사를 붙일 수 있지만, 동사·동사구·형용사만으로 된 이름은 쓰지 않는다.

`Unit` 이 아닌 값을 반환하는 컴포저블은 일반 코틀린 함수처럼 camelCase 로 이름 짓는다. 반환 타입과 같은 PascalCase 이름을 쓰는 팩토리 함수 예외는 `@Composable` 함수에 적용하지 않는다.

## 위반

다음 중 하나에 해당한다.

- `Unit` 을 반환하는 컴포저블의 이름이 PascalCase 명사가 아니다.
- 값을 반환하는 컴포저블의 이름이 camelCase 가 아니다.

```kotlin
@Composable
fun RenderFancyButton(text: String, onClick: () -> Unit) { /* ... */ }  // 동사구

@Composable
fun drawProfileImage(image: ImageBitmap) { /* ... */ }  // camelCase

@Composable
fun FooStyle(): Style { /* ... */ }  // 값을 반환하는데 PascalCase
```

## 수정

```kotlin
@Composable
fun FancyButton(text: String, onClick: () -> Unit) { /* ... */ }

@Composable
fun ProfileImage(image: ImageBitmap) { /* ... */ }

@Composable
fun defaultFooStyle(): Style { /* ... */ }
```

## 허용

- 테스트 코드의 `@Test` 메서드
- 이펙트를 실행하는 `Unit` 반환 컴포저블. 예: `LaunchedEffect`·`DisposableEffect`
- 내부에서 `remember` 한 가변 객체를 반환하는 함수의 `remember` 접두사는 `android/ui/compose/api/remember-prefix` 가 보고한다.
