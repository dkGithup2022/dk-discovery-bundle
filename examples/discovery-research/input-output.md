# discovery-research — 실행 예시

실행 대상: 크루 매거진 커뮤니티 앱 (2026-09-18 실행, 원본: `try_project_discovery_2/planner/260918-1754-crew-magazine-community-app/research/`)

## 호출

당시 명령 이름은 `planner:research`였다. 인자 없이 실행한 것으로 보이며, 아래는 현재 명령 형식으로 다시 적은 것이다(재구성).

```
/dk-discovery-bundle:discovery-research
```

반복 횟수를 제한하고 싶으면 `Iterations: N`을 붙일 수 있다. 이번 실행에서 이 인자를 썼다는 기록은 없다.

## Input

- `init/seed.md`, `init/handoff.json` (discovery-init 예시 참고)
- handoff.json의 `search_keywords`를 검색어 재료로 썼다. 예: `"korean": ["소모임 앱", "크루 커뮤니티", "관심사 모임 플랫폼", "활동 기록 매거진", "크루 모집"]`
- 실행 지시(`order.md`)에서 "참조 이미지의 제품 형태(콘텐츠 퍼스트 소모임 앱)를 기준으로 직접/간접 경쟁을 분류하라"고 했고, 예상 비교군으로 문토·소모임·트레바리·남의집·Meetup을 적어 두었다.

## 유저와 주고받은 것

기록 없음. seed.md가 있었기 때문에 아이디어를 다시 묻는 질문은 필요 없었다(trial-notes: "인간 입력 필요 지점 없음"). 경쟁사 구성과 숫자를 유저에게 검수받는 HITL 단계는 이 실행 뒤에 워크플로에 추가되었기 때문에(커밋 59fe34e) 이번 실행에는 없었다.

## Output

```
research/
├── references.md            # 수집한 서비스 목록 (직접/간접/다른 접근)
├── analysis/
│   ├── munto.md             # 서비스별 분석, 각 73~76줄
│   ├── somoim.md
│   ├── meetup.md
│   ├── ohwoonwan.md
│   └── trevari.md
├── handoff.json             # 다음 단계 입력
├── research-results.tsv     # 반복마다 남긴 로그 (로컬 .gitignore로 커밋 제외)
└── trial-notes.md
```

### references.md (발췌)

```markdown
수집 서비스: 5개 (직접 3, 간접 2, 다른접근 0)

## 직접 경쟁
| 서비스 | URL | 한줄 설명 | 분석 파일 |
| 문토 | https://www.munto.kr/ | 관심사 기반 소모임·원데이클래스 앱 ("내가 찾던 모든 취미 모임") | analysis/munto.md |
| 소모임 | https://www.somoim.co.kr/ | 국내 최대 취미모임 동호회 앱 (주간 14,000개 모임) | analysis/somoim.md |
| Meetup | https://www.meetup.com/ | 관심사 그룹 발견·가입 글로벌 플랫폼 | analysis/meetup.md |

## 간접 경쟁
| 서비스 | … | 겹치는 부분 | … |
| 오운완 | … | 크루 활동 인증·기록이 콘텐츠가 되는 구조 | … |
| 트레바리 | … | 기록(독후감)이 모임 자산이 되는 구조, 신중한 가입자 대상 | … |
```

### analysis/munto.md (발췌)

모든 분석 파일은 같은 틀을 따른다. "중요" 항목 7개(핵심 가치, 핵심 고객, 주요 기능, 가격, BM 구조, 강점, 약점)는 반드시 채우고, 그 아래 "애매"와 "참고" 항목은 확인되는 만큼 채운다.

```markdown
### 핵심 가치
- 원문: "내가 찾던 모든 취미 모임" / "똑같은 일상을 다채롭게 만들어 줄 원데이 취향 모임" (munto.kr 메타/히어로, 2026-09-18)
- 해석: 관심사 기반 모임의 발견·참여를 한곳에 모은 종합 플랫폼. seed의 "크루 발견·가입" 기능과 정면으로 겹치나, 콘텐츠(매거진) 퍼스트 발견 구조는 아니다.

### BM 구조
- 주 수익: 유료 모임 참가비의 운영 수수료 20% (문토 공지 "참가비 정산" 기준)
- 추정 규모: 유료 정산 호스트 1,952명, 최고 연 수입 호스트 9,500만원 (유니콘팩토리 2023.12) — 총매출은 N/A

### 약점
1. 모임 연령 제한(대부분 35세 이하) — 고객층 스스로 좁힘 — 출처: 블라인드 후기
…(생략)
4. 가입 전에 모임 내부 활동을 볼 수 있는 수단이 약함 — 활동 기록이 외부 공개 콘텐츠로 축적되지 않음 (랜딩·피드 구조 확인)

## 접근 실패 기록
| URL | 도구 | 시도 횟수 | 실패 이유 | 대체 데이터 |
| https://www.munto.kr/ | WebFetch | 1 | SPA — 본문 대부분 미렌더링 | 히어로 카피만 확보, 나머지는 WebSearch 2회로 대체 |
```

소모임 분석의 가격 항목처럼 숫자가 확인되면 그대로 적는다.

> - 범위: 프리미엄 모임권 월 15,500원·연 159,000원 / 클래스 모임권 월 42,000원·연 450,000원

### handoff.json (research 커밋 c6c5c49 시점, 발췌)

```json
{
  "tool": "planner:research",
  "references_count": { "direct": 3, "indirect": 2, "alternative": 0, "total": 5 },
  "references": [
    { "name": "소모임", "type": "direct", "important_fields_filled": 7, "important_fields_total": 7,
      "key_weakness": "구형 UI/사용성 혹평 + 모임 내부 활동이 가입 전에 보이지 않음" },
    { "name": "Meetup", "type": "direct", …,
      "key_weakness": "운영자 구독료 인상·멤버 페이월 시도로 운영자 이탈 정서" },
    …(생략)
  ],
  "search_stats": { "total_queries": 5, "categories_used": ["direct", "alternatives", "community"],
                    "duplicates_skipped": 2, "analyze_extra_queries": 7 },
  "market_note": "직접 경쟁자 충분 (국내 2 + 글로벌 1). 단, '활동 기록을 공개 매거진으로 발행해 크루를 발견하게 하는' 콘텐츠 퍼스트 구조는 수집된 서비스 중 없음 — 오운완(운동 인증 피드)·트레바리(독후감 규칙)가 부분 구현."
}
```

이 파일은 다음 단계인 service-recording이 `recorded_services` 필드를 덧붙여 갱신한다.

### research-results.tsv (반복 로그 전문)

```
iteration  commit   metric  status    description
0          258ad7c  0       baseline  research 시작 — 수집 0개
1          598a371  30      keep      collect: 직접 키워드 검색 1회 — 문토·소모임 추가 (직접 2)
2          51239a6  45      keep      collect: 기능 키워드 검색 — 오운완 추가 (간접 1)
3          -        45      discard   collect: alternatives 검색 — 신규 없음 (중복 2건 skip), 리스트 기사 발견
4          dfaab74  75      keep      collect: 직접 키워드 변형 검색 — 트레바리 추가 (간접 2), toptrend 리스트 기사 DNS 실패
5          89cc22e  97      keep      collect: 커뮤니티 검색(reddit) — Meetup 추가. 종료 조건 충족: 직접3 간접2 카테고리3
6          d3c61ee  100     keep      analyze 문토: 7/7 — fetch 1(SPA 실패) + search 2로 채움
7          2840d08  100     keep      analyze 소모임: 7/7 — fetch 1 + search 1로 채움
…(생략: Meetup·오운완·트레바리 모두 7/7)
```

(delta·guard 칸은 생략했다.) 서비스를 하나 수집하거나 분석할 때마다 커밋을 하나씩 남겼고, 전부 합쳐 collect 커밋 4개, analyze 커밋 5개, output 커밋 1개가 생겼다.

## 참고

- 수집 루프는 "직접 경쟁 3개 이상, 간접 경쟁 2개 이상"이 채워지자마자 끝난다. 이번에는 WebSearch 5회 만에 끝났고(상한 20회), 검색 중에 보인 넷플연가·남의집·Heylo는 종료 조건을 채우는 데 필요하지 않아 수집하지 않았다. "다른 접근" 분류는 0개였다.
- 문토와 트레바리처럼 SPA로 만든 사이트는 WebFetch로 본문을 거의 가져오지 못했다. 이런 경우 분석에 필요한 정보는 WebSearch로 대신 채웠고, 각 분석 파일 끝에 "접근 실패 기록"으로 남겼다.
- 같은 레포에 1차 실행의 커밋이 남아 있어서, "git log로 이전 검색 키워드를 확인하라"는 규칙 때문에 이전 실행이 키워드 선택에 영향을 줬다(trial-notes). 검색 자체는 모두 새로 했다.
