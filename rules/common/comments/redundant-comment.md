---
severity: info
applies_to: "**/*.kt"
source: https://google.github.io/eng-practices/review/reviewer/looking-for.html#comments
---

# 코드가 이미 나타내는 내용을 반복하는 주석을 작성하지 않는다

## 이유

주석은 코드가 왜 있는지 설명할 때 유용하다. 코드가 무엇을 하는지 반복한 주석은 정보를 더하지 않고 화면만 복잡하게 한다. 코드를 반복한 주석은 코드가 바뀔 때 함께 수정되지 않아 틀린 설명이 된다.

판정 기준은 "이 주석을 지우면 잃는 정보가 있는가"다.

## 위반

함수·변수 이름, 연산자, 타입, 호출하는 API 이름이 이미 나타내는 내용을 한국어·영어로 다시 적은 주석.

```kotlin
// 사용자 목록을 불러온다
fun loadUsers(): List<User> = api.users()

// null 이면 빈 리스트를 사용한다
val users = response.users ?: emptyList()

// 카운트를 1 증가시킨다
count++

// 로딩 상태로 변경
_uiState.value = UiState.Loading
```

## 수정

주석을 삭제한다.

```kotlin
fun loadUsers(): List<User> = api.users()

val users = response.users ?: emptyList()
count++
_uiState.value = UiState.Loading
```

## 허용

아래 정보는 코드로 나타낼 수 없으므로 남긴다.

- 이유: 이 방식을 선택한 이유, 더 나은 방식을 쓸 수 없는 제약
- 순서 제약: 순서를 바꾸면 동작이 달라지는 호출
- 우회의 근거: 라이브러리·플랫폼 버그를 우회하는 코드와 관련 이슈 링크
- 값의 근거: 타임아웃·재시도 횟수·크기 같은 상수를 그 값으로 정한 이유
- 관용적이지 않은 코드의 설명, 복사한 코드의 원본 링크
- 이름으로 옮길 수 있는 설명은 이 룰이 아니라 `common/comments/comment-instead-of-name` 이 보고한다.
