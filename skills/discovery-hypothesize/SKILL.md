---
name: discovery-hypothesize
description: 경쟁 분석에서 "경쟁사가 충족하지 못하는 것"(Pass 1)과 "경쟁사가 잘하고 있어 유저가 실제로 쓰는 것"(Pass 2)을 추출해, 상위 기획 가설(수요)·하위 기획 가설(유저 심리·니즈 조건)·기능 가설 카드(수단) 세 종류의 가설로 정리한다. placement·proposal의 직접 입력.
argument-hint: "[Pass: all | 2] [Criteria: <text>]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

EXECUTE IMMEDIATELY — do not deliberate, do not ask clarifying questions before reading the protocol.

## Argument Parsing (do this FIRST)

Extract from $ARGUMENTS:
- `Pass:` — "all" (Pass 1+2 전체) 또는 "2" (기존 brainstorm.md가 있을 때 Pass 1을 재사용하고 Pass 2 + 압축만 실행).
  파이프라인에서 `discovery-brainstorm` 다음에 실행될 때는 `Pass: 2`가 표준이다.
  brainstorm 산출물이 없을 때만 "all"로 실행한다.
- `Criteria:` — Critic 공격 기준 오버라이드 (선택)

## Execution

1. Read the hypothesize workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/v1-hypothesize-workflow.md`
2. Read the tone guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tone-guide.md`
3. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
4. Load seed.md + references.md + analysis/ 전부 + screenshots/*/shots.md 전부
   (없으면 → 사용자에게 research·service-recording 먼저 실행 안내 후 중단)
5. Execute: 근거 정합성 체크 → Pass 1(경쟁사가 충족하지 못하는 것 찾기) → Pass 2(경쟁사가 잘하고 있어 유저가 실제로 쓰는 것 찾기) → 세 종류 가설로 정리(상위 기획 가설·하위 기획 가설·기능 가설 카드) → Critic 1회 → 반영·완성 조건 확인
6. Generate hypotheses.md + needs-research.md + handoff.json

IMPORTANT: Start executing immediately. Stream all output live — never run in background.
공통 인프라 요소(디자인 완성도, 로그인/권한, 결제 인프라 등)는 니즈로 기록하지 않는다 — 워크플로의 스킵 필터 참조.
