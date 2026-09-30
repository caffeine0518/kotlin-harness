---
severity: warning
applies_to: "**/src/{test,androidTest}/**/*.kt"
source: https://developer.android.com/training/testing/fundamentals/test-doubles#types
---

# Fake 구현이 있는 타입은 mock·stub·spy 대신 Fake 를 쓴다

## 이유

Android 아키텍처 권장사항은 테스트 더블로 mock 보다 Fake 를 쓰라고 강력히 권장한다. 공식 문서에 따르면 Fake 는 mocking 프레임워크가 필요 없고 가벼워서 권장된다. stub 보다도 단순해서 Fake 를 권장하고, spy 는 복잡도를 높이므로 보통 쓰지 않는다. mock 은 정해 둔 호출 방식과 다르면 테스트를 실패시키므로, 동작이 같아도 테스트 대상의 구현이 바뀌면 테스트를 수정해야 한다.

## 위반

테스트 소스 세트에 타입 `T` 를 구현한 `Fake` 로 시작하는 클래스·객체가 있는데, 테스트가 `T` 의 테스트 더블을 아래 방법으로 만든다.

- `mockk<T>()`·`mock<T>()`·`Mockito.mock(T::class.java)`
- `@MockK`·`@Mock` 프로퍼티
- `spyk(...)`·`spy(...)`·`@SpyK`·`@Spy`

```kotlin
// src/test 에 FakeUserRepository : UserRepository 가 있다
@Test
fun loadsFirstUser() {
    val repository = mockk<UserRepository>()
    every { repository.getUsers() } returns listOf(UserAlice, UserBob)

    val viewModel = UsersViewModel(repository)

    assertEquals(UserAlice.name, viewModel.firstUserName)
}
```

## 수정

```kotlin
@Test
fun loadsFirstUser() {
    val viewModel = UsersViewModel(FakeUserRepository)

    assertEquals(UserAlice.name, viewModel.firstUserName)
}
```

## 허용

- 호출 횟수·순서처럼 상호작용 자체를 검증하고, Fake 가 그 정보를 제공하지 않는 경우
- Fake 구현이 없는 타입
