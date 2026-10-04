# dk-discovery-bundle

서비스 아이디어 한 줄에서 시작해 경쟁 조사, 가설, 가치 기획을 거쳐 사이트맵·유저 흐름·와이어프레임까지 만들고, 클로드 디자인에 넘길 레퍼런스와 진행 가이드까지 만드는 Claude Code 플러그인이다.
기획 단계 12개(정합성 검사·수정 포함)와 디자인 인계 단계 2개, 모두 14개의 스킬이 들어 있다.

## 전체 흐름

`◆`는 유저 확인 지점이다. 단계마다 산출물이 `discovery/{run-id}/` 아래에 쌓이고 커밋 하나를 남긴다.

```
 ┌──────────────────────────── 기획: 무엇을 만들까 ────────────────────────────┐
 │                                                                              │
 │  ① init ──▶ ② research ──▶ ③ service-recording ──▶ ④ brainstorm             │
 │   seed.md     ◆ 대상 확인     screenshots/ + shots.md    brainstorm.md         │
 │                analysis/*.md                                │                │
 │                                                             ▼                │
 │              ⑥ value-proposal ◀────────────────────── ⑤ hypothesize          │
 │                seed-v2.md (고객군·핵심 가치)              hypotheses.md        │
 │                    │                                                         │
 └────────────────────┼─────────────────────────────────────────────────────────┘
                      ▼
 ┌──────────────────────────── 화면 구조: 어떻게 보일까 ───────────────────────┐
 │                                                                              │
 │  ⑦ ui-spec  ── 대화 1·2만 ──  ◆ 용어·기능 확정   ◆ 전역 분위기               │
 │     ui-spec.md (기능 번호 · 전역 분위기)                                     │
 │        │                                         │                           │
 │        │                                         └───────────────┐           │
 │        ▼                                                         │           │
 │  ⑧ sitemap   ◆ 1층 메뉴 확정   ◆ 전체 확인                       │           │
 │     sitemap.md (페이지 트리 · 섹션 목록 · 이동 표)               │           │
 │        │    ▲                    ▲                               │           │
 │        │    │ 추가 후보 (화면)   │ 추가 후보 (섹션·요소)         │           │
 │        │    │ ※ 기존 번호 유지   │ ※ 기존 번호 유지              │           │
 │        ▼    │                    │                               │           │
 │  ⑨ user-flow ─┘                  │                               │           │
 │     ◆ 흐름 목록 확정  ◆ 전체 확인│                               │           │
 │     user-flow.md (F1… 흐름도 · 화면 상태 목록)                   │           │
 │        │                         │                               │           │
 │        ▼                         │                               │           │
 │  ⑩ wireframe ────────────────────┘                               │           │
 │     ◆ 공통 섹션·첫 묶음 확인  ◆ 전체 확인                        │           │
 │     wireframe.html (gen.py 생성) + wireframe.md                  │           │
 │        │                                                         │           │
 │        ▼                                                         │           │
 │  ┌─ 정합성 루프 (최대 3회차) ──────────────────────┐             │           │
 │  │                                                 │             │           │
 │  │  consistency-check ──▶ ◆ 문제마다 처리 결정      │             │           │
 │  │    findings.md          (고친다/의도/보류)       │             │           │
 │  │        ▲                    │                   │             │           │
 │  │        │ 다음 회차          ▼ 고칠 것 있음       │             │           │
 │  │        └──────────── consistency-fix            │             │           │
 │  │                        fix-log.md               │             │           │
 │  │                        (seed-v2→ui-spec→sitemap │             │           │
 │  │                         →user-flow→wireframe 순)│             │           │
 │  └──────────────┬──────────────────────────────────┘             │           │
 │                 │ 고칠 것 없음 / 3회차 끝                        │           │
 └─────────────────┼────────────────────────────────────────────────┼───────────┘
                   │                                                │
                   │                  ⑦만 끝나면 따로 돌 수 있음 ───┘
                   │                                    ▼
 ┌─────────────────┼──────────── 디자인 인계 ─────────────────────────────────┐
 │                 │                       ⑪ design-references                 │
 │                 │                          ◆ 레퍼런스 5곳 선별               │
 │                 │                          selection.md + 캡처              │
 │                 ▼                                  │                        │
 │  ⑫ design-request-guide ◀──────────────────────────┘                        │
 │     request-guide.md (클로드 디자인 6단계 복붙 가이드)                      │
 │     첨부: seed-v2 · ui-spec · sitemap · user-flow · wireframe.html · 레퍼런스│
 └────────────────────┬────────────────────────────────────────────────────────┘
                      ▼
 ┌──────────────────────── 클로드 디자인 (웹, 사람이 진행) ────────────────────┐
 │  ① 이해 확인 → ② 톤 → ③ wireframe.html 다듬기 → ④ 색 → ⑤ Tailwind 테마·  │
 │  공통 컴포넌트 → ⑥ 페이지별 시안                                           │
 └────────────────────┬────────────────────────────────────────────────────────┘
                      ▼
               FE 트랙 (dk-fe-bundle)
```

- ⑧ ← ⑨·⑩: 유저 흐름이나 와이어프레임에서 사이트맵에 없는 화면·섹션이 나오면 추가 후보로 올린다. 작은 변경은 sitemap.md에 바로 더하고, 1층·부모·섹션 순서가 바뀌는 변경은 sitemap을 다시 실행한다. 다시 실행해도 기존 페이지·섹션 번호는 바뀌지 않는다.
- ⑪은 ⑦의 전역 분위기만 있으면 되므로 ⑧~⑩과 따로 돌려도 된다.


## 설치

```
/plugin marketplace add https://github.com/dkGithup2022/dk-discovery-bundle.git
/plugin install dk-discovery-bundle@dk-discovery-bundle
```

설치하면 `/dk-discovery-bundle:discovery-init`처럼 호출한다. 스킬 목록은 아래 "스킬 목록" 표에 있다.

필요한 도구:
- WebSearch, WebFetch — 경쟁 서비스 조사 (`discovery-init`, `discovery-research`)
- Playwright MCP — 화면 캡처 (`discovery-service-recording`, `design-references`)
- python3 — 와이어프레임 HTML 생성 (`discovery-wireframe`)
- git — 단계마다 산출물을 커밋한다. 작업하는 프로젝트가 git 저장소여야 한다.

## 폴더 구성

| 폴더 | 내용 |
|---|---|
| `skills/` | 스킬 14개의 진입점 (`SKILL.md`) |
| `project_discovery/` | 기획 스킬들이 읽는 문서 — 단계별 워크플로, 사이트맵·유저 흐름·와이어프레임 가이드, 문체 규칙, 도구 사용법, git 규칙, 조사 반복 규칙 |
| `project_discovery/tools/wireframe-gen/` | 와이어프레임 HTML 생성기와 본보기 (웹 `example-web/`, 앱 `example/`) |
| `study/` | 사이트맵·유저 흐름·와이어프레임 스킬이 형식 참고로 보는 이미지 |
| `docs/` | 사이트맵·유저 흐름·와이어프레임 단계 추가 계획과 스킬 검사 기록 |
| `cc_design_handoff/` | 디자인 인계 스킬들이 읽는 문서 — 워크플로, 캡처 규칙, 문체 규칙, git 규칙 |
| `examples/` | 단계마다 실제 실행에서 무엇이 들어가고 무엇이 나왔는지 발췌한 문서 |

## 스킬 목록

| # | 스킬 | 하는 일 | 유저 참여 | 실행 예시 |
|---|---|---|---|---|
| 1 | `discovery-init` | 아이디어·고객·가치로 출발점 문서(seed.md) 만들기 | 입력 + 방향 질문 | [보기](examples/discovery-init/input-output.md) |
| 2 | `discovery-research` | 경쟁 서비스 찾고 분석하기 | 끝에 확인 1번 | [보기](examples/discovery-research/input-output.md) |
| 3 | `discovery-service-recording` | 경쟁 서비스 화면 캡처하기 | 없음 | [보기](examples/discovery-service-recording/input-output.md) |
| 4 | `discovery-brainstorm` | 사업 기회와 가능한 영역 찾기 | 없음 | [보기](examples/discovery-brainstorm/input-output.md) |
| 5 | `discovery-hypothesize` | 세 종류 가설 세우기 (`Pass: 2`로 실행) | 없음 | [보기](examples/discovery-hypothesize/input-output.md) |
| 6 | `discovery-value-proposal` | 가설을 보고 채택할 것 정하기 (seed-v2.md) | 결정 대화 | [보기](examples/discovery-value-proposal/input-output.md) |
| 7 | `discovery-ui-spec` | 용어·기능 목록·전역 분위기 확정 (ui-spec.md) | 대화 2번 | [보기](examples/discovery-ui-spec/input-output.md) (이전 버전) |
| 8 | `discovery-sitemap` | 페이지 트리·섹션 목록·이동 표 (sitemap.md) | 1층 확정 + 전체 확인 | 본보기: [example-web](project_discovery/tools/wireframe-gen/example-web/sitemap/sitemap.md) |
| 9 | `discovery-user-flow` | 과업별 흐름도와 화면 상태 목록 (user-flow.md) | 흐름 목록 확정 + 전체 확인 | 본보기: [example-web](project_discovery/tools/wireframe-gen/example-web/user-flow/user-flow.md) |
| 10 | `discovery-wireframe` | 색 없는 와이어프레임·와이어플로 (wireframe.html) | 첫 묶음 확인 + 전체 확인 | 본보기: [example-web](project_discovery/tools/wireframe-gen/example-web/wireframe/wireframe.md) |
| — | `discovery-consistency-check` | 기획 문서 전체에서 모순·누락·미결 찾기 (findings.md) | 문제마다 처리 결정 | — |
| — | `discovery-consistency-fix` | "고친다"로 정한 문제만 앞 문서에 반영 (fix-log.md) | 없음 | — |
| 11 | `design-references` | 톤 레퍼런스 캡처하고 보낼 곳 고르기 | 후보 확정 + 선별 | [보기](examples/design-references/input-output.md) |
| 12 | `design-request-guide` | 클로드 디자인 6단계 진행 가이드 만들기 | 없음 | [보기](examples/design-request-guide/input-output.md) (이전 버전) |

1~7, 11, 12의 실행 예시는 "크루 매거진 커뮤니티 앱" 아이디어로 한 번 끝까지 돌린 결과에서 발췌했다. "이전 버전"은 사이트맵·유저 흐름·와이어프레임 단계가 생기기 전에 실행한 기록이다.
8~10은 와이어프레임 생성기 폴더의 웹 본보기를 참고한다. 정합성 검사·수정은 아직 초안이다.

모든 산출물은 **작업 중인 프로젝트**에서 실행 한 번마다 `discovery/{날짜-시각-서비스이름}/` 아래에 단계별 폴더로 쌓인다.
각 단계는 끝날 때 git 커밋 하나를 남긴다. 기획 단계는 `discovery(...)`, 디자인 단계는 `design(...)`로 시작한다.
각 단계의 `handoff.json`에는 다음에 실행할 단계(`next_step`)가 적혀 있다.

---

## 단계별 설명

### A. 기획

**1. discovery-init — 출발점 문서 만들기**
- 아이디어, 핵심 고객, 제공 가치를 받는다. 빠진 게 있으면 물어본다.
- 웹에서 비슷한 서비스를 간단히 찾아 "이런 것들이 있다"고 보여 준다. 이 결과는 seed에 넣지 않는다.
- 그걸 본 유저에게 방향, 시장에 대한 느낌, 수익 모델, 꼭 하고 싶은 것을 묻는다. 모두 비워 둬도 된다.
- 산출물: `init/seed.md`, 다음 단계에서 쓸 검색 키워드

**2. discovery-research — 경쟁 서비스 찾고 분석하기**
- 수집 반복: 직접 경쟁사 3개 이상, 간접 경쟁사 2개 이상이 모일 때까지 검색한다. 검색은 최대 20번이다.
- 분석 반복: 서비스를 하나씩 정해진 7개 항목으로 분석한다. 부족하면 서비스당 3번까지 보강한다.
- 끝나면 유저 확인을 한 번 받는다. 빠진 서비스는 없는지, 가격이나 수익 모델 정보가 맞는지, 아는 것이 있는지를 묻는다.
- 산출물: `references.md`(경쟁사를 직접·간접·다른 접근으로 나눈 목록), `analysis/{서비스}.md`

**3. discovery-service-recording — 경쟁 서비스 화면 캡처하기**
- 서비스마다 먼저 웹으로 볼 수 있는지 확인한다. 앱에서만 되거나 가입해야 볼 수 있으면 기록만 하고 넘어간다.
- 볼 수 있으면 첫 화면, 처음 들어가는 화면 등 기본 3장을 찍고, 더 둘러봐야 할 화면을 정해서 추가로 찍는다. 서비스당 최대 8장이다.
- 산출물: `screenshots/{서비스}/`, 각 캡처가 무엇을 보여 주는지 적은 `shots.md`

**4. discovery-brainstorm — 기회 찾기** (자동)
- seed를 경쟁 분석, 화면 기록과 비교한다. 서비스별로 보고, 여러 서비스를 한꺼번에 비교하고, 우리 아이디어에서 출발해 넓혀 본다.
- 반박 검토(Critic)를 한 번 거쳐 보완한다.
- 산출물: `brainstorm.md`(사업 기회와 가능한 영역), `needs-research.md`(추가로 조사할 항목)

**5. discovery-hypothesize — 가설 세우기** (자동, `Pass: 2`로 실행)
- 경쟁사가 채우지 못한 것(Pass 1)은 4단계 결과를 그대로 다시 쓴다.
- 경쟁사가 잘해서 유저가 실제로 쓰는 것(Pass 2)을 새로 찾는다. 로그인이나 결제처럼 어느 서비스에나 있는 기반 기능은 뺀다.
- 가설을 세 종류로 정리한다.
  - 상위 가설 1~3개: 어떤 수요가 있는가
  - 하위 가설 3~7개: 유저가 어떤 심리와 조건에서 움직이는가
  - 기능 카드 7개 이상: 그 수요를 어떤 기능으로 채울 것인가
- 반박 검토를 한 번 거치고, 가설마다 추가 조사가 필요한지 판정한다.
- 산출물: `hypotheses.md`, `needs-research.md`

**6. discovery-value-proposal — 무엇을 채택할지 정하기** (대화)
- 시드, 경쟁사, 가설, 아직 확인 안 된 가정을 한눈에 볼 수 있는 페이지를 만들어 보여 준다.
- 유저가 다 봤다고 하면 질문으로 결정을 받는다. 기본 2라운드, 라운드당 최대 4문항이다.
- 산출물: `seed-v2.md`. 처음 seed를 자세하게 만든 판으로, 고객 세그먼트, 핵심 가치, 기본으로 있어야 하는 기능, 채택하지 않은 것과 그 이유, 남은 확인 과제가 들어간다.

**7. discovery-ui-spec — 용어·기능·분위기 확정** (대화 2번)
- 대화 1: 서비스 용어를 먼저 정하고, 핵심 기능을 유저 행동 수준으로 나열한다 (번호 1~N).
- 대화 2: 핵심 기능을 받쳐 주는 보조 기능을 나열하고 (번호 s1~sN), 전역 분위기를 한 문단으로 정한다.
- 페이지는 여기서 정하지 않는다. 산출물: `ui-spec.md`

### B. 화면 구조

**8. discovery-sitemap — 사이트맵** (확인 2번)
- 기능을 페이지로 묶고, 1층 메뉴를 유저와 확정한 뒤, 나머지 페이지를 트리에 매단다.
- 페이지마다 위에서 아래 순서로 섹션 목록(P4-3)을 쓰고, 페이지 사이 이동을 표로 적는다.
- 뒤 단계가 추가 후보를 넘기면 다시 실행한다. 이때 기존 번호는 바꾸지 않는다.
- 산출물: `sitemap.md`

**9. discovery-user-flow — 유저 흐름** (확인 2번)
- 고객군별 핵심 과업과 흔한 흐름(로그인, 온보딩, 검색 등)을 흐름도(F1…)로 그린다. 실패 경로도 그린다.
- 흐름에서 나온 화면 상태(비로그인, 빈 목록, 오류 등)를 모아 와이어프레임에 넘긴다.
- 산출물: `user-flow.md`

**10. discovery-wireframe — 와이어프레임** (확인 2번)
- 박스 하나가 사이트맵 섹션 하나다. 공통 섹션, 페이지별 기본 모양, 상태 화면, 와이어플로를 그린다.
- 에이전트는 그림 데이터만 쓰고 HTML은 `tools/wireframe-gen/gen.py`가 만든다. 기본은 웹 폭이다.
- 산출물: `wireframe.html`, `wireframe.md`

**정합성 검사·수정 — consistency-check ⇄ consistency-fix** (최대 3회차)
- check가 seed-v2부터 wireframe까지 결정 기록을 기준으로 대조해 문제를 찾고, 유저가 문제마다 고친다/의도한 것/보류를 정한다.
- fix가 "고친다"만 앞 문서부터 순서대로 고친다. 기존 번호는 바꾸지 않는다.
- 산출물: `consistency/round-{N}/findings.md`, `fix-log.md`

### C. 디자인 인계

**11. design-references — 톤 레퍼런스 모으기** (대화 → 자동 → 대화)
- ui-spec의 "전역 분위기"를 기준으로 후보 12~18곳을 제안하고, 유저가 더하거나 빼서 확정한다. 경쟁사가 아니라 닮고 싶은 분위기가 기준이다.
- 사이트마다 2~3장을 캡처한다. 막힌 곳은 기록하고 넘어간다.
- 캡처를 보고 디자인 도구에 보낼 약 5곳을 함께 고른다. 다 보내면 디자인이 평균을 내 버려서 톤이 흐려지기 때문이다.
- 산출물: `design_handoff/references/`, `selection.md`(고른 곳과 각각 봐 달라고 할 점)

**12. design-request-guide — 클로드 디자인 진행 가이드 만들기** (자동)
- seed-v2, ui-spec, sitemap, user-flow, wireframe, 레퍼런스를 읽고 6단계 프롬프트를 바로 붙여 넣을 수 있는 완성문으로 조립한다.
- 아직 정하지 않은 값(글자 수, 사진 장수 등)은 "정해야 할 값"으로 모은다.
- 산출물: `request-guide.md`

### D. 클로드 디자인 (외부에서 직접 진행)

1. 기획 문서 네 개를 보내고, 제작하지 말고 이해한 내용만 요약해 달라고 해서 맞는지 확인한다
2. 레퍼런스 약 5장을 보내 분위기를 맞춘다
3. 우리 wireframe.html을 보내 섹션 번호를 유지한 채 다듬게 한다
4. 색과 스타일 2~3안 중 하나를 골라 팔레트와 서체를 확정한다
5. Tailwind 테마 파일과 공통 컴포넌트 코드를 받는다
6. 전 페이지 최종 시안을 받아 FE 트랙으로 넘긴다

---

## 유저가 참여하는 지점

| 단계 | 참여 방식 |
|---|---|
| 1 discovery-init | 입력 + 방향 질문 |
| 2 discovery-research | 끝에 확인 1번 |
| 3~5 | 없음 (자동으로 이어서 실행 가능) |
| 6 discovery-value-proposal | 결정 대화 |
| 7 discovery-ui-spec | 대화 2번 |
| 8 discovery-sitemap | 1층 확정 + 전체 확인 |
| 9 discovery-user-flow | 흐름 목록 확정 + 전체 확인 + 추가 후보 결정 |
| 10 discovery-wireframe | 공통 섹션·첫 묶음 확인 + 전체 확인 + 추가 후보 결정 |
| consistency-check / fix | 회차마다 문제별 처리 결정 / 없음 |
| 11 design-references | 후보 확정 + 최종 선별 |
| 12 design-request-guide | 없음 |
| 클로드 디자인 ①~⑥ | 직접 진행 |

## 흐름에서 끊겨 있는 곳

1. **`needs-research.md`를 받아 처리하는 단계가 없다.** 4단계와 5단계가 추가 조사 항목을 기록하지만, 그걸 조사하는 단계는 지금 파이프라인에 없다. 지금은 6단계에서 유저에게 "확인 안 된 가정"으로 보여 주는 데서 끝난다.
2. **클로드 디자인 결과물을 FE 코드로 옮기는 단계는 이 플러그인에 없다.** 별도 플러그인 dk-fe-bundle이 맡는다.
3. **정합성 검사·수정 스킬은 초안이다.** 테스트 실행에서 나온 스킬 피드백이 아직 반영되지 않았다.
