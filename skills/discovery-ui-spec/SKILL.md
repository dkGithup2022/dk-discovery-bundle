---
name: discovery-ui-spec
description: 가치 관점 기획(채택된 가설·기능 목록)을 받아, 두 번의 대화로 서비스 용어와 핵심 기능 → 보조 기능과 전역 분위기를 확정해 ui-spec.md를 만든다. 페이지 구성은 정하지 않는다 — 다음 단계인 사이트맵의 입력. 어떤 서비스 기획에도 쓰는 범용 절차.
argument-hint: "[Input: <기획 문서 경로>] [Resume: <대화 번호>]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

READ THE PROTOCOL FIRST — 이 단계는 유저와의 대화가 본체다. 대화 없이 산출물을 만들지 마라.

## 전제 조건 (실행 전 확인)

1. **대화형 환경인지 확인한다.** AskUserQuestion 또는 자유 대화가 불가능한 환경이면
   즉시 중단하고 "이 단계는 유저 참여가 필요합니다"라고 안내한다. 유저 답변을 지어내지 않는다.
2. 입력 확인:
   - 필수: 채택된 가치·기능이 정리된 기획 문서 — 이 파이프라인에서는
     value-proposal/seed-v2.md. `Input:` 인자로 다른 문서를 지정할 수도 있다.
     없으면 이전 단계(discovery-value-proposal) 실행을 안내 후 중단.
   - 선택: hypothesize/hypotheses.md, 경쟁사 화면 자료 (research/screenshots/*/shots.md) —
     있으면 기능 도출과 분위기 비교의 참조로 쓴다. 없어도 진행 가능.

## Argument Parsing

- `Input:` — 기준 기획 문서 경로 (기본: 현재 run의 value-proposal/seed-v2.md)
- `Resume:` — 중단했던 대화 번호부터 재개 (기본: 1. ui-spec.md의 진행 상태를 읽어 이어간다)

## Execution

1. Read the workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/v1-ui-spec-workflow.md`
2. Read the tone guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tone-guide.md` — 산출물 언어 규칙 적용 (질문 문구 포함)
3. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
4. Execute 대화 1~2 (workflow 참조). 각 대화의 확정 내용을 ui-spec.md에 누적 기록한다.
5. Generate ui-spec/ui-spec.md + handoff.json

IMPORTANT: Stream all output live — never run in background.
페이지 목록과 페이지 배치는 정하지 않는다. 대화 중 나온 페이지 이야기는 "사이트맵 단계로 넘기는 메모"에만 적는다.
Next step after completion: `/dk-discovery-bundle:discovery-sitemap` (사이트맵).
전역 분위기가 확정되었으므로 `/dk-discovery-bundle:design-references` (레퍼런스 수집)는 사이트맵과 따로 지금 돌려도 된다.
