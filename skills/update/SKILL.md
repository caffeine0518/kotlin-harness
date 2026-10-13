---
name: update
description: kotlin-harness 플러그인을 최신 버전으로 업데이트하고 변경 내역을 보여 준다.
---

# kotlin-harness 업데이트

## 1. 설치된 버전 확인

`claude plugin list --json` 에서 `id` 가 `kotlin-harness@kotlin-harness` 인 항목을 모두 찾는다. 항목마다 `version`, `scope`, `projectPath`(project·local scope 인 경우)를 기록한다. 항목이 없으면 설치 명령을 안내하고 중단한다.

```
/plugin marketplace add caffeine0518/kotlin-harness
/plugin install kotlin-harness@kotlin-harness
```

## 2. 최신 버전 확인

1. `claude plugin marketplace update kotlin-harness` 를 실행한다.
   - 실패하면 업데이트하지 않고 중단한다. 오류 메시지를 출력한다.
2. `claude plugin marketplace list --json` 에서 `name` 이 `kotlin-harness` 인 항목의 `installLocation` 을 찾는다.
3. `<installLocation>/.claude-plugin/plugin.json` 의 `version` 이 최신 버전이다.

모든 항목의 버전이 최신 버전과 같으면 `최신 버전입니다 (x.y.z)` 를 출력하고 5단계의 자동 업데이트 안내만 출력한 뒤 끝낸다.

## 3. 업데이트

버전이 최신이 아닌 항목마다 실행한다.

```
claude plugin update kotlin-harness@kotlin-harness --scope <scope>
```

- `project`·`local` scope 는 그 항목의 `projectPath` 에서 실행한다.
- 실패한 항목은 오류 메시지를 기록하고 나머지 항목을 계속 업데이트한다.

## 4. 변경 내역

`<installLocation>/CHANGELOG.md` 에서 설치돼 있던 버전보다 높고 최신 버전 이하인 섹션을 출력한다. 파일이 없거나 해당 섹션이 없으면 생략한다.

## 5. 결과 출력

```
kotlin-harness 0.4.0 → 0.6.0 (scope: project, /path/to/project)

변경 내역
## 0.6.0
- ...

`/reload-plugins` 를 실행하면 현재 세션에 적용됩니다.
```

마지막에 자동 업데이트 안내를 출력한다.

```
업데이트를 자동으로 받으려면 /plugin → Marketplaces → kotlin-harness → Enable auto-update 를 선택하세요.
```
