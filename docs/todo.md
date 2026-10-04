# 작업 기록과 할 일

## 할 일

### 1. 바뀐 흐름 전체를 한 번 돌려 보기 (가장 먼저)

2026-10-04에 바꾼 흐름은 처음부터 끝까지 한 번도 실행하지 않았다.
9/28~29 테스트 실행(`dev_automation/try_sitemap_flow_wireframe/`)은 옛 ui-spec(대화 5번)으로 만든 문서에서 출발했으므로,
새 ui-spec(대화 2번)이 만든 ui-spec.md를 sitemap이 그대로 받는지 확인되지 않았다.

돌릴 순서:
```
discovery-ui-spec (대화 1·2) → discovery-sitemap → discovery-user-flow → discovery-wireframe
→ discovery-consistency-check ⇄ discovery-consistency-fix → design-request-guide
```
- 출발 문서: 기존 테스트 run의 seed-v2.md를 복사해 쓰면 1~6단계를 건너뛸 수 있다
- 따로 테스트 run을 만들지 않고, 다음 실제 프로젝트의 첫 실행을 테스트로 삼아도 된다

볼 것:
- ui-spec.md의 기능 번호(1~N, s1~sN), 용어 표, 전역 분위기, 흐름 정책이 sitemap·user-flow 입력으로 맞는가
- sitemap "다시 만들기"(추가 후보 반영, 기존 번호 유지)가 user-flow `Resume: 6`, wireframe `Resume: 5`와 맞물리는가
- 정합성 검사에서 C1 오탐이 사라졌는가, 루프 마무리(summary.md, 루프 뒤 유저 확인 목록)가 만들어지는가
- request-guide가 `Run:` 하나로 문서 다섯 개를 읽고, 3단계에 wireframe.html을 첨부하는가

### 2. 필수는 아닌 것

- `tools/` 공용 점검 스크립트 — 번호 참조, 이동 표 양쪽 대조, mermaid 파싱(Node + jsdom + mermaid 11), id 중복, 생성기 재생성 대조.
  지금은 정합성 검사·수정이 실행할 때마다 새로 짠다
- 와이어프레임 생성기 개선 — 막힌 버튼 요소, 하단 고정 섹션 표시, 모든 페이지에 붙는 공통 주석,
  와이어플로의 줄인 프레임이 강조 버튼을 버리는 문제
- user-flow 가이드 — 누르기 전에 이미 막힌 버튼(마감·정원·권한)을 흐름에 그리는 모양,
  한 페이지에 같은 이름의 화면 상태가 둘 필요할 때의 규칙
- 새 스킬 다섯 개(sitemap, user-flow, wireframe, consistency-check, consistency-fix)의 `examples/` 실행 예시
- 실행 예시 `discovery-ui-spec`, `design-request-guide`는 옛 버전 기록이다 — 1번 실행 뒤 새로 만든다

## 작업 기록

### 2026-10-04 — 계획대로 흐름 맞추기, 정합성 스킬 피드백 반영 (0.2.0, main 838b198)

계획 문서(`plan-sitemap-flow-wireframe.md`)대로 스킬끼리 이어지지 않던 세 곳을 고쳤다:

| 커밋 | 내용 |
|---|---|
| `a4ba969` | ui-spec을 대화 1·2만으로 — 용어·핵심 기능 → 보조 기능·전역 분위기. 페이지는 정하지 않고 다음 단계를 sitemap으로 |
| `1c8976e` | sitemap "다시 만들기" — user-flow·wireframe이 넘긴 추가 후보를 받고 기존 페이지·섹션 번호를 지킨다 (P4-3a, 취소선) |
| `cec22d0` | request-guide 3단계를 "wireframe.html을 첨부해 다듬기"로. `Run:` 하나로 기획 문서 다섯 개를 읽고, 정해야 할 값을 모은다 |
| `9b084a1` | README 맨 위에 전체 흐름 도식, 14개 스킬 기준으로 표·설명 갱신 |
| `1c6c9ea` | 0.2.0, plugin.json·marketplace.json 설명 갱신 |

테스트 실행(`try_sitemap_flow_wireframe/…/test-notes/consistency-*-skill-feedback.md`)의 피드백 중 규칙 문서에 해당하는 것을 반영했다:

| 커밋 | 내용 |
|---|---|
| `acc5d11` | consistency-check — C1 오탐 제외, 항목별 확인 방법 표시, 대리 확인 두 갈래, 빈 항목 4개(D2 확장·E3·E4·I1), 수정 제안 규칙(섹션 번호·권장·생성기로 그릴 수 있는 것만), 2·3회차 범위 |
| `2dc5e44` | consistency-fix — 와이어프레임은 그림 데이터 + 생성기로, 결정 기록은 덧붙이기, 참조 따라가기 범위, 고쳤지만 확인할 점, 이어서 하기 |
| `2c9197d` | 루프 마무리 — 마지막 회차는 넘김 금지·기계 점검 전부, summary.md와 루프 뒤 유저 확인 목록 |
| `fe086c8` | ui-spec "흐름 정책" 절 — 기능이 아닌 동작 규칙(자동 가입, 정원 마감 등)을 적는 곳 |
| `de12f80` | user-flow 흐름 그림의 " · " 뒤에는 여섯 가지 상태 이름만 |
| `0f0acac`, `838b198` | README 상태 갱신, .playwright-mcp/ 무시 |

### 2026-09-28~29 — 사이트맵·유저 흐름·와이어프레임·정합성 스킬 추가

- 새 스킬 5개: discovery-sitemap, discovery-user-flow, discovery-wireframe(생성기 `tools/wireframe-gen/`), discovery-consistency-check, discovery-consistency-fix
- user-flow·wireframe은 스킬 문서 자체 검사 2회차 (`review-log-*.md`)
- 테스트 실행: `dev_automation/try_sitemap_flow_wireframe/` — 크루 매거진 run으로 sitemap부터 정합성 3회차까지. 결과 정리는 그 run의 `consistency/summary.md`
- 웹을 기본 플랫폼으로, 웹 본보기 `example-web`
