---
severity: warning
applies_to: "**/*.kt"
source: https://www.oreilly.com/library/view/clean-code-a/9780136083238/
---

# 구분선·위치 표시 주석으로 코드를 구획하지 않는다

## 이유

Robert C. Martin 의 《Clean Code》 4장은 `// ///////// Actions //////////` 같은 위치 표시(position marker) 주석을 화면만 복잡하게 하는 주석으로 분류한다. 구분선이 많으면 독자는 무시하게 된다. 구획이 필요할 만큼 클래스나 파일이 길어졌다면 주석이 아니라 클래스·파일을 나눈다. 코틀린 코딩 관례의 클래스 멤버 순서를 따르면 구획 주석 없이도 프로퍼티·메서드·companion object 의 위치가 일정하다.

## 위반

`=`·`-`·`*`·`/`·`#` 을 세 개 이상 반복한 구분선이나, 구획 이름만 적은 주석으로 멤버를 나눈다.

```kotlin
class PaymentViewModel : ViewModel() {
    // ===================== 상태 =====================
    private val _uiState = MutableStateFlow(UiState())

    // --------------------- Actions ---------------------
    fun pay() { /* ... */ }

    //region Helpers
    private fun format() { /* ... */ }
    //endregion
}
```

## 수정

구분선을 삭제한다. 구획마다 역할이 다르면 클래스를 나눈다.

```kotlin
class PaymentViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState())

    fun pay() { /* ... */ }

    private fun format() { /* ... */ }
}
```

## 허용

- 자동 생성 코드
- 테스트의 Given·When·Then 처럼 프로젝트가 정한 형식의 단계 구분 주석
