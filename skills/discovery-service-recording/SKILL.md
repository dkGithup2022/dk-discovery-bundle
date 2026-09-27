---
name: discovery-service-recording
description: research에서 수집한 서비스들의 화면을 캡처하여 "이미지만 보고 서비스 파악이 가능한" 시각 기록을 만든다.
argument-hint: "[Target: all | <service-name>[, ...]] [MaxShots: N]"
---

> 이 스킬이 읽는 문서는 `${CLAUDE_PLUGIN_ROOT}/project_discovery/` 아래에 있다. 그 문서들 안에 나오는 상대 경로(`references/`, `git/`, `loop/`, `tone-guide.md` 등)도 이 폴더 기준으로 찾는다.
> 산출물은 플러그인 폴더가 아니라 **현재 작업 중인 프로젝트** 아래에 만든다.

EXECUTE IMMEDIATELY — do not deliberate, do not ask clarifying questions before reading the protocol.

## Argument Parsing (do this FIRST)

Extract from $ARGUMENTS:
- `Target:` — "all" (기본값, references.md의 전체 서비스) 또는 서비스명 쉼표 목록 (예: `Target: 문토, Meetup` — 해당 서비스만 재캡처)
- `MaxShots:` — 서비스당 캡처 상한 (기본 8)

## Execution

1. Read the recording workflow: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/service-recording-workflow.md`
2. Read the tools guide: `${CLAUDE_PLUGIN_ROOT}/project_discovery/references/tools-guide.md` (특히 "Playwright 화면 캡처" 섹션)
3. Read the git verification: `${CLAUDE_PLUGIN_ROOT}/project_discovery/git/git-verification.md`
4. Load references.md + research의 handoff.json (없으면 → 사용자에게 research 먼저 실행 안내 후 중단)
5. Execute per-service recording loop (Probe → 기본 캡처 → 계획 → 탐색 캡처 → Verify → 기록·Commit)
6. Generate screenshots/{service}/ + shots.md + analysis 링크 갱신 + handoff.json

IMPORTANT: Start executing immediately. Stream all output live — never run in background.
You MUST run Bash("sleep 3") between each WebSearch/WebFetch/Playwright call.
You MUST record the final rendered URL when it differs from the reference URL.
