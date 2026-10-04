---
severity: warning
applies_to: "**/src/{test,androidTest}/**/*.kt"
source: https://developer.android.com/training/testing/fundamentals/test-doubles#types
---

# Fake 구현이 있는 타입은 mock·stub·spy 대신 Fake 를 쓴다

## 이유

Fake 는 실제 구현처럼 동작하는 가벼운 구현이라 mocking 프레임워크가 필요 없다. 다른 테스트 더블에는 다음 문제가 있다.

- mock: 정해 둔 호출 방식과 다르면 테스트가 실패한다. 동작이 같아도 테스트 대상의 구현이 바뀌면 테스트를 수정해야 한다.
- stub: 테스트마다 반환값을 정해야 해서 Fake 보다 복잡하다.
- spy: 실제 객체와 정해 둔 동작이 섞여 테스트가 복잡해진다.

## 위반

Fake 구현이 있는 타입의 테스트 더블을 mocking 라이브러리로 만든다. Fake 구현은 테스트 소스 세트에서 그 타입을 구현하고, 이름이 `Fake` 로 시작하는 클래스·객체다. 예:

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

mocking 라이브러리로 만든 테스트 더블을 Fake 구현으로 바꾼다.

```kotlin
@Test
fun loadsFirstUser() {
    val viewModel = UsersViewModel(FakeUserRepository)

    assertEquals(UserAlice.name, viewModel.firstUserName)
}
```

## 허용

- 상호작용 자체를 검증하는데 Fake 가 그 정보를 제공하지 않는 경우. 예: 호출 횟수·순서
- Fake 구현이 없는 타입
