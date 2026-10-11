#!/bin/sh
# PostToolUse 훅: .kt·.kts 파일을 수정하면, 설정의 onWrite 에 지정한 룰만 확인하도록 Claude 에 전달한다.
# python3·jq 없이 실행되도록 JSON 은 sed 로 읽고, onWrite 값의 해석은 Claude 에 맡긴다.

path=$(sed -n 's/.*"file_path" *: *"\([^"]*\)".*/\1/p' | head -n 1)
case "$path" in
  *.kt | *.kts) ;;
  *) exit 0 ;;
esac

config="${CLAUDE_PROJECT_DIR:-.}/.claude/kotlin-harness.json"
grep -q '"onWrite"' "$config" 2>/dev/null || exit 0

msg="kotlin-harness: \`$path\` 를 수정했습니다. \`$config\` 의 \`onWrite\` 에 지정한 룰만 확인하세요. 값은 룰 ID(\`common/null-safety/not-null-assertion\`) 또는 카테고리 경로(\`common/null-safety\`)이고, 룰 파일은 \`${CLAUDE_PLUGIN_ROOT}/rules/\` 아래에 있습니다. 이번 변경이 그 룰을 위반하면 룰의 \`## 수정\` 대로 수정하세요. 없는 룰 ID·카테고리가 있으면 사용자에게 알리세요."

printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"%s"}}\n' \
  "$(printf '%s' "$msg" | sed 's/\\/\\\\/g; s/"/\\"/g')"
