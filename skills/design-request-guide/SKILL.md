---
name: design-request-guide
description: 디자인 인계 6단계 각각에 대해 "무엇을 첨부하고, 어떤 문구를 복붙해 보내고, 무엇이 확정되면 다음으로 넘어가는지"를 담은 진행 가이드를 만든다. 기획 산출물의 내용을 채워 실제로 보낼 수 있는 프롬프트로 완성한다.
argument-hint: "[Run: <discovery/{run-id} 경로>] [Refs: <레퍼런스 폴더 경로>]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/cc_design_handoff/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

READ THE PROTOCOL FIRST.

## 전제 조건 (실행 전 확인)

- 같은 run(`Run:`, 기본: 가장 최근 discovery/{run-id})의 기획 문서 다섯 개:
  value-proposal/seed-v2.md, ui-spec/ui-spec.md, sitemap/sitemap.md, user-flow/user-flow.md, wireframe/wireframe.html
  — 없는 문서가 있으면 그 단계 스킬을 먼저 실행하라고 안내 후 중단.
  wireframe.md의 진행 상태가 "전체 확정"이 아니면 discovery-wireframe을 마치라고 안내 후 중단.
- 정합성 검사 결과 (consistency/) — 선택. 없으면 가이드 맨 위에 "정합성 검사를 거치지 않은 기획"이라고 적는다
- 레퍼런스 폴더 (`Refs:`) — 선택. 없으면 2단계 프롬프트에 "레퍼런스 준비 후 진행" 표시

## Execution

1. Read the workflow: `${CLAUDE_PLUGIN_ROOT}/cc_design_handoff/references/v1-request-guide-workflow.md`
2. Read the tone guide: `${CLAUDE_PLUGIN_ROOT}/cc_design_handoff/references/tone-guide.md`
3. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/cc_design_handoff/git/git-verification.md`
4. 기획 문서를 읽고, 워크플로의 프롬프트 틀에 실제 내용(서비스 한 줄, 분위기, 페이지 목록,
   첫 묶음, 컴포넌트 후보, 상태 화면 목록)을 채워 6단계 가이드를 조립한다.
   3단계는 wireframe.html을 첨부해 다듬게 한다 — 디자인 도구에 와이어프레임을 새로 만들게 하지 않는다.
   "조건 미정"·"확인 필요"로 남은 값은 "정해야 할 값" 절에 모은다
5. Generate design_handoff/request-guide.md + handoff.json

IMPORTANT: 프롬프트는 그대로 복사해서 보낼 수 있는 완성문이어야 한다 — {채울 곳}을 남기지 않는다
(레퍼런스처럼 아직 없는 재료만 예외로 표시). 기획에 없는 내용을 지어내지 않는다.
