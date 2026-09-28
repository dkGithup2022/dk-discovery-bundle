# Consistency Check Workflow v1 — /dk-discovery-bundle:discovery-consistency-check

> **이 동작은 에이전틱(agentic)한 동작이며, 1회차 끝에서 유저 확인을 받습니다.**
> 아래의 명령을 수행하되, 한 번의 훑어보기로 끝내지 마세요.
> 검사 항목(consistency-check-items.md)을 하나씩 대조하고, "완성 조건" 체크리스트로 스스로 점검해
> 미달 항목이 있으면 해당 단계로 돌아가 다시 수행하세요.
> 이 스킬은 **문서를 고치지 않습니다.** 문제를 찾고 기록하는 것까지만 합니다.
> 유저 확인 지점(문제별 처리 결정)에서는 유저의 결정을 대신 내리지 마세요.

## 목적

와이어프레임까지 끝난 기획 문서 전체(seed-v2 · ui-spec · sitemap · user-flow · wireframe)를 한자리에 놓고,
문서끼리 모순되거나 빠진 것을 찾는다. 찾은 문제마다 유저가 "고친다 / 의도한 것 / 보류"를 정하고,
고치기로 한 것은 discovery-consistency-fix가 반영한다.

이 검사와 수정은 **최대 3회차** 돈다. 새로 나온 문제가 없으면 그 회차에서 끝난다.
- 1회차: 전체 검사. 유저가 문제마다 처리를 정한다 — 대부분의 판단이 여기서 끝난다.
- 2·3회차: 앞 회차 수정이 결정대로 되었는지, 수정이 새로 만든 문제가 있는지만 본다.
  유저 판단이 새로 필요한 문제가 나왔을 때만 묻는다.

검사와 수정을 나눈 이유: 고친 쪽이 자기 수정을 채점하면 수정이 만든 문제를 놓친다.
검사는 고친 적이 없는 눈으로 다시 본다.

## 참조 레퍼런스

```
You MUST read these before starting:
  consistency-check-items.md — 검사 항목, 판단 기준이 되는 결정 기록, 대상 밖
  sitemap-guide.md, user-flow-guide.md, wireframe-guide.md — 번호 규칙과 표기 규칙 (B·H 항목의 기준)
  tone-guide.md — 산출물 언어 규칙 (문제 설명과 질문 문구 포함)
  git/git-verification.md — 커밋 규칙
```

## 입력

```
필수 (run 디렉토리 기준):
  value-proposal/seed-v2.md
  ui-spec/ui-spec.md
  sitemap/sitemap.md
  user-flow/user-flow.md
  wireframe/wireframe.md, wireframe/wireframe.html
  각 단계의 handoff.json
2·3회차 추가:
  consistency/round-{N-1}/findings.md — 앞 회차 문제와 유저 결정
  consistency/round-{N-1}/fix-log.md — 앞 회차 수정 기록
선택:
  git log --oneline | grep "discovery(" — 결정이 언제 어느 문서에 들어갔는지
```

## 진행 순서

### 0. 회차 정하기와 준비

```
consistency/handoff.json을 읽어 이번 회차 N을 정한다 (없으면 1).
N이 4 이상이면 시작하지 않는다 — 3회차에서 끝났다고 안내하고, 남은 문제 목록 위치를 알려준다.
2·3회차면 앞 회차 fix-log.md가 있는지 확인한다. 없으면 수정 단계가 안 돌았으므로
discovery-consistency-fix 실행을 안내하고 중단한다.
```

### 1. 결정 기록 모으기

```
입력 문서의 결정 기록과 handoff.json에서 유저 결정을 모아 한 표로 만든다:
  | 출처(문서·단계) | 무엇을 | 유저 결정 원문 | 유저 결정인가 (원문 / 대리 확인 / 초안) |
이 표가 A 항목(결정 기록과 어긋남)의 기준이다.
```

### 2. 항목별 대조

```
검사 항목 A~H를 순서대로 대조한다. 한 항목씩 끝내고 다음으로 간다.
  - 기계로 셀 수 있는 항목(B 번호, C1 이동 표 양쪽, D1 입력과 요소, H2 mermaid)은
    스크립트로 확인하고, 스크립트가 무엇을 셌는지 findings.md에 적는다
  - 판단이 필요한 항목(A, E, F2)은 두 곳의 원문을 나란히 인용한다
2·3회차: 전체를 다시 보지 않는다. 다음만 본다
  - 앞 회차에서 "고친다"로 정한 문제가 fix-log대로 고쳐졌는가
  - fix-log가 바꾼 곳과, 그 번호를 참조하는 곳에서 새 문제가 생겼는가
  - 앞 회차에서 "의도한 것"이나 "보류"로 정한 문제는 다시 올리지 않는다 (같은 종류·같은 위치)
```

### 3. 문제 기록

```
찾은 문제를 findings.md에 적는다. 문제마다:
  - 번호: R{회차}-{순번} (예: R1-07)
  - 항목: A1~H3
  - 종류: 모순 / 누락 / 미결
  - 위치: 문서·번호 (예: user-flow.md F3 "누가" 칸 / sitemap.md 이동 표 P4 줄)
  - 근거: 두 곳의 원문 인용 (누락이면 요구한 곳의 원문과 "받을 곳 없음")
  - 영향: 이 문제를 그대로 두면 어느 뒤 단계에서 무엇이 잘못되는가 (한 줄)
  - 수정 제안: 어느 문서의 무엇을 어떻게 바꾸면 되는가. 방법이 둘 이상이면 모두 적는다
  - 유저 판단 필요: 예 / 아니오 (번호 밀림 정리처럼 결정 기록만 따르면 되는 것은 아니오)
같은 원인에서 나온 문제 여러 개는 하나로 묶고 위치를 모두 적는다.
```

### 4. 점검

```
"완성 조건"으로 점검한다. 미달이면 2~3단계로 돌아간다.
```

### 5. 처리 결정 — 유저 확인 (1회차 필수, 2·3회차는 판단 필요한 문제가 있을 때만)

```
문제 목록을 유저 판단 필요 여부로 나눠 보여준다.
  - 유저 판단 필요 "아니오": 한 번에 보여주고 "제안대로 고친다"를 한 번에 확인받는다
  - 유저 판단 필요 "예": 문제마다 처리를 묻는다 — 고친다(어느 수정 제안으로) / 의도한 것(유지, 이유) / 보류
    AskUserQuestion 라운드당 최대 4문. 문제가 많으면 영향이 큰 것부터 묻는다
유저 답변 원문을 findings.md의 "처리" 칸에 적는다.
대화형이 아닌 환경이면: "처리" 칸을 비워 두고 "유저 확인 전"으로 표시한 뒤 멈춘다. 처리를 지어내지 않는다.
```

### 6. 산출과 다음 단계 결정

```
findings.md와 consistency/handoff.json을 쓰고 커밋한다.
다음 단계:
  "고친다"가 1건 이상 → discovery-consistency-fix
  "고친다"가 0건 → 종료. 남은 "보류"와 "의도한 것"을 요약해 보여주고 design-request-guide로 넘어간다
  N = 3이고 "고친다"가 남음 → fix는 돌리되, 그 뒤 검사는 하지 않는다 (fix 뒤 종료)
```

## 완성 조건

```
□ 검사 항목 A~H를 모두 대조했다 (2·3회차는 "2. 항목별 대조"의 2·3회차 범위)
□ 기계로 센 항목마다 무엇을 셌는지 적혀 있다
□ 모든 문제에 번호·항목·종류·위치·근거·영향·수정 제안·유저 판단 필요 여부가 있다
□ 근거가 원문 인용이다 (요약이나 해석이 아님)
□ 대리 확인·초안 결정을 유저 결정으로 쓴 문제가 없다
□ 앞 회차에서 "의도한 것"·"보류"로 정한 문제를 다시 올리지 않았다
□ 이 스킬이 입력 문서를 고치지 않았다 (git diff에 consistency/ 밖 변경 없음)
□ 1회차: 모든 문제에 유저 처리가 적혀 있다 (대화형이 아니면 "유저 확인 전" 표시)
□ 내부 용어·발명 조어 노출 0 (tone-guide)
미달 시: 해당 단계로 돌아가 보완한다. 보완 불가하면 "최소 기준 미달: {항목} — {사유}"를 findings.md 상단에 적는다.
```

## Output

```
discovery/{run-id}/
  consistency/
    round-{N}/findings.md
    handoff.json
```

### findings.md 구조

```markdown
# 정합성 검사 {N}회차 — {서비스 한 줄}

진행 상태: 유저 확인 전 | 처리 확정
대조한 문서: (경로와 마지막 커밋)

## 결정 기록 모음
| 출처 | 무엇을 | 유저 결정 원문 | 유저 결정인가 |

## 요약
| 종류 | 건수 | 유저 판단 필요 |

## 문제 목록
### R{N}-01 {한 줄 제목}
- 항목 / 종류 / 위치 / 근거 / 영향 / 수정 제안 / 유저 판단 필요
- 처리: 고친다 (제안 {a}) | 의도한 것 — {이유} | 보류 — 유저 원문: "…"

## 기계 점검 기록
| 항목 | 무엇을 셌나 | 결과 |
```

### handoff.json

```json
{
  "version": "1.0",
  "tool": "dk-discovery-bundle:discovery-consistency-check",
  "generated_at": "ISO timestamp",
  "round": 1,
  "max_rounds": 3,
  "findings": 12,
  "by_kind": { "모순": 5, "누락": 4, "미결": 3 },
  "to_fix": 9,
  "intended": 2,
  "deferred": 1,
  "next_step": "dk-discovery-bundle:discovery-consistency-fix"
}
```

## Commit

```
git add consistency/ 산출물만 → staged 검증 (git/git-verification.md)
git commit -m "discovery(consistency-check): {N}회차 — 문제 {M}건 (고친다 {a}·의도 {b}·보류 {c})"
```
