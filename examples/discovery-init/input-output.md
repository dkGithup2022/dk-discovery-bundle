# discovery-init — 실행 예시

실행 대상: 크루 매거진 커뮤니티 앱 (2026-09-18 실행, 원본: `try_project_discovery_2/planner/260918-1754-crew-magazine-community-app/init/`)

## 호출

당시 명령 이름은 `planner:init`이었고, 지금 번들에서는 `discovery-init`이다. 아래 호출은 `try_project_discovery/order.md`의 인라인 필드 4개를 현재 명령 형식에 맞춰 다시 적은 것이다(재구성).

```
/dk-discovery-bundle:discovery-init
Idea: 크루(소모임)가 활동 기록을 매거진(아티클)으로 발행하고, 유저는 콘텐츠를 읽다가 마음에 드는 크루를 팔로우·가입하는 콘텐츠 퍼스트 커뮤니티 앱.
Customer: 모임에 바로 뛰어들기보다 "이 모임이 실제로 뭘 하는지" 보고 결정하고 싶은 신중한 가입자. 자기 모임을 알리고 싶은 크루 운영자.
Value: 발견→기록→연결의 순환. 광고성 소개글 대신 실제 활동 기록이 크루의 포트폴리오가 된다.
Extras: 매거진에 좋아요·스크랩·팔로우가 붙어 크루 성장 지표가 된다. 커뮤니티 탭(가입인사/크루원 모집/일상)이 라이트 유저의 진입로. 크루 가입은 심사제(지원서) 기반.
```

## Input

- 필수 필드 3개(Idea, Customer, Value)와 선택 필드 Extras가 모두 인라인으로 들어왔다. 그래서 처음에 네 가지를 묻는 AskUserQuestion 단계는 건너뛰었다.
- `order.md`에는 레퍼런스 UI로 peeple 앱 캡처 이미지 4장(004·005·006·007)도 붙어 있었다.

| # | 내용 (order.md 표 그대로) |
|---|------|
| 005 | 크루가 발행한 매거진 아티클 상세 (좋아요·댓글·스크랩·팔로우) |
| 006 | 홈 — 인기 매거진 피드 + HOST EVENT 배너 |
| 004 | 커뮤니티 탭 — 가입인사/크루원 모집/일상/크루 찾기/미션 필터 |
| 007 | 매거진 콘텐츠 아래 관심사 기반 추천 크루 리스트 |

실행 기록(trial-notes)에 따르면 이 이미지들은 제품 형태를 이해하는 데만 쓰였다. 유저가 선언한 내용이 아니므로 seed에는 넣지 않았다.

## 유저와 주고받은 것

- 처음에 아이디어·고객·가치·추가 정보를 묻는 질문은 입력이 모두 인라인으로 들어와서 하지 않았다.
- 시장을 간단히 훑어본 뒤(Quick Scan) 방향·시장 인식·BM·꼭 지키고 싶은 특징을 묻는 방향성 질문 4개를 해야 하지만, 이번 실행은 사람이 답할 수 없는 환경이었다. trial-notes 원문은 다음과 같다.

> 사람과 상호작용 불가 → AskUserQuestion을 호출하지 않고, 워크플로우가 명시적으로 허용하는 "모든 응답 빈칸" 경로 적용. … 유저 선언을 임의로 창작하지 않음.

그 결과 handoff.json의 `user_direction` 네 칸은 모두 `null`로 남았다.

## Output

```
init/
├── seed.md        # 유저가 준 입력만 정리한 문서
└── handoff.json   # 다음 단계(research)가 읽는 입력 + 검색 키워드
```

### seed.md (거의 전문)

```markdown
# Seed

생성일: 2026-09-18

## 아이디어
크루(소모임)가 활동 기록을 매거진(아티클)으로 발행하고, 유저는 콘텐츠를 읽다가 마음에 드는 크루를 팔로우·가입하는 콘텐츠 퍼스트 커뮤니티 앱.

## 핵심 고객
모임에 바로 뛰어들기보다 "이 모임이 실제로 뭘 하는지" 보고 결정하고 싶은 신중한 가입자. 자기 모임을 알리고 싶은 크루 운영자.

## 제공 가치
발견→기록→연결의 순환. 광고성 소개글 대신 실제 활동 기록이 크루의 포트폴리오가 된다.

## 추가 정보
### 디자인
없음
### 기능
매거진에 좋아요·스크랩·팔로우가 붙어 크루 성장 지표가 된다. 커뮤니티 탭(가입인사/크루원 모집/일상)이 라이트 유저의 진입로. 크루 가입은 심사제(지원서) 기반.
### BM
없음
…(기술·기타도 "없음")
```

Extras 원문이 전부 기능에 관한 내용이라 "기능" 칸에 그대로 옮겼고, 나머지 칸은 "없음"으로 두었다.

### handoff.json (발췌)

```json
{
  "tool": "planner:init",
  "generated_at": "2026-09-18T07:54:51Z",
  "seed": {
    "idea": "크루(소모임)가 활동 기록을 …",
    "extras": { "design": null, "features": "매거진에 좋아요·스크랩·팔로우가 …", "bm": null, "tech": null, "other": null },
    "user_direction": { "direction": null, "market_view": null, "bm": null, "characteristics": null }
  },
  "quick_scan": {
    "services_found": 17,
    "search_queries_used": 8,
    "note": "탐색 결과는 seed에 미반영. research 단계에서 재조사."
  },
  "search_keywords": {
    "domain": ["social club platform", "content-first community app"],
    "target": ["cautious community joiner", "club organizer"],
    "function": ["activity magazine publishing", "follow and join groups", "membership application screening"],
    "korean": ["소모임 앱", "크루 커뮤니티", "관심사 모임 플랫폼", "활동 기록 매거진", "크루 모집"]
  },
  "domain": "관심사 기반 소모임/크루 커뮤니티 (콘텐츠 퍼스트)",
  "next_step": "planner:research"
}
```

### Quick Scan 결과 (유저에게 보여주는 표, seed에는 들어가지 않음)

1차 실행의 trial-notes에 "유저에게 보여줬을 내용"으로 남아 있는 표다. WebSearch 8회로 서비스 17개를 찾았다.

| 서비스 | 설명 | 관계 | 가격대 |
|--------|------|------|--------|
| PEEPLE (파빌리카) | 모임 순간을 매거진·미션·리뷰 콘텐츠로 축적, 브랜드 협업·리워드 연결. 레퍼런스 UI의 실제 서비스 | 직접 유사 | 무료(앱) |
| 소모임 | 국내 1위 취미 동호회 앱. 주 14,000 정모, 관심사 기반 추천 | 직접 유사 | 무료+ |
| 문토 | 원데이 소셜링 중심 관심사 모임 플랫폼 | 직접 유사 | 모임별 유료 |
| 트레바리 | 유료 멤버십 독서/자기계발 클럽 | 간접 유사 | 고가 멤버십 |
| 넷플연가 | 호스트 심사제 N회차 취향 모임 (2030 93%) | 간접 유사 | 유료 |
| …(생략: 남의집, 1km, Meetup, Eventbrite, Geneva, Heylo, Mighty Networks, Circle, 러너온 등) | | | |

> 주요 관찰:
> - 레퍼런스 UI(peeple)는 실제 운영 중인 제품(파빌리카 …)으로, "활동 기록→매거진→크루 발견" 구조가 이미 시장에 존재.
> - 국내 시장은 무료 동호회형(소모임)과 유료 큐레이션형(트레바리·넷플연가·남의집)으로 양분. …

## 참고

- 이 폴더의 seed.md와 handoff.json은 같은 날 16:54에 먼저 돌린 1차 실행(`try_project_discovery/planner/260918-1654-…/init/`)의 결과를 복사한 것이다(커밋 258ad7c "2차 트라이얼 준비 — seed 복사"). 두 파일 내용은 1차와 똑같다.
- 1차 실행 때 Quick Scan 검색어 예시가 B2B SaaS 쪽("{도메인} SaaS", "G2", "Product Hunt")으로 치우쳐 있어서, 소비자용 커뮤니티 앱에서는 G2·Product Hunt 검색이 쓸모 있는 결과를 거의 주지 못했다. 이 문제는 이후 컨슈머 서비스용 검색어를 추가하는 방식으로 고쳐졌다(커밋 59fe34e).
- 1차 실행에서 `git commit`이 유저가 미리 스테이징해 둔 파일 7개까지 함께 커밋한 사고가 있었다. 지금 문서에는 커밋 전에 `git diff --cached --name-only`로 스테이징된 파일 목록을 확인하라는 규칙이 들어가 있다.
