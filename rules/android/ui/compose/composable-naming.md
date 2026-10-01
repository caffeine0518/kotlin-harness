---
severity: info
applies_to: "**/*.kt"
source: https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/docs/compose-api-guidelines.md#naming-unit-composable-functions-as-entities
---

# `Unit` 을 반환하는 컴포저블은 PascalCase 명사로, 값을 반환하는 컴포저블은 camelCase 로 이름 짓는다

## 이유

Compose API 가이드라인에 따르면 `Unit` 을 반환하는 `@Composable` 함수는 PascalCase 로 이름 짓고, 이름은 명사여야 한다(MUST). 앞에 형용사를 붙일 수 있지만 동사·동사구·형용사만으로 된 이름은 쓸 수 없다. 이 함수는 명령을 실행하는 것이 아니라 UI 에 존재하는 요소를 선언하기 때문이다.

`Unit` 이 아닌 값을 반환하는 `@Composable` 함수는 일반 코틀린 함수처럼 camelCase 로 이름 짓는다(MUST). 코틀린 코딩 관례의 팩토리 함수 예외(반환 타입과 같은 PascalCase 이름)는 `@Composable` 함수에 적용하지 않는다.

## 위반

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
- `LaunchedEffect`·`DisposableEffect` 처럼 이펙트를 실행하는 `Unit` 반환 컴포저블. 공식 API 도 명사형 이름(`LaunchedEffect`)을 쓴다.
- 내부에서 `remember` 한 가변 객체를 반환하는 함수의 `remember` 접두사는 `android/ui/compose/remember-prefix` 가 보고한다.
