# Service Recording Workflow — /dk-discovery-bundle:discovery-service-recording

research에서 수집·분석한 서비스들의 화면을 캡처하여, **이 서비스를 모르는 사람이 이미지만 보고 서비스를 파악할 수 있는** 시각 기록을 만든다. 산출물은 hypothesize(가설 수립)와 이후 디자인 단계의 입력이 된다.

**이 루프가 끝나는 조건:**
- references.md의 모든 대상 서비스에 대해 캡처 세트 + shots.md가 완성되고, 각 세트가 "모르는 사람 테스트"를 통과했을 때

## 참조 레퍼런스

```
You MUST read these before starting:
  tools-guide.md — 도구 사용 정책, "Playwright 화면 캡처" 섹션, 3초 대기 규칙
  tone-guide.md — 톤 가이드 (캡션·문서 공통)
  git/git-verification.md — 루프형 git 단계 검증
  loop/results-logging.md — 이터레이션 TSV 로깅
```

## 입력

```
You MUST load:
  references.md — 대상 서비스 목록 + URL
  analysis/{service}.md — 서비스 이해용 (제품 형태·주요 기능 파악)
  research의 handoff.json — 서비스 메타데이터
```

## 루프 구조

서비스를 **하나씩 순차적으로** 기록한다.

```
FOR each service in references.md (Target 인자로 필터):
  Phase 1 (Probe — 접근성 판정):
    - 서비스 URL에 접근하여 렌더링 확인
    - 리다이렉트되면 최종 URL을 기록 (참조 URL ≠ 최종 URL인 경우 references.md에 정정 메모)
    - 판정 (케이스 표기는 문서 전체에서 web | external 두 값만 사용):
      web — 웹으로 서비스 제공 (랜딩 + 탐색 가능한 페이지 존재)
      external — 웹 미제공 / 앱 전용 / 가입 장벽으로 둘러볼 수 없음
    You MUST record the final rendered URL. NEVER trust the reference URL blindly.

  [web — 웹 제공]

  Phase 2 (기본 캡처 — 무조건 3종):
    - 메인(랜딩) 페이지
    - 서비스 진입점 (가입/시작하기/둘러보기 등 유저가 처음 밟는 화면)
    - 회사/서비스 소개 페이지 (있는 경우)
    You MUST capture these regardless of judgment.

  Phase 3 (계획 수립):
    - 기본 캡처와 analysis/{service}.md를 근거로 판단:
      "어디를 더 찍어야 이 서비스 파악이 쉬운가?"
    - 다음을 파악할 수 있는 경로를 계획한다:
      · 메인 페이지 구조
      · 읽기 리소스 (콘텐츠/피드/매거진 등 소비 화면)
      · 주요 피쳐 (핵심 기능이 드러나는 화면)
    - 제외 대상: 약관, 개인정보처리방침, 서비스 설명 텍스트 페이지 등
      주요 피쳐가 아닌 부분은 읽지도, 찍지도 않는다.

  Phase 4 (탐색 캡처):
    - Phase 3 계획을 실행한다
    - 진행 중 추가로 탐색할 가치가 있는 경로가 보이면 찍는다
    - 서비스당 총 캡처 상한: MaxShots (기본 8장, 기본 캡처 3장 포함)
    NEVER exceed MaxShots per service — 상한 도달시 가장 정보량 높은 화면 우선.
    부분 장벽 하이브리드: web 케이스 진행 중 일부 영역만 로그인 장벽이면
    (예: 피드/라운지), 그 영역에 한해 external 방식(검색 캡처)으로 보충할 수 있다.
    보충 컷은 shots.md에 출처 URL과 함께 기록한다.

  [external — 웹 미제공 / 가입 장벽]

  Phase 2' (검색 캡처):
    - WebSearch: "{서비스명} 앱 화면", "{서비스명} 사용법", "{서비스명} 리뷰 스크린샷" 등
    - 실제 서비스의 구조가 보이는 이미지(스토어 프리뷰, 블로그 리뷰의 캡처 등)를
      표시한 페이지를 열어 캡처한다 — 3~5장
    - 각 캡처의 캡션에 출처 URL을 반드시 기록 (외부 저작물임을 명시)
    You MUST NOT fabricate structure descriptions — capture only what a source actually shows.

  [공통]

  Phase 5 (Verify — 모르는 사람 테스트):
    - 자가 체크: "이 서비스를 전혀 모르는 사람이 이 이미지들만 보고
      ① 무엇을 하는 서비스인지 ② 핵심 화면 흐름이 어떤지 파악할 수 있는가?"
    - 요소별 판정 기준 (각 요소는 캡처에서 직접 보여야 충족):
      서비스 정체 — 무엇을 하는 서비스인지 한 컷에서 읽힘 (랜딩 카피/카테고리)
      진입 흐름 — 유저가 처음 밟는 화면이 보임 (가입/시작/둘러보기)
      핵심 기능 — 대표 기능이 실사용 형태로 보임 (상세 화면 등)
      콘텐츠 구조 — 서비스의 핵심 오브젝트가 목록/피드 형태로 보임
        (콘텐츠형이 아니면 핵심 오브젝트 리스트로 대체 해석 — 예: 모임 리스트, 상품 진열)
    - 분모 규칙: 로그인 장벽 등 서비스 특성상 확보 불가한 요소는
      "확보 불가 — {사유}"로 shots.md에 기록하고 분모에서 제외한다.
      recording_score = 충족_요소 / 확보_가능_요소 * 100
    - 통과 기준: 75 이상이면 통과(완료). 100이 이상적 목표.
      75 미만이면 Phase 3으로 돌아가 보강 — 서비스당 최대 2회 재시도.
    NEVER spend more than 2 retry rounds per service.

  Phase 6 (기록·Commit):
    - screenshots/{service}/shots.md 생성:
      각 이미지 파일명 + 한 줄 캡션 (무슨 화면인지) + 캡처일 + 최종 URL
      external은 캡션에 출처 URL 포함
    - analysis/{service}.md에 `## 스크린샷` 섹션 생성 또는 갱신
      (상대 경로 링크: `../screenshots/{service}/...`)
    - 커밋 전 검증: git diff --cached --name-only 실행,
      staged 목록이 정확히 이번 서비스의 산출물만인지 확인.
      예상 밖 파일이 있으면 unstage 후 커밋.
    - git add {이번 서비스 산출물만}
    - git commit -m "discovery(service-recording): {서비스명} — {N}장 (web|external)"
    NEVER use git commit -a. NEVER stage files outside the output directory.

  Phase 7 (Log):
    recording-results.tsv에 기록.
    스키마 (헤더): service, case(web|external), shots, recording_score, retries, note
    로컬 로그다 — research/ 하위 .gitignore로 제외하고 커밋하지 않는다.
```

## 캡처 품질 규칙 (전 케이스 공통)

```
줌아웃:
  캡처는 내용이 파악될 정도로 찍는다 — 화면 상단 히어로만 담기고 실제 내용(리스트·피드·본문)이
  잘려 있으면, 줌아웃(뷰포트 확대: browser_resize) 또는 풀페이지 캡처로 다시 찍고 잘린 컷은 폐기한다.
  권장 뷰포트: 리스트·피드형 페이지는 1280×2000. 세로가 짧은 페이지(가입 폼 등)는
  원래 뷰포트(1280×720)로 복귀해 여백 과다를 피한다.

쿠키/동의 배너:
  배너가 내용을 가리면 캡처 전에 한 번 Decline(거부)을 클릭해 닫는다.
  버튼 문구는 사이트마다 다르다 — "Decline", "거부", "Continue without accepting",
  "필수만 허용" 등 거부 계열을 찾는다.
  거부로 닫히지 않아 내용이 계속 가려지면, 그 상태를 shots.md 비고에 기록하고 넘어간다.
```

## 종료 조건

```
서비스별:
  - recording_score ≥ 75 → 완료
  - 2회 재시도 후에도 미달 → 미달 사유 기록 후 완료 처리
  - external에서 유의미한 이미지가 검색되지 않음 → "시각 자료 확보 실패" 기록 후 완료 처리

전체:
  - 모든 대상 서비스의 기록이 완료되면 종료
```

## Output

### 디렉토리 구조

```
discovery/{run-id}/
  research/
    screenshots/
      {service}/
        landing.png, entry.png, about.png, ...   ← web
        external-01.png, ...                     ← external (출처는 shots.md에)
        shots.md                                 ← 캡션 색인 + 최종 URL
    recording-results.tsv                        ← 로컬 로그 (커밋 안 함)
    handoff.json (갱신)
```

### shots.md 템플릿

```markdown
# {서비스명} — 화면 기록

캡처일: {날짜}
참조 URL: {references.md의 URL}
최종 URL: {실제 렌더링된 URL — 다르면 명시}
케이스: web | external
recording_score: {N}/100

| 파일 | 화면 | URL | 비고 |
|------|------|-----|------|
| landing.png | 메인 페이지 | {캡처한 페이지 URL} | |
| entry.png | 가입 진입점 | {캡처한 페이지 URL} | |
| ... | | | external은 출처 URL |

컷별 URL을 반드시 기록한다 — 재캡처 시 같은 페이지를 다시 찾을 수 있어야 한다.
```

### handoff.json (갱신 필드)

갱신은 **병합**이다 — 기존 handoff.json의 다른 필드(seed_idea, references 등)는 보존하고
아래 필드만 추가/갱신한다. 교체(전체 덮어쓰기) 금지.

```json
{
  "tool": "dk-discovery-bundle:discovery-service-recording",
  "generated_at": "ISO timestamp",
  "recorded_services": [
    {
      "name": "서비스명",
      "case": "web|external",
      "shots": 6,
      "recording_score": 100,
      "final_url": "실제 URL",
      "url_corrected": false
    }
  ],
  "next_step": "dk-discovery-bundle:discovery-brainstorm"
}
```

다음 단계: `commands/v1-brainstorm.md` (기회·가능 영역 도출) → `commands/v1-hypothesize.md` (가설 추론).
