---
severity: warning
applies_to: "**/*.kt"
source: https://developer.android.com/guide/topics/resources/localization#manage-strings-for-localization
---

# 화면에 표시하는 문구는 코드에 리터럴로 작성하지 않고 문자열 리소스로 선언한다

## 이유

공식 문서는 문자열을 하드코딩하지 말고 기본 `strings.xml` 에 리소스로 선언하라고 한다. 리소스로 선언하면 컴파일된 코드를 바꾸지 않고 문구를 추출·번역·수정할 수 있다. Android Lint 의 `HardcodedText` 는 레이아웃 XML 만 검사하므로, 컴포저블과 코드에서 설정한 문구는 검출하지 않는다.

문구를 문자열 템플릿이나 `+` 로 조립하는 것도 같은 문제다. 조각마다 리터럴이 코드에 남고, 언어마다 어순이 달라 조각을 따로 번역할 수 없다. 자리 표시자를 포함한 리소스 하나로 선언하고 인수를 전달한다.

## 위반

`Text`·`Button` 등 컴포저블의 문구 파라미터, `TextView.text`·`setText()`·`Toast.makeText()`·`Snackbar.make()`·`setTitle()`·`setMessage()`·`NotificationCompat.Builder.setContentTitle()`·`setContentText()` 에 사람이 읽는 문장·단어를 리터럴이나 템플릿으로 전달한다.

```kotlin
Text(text = "확인")
Text(text = "안녕하세요, ${name}님")
Toast.makeText(context, "저장했습니다", Toast.LENGTH_SHORT).show()
binding.title.text = "총 " + count + "개"
```

## 수정

```kotlin
// <string name="confirm">확인</string>
// <string name="greeting">안녕하세요, %1$s님</string>
Text(text = stringResource(R.string.confirm))
Text(text = stringResource(R.string.greeting, name))
Toast.makeText(context, R.string.saved, Toast.LENGTH_SHORT).show()
```

## 허용

- 로그 메시지, 분석 이벤트 이름, 인텐트 extra 키, 테스트 태그 등 사용자에게 보이지 않는 문자열
- 숫자·기호만 있거나(`"%"`, `"·"`), 서버·사용자가 입력한 값을 그대로 표시하는 경우
- `@Preview` 함수와 테스트 코드
- 앱 이름·브랜드명처럼 번역하지 않는 고유명사. 리소스로 선언할지 판단이 필요하므로 리포트에 판정 불가로 적는다.
- 개수에 따라 문구를 분기하는 코드는 `android/ui/strings/plurals` 가 보고한다.
