---
name: discovery-sitemap
description: 확정된 기능 목록(ui-spec)을 받아 페이지 트리·페이지별 섹션 목록·페이지 간 이동 표로 이루어진 사이트맵을 만든다. 1층 내비게이션 확정과 전체 확인, 두 번의 유저 확인을 거친다. 유저 흐름과 와이어프레임 단계의 직접 입력. 두 단계가 넘긴 추가 후보로 다시 실행하면 기존 번호를 지키며 바뀐 곳만 고친다.
argument-hint: "[Input: <기능 목록 문서 경로>] [Platform: web | app | both] [Candidates: <user-flow.md 또는 wireframe.md 경로>]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

READ THE PROTOCOL FIRST — 초안 생성과 점검은 스스로 반복하고, 1층 확정과 전체 확인은 유저가 결정한다.

## 전제 조건 (실행 전 확인)

1. **대화형 환경인지 확인한다.** AskUserQuestion 또는 자유 대화가 불가능한 환경이면
   7단계(점검)까지 진행한 초안만 만들고, sitemap.md 상단에 "유저 확인 전 초안"을 표시한 뒤 멈춘다.
   유저 답변을 지어내지 않는다. 이 경우 handoff.json의 next_step은 비워 둔다.
2. 입력 확인:
   - 필수: 기능 목록 문서 — 이 파이프라인에서는 ui-spec/ui-spec.md. `Input:` 인자로 다른 문서를 지정할 수 있다.
     없으면 이전 단계(discovery-ui-spec) 실행을 안내 후 중단.
   - 필수: value-proposal/seed-v2.md — 고객군과 핵심 가치. 없으면 discovery-value-proposal 실행을 안내 후 중단.
   - 선택: research/screenshots/*/shots.md, research/analysis/*.md, hypothesize/hypotheses.md —
     있으면 1층과 섹션 구성의 참고로 쓴다. 없어도 진행 가능.
3. sitemap/sitemap.md가 이미 있는지 확인한다. 있으면 처음 만들기를 하지 않는다 —
   user-flow.md나 wireframe.md의 진행 상태가 "사이트맵 재실행 대기"이거나 `Candidates:`가 있으면 다시 만들기로 가고,
   아니면 유저에게 고칠지 처음부터 할지 묻는다 (워크플로 0단계). 대화형이 아니면 기존 파일을 건드리지 않고 멈춘다.

## Argument Parsing

- `Input:` — 기능 목록 문서 경로 (기본: 현재 run의 ui-spec/ui-spec.md)
- `Candidates:` — 다시 만들기에 쓸 추가 후보 문서 (기본: 진행 상태가 "사이트맵 재실행 대기"인 user-flow.md, wireframe.md를 찾는다)
- `Platform:` — web / app / both (기본: web. seed-v2에 플랫폼이 적혀 있으면 그 값). 웹이면 1층은 상단 메뉴이고 페이지 목록에 URL 경로를 적는다

## Execution

1. Read the workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/v1-sitemap-workflow.md`
2. Read the sitemap guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/sitemap-guide.md`
3. Read the tone guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tone-guide.md` — 산출물 언어 규칙 적용 (페이지 이름·질문 문구 포함)
4. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
5. Look at the reference images: `${CLAUDE_PLUGIN_ROOT}/study/sitemap/` 아래 이미지 전부 (Read 도구로 연다) —
   형식 참고용이다. 무엇을 봐야 하는지는 워크플로의 "참조 레퍼런스"에 있다. 이미지 속 내용을 우리 서비스로 가져오지 않는다.
6. Execute: 재료 읽기·전제 확인 → 기능을 페이지로 묶기 → 페이지 유형 나누기 → 1층 확정(유저 확인 1) → 트리에 매달기 → 페이지별 섹션 목록 → 이동 표 → 완성 조건 점검(미달 시 해당 단계로) → 전체 확인(유저 확인 2)
   다시 만들기: 후보 모으기 → 영향받는 단계만 다시 → 번호 지키기 → 점검과 바뀐 곳 확인(유저 확인) → 되돌려 보내기 (워크플로 "다시 만들기")
7. Generate sitemap/sitemap.md + handoff.json

IMPORTANT: Stream all output live — never run in background.
페이지를 가로지르는 이동은 트리 그림에 그리지 않고 이동 표에만 적는다. 기능 번호는 ui-spec의 번호를 그대로 쓴다.
다시 만들기에서는 기존 페이지·섹션 번호를 다시 매기지 않는다 — 새 것은 다음 번호나 소문자(P4-3a), 없앤 것은 취소선.
Next step after completion: `/dk-discovery-bundle:discovery-user-flow` (유저 흐름). 다시 만들기 뒤에는 `Resume: 6`으로 부르고, 후보가 와이어프레임에서 왔으면 이어서 `/dk-discovery-bundle:discovery-wireframe Resume: 5`.
