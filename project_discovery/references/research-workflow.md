# Research Workflow — /dk-discovery-bundle:discovery-research

seed.md의 아이디어/고객/가치를 기반으로 유사 서비스를 찾고, 각 서비스를 분석하여 이후 단계에서 사용할 비교 재료를 만든다.

**이 루프가 끝나는 조건:**
- 직접 경쟁사 최소 3개, 간접 경쟁사 최소 2개를 수집하고
- 각 서비스의 "중요" 항목이 모두 채워진 analysis 파일이 완성되었을 때

## 참조 레퍼런스

```
You MUST read these before starting:
  tools-guide.md — 도구 사용 정책, 검색어 전략, 예외 처리, 3초 대기 규칙
  analysis-elements.md — 수집 항목 (중요/애매/참고), 서비스 분석 템플릿
  tone-guide.md — 톤 가이드 (전 문서 공통)
  git/git-verification.md — 루프형 git 단계 검증
  loop/planner-loop-protocol.md — Phase 구조, Git as Memory
  loop/results-logging.md — 이터레이션 TSV 로깅
```

## 루프 구조

이 단계는 두 개의 독립 루프가 순차 실행된다.

```
Collect 루프 (유사 서비스 수집)
  │ 종료: 충분한 수의 서비스가 수집되었을 때
  ▼
Analyze 루프 (서비스별 분석, 하나씩 순차)
  │ 종료: 모든 수집된 서비스의 analysis가 완성되었을 때
  ▼
Output 생성: references.md + handoff.json
```

### Collect 루프

```
LOOP:
  Phase 1 (Review):
    You MUST do ALL of the following:
    - Read references.md — 현재 수집된 서비스 목록
    - Read research-results.tsv — 이전 이터레이션 결과
    - Run git log --oneline -20 — 이전 검색 키워드 확인 (중복 방지)
    You MUST check git log before choosing next search query.

  Phase 2 (Search):
    - seed.md에서 추출한 키워드로 검색
    - 검색어 생성: tools-guide.md "검색어 Populating 전략" 참조
    - 도구 사용: tools-guide.md "도구 기본 정책" 참조
    You MUST run Bash("sleep 3") between each tool call.

  Phase 3 (Filter):
    Step 1 — 서비스인가?
      - URL이 서비스 랜딩 페이지인가 (블로그/뉴스/리스트 기사가 아닌가)
      - 가격 페이지가 있거나, 다운로드/가입이 가능한가
      - 서비스가 아니면 skip. 리스트 기사면 그 안의 서비스 URL을 추출하여 개별 판단.
    
    Step 2 — 관련 있는가?
      - seed.md의 아이디어/고객/가치와 비교
      - 관계 유형 분류:
        직접 경쟁 — 같은 기능 + 같은 고객
        간접 경쟁 — 일부 기능 겹침 또는 인접 고객
        다른 접근 — 같은 문제, 다른 해결 방법
        무관 — skip
    
    You MUST classify each service. NEVER add without classification.
    You MUST check deduplication — if already in references.md, skip.

  Phase 4 (Commit):
    git add references.md
    git commit -m "discovery(research-collect): add {서비스명} — {관계 유형}"
    한 검색에서 여러 서비스를 발견했으면 묶음 커밋 허용:
      "discovery(research-collect): add {A·B·C} — {유형 요약}"
    Git 전략: git/git-verification.md 참조 (커밋 전 staged 검증 포함)

  Phase 5 (Verify):
    collect_score 계산 (아래 스코어링 참조)

  Phase 6 (Decide):
    종료 조건 충족 → collect 루프 종료, analyze 루프 진입
    미충족 → Phase 1로

  Phase 7 (Log):
    research-results.tsv에 기록 (컬럼: iteration, phase, score, 검색수, 발견/채움 요약).
    로컬 로그다 — research/ 하위 .gitignore로 제외하고 커밋하지 않는다.
    일반 원칙: loop/results-logging.md (파일명·스키마는 본 문서가 우선)
```

### Analyze 루프

수집된 서비스를 **하나씩 순차적으로** 분석한다.

```
FOR each service in references.md (미분석 서비스만):
  LOOP (per service):
    Phase 1 (Review):
      - 해당 서비스의 현재 analysis 파일 읽기 (없으면 템플릿 생성)
      - 채워진 항목 / 미채워진 항목 파악
      - analysis-elements.md의 "중요" 항목 7개 기준으로 체크

    Phase 2 (Fetch):
      - 미채워진 항목의 소스에 접근
      - 도구 사용: tools-guide.md "도구 기본 정책" 참조
      - 예외 처리: tools-guide.md "예외 처리 전략" 참조
      You MUST run Bash("sleep 3") between each tool call.

    Phase 3 (Extract):
      - 접근한 페이지에서 정보 추출
      - analysis/{service}.md에 기록
      - 템플릿: analysis-elements.md "analysis/{service}.md 템플릿" 참조
      You MUST fill all "중요" fields.
      You SHOULD fill "애매" fields when accessible within 2 extra tool calls.
      "참고만" fields: record only if discovered during other lookups.

    Phase 4 (Commit):
      git add analysis/{service}.md
      git commit -m "discovery(research-analyze): {서비스명} — {채운 항목 요약}"

    Phase 5 (Verify):
      analyze_score = 중요_항목_채움_수 / 7 * 100

    Phase 6 (Decide):
      7/7 채움 → complete, 다음 서비스로
      미달 → 미채워진 항목 보강 시도
      3회 보강 시도 후에도 미달 → 접근 실패 기록, 다음 서비스로
      NEVER spend more than 3 retry attempts per service.

    Phase 7 (Log):
      research-results.tsv에 기록
```

**약점 수집 비용:** 약점(유저 불만)은 리뷰 사이트 접근이 필요하여 도구 호출이 더 필요하다. 한 서비스당 약점 수집에 최대 3회 도구 호출 허용. analysis-elements.md "약점" 항목 참조.

## 스코어링

### Collect 루프 스코어

```
collect_score = (직접경쟁_수 / 3) * 50
             + (간접경쟁_수 / 2) * 30
             + (다른접근_수 / 1) * 10
             + (검색_다양성) * 10

검색_다양성 = 사용된 고유 검색어 카테고리 수 / 4
  카테고리: 직접 키워드, alternatives 검색, 리뷰사이트 검색, 커뮤니티 검색

Direction: higher is better
점수는 진행 상황 참고 지표다. 종료 판정은 아래 "종료 조건"이 우선한다 —
종료 조건 충족 시 점수가 100 미만(예: 87.5)이어도 정상 종료다.
```

### Analyze 루프 스코어

```
analyze_score = 중요_항목_채움_수 / 7 * 100

Direction: higher is better
목표: 100
```

## 종료 조건

### Collect 루프 종료

```
충분 조건 (모두 충족시 종료):
  - 직접 경쟁사 ≥ 3개
  - 간접 경쟁사 ≥ 2개
  - 검색 카테고리 ≥ 3개 사용

니치 도메인 완화:
  - 15회 검색 후에도 직접 경쟁사 < 3개:
    → 검색어 일반화 (tools-guide.md "니치 도메인 대응" 참조)
    → 일반화 후에도 직접 + 간접 합산 < 3개:
      → "시장에 직접 경쟁자 부족" 기록 후 수집된 것으로 진행

최대 검색 횟수: 20회. 이후 강제 종료.
You MUST stop collecting after 20 search queries regardless of count.
카운트 범위: Collect 루프의 WebSearch만 센다. Analyze 단계의 보강 검색은
별도이며 서비스당 재시도 3회 제한을 따른다.
```

### Analyze 루프 종료

```
서비스별:
  - 중요 항목 7/7 채움 → 완료
  - 3회 보강 시도 후에도 미달 → 접근 실패 기록 후 완료 처리

전체:
  - 모든 수집된 서비스의 분석이 완료되면 종료
```

## HITL 체크 — 경쟁사 파악 검수 (Analyze 완료 후)

경쟁사 구성과 핵심 숫자가 확정되는 지점이므로, 여기서 유저 검수를 1회 수행한다.

```
IF 대화형 환경 (AskUserQuestion 사용 가능):
  1. 유저에게 요약을 보여준다:
     - 경쟁사 분류표 (직접/간접/다른접근 + 한줄 설명)
     - 서비스별 핵심 발견 1줄 (가격·BM·약점 중 두드러진 것)
     - 시장 관찰 (있다면)
  2. AskUserQuestion 1회 (질문 배치):
     | # | Header | Question |
     |---|--------|----------|
     | 1 | 구성 | "빠졌거나 잘못 분류된 서비스가 있나요?" |
     | 2 | 숫자 | "가격·BM 등 아는 것과 다른 정보가 있나요?" |
     | 3 | 인사이트 | "이 시장에 대해 공유할 경험·인사이트가 있나요?" |
  3. 피드백 반영: references.md / analysis/ 수정, 유저 제공 정보는 출처를 "유저 제공"으로 태깅
  4. 반영 후 커밋: "discovery(research-hitl): user feedback — {요약}"

IF 비대화형 환경:
  Skip. handoff.json에 "hitl": "skipped" 기록.
  절대 유저 응답을 지어내지 않는다.
```

## Output

### references.md

```markdown
# 유사 서비스 레퍼런스

seed: {seed.md의 아이디어 한 줄}
검색일: {날짜}
수집 서비스: {N}개 (직접 {n1}, 간접 {n2}, 다른접근 {n3})

## 직접 경쟁

| 서비스 | URL | 한줄 설명 | 분석 파일 |
|--------|-----|----------|----------|

## 간접 경쟁

| 서비스 | URL | 한줄 설명 | 겹치는 부분 | 분석 파일 |
|--------|-----|----------|-----------|----------|

## 다른 접근

| 서비스 | URL | 한줄 설명 | 어떻게 다른가 | 분석 파일 |
|--------|-----|----------|-------------|----------|
```

### handoff.json

```json
{
  "version": "1.0",
  "tool": "dk-discovery-bundle:discovery-research",
  "hitl": "done|skipped",
  "generated_at": "ISO timestamp",
  "seed_idea": "seed.md의 아이디어 한 줄",
  "references_count": {
    "direct": 3,
    "indirect": 2,
    "alternative": 1,
    "total": 6
  },
  "references": [
    {
      "name": "서비스명",
      "url": "URL",
      "type": "direct|indirect|alternative",
      "analysis_file": "analysis/{service}.md",
      "important_fields_filled": 7,
      "important_fields_total": 7,
      "key_weakness": "핵심 약점 한 줄"
    }
  ],
  "search_stats": {
    "collect_queries": 14,
    "analyze_queries": 6,
    "categories_used": ["direct", "alternatives", "review_sites", "community"],
    "duplicates_skipped": 3
  },
  "market_note": "직접 경쟁자 충분 또는 니치 도메인 — 직접 경쟁자 부족",
  "next_step": "dk-discovery-bundle:discovery-service-recording"
}
```

### Output 디렉토리

```
discovery/{run-id}/
  research/
    .gitignore            ← research-results.tsv 제외용
    references.md
    analysis/
      {service-name}.md
      ...
    research-results.tsv  ← 로컬 로그 (커밋 안 함)
    handoff.json
```
