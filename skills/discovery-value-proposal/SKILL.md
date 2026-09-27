---
name: discovery-value-proposal
description: 가설 재료를 유저와 함께 열람·채택하는 대화를 거쳐, 원본 seed의 상세판(Seed v2 — 가치 관점 기획)을 만든다. 이 단계는 대화형이 본체다.
argument-hint: "[Rounds: N]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

READ THE PROTOCOL FIRST — 이 단계는 유저와의 대화가 본체다. 대화 없이 산출물을 만들지 마라.

## 전제 조건 (실행 전 확인)

1. **대화형 환경인지 확인한다.** AskUserQuestion을 쓸 수 없는 환경(서브에이전트 등)이면
   즉시 중단하고 "이 단계는 유저 참여가 필요합니다"라고 안내한다. 유저 답변을 지어내는 것은 금지.
2. 입력 파일 확인 — 없으면 해당 단계를 먼저 실행하라고 안내 후 중단:
   - init/seed.md
   - research/references.md + analysis/
   - research/screenshots/*/shots.md (없어도 진행 가능하나 열람 자료가 약해짐을 안내)
   - hypothesize/hypotheses.md + needs-research.md

## Argument Parsing

- `Rounds:` — 채택 대화 질문 라운드 수 (기본 2)

## Execution

1. Read the workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/v1-value-proposal-workflow.md`
2. Read the tone guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tone-guide.md` — 특히 "산출물 언어 규칙" (이 단계의 산출물은 전부 사람이 읽는다)
3. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
4. Execute: 열람 자료 제시 → 채택 대화 (질문 라운드) → Seed v2 생성 → 열람 자료에 결정 반영
5. Generate value-proposal/seed-v2.md + handoff.json
