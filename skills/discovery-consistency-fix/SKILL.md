---
name: discovery-consistency-fix
description: discovery-consistency-check가 찾고 유저가 "고친다"로 정한 문제만 앞 단계 문서(seed-v2·ui-spec·sitemap·user-flow·wireframe)에 반영한다. 기존 번호를 바꾸지 않고, 고친 곳을 가리키는 참조를 따라 맞추며, 새 판단이 필요한 곳은 다음 회차 검사로 넘긴다.
argument-hint: "[Round: <회차 번호>]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

EXECUTE IMMEDIATELY — 판단은 검사 단계에서 끝났다. 유저가 "고친다"로 정한 것만 고치고, 새 판단은 하지 않는다.

## 전제 조건 (실행 전 확인)

1. consistency/round-{N}/findings.md가 있고 진행 상태가 "처리 확정"인지 확인한다.
   없거나 "유저 확인 전"이면 discovery-consistency-check의 처리 결정을 먼저 받으라고 안내 후 중단.
2. 처리가 "고친다"인 문제가 0건이면 고칠 것이 없다고 알리고 종료한다.

## Argument Parsing

- `Round:` — 회차 (기본: consistency/handoff.json의 현재 회차)

## Execution

1. Read the workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/v1-consistency-fix-workflow.md`
2. Read the check items: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/consistency-check-items.md`
3. Read the format guides: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/sitemap-guide.md`, `user-flow-guide.md`, `wireframe-guide.md`
4. Read the tone guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tone-guide.md`
5. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
6. Execute: 준비(와이어프레임 생성기 확인, 이어서 하기) → 수정 순서 정하기(seed-v2 → ui-spec → sitemap → user-flow → wireframe) → 문서별 수정 → 참조 따라가기 → 기록(고친 것 / 넘김 / 고쳤지만 확인할 점) → 완성 조건 점검
7. Generate consistency/round-{N}/fix-log.md + 고친 문서들 + consistency/handoff.json 갱신

IMPORTANT: Stream all output live — never run in background.
기존 번호는 바꾸지 않는다 — 중간 삽입은 소문자 덧붙임(P11-3a), 삭제는 취소선. "의도한 것"·"보류" 문제는 건드리지 않는다.
와이어프레임은 wireframe/.gen/ 그림 데이터를 고치고 생성기로 다시 만든다. 결정 기록의 옛 줄은 지우지 않고 덧붙인다.
Next step after completion: 3회차 전이면 `/dk-discovery-bundle:discovery-consistency-check` (다음 회차), 3회차면 `/dk-discovery-bundle:design-request-guide`.
