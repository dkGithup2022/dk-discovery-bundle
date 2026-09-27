# 외부 서비스 조사 도구 가이드

이 문서는 기획서 제작 스킬에서 외부 서비스를 조사할 때 참조하는 레퍼런스이다. 다른 스킬의 `references/`에 넣어서 쓴다.

---

## 도구 기본 정책

```
도구 우선순위:
  1차: WebSearch (검색) + WebFetch (페이지 읽기)
  2차: Playwright (WebFetch 실패시 폴백)

호출 규칙:
  You MUST wait 3 seconds between ANY tool calls.
  Implementation: Bash("sleep 3") between each call.
  This applies to:
    - 같은 도구 반복 호출 (WebSearch → sleep 3 → WebSearch)
    - 다른 도구 번갈아 호출 (WebSearch → sleep 3 → WebFetch)
    - 폴백 전환 (WebFetch 실패 → sleep 3 → Playwright)

  Rate limit (429) 대기: Bash("sleep 30")
```

```
PLAYWRIGHT USAGE:
  Playwright is an MCP server. Tool names are not known until runtime.
  Before first use in a session:
    Run ToolSearch("playwright") to discover available tool names and schemas.
  You MUST run ToolSearch before calling any Playwright tool.
```

---

## 1. 서비스 조사시 기록/파악 항목

유사 서비스를 발견하면 아래 항목을 수집한다.

### 필수 항목

| 항목 | 설명 | 어디서 찾는가 |
|------|------|-------------|
| 서비스명 | 정식 명칭 | 랜딩 페이지 타이틀 |
| URL | 메인 도메인 | 검색 결과 |
| 한줄 설명 | 서비스가 스스로 말하는 가치 | 랜딩 페이지 히어로 섹션 |
| 핵심 고객 | 누구를 위한 서비스인가 | 랜딩 "For ~" 섹션, 가격 페이지 플랜명 |
| 핵심 기능 (3개 이상) | 주요 기능 목록 | 랜딩 feature 섹션, 제품 페이지 |
| 가격 모델 | 무료/프리미엄/구독/건당 | 가격 페이지 (pricing). B2C 앱은 가격 페이지가 없는 경우가 많다 → 앱스토어/플레이스토어 인앱결제 목록에서 수집 |
| 가격 범위 | 최저~최고 플랜 가격 | 가격 페이지 또는 앱스토어 인앱결제 목록 |

### 선택 항목 (찾을 수 있으면 수집)

| 항목 | 설명 | 어디서 찾는가 |
|------|------|-------------|
| BM 구조 | 수익을 어떻게 내는가 | 가격 페이지, 블로그, 투자 기사 |
| 기술 스택 | 어떤 기술로 만들었는가 | 블로그, 채용 페이지, BuiltWith |
| 투자 이력 | 펀딩 라운드, 금액 | Crunchbase, 기사 |
| 팀 규모 | 직원 수 | LinkedIn, 채용 페이지, About |
| 사용자 후기 | 실제 유저 피드백 | G2, Capterra, Product Hunt, 앱스토어 |
| 약점/불만 | 유저 불만 포인트 | 도메인에 맞는 소스 선택 — B2B: G2/Capterra 부정 리뷰, Reddit / 한국 B2C: 앱스토어·플레이스토어 리뷰, 네이버 블로그·카페 후기, 커뮤니티 |
| 차별화 포인트 | 경쟁사 대비 고유한 것 | 랜딩 "Why us" 섹션 |
| 런칭 시기 | 서비스 시작 시점 | About, Crunchbase, Product Hunt |

### 수집 지시

```
You MUST collect ALL required fields for each service.
If a required field cannot be found after checking the expected source:
  1. Try alternative sources (blog, press, review sites)
  2. If still not found: record as "N/A — not found on {checked sources}"
  NEVER leave a required field empty without explanation.

You SHOULD collect optional fields when they are easily accessible.
Do NOT spend more than 2 tool calls per optional field.
```

### 서비스 분석 파일 템플릿

템플릿은 `analysis-elements.md`가 유일한 원본이다 — 그 문서의
"analysis/{service}.md 템플릿"을 사용한다. (이 문서에 템플릿을 중복 정의하지 않는다.)

### 수집 흐름 예시

```
서비스 "Notion" 조사:

1. [WebFetch] https://notion.so → 랜딩 페이지
   → 서비스명: Notion
   → 한줄 설명: "The connected workspace for your docs, projects, & knowledge"
   → 핵심 고객: 팀/개인
   → 핵심 기능: 문서, 프로젝트 관리, 위키, AI
   [Bash] sleep 3

2. [WebFetch] https://notion.so/pricing → 가격 페이지
   → 가격 모델: 프리미엄 (Free / Plus / Business / Enterprise)
   → 가격 범위: $0 ~ $25/user/month
   [Bash] sleep 3

3. [WebSearch] "Notion review G2" → 리뷰 검색
   → G2 URL 발견
   [Bash] sleep 3

4. [WebFetch] G2 리뷰 페이지 URL
   → 실패 (빈 응답 — JS 렌더링 필요)
   [Bash] sleep 3

5. [Playwright] G2 리뷰 페이지 → 폴백 성공
   → 평점 4.7/5, 주요 불만: "무거움", "학습 곡선"
```

---

## 2. 예외 처리 전략

### 폴백 흐름

```
WebFetch 시도
  ├── 성공 → 데이터 수집, 다음 항목으로
  └── 실패 (아래 케이스 판단)
        │
        ├── HTTP 403/401 (봇 차단, 인증 필요)
        │     → sleep 3 → Playwright로 재시도
        │     → Playwright도 실패 → "blocked" 기록, 다음으로
        │
        ├── HTTP 404 (페이지 없음)
        │     → 재시도 불필요. "page not found" 기록, 다음으로
        │
        ├── 타임아웃
        │     → sleep 3 → WebFetch 1회 재시도
        │     → 재시도도 타임아웃 → sleep 3 → Playwright 폴백
        │     → Playwright도 타임아웃 → "timeout" 기록, 다음으로
        │
        ├── 빈 응답 / 파싱 불가 (JS 렌더링 필요)
        │     → sleep 3 → Playwright로 재시도
        │     → 성공 → 데이터 수집
        │
        ├── 가짜 성공 (JS SPA — 페이지 제목만 오고 본문 없음)
        │     → 실패로 취급한다. HTTP 200이어도 본문이 비었으면 성공이 아니다.
        │     → sleep 3 → Playwright로 재시도
        │
        ├── 308/301 영구 리다이렉트
        │     → 최종 URL로 직접 재시도, 최종 URL을 기록 (리브랜딩·도메인 이전 정황 메모)
        │
        └── Rate limit (429)
              → sleep 30 → 1회 재시도
              → 재시도도 429 → "rate limited" 기록, 다른 서비스로
```

### 지시형 규칙

```
FALLBACK RULES:
  You MUST try WebFetch first for any URL.
  IF WebFetch fails with 403, empty response, or JS-rendering issue:
    Bash("sleep 3"), then retry with Playwright.
  IF WebFetch fails with 404:
    Do NOT retry. Record "page not found" and move on.
  IF WebFetch times out:
    Bash("sleep 3"), retry WebFetch once.
    If still timeout: Bash("sleep 3"), try Playwright.
  IF Playwright also fails:
    Record the failure reason and move on.
  IF HTTP 429 (rate limit):
    Bash("sleep 30"), retry once. If still 429, move to next service.

NEVER retry more than 3 times for a single URL (across all tools combined).
NEVER skip recording a failure — always log what was attempted and why it failed.
```

### 접근 실패 기록 형식

```markdown
## 접근 실패 기록

| URL | 도구 | 시도 횟수 | 실패 이유 | 대체 데이터 |
|-----|------|----------|----------|------------|
| https://example.com/pricing | WebFetch → Playwright | 2 | 403 blocked | 가격 정보는 G2 리뷰에서 추출 |
| https://example.com/about | WebFetch | 1 | 404 | N/A |
```

---

## 3. 검색어 Populating 전략

### 검색어 생성 흐름

```
Step 1: seed.md에서 키워드 추출
  아이디어 → 도메인 키워드 추출
  고객 → 타겟 키워드 추출
  가치 → 기능/가치 키워드 추출

Step 2: 1차 검색 (직접 키워드, 3-5개)
  "{도메인} tool for {타겟}"
  "{도메인} SaaS"
  "{기능} software"

Step 3: 결과 기반 확장 (2차 검색, 발견된 상위 3개 서비스에 대해)
  "alternatives to {서비스}"
  "{서비스} vs"
  "{서비스} competitors"

Step 4: 다양성 확보 (3차 검색, 2-3개) — 도메인에 맞는 소스로:
  B2B/SaaS: "best {도메인} tools {year} G2", "{도메인} Product Hunt"
  컨슈머/커뮤니티 앱: "{도메인} 앱 추천", "{도메인} 앱 비교 블로그", "{서비스} 후기"
  공통: "{도메인} tools reddit" / "{도메인} 앱 디시·커뮤니티"
```

### 키워드 추출 예시

```
seed.md:
  아이디어: "프리랜서를 위한 프로젝트 관리 + 인보이스 통합 툴"
  고객: "1인 프리랜서, 소규모 에이전시"
  가치: "프로젝트 관리와 청구를 한 곳에서"

추출:
  도메인 키워드: project management, invoice, freelancer tool
  타겟 키워드: freelancer, small agency, solo
  기능 키워드: project tracking, invoicing, billing, time tracking

1차 검색어:
  "freelancer project management tool"
  "invoice software for freelancers"
  "freelancer all-in-one tool"
  "project management + invoicing SaaS"

2차 검색어 (1차에서 Bonsai, HoneyBook 발견 후):
  "alternatives to Bonsai"
  "HoneyBook vs"
  "Bonsai competitors"

3차 검색어 (다양성):
  "best freelancer tools 2024 G2"
  "top invoicing software Product Hunt"
  "freelancer business management reddit"
```

한국어 서비스 조사시 검색어 추가:

```
한국어 키워드도 병행:
  "{도메인} 툴 추천"
  "{타겟} {기능} 서비스"
  "{도메인} 솔루션 비교"
  
예시:
  "프리랜서 프로젝트 관리 툴 추천"
  "인보이스 자동화 서비스 한국"
  "프리랜서 올인원 툴 비교"
```

### 검색어 규칙

```
SEARCH QUERY RULES:

Step 1 — Keyword extraction:
  You MUST extract at least:
    - 2 domain keywords (what the service does)
    - 1 target keyword (who it's for)
    - 2 function keywords (specific features)
  Source: seed.md (idea, customer, value fields)

Step 2 — First search (3-5 queries):
  Combine domain + target: "{domain} tool for {target}"
  Combine domain + function: "{domain} {function} software"
  Generic category: "{domain} SaaS"
  You MUST run at least 3 different first-search queries.
  Bash("sleep 3") between each WebSearch call.

Step 3 — Expansion search (2-3 queries per top 3 discovered services):
  "alternatives to {service_name}"
  "{service_name} vs"
  "{service_name} competitors"

Step 4 — Diversity search (2-3 queries):
  Review sites: "best {domain} tools {year} G2"
  Community: "{domain} tools reddit"
  Launch platforms: "{domain} Product Hunt"

TOTAL: aim for 10-15 search queries per investigation.
NEVER run more than 20 search queries — diminishing returns.

DEDUPLICATION:
  After each search, check if the service was already found.
  If duplicate: skip, do not re-analyze.
  Track found services in a running list.
```

### 검색 다양성 체크

```
검색 완료 후, 다음을 확인 (종료 조건의 원본은 research-workflow.md — 직접 ≥3, 간접 ≥2):
  - 직접 경쟁사 (같은 기능, 같은 고객): 3개
  - 간접 경쟁사 (일부 기능 겹침): 2개
  - 다른 접근 (같은 문제, 다른 해결): 1개
  아래 "최소 기준(직접 1, 간접 1)"은 니치 도메인 완화 규칙에서만 적용된다.

니치 도메인에서 목표 수가 안 나올 경우:
  - 최소 기준(직접 1, 간접 1)을 충족하면 진행
  - 최소 기준도 안 되면: 검색어를 더 일반적으로 확장
    예: "freelancer invoicing" → "small business invoicing" → "invoicing software"
  - 확장 후에도 부족하면: "해당 도메인에 직접 경쟁사가 부족함" 기록 후 진행

부족한 카테고리가 있으면 해당 방향으로 추가 검색:
  직접 경쟁 부족 → "{핵심 기능} tool for {타겟}" 변형
  간접 경쟁 부족 → "{인접 기능} software"
  다른 접근 부족 → "how do {타겟} solve {문제} without {도메인}"
```

## Playwright 화면 캡처 (service-recording 전용)

실전 검증된 사용 규칙 (2026-09 트라이얼 기준):

```
도구 로딩:
  ToolSearch는 키워드 검색만으로 부족하다. 정확한 도구명으로 로딩:
  ToolSearch("select:mcp__playwright__browser_navigate,mcp__playwright__browser_take_screenshot,mcp__playwright__browser_snapshot,mcp__playwright__browser_close")

캡처 저장:
  browser_take_screenshot의 filename에 절대 경로를 주면 그 위치에 바로 저장된다.
  중간 폴더를 거쳐 옮길 필요 없음.
  scale 파라미터는 기본값이 있어도 명시하는 것이 안전하다.

부산물 정리:
  navigate/screenshot마다 repo 루트 .playwright-mcp/에 snapshot .yml과 console .log가 쌓인다.
  이 YAML은 탐색 계획에 유용하다 (내부 링크 목록 추출 가능).
  단, 작업 종료 시 반드시 rm -rf .playwright-mcp/ — staged 전에 제거해야 repo가 오염되지 않는다.

URL 기록:
  참조 URL과 실제 렌더링 URL이 다른 경우가 흔하다 (리다이렉트, 리브랜딩, 도메인 소멸).
  최종 URL을 반드시 기록하고, references.md와 다르면 정정 메모를 남긴다.

세션 정리:
  작업 완료 후 browser_close 호출.
```
