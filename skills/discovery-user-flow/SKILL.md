---
name: discovery-user-flow
description: 확정된 사이트맵을 받아 고객군별 핵심 과업마다 시작부터 목표까지 거치는 화면과 행동의 순서를 흐름도(F1, F2…)로 그린다. 성공 경로와 분기·실패 경로를 모두 그리고, 사이트맵에 없는 화면은 추가 후보로 올리며, 흐름에서 나온 화면 상태 목록을 와이어프레임 단계에 넘긴다.
argument-hint: "[Input: <사이트맵 문서 경로>] [Resume: <진행 순서 단계 번호>]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

READ THE PROTOCOL FIRST — 흐름 초안 생성과 점검은 스스로 반복하고, 흐름 목록 확정과 전체 확인(사이트맵 추가 후보 반영 포함)은 유저가 결정한다.

## 전제 조건 (실행 전 확인)

1. **대화형 환경인지 확인한다.** AskUserQuestion 또는 자유 대화가 불가능한 환경이면
   진행 순서의 8단계(점검)까지 진행한 초안만 만들고, user-flow.md 상단에 "유저 확인 전 초안"을 표시한 뒤 멈춘다.
   흐름 목록도 유저가 확정하지 않은 초안 그대로 쓴다. 사이트맵 추가 후보는 목록으로만 남기고 sitemap.md는 고치지 않는다.
   진행 상태는 "유저 확인 전 초안"으로 적고, 워크플로 "Commit"의 초안 메시지로 커밋한다.
   유저 답변을 지어내지 않는다. 이 경우 handoff.json의 next_step은 비워 둔다.
2. 입력 확인:
   - 필수: 사이트맵 문서 — 이 파이프라인에서는 sitemap/sitemap.md. `Input:` 인자로 다른 문서를 지정할 수 있다.
     없으면 이전 단계(discovery-sitemap) 실행을 안내 후 중단.
     있더라도 문서 상단의 진행 상태가 "전체 확정"이 아니거나 "유저 확인 전 초안" 표시가 있으면,
     discovery-sitemap의 전체 확인을 먼저 마치도록 안내 후 중단. 유저가 확정하지 않은 페이지 번호 위에 흐름을 그리지 않기 위해서다.
   - 필수: ui-spec/ui-spec.md — 기능 목록. 흐름마다 어떤 기능을 다루는지 기능 번호로 적는 데 쓴다.
     없으면 discovery-ui-spec 실행을 안내 후 중단.
   - 필수: value-proposal/seed-v2.md — 고객군과 핵심 가치. 그릴 흐름을 고르는 기준이다.
     없으면 discovery-value-proposal 실행을 안내 후 중단.
   - 선택: research/screenshots/*/shots.md — 경쟁사가 같은 과업을 어떤 화면 순서로 처리하는지 참고한다. 없어도 진행 가능.
3. 이미 user-flow/user-flow.md가 있으면 덮어쓰지 않는다. 진행 상태를 유저에게 보여주고
   이어서 할지(`Resume:`) 처음부터 다시 할지 묻는다. 처음부터 다시 하기로 하면 그때 새로 쓴다
   (이전 내용은 커밋 기록에 남아 있다). `Resume:` 인자를 주고 불렀으면 묻지 않고 그 단계부터 이어간다.
   대화형이 아닌 환경이면 묻지 않고, 기존 파일을 건드리지 않은 채 멈춘다.

## Argument Parsing

- `Input:` — 사이트맵 문서 경로 (기본: 현재 run의 sitemap/sitemap.md).
  기능 목록과 고객군 문서는 같은 run의 ui-spec/ui-spec.md, value-proposal/seed-v2.md에서 읽는다.
- `Resume:` — 중단했던 진행 순서 단계 번호부터 재개 (기본: 없음. user-flow.md의 진행 상태를 읽어 이어간다).
  진행 상태에 따라 이어가는 단계:
    "흐름 목록 확정" → 3단계(성공 경로 그리기)부터
    "사이트맵 재실행 대기" → 사이트맵이 다시 "전체 확정"인지 확인한 뒤 6단계(사이트맵 대조)부터
    "유저 확인 전 초안" → 2단계(흐름 목록 확정)부터. 초안의 흐름 목록을 유저에게 보여주고 확정받는다
    "전체 확정" → 이어갈 단계가 없다. 고칠 부분이 있는지 유저에게 묻는다
  사이트맵 추가 후보를 반영하려고 discovery-sitemap을 다시 돌린 뒤 돌아올 때는 `Resume: 6`으로 부른다.

## Execution

1. Read the workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/v1-user-flow-workflow.md`
2. Read the user flow guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/user-flow-guide.md`
3. Read the sitemap guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/sitemap-guide.md` — "번호 규칙"과 "이동 표" 형식만 확인한다
4. Read the tone guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tone-guide.md` — 산출물 언어 규칙 적용 (흐름 이름·노드 글자·질문 문구 포함)
5. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
6. Look at the reference images: `${CLAUDE_PLUGIN_ROOT}/study/user_flow/` 아래 이미지 전부와 `${CLAUDE_PLUGIN_ROOT}/study/sitemap/yozum_example.png` (Read 도구로 연다) —
   형식 참고용이다. 무엇을 봐야 하는지는 워크플로의 "참조 레퍼런스"에 있다. 이미지 속 화면 이름과 조건 값을 우리 서비스로 가져오지 않는다.
7. Execute: 재료 읽기·전제 확인 → 그릴 흐름 목록 정하기 → 흐름 목록 확정(유저 확인 1) → 흐름마다 성공 경로 → 분기와 실패 경로 → 두 사람이 주고받는 흐름 나누기 → 사이트맵·이동 표와 대조 → 화면 상태 목록 → 완성 조건 점검(미달 시 해당 단계로) → 전체 확인과 사이트맵 추가 후보 반영(유저 확인 2)
8. Generate user-flow/user-flow.md + handoff.json (사이트맵 추가 후보를 sitemap.md 갱신으로 반영했으면 sitemap/sitemap.md와 sitemap/handoff.json도)

IMPORTANT: Stream all output live — never run in background.
흐름의 화면 노드는 사이트맵 페이지 번호를 그대로 쓴다. 사이트맵에 없는 화면은 "(추가 후보) 이름"으로 적고, 유저 확인 전에는 sitemap.md를 고치지 않는다.
완성 조건(워크플로 "완성 조건")을 채우지 못한 항목은 강제로 채우지 않고 user-flow.md 상단에 "최소 기준 미달: {항목} — {사유}"로 남긴다.
Next step after completion: `/dk-discovery-bundle:discovery-wireframe` (와이어프레임).
