---
name: discovery-brainstorm
description: 경쟁 서비스 분석과 화면 기록을 seed와 대조하여, 사업 기회 목록·가능 영역·추가 조사 항목을 도출한다. discovery-hypothesize(가설 추론)의 입력이 된다.
argument-hint: "[Criteria: <text>]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

EXECUTE IMMEDIATELY — do not deliberate, do not ask clarifying questions before reading the protocol.

## Argument Parsing (do this FIRST)

Extract from $ARGUMENTS:
- `Criteria:` — Critic 공격 기준 오버라이드 (선택)

## Execution

1. Read the brainstorm workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/v1-brainstorm-workflow.md`
2. Read the tone guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tone-guide.md`
3. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
4. Load seed.md + references.md + analysis/ 전부 + screenshots/*/shots.md 전부
   (없으면 → 사용자에게 research·service-recording 먼저 실행 안내 후 중단)
5. Execute: 근거 정합성 체크 → 작업 1(서비스별 질문) → 작업 2(서비스 간 교차 비교) → 작업 3(seed 확장) → 작업 4(추가 조사 항목 식별) → Critic 1회 → 반영·완성 조건 확인
6. Generate brainstorm.md + needs-research.md + handoff.json

IMPORTANT: Start executing immediately. Stream all output live — never run in background.
Next step after completion: `/dk-discovery-bundle:discovery-hypothesize` (Pass: 2로 호출 — 이 단계의 산출물을 재사용한다).
