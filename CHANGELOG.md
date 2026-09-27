# Changelog

## 0.7.0
- 위반마다 현재 코드에서 실제로 문제가 발생하는지 판정한다(`실제 문제`·`방어용`·`판정 불가`). 결과는 리포트의 `영향` 에 근거와 함께 적는다.
- 커밋 메시지가 영향 판정을 따른다. 방어용 수정은 현재 동작이 바뀌지 않는다고 적고, `fix` 타입을 쓰지 않는다.
- 검수가 영향 판정과 커밋 메시지의 과장 여부를 확인한다. ([#1](https://github.com/caffeine0518/kotlin-harness/issues/1))

## 0.6.0
- `/kotlin-harness:update` 추가. 플러그인을 최신 버전으로 업데이트하고 변경 내역을 보여 준다.

## 0.5.0
- `/kotlin-harness:issue` 추가. 오탐·누락·잘못된 수정을 이 리포에 GitHub 이슈로 등록한다.
- 검수를 한 번만 실행한다. 검수에서 나온 문제는 반영하고, 다시 검수하지 않는다.

## 0.4.0
- Android 룰 35개 추가: `ui/compose`, `ui/view`, `ui/viewmodel`, `data`, `coroutines`, `security`
- `excludeCategories` 에 하위 경로(`ui/view` 등)를 지정할 수 있다.

## 0.3.0
- 설정 파일 없이 실행할 수 있다. platform 은 `build.gradle(.kts)` 로 자동 판정한다.
- 리포트 디렉터리에 `.gitignore` 를 자동으로 만든다.
- `branch` 범위의 기본 base 를 리포의 기본 브랜치로 변경했다.

## 0.2.0
- GitHub marketplace 로 설치할 수 있다.
- `python3` 가 없으면 훅을 오류 없이 건너뛴다.

## 0.1.0
- `/kotlin-harness:gate`: 룰 기반 리뷰, 위반 수정·커밋, 리포트 작성, 별도 에이전트 검수
- 코틀린 공통 룰 39개: `null-safety`, `immutability`, `exceptions`, `coroutines`, `types`, `scope-functions`, `collections`
