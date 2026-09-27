---
name: discovery-init
description: 기획서 초기 입력 수집. 아이디어/고객/가치를 받아 seed.md를 생성한다.
argument-hint: "[Idea: <text>] [Customer: <text>] [Value: <text>] [Extras: <text>]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

EXECUTE IMMEDIATELY — do not deliberate, do not ask clarifying questions before reading the protocol.

## Argument Parsing (do this FIRST)

Extract these from $ARGUMENTS:

- `Idea:` — 아이디어 설명 (필수)
- `Customer:` — 핵심 고객 (필수)
- `Value:` — 제공 가치 (필수)
- `Extras:` — 추가 정보 (선택)

If all 3 required fields are extracted → skip AskUserQuestion, proceed to execution.
If any required field is missing → AskUserQuestion per init-workflow.md.
If required fields are missing AND the environment cannot ask the user (non-interactive):
  STOP with a clear message listing the missing fields — never invent them.

## Execution

1. Read the init workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/init-workflow.md`
2. Read git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
3. If any required field missing → AskUserQuestion (4 questions, 1 batch)
4. Generate seed.md (init-workflow.md 템플릿 따름)
5. Extract search keywords → generate handoff.json
6. git add {출력 디렉토리}/init/seed.md {출력 디렉토리}/init/handoff.json (경로는 git/git-verification.md의 커밋 규칙 참조)
7. git commit -m "discovery(init): seed — {idea 한줄 요약}"

IMPORTANT: Start executing immediately. Stream all output live — never run in background.
