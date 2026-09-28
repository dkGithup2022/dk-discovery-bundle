# Consistency Fix Workflow v1 — /dk-discovery-bundle:discovery-consistency-fix

> **이 동작은 에이전틱(agentic)한 동작입니다.**
> 아래의 명령을 수행하되, 한 번의 수정으로 끝내지 마세요.
> "완성 조건" 체크리스트로 스스로 점검하고, 미달 항목이 있으면 해당 단계로 돌아가 다시 수행하세요.
> 이 스킬은 **유저가 "고친다"로 정한 문제만** 고칩니다. 새로 판단하지 않습니다.
> 고치다가 유저 판단이 새로 필요한 곳이 나오면, 스스로 정하지 말고 다음 회차 검사로 넘기세요.

## 목적

discovery-consistency-check가 찾고 유저가 처리를 정한 문제 중 "고친다"인 것을 앞 단계 문서에 반영한다.
수정이 끝나면 다음 회차 검사가 수정 결과를 다시 본다 (최대 3회차).

이 스킬이 스스로 판단하지 않는 이유: 판단이 필요한 것은 검사 단계에서 유저가 이미 정했다.
수정 단계가 새 판단을 섞으면, 유저가 모르는 결정이 문서에 들어가고 다음 검사도 그것을 기준 삼게 된다.

## 참조 레퍼런스

```
You MUST read these before starting:
  consistency-check-items.md — 문제의 종류와 판단 기준
  sitemap-guide.md, user-flow-guide.md, wireframe-guide.md — 고칠 문서의 형식과 번호 규칙
  tone-guide.md — 산출물 언어 규칙
  git/git-verification.md — 커밋 규칙
```

## 입력

```
필수:
  consistency/round-{N}/findings.md — 처리가 확정된 문제 목록 (진행 상태: 처리 확정)
  고칠 대상 문서: seed-v2.md, ui-spec.md, sitemap.md, user-flow.md, wireframe.md, wireframe.html
findings.md가 "유저 확인 전"이면 시작하지 않는다 — 검사 단계의 처리 결정을 먼저 받으라고 안내한다.
```

## 진행 순서

### 0. 준비

```
consistency/handoff.json에서 회차 N을 읽는다. round-{N}/fix-log.md가 이미 있으면
이어서 하는지 확인한다 (완료된 문제는 건너뛴다).
findings.md에서 처리가 "고친다"인 문제만 뽑는다.
```

### 1. 수정 순서 정하기

```
앞 단계 문서부터 고친다: seed-v2 → ui-spec → sitemap → user-flow → wireframe
  뒤 문서는 앞 문서의 번호와 이름을 참조하므로, 앞을 먼저 고쳐야 뒤를 한 번에 맞출 수 있다.
한 문제가 여러 문서에 걸치면 문서 순서대로 나눠 고친다.
```

### 2. 문서별 수정

```
문제마다 findings.md의 수정 제안 중 유저가 고른 것을 그대로 적용한다.
번호 규칙 (모든 문서 공통):
  - 한 번 붙인 페이지·섹션·흐름·기능 번호는 바꾸지 않는다
  - 섹션을 중간에 넣어야 하면 앞 섹션 번호에 소문자를 붙인다 (P11-3 뒤 → P11-3a). 뒤 번호를 밀지 않는다
  - 지운 것은 취소선으로 남긴다. 번호를 재사용하지 않는다
수정한 문서의 결정 기록에 한 줄 추가:
  | consistency {N}회차 | {무엇을} | 검사 R{N}-{순번} 처리 원문 인용 |
진행 상태·확정 표시는 건드리지 않는다 (이 수정은 이미 유저가 정한 것을 반영하는 것이다).
```

### 3. 참조 따라가기

```
고친 곳을 가리키는 뒤 문서의 참조를 찾아 함께 맞춘다.
  예: sitemap.md에서 섹션 이름을 바꿨으면 user-flow.md 노드 글자와 wireframe.html 박스 이름도 바꾼다
참조를 맞추는 것은 새 판단이 아니다. 단, 맞추려면 새 판단이 필요하면(예: 이름을 바꿨더니 흐름의 분기가
의미를 잃음) 고치지 않고 fix-log.md의 "다음 회차로 넘김"에 적는다.
wireframe.html은 바뀐 섹션·박스만 고친다. 전체를 다시 그리지 않는다.
```

### 4. 기록

```
fix-log.md에 문제마다: 문제 번호, 고친 문서·위치, 바꾸기 전 원문, 바꾼 뒤 원문, 따라 고친 참조.
```

### 5. 점검

```
"완성 조건"으로 점검한다. 미달이면 2~4단계로 돌아간다.
기계로 확인할 수 있는 것(번호 참조가 모두 존재하는가, mermaid 파싱, HTML id 중복)은 스크립트로 확인한다.
```

### 6. 산출과 다음 단계

```
fix-log.md와 consistency/handoff.json을 갱신하고 커밋한다.
다음 단계:
  N < 3 → discovery-consistency-check ({N+1}회차)
  N = 3 → 종료. "다음 회차로 넘김"이 남아 있으면 목록으로 보여주고, 유저가 직접 판단하도록 안내한다.
          남은 것이 없으면 design-request-guide로 넘어간다.
```

## 완성 조건

```
□ 처리가 "고친다"인 문제가 모두 fix-log.md에 있다 (고침 / 다음 회차로 넘김 중 하나)
□ "의도한 것"·"보류" 문제는 하나도 고치지 않았다
□ 바꾼 곳마다 바꾸기 전 원문과 바꾼 뒤 원문이 있다
□ 기존 번호가 바뀐 곳이 없다 (새 번호는 소문자 덧붙임만, 지운 것은 취소선)
□ 고친 곳을 가리키는 뒤 문서의 참조가 모두 맞춰졌다 (스크립트로 확인)
□ 수정한 문서마다 결정 기록에 consistency 줄이 있다
□ mermaid가 파싱되고, wireframe.html의 id가 겹치지 않는다
□ 새 판단이 필요한 곳을 스스로 정하지 않고 "다음 회차로 넘김"에 적었다
□ 내부 용어·발명 조어 노출 0 (tone-guide)
미달 시: 해당 단계로 돌아가 보완한다. 보완 불가하면 "최소 기준 미달: {항목} — {사유}"를 fix-log.md 상단에 적는다.
```

## Output

```
discovery/{run-id}/
  consistency/
    round-{N}/fix-log.md
    handoff.json (갱신)
  (그리고 고친 앞 단계 문서들)
```

### fix-log.md 구조

```markdown
# 정합성 수정 {N}회차

기준: round-{N}/findings.md (처리 확정)

## 고친 것
| 문제 | 문서·위치 | 바꾸기 전 | 바꾼 뒤 | 따라 고친 참조 |

## 다음 회차로 넘김
| 문제 | 왜 고치지 못했나 | 필요한 판단 |
```

### handoff.json (갱신 필드)

```json
{
  "tool": "dk-discovery-bundle:discovery-consistency-fix",
  "round": 1,
  "fixed": 8,
  "passed_to_next_round": 1,
  "touched_docs": ["ui-spec/ui-spec.md", "sitemap/sitemap.md", "user-flow/user-flow.md", "wireframe/wireframe.html"],
  "next_step": "dk-discovery-bundle:discovery-consistency-check"
}
```

## Commit

```
git add consistency/ 와 이번에 고친 문서만 → staged 검증 (git/git-verification.md)
git commit -m "discovery(consistency-fix): {N}회차 — 고침 {a}건·넘김 {b}건 ({고친 문서 나열})"
```
