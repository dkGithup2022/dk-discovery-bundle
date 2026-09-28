---
name: discovery-wireframe
description: 확정된 사이트맵의 페이지별 섹션 목록과 유저 흐름의 화면 상태 목록을 받아, 색 없는 저해상도 와이어프레임을 HTML 한 장으로 만든다. 섹션마다 박스와 라벨을 붙이고, 화면 상태별 모양과 흐름마다 화면을 화살표로 잇는 와이어플로까지 그린다. 클로드 디자인 3단계에 첨부해 "이 와이어프레임을 다듬어달라"로 요청하는 입력.
argument-hint: "[Input: <사이트맵 문서 경로>] [Flow: <유저 흐름 문서 경로>] [Resume: <진행 순서 단계 번호>]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

READ THE PROTOCOL FIRST — 와이어프레임 초안 생성과 점검은 스스로 반복하고, 공통 섹션과 첫 묶음 확인과 전체 확인(추가 후보 반영 포함)은 유저가 결정한다.

## 전제 조건 (실행 전 확인)

1. **대화형 환경인지 확인한다.** AskUserQuestion 또는 자유 대화가 불가능한 환경이면
   진행 순서의 9단계(점검)까지 진행한 초안만 만들고, wireframe.md 상단과 wireframe.html 머리(파일 맨 위 `<header>`)에
   "유저 확인 전 초안"을 표시한 뒤 멈춘다.
   공통 섹션과 첫 묶음도 유저가 확정하지 않은 방식 그대로 나머지 페이지를 그린다.
   추가 후보는 목록으로만 남기고 sitemap.md와 user-flow.md는 고치지 않는다.
   진행 상태는 "유저 확인 전 초안"으로 적고, 워크플로 "Commit"의 초안 메시지로 커밋한다.
   유저 답변을 지어내지 않는다. 이 경우 handoff.json의 next_step은 비워 둔다.
2. 입력 확인:
   - 필수: 사이트맵 문서 — 이 파이프라인에서는 sitemap/sitemap.md. `Input:` 인자로 다른 문서를 지정할 수 있다.
     없으면 discovery-sitemap 실행을 안내 후 중단.
     있더라도 문서 상단의 진행 상태가 "전체 확정"이 아니거나 "유저 확인 전 초안" 표시가 있으면,
     discovery-sitemap의 전체 확인을 먼저 마치도록 안내 후 중단. 유저가 확정하지 않은 섹션 목록을 박스로 옮기지 않기 위해서다.
   - 필수: 유저 흐름 문서 — 이 파이프라인에서는 user-flow/user-flow.md. `Flow:` 인자로 다른 문서를 지정할 수 있다.
     화면 상태 목록과 흐름별 그림을 읽는다. 없으면 discovery-user-flow 실행을 안내 후 중단.
     진행 상태가 "전체 확정"이 아니면 중단한다. "사이트맵 재실행 대기"이면 discovery-sitemap 재실행과
     discovery-user-flow `Resume: 6`을 먼저 마치도록, 그 밖의 상태이면 discovery-user-flow의 전체 확인을 먼저 마치도록 안내한다.
     그리지 않은 상태나 흐름이 뒤에 더해지면 와이어프레임을 다시 그려야 하기 때문이다.
   - 선택: research/screenshots/*/shots.md와 같은 폴더의 캡처 — 경쟁사가 같은 성격의 페이지에서 섹션을 어떻게 놓았는지 참고한다.
     없어도 진행 가능.
   - 읽지 않음: ui-spec/ui-spec.md의 전역 분위기. 이 단계는 색을 쓰지 않는다.
3. 이미 wireframe/wireframe.md가 있으면 덮어쓰지 않는다. 진행 상태를 유저에게 보여주고
   이어서 할지(`Resume:`) 처음부터 다시 할지 묻는다. 처음부터 다시 하기로 하면 그때 새로 쓴다
   (이전 내용은 커밋 기록에 남아 있다). `Resume:` 인자를 주고 불렀으면 묻지 않고 그 단계부터 이어간다.
   대화형이 아닌 환경이면 묻지 않고, 기존 파일을 건드리지 않은 채 멈춘다.

## Argument Parsing

- `Input:` — 사이트맵 문서 경로 (기본: 현재 run의 sitemap/sitemap.md).
- `Flow:` — 유저 흐름 문서 경로 (기본: `Input:`으로 준 사이트맵과 같은 run의 user-flow/user-flow.md).
  산출물은 유저 흐름 문서와 같은 run의 wireframe/ 아래에 만든다.
- `Resume:` — 중단했던 진행 순서 단계 번호부터 재개 (기본: 없음. wireframe.md의 진행 상태를 읽어 이어간다).
  진행 상태에 따라 이어가는 단계:
    "첫 묶음 확정" → 5단계(나머지 페이지 그리기)부터
    "사이트맵 재실행 대기" → 사이트맵과 유저 흐름이 다시 "전체 확정"인지 확인한 뒤 5단계부터.
      sitemap.md에서 바뀐 페이지만 다시 그리고, 그 페이지의 상태 화면과 그 페이지가 나오는 와이어플로도 다시 그린다.
      바뀐 페이지를 찾는 법은 워크플로 5단계에 있다
    "유저 확인 전 초안" → 4단계(공통 섹션과 첫 묶음 확인)부터. 초안의 공통 섹션과 첫 묶음을 유저에게 보여주고 확정받는다.
      유저가 그리는 방식을 바꾸면 이미 그린 나머지 페이지, 상태 화면, 와이어플로도 5~7단계에서 같이 고친다
    "전체 확정" → 이어갈 단계가 없다. 고칠 부분이 있는지 유저에게 묻는다
  사이트맵 재실행 뒤 돌아올 때는 `Resume: 5`로 부른다.

## Execution

1. Read the workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/v1-wireframe-workflow.md`
2. Read the wireframe guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/wireframe-guide.md`
3. Read the sitemap guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/sitemap-guide.md` — "번호 규칙"과 "페이지별 섹션 목록" 형식만 확인한다
4. Read the user flow guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/user-flow-guide.md` — "구성 요소"(도형 규칙), "화면 상태", "번호 규칙"만 확인한다
5. Read the tone guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tone-guide.md` — 산출물 언어 규칙 적용 (요소 이름·버튼 이름·동작 주석·질문 문구 포함)
6. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
7. Look at the reference images: `${CLAUDE_PLUGIN_ROOT}/study/wireframe/` 아래 이미지 전부 (Read 도구로 연다) —
   형식 참고용이다. 무엇을 봐야 하는지와 이미지에서 따라 그리지 않을 곳은 워크플로의 "참조 레퍼런스"에 있다.
   이미지 속 페이지 이름, 섹션 구성, 문구를 우리 서비스로 가져오지 않는다.
8. Read the generator guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/tools/wireframe-gen/README.md` —
   HTML은 직접 짜지 않고 이 생성기로 만든다. 에이전트는 그림 데이터(`dsl.py` 등)만 쓰고 `gen.py`·`mdgen.py`를 실행한다.
   본보기 데이터는 `tools/wireframe-gen/example/`에 있다
9. Execute: 재료 읽기·전제 확인 → 그릴 목록과 첫 묶음 정하기 → 공통 섹션 그리기 → 첫 묶음 페이지의 기본 모양 → 공통 섹션과 첫 묶음 확인(유저 확인 1) → 나머지 페이지의 기본 모양 → 상태 화면 → 와이어플로 → 사이트맵·유저 흐름과 대조(추가 후보 모으기) → 완성 조건 점검(미달 시 해당 단계로) → 전체 확인과 추가 후보 반영(유저 확인 2)
10. Generate wireframe/wireframe.html + wireframe/wireframe.md + wireframe/handoff.json (추가 후보를 sitemap.md 갱신으로 반영했으면 sitemap/sitemap.md도)

IMPORTANT: Stream all output live — never run in background.
색은 쓰지 않는다. 박스 하나가 사이트맵 섹션 하나이고, 박스 라벨은 사이트맵의 섹션 번호와 이름(P4-3 행동 버튼)을 그대로 쓴다.
사이트맵에 없는 섹션·요소나 유저 흐름에 없는 화면 상태는 추가 후보로 적고, 유저 확인 전에는 sitemap.md와 user-flow.md를 고치지 않는다.
완성 조건(워크플로 "완성 조건")을 채우지 못한 항목은 강제로 채우지 않고 wireframe.md 상단과 wireframe.html 머리(`<header>`)에 "최소 기준 미달: {항목} — {사유}"로 남긴다.
Next step after completion: `/dk-discovery-bundle:design-references` (디자인 레퍼런스). 현재 run에 design_handoff/references/selection.md가 이미 있으면 `/dk-discovery-bundle:design-request-guide`.
