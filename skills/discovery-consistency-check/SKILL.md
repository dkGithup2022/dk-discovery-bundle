---
name: discovery-consistency-check
description: 와이어프레임까지 끝난 기획 문서 전체(seed-v2·ui-spec·sitemap·user-flow·wireframe)를 결정 기록 기준으로 대조해 모순·누락·미결을 찾고, 문제마다 유저에게 처리(고친다/의도한 것/보류)를 받는다. 문서는 고치지 않는다. discovery-consistency-fix와 번갈아 최대 3회차 돈다.
argument-hint: "[Round: <회차 번호>]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

READ THE PROTOCOL FIRST — 대조와 점검은 스스로 반복하고, 문제별 처리는 유저가 정한다. 이 스킬은 입력 문서를 고치지 않는다.

## 전제 조건 (실행 전 확인)

1. 입력 확인 — 없으면 해당 단계를 먼저 실행하라고 안내 후 중단:
   - value-proposal/seed-v2.md, ui-spec/ui-spec.md, sitemap/sitemap.md, user-flow/user-flow.md, wireframe/wireframe.md + wireframe.html
2. 회차 확인: consistency/handoff.json의 tool이 fix면 round + 1, 없으면 1 (check면 워크플로 0단계대로 fix를 먼저 안내).
   4회차 이상이면 실행하지 않는다. 2·3회차는 앞 회차 fix-log.md가 있어야 한다.
3. 대화형 환경인지 확인한다. 불가능한 환경이면 문제 목록까지 만들고 "처리" 칸을 비운 채 "유저 확인 전"으로 표시하고 멈춘다.
   유저 처리를 지어내지 않는다.

## Argument Parsing

- `Round:` — 회차 (기본: consistency/handoff.json에서 다음 회차, 없으면 1)

## Execution

1. Read the workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/v1-consistency-check-workflow.md`
2. Read the check items: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/consistency-check-items.md`
3. Read the format guides: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/sitemap-guide.md`, `user-flow-guide.md`, `wireframe-guide.md` — 전부 읽지 않고 워크플로 "참조 레퍼런스"에 적힌 절만
4. Read the tone guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tone-guide.md`
5. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
6. Execute: 회차 정하기 → 결정 기록 모으기 → 항목별 대조(A~I, 항목마다 스크립트/브라우저/눈. 2·3회차는 수정 검증·수정이 만든 문제·넘김 줄만) → 문제 기록(위치는 섹션 번호까지, 제안이 둘이면 권장 표시) → 완성 조건 점검 → 처리 결정(유저 확인)
7. Generate consistency/round-{N}/findings.md + consistency/handoff.json

IMPORTANT: Stream all output live — never run in background.
판단 기준은 문서의 결정 기록뿐이다 — 이전 세션의 대화는 없다. 대리 확인·초안 결정은 유저 결정으로 쓰지 않는다.
"고친다"가 0건이면 이 스킬이 루프를 끝낸다 — consistency/summary.md와 루프 뒤 유저 확인 목록을 만든다 (워크플로 "루프 마무리").
Next step after completion: 고칠 문제가 있으면 `/dk-discovery-bundle:discovery-consistency-fix`, 없으면 `/dk-discovery-bundle:design-request-guide`.
