# 계획 — 사이트맵·유저 흐름·와이어프레임 단계 추가

## 배경

지금 흐름은 경쟁사 화면과 평가를 모은 뒤, 줄글로 쓴 UI 기획(ui-spec)을 거쳐 바로 클로드 디자인으로 넘어간다.
사이트맵, 유저 흐름, 와이어프레임을 만드는 일은 클로드 디자인 3단계에 한 줄 요청으로 들어가 있고,
이 결과물들을 우리가 직접 만드는 절차가 없다.
경쟁사 화면은 각 절차 안에서 참고하는 재료로 쓰고, 절차 자체를 먼저 만든다.

단계마다 사람이 결과를 보고 okay하면 다음 단계로 넘어가는 방식은 그대로 유지한다.

## 지금 흐름

```
1 init → 2 research → 3 service-recording → 4 brainstorm → 5 hypothesize
→ 6 value-proposal → 7 ui-spec (대화 1~5) → 8 design-references → 9 design-request-guide
→ 클로드 디자인 ① 이해 확인 ② 톤 ③ 와이어프레임 ④ 색 ⑤ Tailwind ⑥ 시안
```

## 바꿀 흐름

```
1 init → 2 research → 3 service-recording → 4 brainstorm → 5 hypothesize → 6 value-proposal
→ 7 ui-spec (대화 1·2만: 기능 확정 + 전역 분위기)
→ 8 sitemap
→ 9 user-flow ──(사이트맵에 없는 화면이 나오면 8로 돌아감)
→ 10 wireframe
→ 11 design-references   (7의 전역 분위기만 있으면 되므로 8~10과 따로 돌려도 됨)
→ 12 design-request-guide
→ 클로드 디자인 ① 이해 확인 ② 톤 ③ 와이어프레임 다듬기 ④ 색 ⑤ Tailwind ⑥ 시안
```

## 단계별로 읽는 것

| 단계 | 앞 단계 결과물 (입력) | 레퍼런스 (만드는 방법) | 경쟁사 자료 (선택) |
|---|---|---|---|
| 7 ui-spec | seed-v2.md, hypotheses.md | 기존 `v1-ui-spec-workflow.md` (대화 1·2 부분) | — |
| 8 sitemap | ui-spec.md의 기능 목록, seed-v2.md의 고객군 | 새 문서: 사이트맵 가이드 (재료: `study/sitemap/`) | shots.md — 경쟁사의 페이지 구성 |
| 9 user-flow | sitemap, ui-spec.md의 기능 목록, seed-v2.md의 고객군 | 새 문서: 유저 흐름 가이드 + 기본 흐름 틀 (재료: `study/user_flow/`) | shots.md — 경쟁사의 과업 흐름 |
| 10 wireframe | sitemap의 페이지별 섹션 목록, user-flow에서 나온 화면 상태 | 새 문서: 와이어프레임 가이드 (재료: `study/wireframe/`) | screenshots — 경쟁사의 섹션 배치 |
| 11 design-references | ui-spec.md의 전역 분위기 | 기존 `v1-design-references-workflow.md`, `capture-guide.md` | — |
| 12 design-request-guide | seed-v2, ui-spec, sitemap, user-flow, wireframe, selection.md | 기존 `v1-request-guide-workflow.md` (3단계 문구 수정) | — |

새 레퍼런스 문서 세 개는 `project_discovery/references/` 아래에 둔다.

## 순서를 이렇게 정한 이유

- 사이트맵이 먼저다. 유저 흐름은 어느 화면에서 어느 화면으로 가는지를 그리므로 화면 목록이 먼저 있어야 한다.
- 유저 흐름이 와이어프레임보다 먼저다. 흐름을 그리다 보면 오류 화면, 빈 목록, 비로그인 상태처럼
  사이트맵에 없던 화면과 상태가 나온다. 이것들을 확정한 뒤에 그려야 와이어프레임을 다시 그리지 않는다.
- 9에서 8로 되돌아가는 경로를 둔다. 흐름에서 새 화면이 나오면 사람이 보고 사이트맵에 추가할지 정한다.
- 전역 분위기는 7에 남긴다. design-references는 분위기만 있으면 돌 수 있어서 8~10을 기다리지 않아도 된다.

## study 자료에서 가져올 것

- `study/sitemap/`: 페이지 트리, 트리 밖 페이지(로그인·가입·프로필) 분리, 페이지마다 섹션을 위에서 아래 순서로 적는 목록
- `study/user_flow/`: 도형 규칙(원=시작·목표, 사각형=화면·단계, 평행사변형=유저 입력, 마름모=분기,
  알약=시스템 결과, 주석=조건), 모든 흐름에 실패 경로를 그리는 것, 두 사람이 주고받는 흐름(referral).
  로그인·온보딩·검색 같은 흔한 흐름은 기본 틀로 쓴다
- `study/wireframe/`: 섹션마다 라벨을 붙인 저해상도 와이어프레임, 화면을 흐름으로 잇는 와이어플로,
  참고 글(GeeksforGeeks)의 "사이트맵 먼저 → 라벨 → 공통 헤더·푸터 재사용" 순서
