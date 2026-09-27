---
name: discovery-research
description: 유사 서비스 검색 + 분석. seed.md 기반으로 경쟁사를 찾고 각 서비스를 분석한다.
argument-hint: "[Iterations: N]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

EXECUTE IMMEDIATELY — do not deliberate, do not ask clarifying questions before reading the protocol.

## Argument Parsing (do this FIRST)

Extract from $ARGUMENTS:
- `Iterations:` or `--iterations N` — bounded mode (선택)

## Execution

1. Read the research workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/research-workflow.md`
2. Read the tools guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tools-guide.md`
3. Read the analysis elements: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/analysis-elements.md`
4. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
5. Read the loop protocol: `${CLAUDE_PLUGIN_ROOT}/project_discovery/loop/planner-loop-protocol.md` (적용 범위 헤더 참조)
6. Read the results logging: `${CLAUDE_PLUGIN_ROOT}/project_discovery/loop/results-logging.md`
7. Read the tone guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tone-guide.md`
8. Load seed.md (or handoff.json from init)
9. If seed.md not found → AskUserQuestion for idea/customer/value
10. Execute Collect loop → Analyze loop
11. HITL 체크 (대화형 환경 한정 — research-workflow.md의 "HITL 체크" 섹션)
12. Generate references.md + analysis/ + handoff.json

IMPORTANT: Start executing immediately. Stream all output live — never run in background.
You MUST run Bash("sleep 3") between each WebSearch/WebFetch/Playwright call.

Next step after completion: `/dk-discovery-bundle:discovery-service-recording` (서비스 화면 기록).
