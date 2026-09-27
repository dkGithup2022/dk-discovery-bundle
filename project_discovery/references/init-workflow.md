# Init Workflow — /dk-discovery-bundle:discovery-init

아이디어를 수집하고, 간략한 시장 탐색을 수행하여 유저의 방향성을 구체화한 뒤, seed.md를 생성한다.

**비루프 — 1회 실행. 단, 3단계 구조:**

```
Step 1: 초기 입력 수집 → seed-raw.md
Step 2: 간략 탐색 (WebSearch 5~10회) → 유저에게 현황 보여주기
Step 3: 방향성 대화 → 유저 선언만 반영 → seed.md 확정
```

---

## Step 1: 초기 입력 수집

유저가 인라인으로 Idea/Customer/Value를 제공하지 않았으면, AskUserQuestion으로 수집한다.

You MUST call AskUserQuestion with ALL 4 questions in ONE batched call:

| # | Header | Question | Required |
|---|--------|----------|----------|
| 1 | `Idea` | "어떤 서비스를 만들려고 하나요? 아이디어를 설명해주세요." | 필수 |
| 2 | `Customer` | "핵심 고객은 누구인가요? (예: 프리랜서, 중소기업, 학생 등)" | 필수 |
| 3 | `Value` | "이 서비스가 제공하는 핵심 가치는 무엇인가요?" | 필수 |
| 4 | `Extras` | "추가 정보가 있으면 자유롭게 입력해주세요. (디자인/기능/BM/기술 등, 없으면 건너뛰기)" | 선택 |

```
You MUST ask all 4 questions in a single AskUserQuestion call.
NEVER ask one at a time.
If Idea, Customer, Value are all provided inline → skip AskUserQuestion entirely.
If any of the 3 required fields is missing → ask ALL 4 questions.
```

수집 내용은 seed-raw로 임시 보관한다 — 파일로 저장하지 않는다 (대화 내 버퍼).
Step 3 완료 후 seed.md 하나만 생성한다. seed-raw.md라는 파일을 남기면 안 된다.

---

## Step 2: 간략 탐색 (Quick Scan)

### 목적

유저가 방향성을 선언할 때 맥락을 갖도록, 현재 시장 현황을 간략히 보여준다.

```
IMPORTANT:
  이 탐색의 결과는 seed.md에 반영하지 않는다.
  이후 research 단계에서 더 강한 조사를 수행하기 때문이다.
  여기서는 유저에게 "이런 것들이 있다"를 보여주는 것이 목적이다.
```

### 탐색 방법

```
seed-raw.md에서 키워드 추출 (Step 1과 동일한 로직):
  아이디어 → 도메인 키워드 2개
  고객 → 타겟 키워드 1개
  가치 → 기능 키워드 2개

WebSearch 5~10회:
  1차 (3~5회): "{도메인} tool for {타겟}", "{도메인} SaaS", "{기능} software"
  2차 (2~3회): 발견된 상위 서비스에 대해 "alternatives to {서비스}", "{서비스} vs"
  3차 (1~2회): "{도메인} tools {year} G2", "{도메인} Product Hunt"

각 검색 결과에서 수집:
  - 서비스명 + 한줄 설명
  - 분류: 직접 유사 / 간접 유사 / 다른 접근
  - 가격대 (보이면)
```

### 유저에게 보여주는 형식

```
You MUST present the scan results to the user in this format.
탐색 시작 전, 진행 중, 완료 후 3번에 걸쳐 유저에게 맥락을 전달한다.

--- 탐색 시작 시 (검색 전에 먼저 출력) ---

"아이디어를 기록했습니다. 
지금부터 간략한 시장 탐색을 수행합니다. (WebSearch 5~10회)

이 탐색에는 다음 규칙이 있습니다:
- 탐색 결과는 seed에 반영하지 않습니다. 이후 research 단계에서 더 정확한 조사를 합니다.
- 탐색 결과를 보여드린 후 몇 가지 방향성 질문을 드릴 겁니다.
- 질문에 답하신 내용만 seed에 반영됩니다. 빈칸으로 남기셔도 됩니다.

잠시만 기다려주세요."

--- 탐색 완료 후 (결과 출력) ---

"간략 탐색이 완료되었습니다.

[시장 간략 현황]

발견된 유사 서비스:
  | 서비스 | 설명 | 관계 | 가격대 |
  |--------|------|------|--------|
  | ... | ... | 직접 유사 | ... |
  | ... | ... | 간접 유사 | ... |
  | ... | ... | 다른 접근 | ... |

주요 관찰:
  - {시장에 대한 사실 1~3개, 간결하게}

⚠️ 위 정보는 참고용입니다. 이후 research 단계에서 더 정확한 조사를 수행합니다.
⚠️ 이 결과는 seed에 반영되지 않습니다.

위 내용을 보시고, 아래 질문에 답해주세요.
생각나는 게 있으면 적고, 없으면 비워두셔도 됩니다.
답하신 내용만 seed에 기록되고, 비워두신 항목은 건너뜁니다."

--- 이후 Step 3 질문으로 이어짐 ---
```

```
You MUST NOT:
  - 이 탐색 결과를 seed.md에 기록하지 않는다
  - 유저에게 "이렇게 해야 한다"고 방향을 제시하지 않는다
  - 탐색 결과를 근거로 아이디어를 판단하거나 평가하지 않는다
  - 10회를 초과하여 검색하지 않는다
```

---

## Step 3: 방향성 대화

### 목적

간략 탐색 결과를 본 유저에게 방향성을 물어, seed를 구체화한다.

### 질문

```
You MUST call AskUserQuestion with the following questions.
유저가 빈칸으로 남기면 해당 항목은 seed에 포함하지 않는다.
모든 질문에 빈칸이어도 기존 seed-raw.md 내용으로 진행한다.

| # | Header | Question | Required |
|---|--------|----------|----------|
| 1 | `Direction` | "위 서비스들을 보고, 어떤 방향으로 가고 싶은지 있나요? (없으면 비워주세요)" | 선택 |
| 2 | `MarketView` | "현재 이 시장에 대해 느끼는 점이 있나요? (경쟁 상황, 타이밍 등. 이후 조사에서 바뀔 수 있습니다)" | 선택 |
| 3 | `BM` | "수익 모델에 대해 생각해본 게 있나요? (없으면 비워주세요)" | 선택 |
| 4 | `Characteristics` | "이 서비스만의 특징이나 '이건 꼭 이렇게 하고 싶다'는 게 있나요?" | 선택 |
```

### 반영 규칙

```
CRITICAL RULES:

1. 유저가 선언한 내용만 seed.md에 반영한다.
   - 유저가 "타이밍 베팅으로 가고 싶다"고 했으면 → seed에 기록
   - 유저가 비워뒀으면 → seed에 해당 항목 없음

2. 탐색 결과(Step 2)는 seed.md에 반영하지 않는다.
   - 발견된 서비스, 가격대, 시장 관찰 → seed에 기록하지 않음
   - 이것들은 이후 research 단계에서 더 정확하게 수집된다

3. 유저의 원문을 보존한다.
   - 유저가 말한 그대로 기록. 요약하거나 바꾸지 않는다.
   - "유저가 이렇게 말했다"를 남기는 것이지 "유저의 의도는 이것이다"를 해석하지 않는다.

4. 모든 질문에 빈칸이어도 진행한다.
   - seed-raw.md의 4개 필드(Idea/Customer/Value/Extras)만으로 research 진입 가능.
   - Step 3 응답이 전부 빈칸이면 seed.md = seed-raw.md + 검색 키워드.
```

---

## seed.md 생성

Step 1 + Step 3의 유저 선언을 합쳐 seed.md를 생성한다.

### 템플릿

```markdown
# Seed

생성일: {날짜}

## 아이디어

{Step 1에서 유저가 입력한 아이디어 원문}

## 핵심 고객

{Step 1에서 유저가 입력한 고객 원문}

## 제공 가치

{Step 1에서 유저가 입력한 가치 원문}

## 추가 정보

### 디자인
{해당 내용 또는 "없음"}

### 기능
{해당 내용 또는 "없음"}

### BM
{Step 3 BM 응답 또는 Step 1 Extras의 BM 내용 또는 "없음"}

### 기술
{해당 내용 또는 "없음"}

### 기타
{해당 내용 또는 "없음"}

## 유저 방향성 (Step 3 응답, 있는 경우만)

### 방향
{Step 3 Direction 응답 — 빈칸이면 이 섹션 생략}

### 시장 인식
{Step 3 MarketView 응답 — 빈칸이면 이 섹션 생략}

### 서비스 특징
{Step 3 Characteristics 응답 — 빈칸이면 이 섹션 생략}
```

```
IMPORTANT:
  "유저 방향성" 섹션은 Step 3에서 유저가 1개 이상 응답한 경우에만 포함한다.
  모든 응답이 빈칸이면 이 섹션 자체를 생략한다.
  seed.md는 유저의 선언만 포함한다. 시스템의 분석이나 탐색 결과를 넣지 않는다.
```

---

## 검색 키워드 자동 추출

seed.md 작성 후, 다음 단계(research)에서 사용할 검색 키워드를 자동 추출한다.

```
추출 규칙:
  아이디어에서 → 도메인 키워드 2개 이상 (서비스가 속한 분야)
  고객에서 → 타겟 키워드 1개 이상 (누구를 위한 것인가)
  가치에서 → 기능 키워드 2개 이상 (어떤 기능/가치를 제공하는가)

You MUST extract at least 5 keywords total (2 domain + 1 target + 2 function).
Keywords are in English (for search effectiveness). Korean keywords도 병행 추출.
```

---

## handoff.json 스키마

```json
{
  "version": "1.0",
  "tool": "dk-discovery-bundle:discovery-init",
  "generated_at": "ISO timestamp",
  "seed": {
    "idea": "유저 입력 원문",
    "customer": "유저 입력 원문",
    "value": "유저 입력 원문",
    "extras": {
      "design": "내용 또는 null",
      "features": "내용 또는 null",
      "bm": "내용 또는 null",
      "tech": "내용 또는 null",
      "other": "내용 또는 null"
    },
    "user_direction": {
      "direction": "응답 또는 null",
      "market_view": "응답 또는 null",
      "bm": "응답 또는 null",
      "characteristics": "응답 또는 null"
    }
  },
  "quick_scan": {
    "services_found": 0,
    "search_queries_used": 0,
    "note": "탐색 결과는 seed에 미반영. research 단계에서 재조사."
  },
  "search_keywords": {
    "domain": ["keyword1", "keyword2"],
    "target": ["keyword1"],
    "function": ["keyword1", "keyword2"],
    "korean": ["한국어 키워드1", "한국어 키워드2"]
  },
  "domain": "자동 추출된 도메인",
  "next_step": "dk-discovery-bundle:discovery-research"
}
```

---

## Git 커밋

비루프 축소 버전 적용. 상세: git/git-verification.md

```
작업 전:
  git rev-parse --git-dir || STOP
  dirty 체크: git/git-verification.md의 스코프 규칙 적용

작업 완료 후:
  git add discovery/{run-id}/init/seed.md discovery/{run-id}/init/handoff.json
  git diff --cached --name-only → 목록이 위 2개 파일뿐인지 확인 (아니면 unstage)
  git commit -m "discovery(init): seed — {아이디어 한줄 요약}"
```

---

## Output 디렉토리

```
discovery/{run-id}/          ← run-id = {YYMMDD}-{HHMM}-{slug}
  init/
    seed.md
    handoff.json
```

기준 경로: 스킬을 실행한 현재 작업 디렉토리(cwd). 시각은 로컬 시간.
slug는 아이디어에서 자동 생성 (영문 소문자, 하이픈 구분, 최대 30자).
