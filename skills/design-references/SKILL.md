---
name: design-references
description: 서비스의 분위기 선언에 맞는 톤 레퍼런스(닮고 싶은 웹페이지)를 찾아 playwright로 캡처해 로컬에 보관하고(~15곳), 그중 디자인 도구에 보낼 것(~5곳)을 유저와 골라낸다. 디자인 인계 2단계의 재료.
argument-hint: "[Mood: <분위기 문단 또는 문서 경로>] [Add: <유저 추가 후보>]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/cc_design_handoff/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

READ THE PROTOCOL FIRST — 후보 확정과 선별은 유저와의 대화로 진행한다.

## 전제 조건

- 분위기 기준 확인: `Mood:` 인자, 또는 UI 기획 문서의 "전역 분위기" 절.
  없으면 유저에게 물어본다 — 분위기 기준 없이 레퍼런스를 모으지 않는다.
- 대화형 환경 확인: 후보 확정(수집 전)과 선별(수집 후)에 유저 참여가 필요하다.
  비대화형이면 수집(캡처)만 하고 선별은 보류로 기록한다.

## Execution

1. Read the workflow: `${CLAUDE_PLUGIN_ROOT}/cc_design_handoff/references/v1-design-references-workflow.md`
2. Read the capture guide: `${CLAUDE_PLUGIN_ROOT}/cc_design_handoff/references/capture-guide.md`
3. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/cc_design_handoff/git/git-verification.md`
4. Execute: 후보 제안·확정 (대화) → playwright 캡처 (로컬 보관) → 선별 (대화)
5. Generate design_handoff/references/ (캡처 + 색인) + handoff.json 갱신

주의: 여기서 모으는 것은 경쟁사가 아니라 **닮고 싶은 톤**이다 — 기능이 다른 서비스여도
분위기가 맞으면 후보가 된다. 반대로 직접 경쟁사라도 톤이 다르면 후보가 아니다.
