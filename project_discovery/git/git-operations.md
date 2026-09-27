# Git 연산 주입 가이드 v3 — 스킬/워크플로 레퍼런스

이 문서의 목적: 다른 CC 스킬이나 워크플로를 생성할 때 "git을 통한 단계 검증"을 주입하기 위한 레퍼런스. 참조형 설명과 지시형 실행 블록을 모두 포함한다.

원본 소스: `.claude/skills/autoresearch/references/autonomous-loop-protocol.md`

---

## 0. 전반적인 연산 흐름

autoresearch 루프 한 사이클에서 git 연산은 아래 순서로 일어난다.

```
Phase 0 (1회) ─── 환경 검증: git rev-parse, git status
    │
Phase 1 (매회) ── 학습: git log, git diff, git show
    │
Phase 3 (매회) ── 변경: 코드 수정 + git diff --name-only (원자성 검증)
    │
Phase 4 (매회) ── 기록: git add, git diff --cached, git commit
    │
Phase 5-6 (매회) ─ 판정: 검증 후 keep이면 유지, discard면 git revert
    │
크래시시 ──────── 복구: git status + git log로 상태 판단 후 분기
```

이터레이션 흐름 예시 — 테스트 커버리지 개선 루프:

```
이터레이션 1:
  Phase 1: git log --oneline -20 → 히스토리 없음 (첫 회)
  Phase 3: auth 미들웨어에 테스트 추가
  Phase 4: git add src/auth.test.ts → git commit "experiment(auth): add middleware tests"
  Phase 5: 커버리지 72% → 75% (+3%)
  Phase 6: 올랐으니 keep

이터레이션 2:
  Phase 1: git log → "experiment(auth): add middleware tests — KEPT" 확인
           git diff HEAD~1 → auth.test.ts에 뭘 추가했는지 확인
  Phase 3: 같은 방향으로 API 라우트 테스트 추가
  Phase 4: git add src/api.test.ts → git commit "experiment(api): add route tests"
  Phase 5: 커버리지 75% → 78% (+3%)
  Phase 6: 올랐으니 keep

이터레이션 3:
  Phase 1: git log → 2개의 keep 확인. 테스트 추가가 잘 먹힘.
  Phase 3: DB 레이어 리팩토링 시도
  Phase 4: git add src/db.ts → git commit "experiment(db): refactor query builder"
  Phase 5: 커버리지 78% → 76% (-2%)
  Phase 6: 떨어짐 → discard → git revert HEAD --no-edit

이터레이션 4:
  Phase 1: git log → "Revert experiment(db): refactor query builder" 확인
           → DB 리팩토링은 안 먹힘. 테스트 추가 방향으로 돌아감.
```

---

## 1. 쓰기 연산 — 상태를 변경한다

### git add — in-scope 파일 스테이징

**목적:** 수정한 파일만 명시적으로 스테이징한다. `git add -A`는 금지.

**언제:** Phase 4 (변경 완료 후, 커밋 전)

원본 (`autonomous-loop-protocol.md` Phase 4):

```bash
# Stage ONLY in-scope files (safer than git add -A)
# List the specific files you modified and add them individually:
git add <file1> <file2> ...
# AVOID git add -A — it stages ALL files including .env, node_modules, and user's unrelated work
```

스테이징 후 검증 (원본):

```bash
# After staging, verify with git diff --cached --name-only that only in-scope files are staged
git diff --cached --name-only
```

**실행 지시 (스킬 md에 복사용):**

```
You MUST stage only in-scope files explicitly.
Run: git add <file1> <file2> ...
NEVER use git add -A.
After staging, verify: git diff --cached --name-only — only in-scope files should appear.
```

### git commit — 실험 기록

**목적:** 변경을 검증 전에 커밋한다. 실패시 `git revert` 한 줄로 복원하기 위함.

**언제:** Phase 4 (스테이징 후, 검증 전)

**커밋 단위:** 1이터레이션 = 1변경 = 1커밋이다. Phase 3의 1회 1변경 규칙과 직접 연결된다. 변경이 한 문장으로 설명 가능해야 하므로, 커밋 메시지도 자연스럽게 한 문장이 된다.

원본 (`autonomous-loop-protocol.md` Phase 3 + Phase 4):

```
- Make ONE focused change to in-scope files
- The change should be explainable in one sentence
- Write the description BEFORE making the change (forces clarity)
```

```bash
# Check if there's actually something to commit
git diff --cached --quiet
# → If exit code 0 (no staged changes): skip commit, log as "no-op", go to next iteration
# → If exit code 1 (changes exist): proceed with commit

# Commit with descriptive experiment message
git commit -m "experiment(<scope>): <one-sentence description of what you changed and why>"
```

**커밋 메시지 포맷** (원본):

```
Commit message format: Use conventional commit format with `experiment` type: 
experiment(<scope>): <description>. 
This keeps compatibility with commit-lint while clearly marking autoresearch iterations. 
Example: experiment(auth): increase timeout from 5s to 30s — hypothesis: reduces flaky test failures
```

이 포맷이 중요한 이유: Phase 1에서 `git log --oneline -20 | grep "experiment"`로 실험 히스토리만 필터링할 수 있고, `Revert "experiment(...)"` 패턴으로 실패한 실험을 식별할 수 있다.

**실행 지시 (스킬 md에 복사용):**

```
You MUST commit before running verification. This enables clean rollback.
Run: git diff --cached --quiet
  If exit 0 (no changes): log "no-op", skip to next iteration. Do NOT create empty commit.
  If exit 1 (changes exist): git commit -m "<PREFIX>(<scope>): <description>"
NEVER use --no-verify to bypass hooks.
```

hook 실패 처리 (원본, Phase 4):

```bash
# Hook failure handling: If a pre-commit hook blocks the commit:
# 1. Read the hook's error output to understand WHY it blocked
# 2. If fixable (lint error, formatting): fix the issue, re-stage, and retry
#    — do NOT use --no-verify
# 3. If not fixable within 2 attempts: log as status=hook-blocked,
#    revert the in-scope file changes:
git checkout -- <in-scope files>
#    and move to next iteration
# 4. NEVER bypass hooks with --no-verify
```

### git revert / git reset — 실패한 실험 되돌리기

**목적:** 실패한 실험을 되돌린다. `git revert` 우선 — 히스토리에 남겨서 다음 이터레이션에서 학습 재료로 쓴다.

**언제:** Phase 6 (판정 결과가 discard 또는 crash)

원본 (`autonomous-loop-protocol.md` Phase 6):

```bash
safe_revert() {
  echo "Reverting: $(git log --oneline -1)"

  # Attempt 1: git revert (preserves history — preferred)
  if git revert HEAD --no-edit 2>/dev/null; then
    echo "✓ Reverted via git revert (experiment preserved in history for learning)"
    return 0
  fi

  # Attempt 2: revert conflicted — fallback to reset
  git revert --abort 2>/dev/null
  echo "⚠ Revert conflicted — using git reset --hard HEAD~1"
  git reset --hard HEAD~1
  echo "✓ Reverted via reset (experiment removed from history)"
  return 0
}
```

revert를 우선하는 이유 (원본):

```
git revert preserves the failed experiment in history — this IS the "memory." 
Future iterations can read git log and see what was tried and failed.
git reset --hard destroys the commit entirely — the agent loses memory of what was attempted.
```

**실행 지시 (스킬 md에 복사용):**

```
On discard or crash, you MUST revert:
  Preferred: git revert HEAD --no-edit (preserves history for learning)
  Fallback: git revert --abort && git reset --hard HEAD~1 (if revert conflicts)
Do NOT use git reset --hard as first choice — it destroys experiment history.
```

### git checkout -- \<files\> — 커밋 전 변경 폐기

**목적:** 크래시 복구시 또는 hook 실패시, 커밋되지 않은 변경을 버린다.

**언제:** 크래시 복구 (Phase 3에서 죽었을 때), hook 실패시

원본 (`autonomous-loop-protocol.md` Phase 4, Session crash):

```bash
# Phase 4 safety: If git commit itself fails
git reset HEAD -- .   # unstage everything
git checkout -- <in-scope files>   # restore files to last committed state
```

```
IF working tree is dirty (changes not yet committed):
    git checkout -- <in-scope files>
    LOG "Recovered from session crash: discarded uncommitted modifications"
```

이터레이션 흐름에서 쓰기 연산이 일어나는 시점:

```
이터레이션 5:
  Phase 4: git add src/utils.ts
           git diff --cached --quiet → exit 1 (변경 있음)
           git commit -m "experiment(utils): extract helper functions"
  Phase 5: 커버리지 80% → 82%
  Phase 6: keep → 쓰기 연산 없음 (커밋 유지)

이터레이션 6:
  Phase 4: git add src/utils.ts
           git commit -m "experiment(utils): inline hot-path functions"
  Phase 5: 커버리지 82% → 79% (떨어짐)
  Phase 6: discard → safe_revert() → git revert HEAD --no-edit

이터레이션 7:
  Phase 4: git add src/utils.ts
           git commit -m "experiment(utils): add error boundary tests"
           → pre-commit hook이 lint 에러로 블록
           → lint 수정 후 re-stage, 재시도 → 성공
  Phase 5: 커버리지 82% → 84%
  Phase 6: keep
```

| 연산 | 주입시 변형 | 변형 방법 |
|------|-----------|----------|
| `git add <files>` | 변형 필요 | 스코프를 자신의 스킬 대상 파일로 변경 |
| `git commit -m "experiment(...)"` | 변형 필요 | prefix를 자신의 스킬명으로 (예: `dk-translate`) |
| `safe_revert()` | 변형 불필요 | 그대로 차용 |
| `git checkout -- <files>` | 변형 필요 | 스코프만 변경 |
| `git reset HEAD -- .` | 변형 불필요 | 그대로 차용 |

---

## 2. 읽기 연산 — 상태를 참조한다

### git log — 실험 히스토리 읽기

**목적:** 이전 이터레이션에서 뭘 시도했고 뭐가 성공/실패했는지 파악한다.

**언제:** Phase 1 (매 이터레이션 시작), Phase 2 (방향 결정)

원본 (`autonomous-loop-protocol.md` Phase 1):

```
3. MUST run: git log --oneline -20 to see recent changes
```

```bash
# Step 1: Read recent experiment history
git log --oneline -20
# Shows: kept commits remain, discarded ones were reverted

# Step 3: Check what was tried (avoid repeating failures)
git log --oneline -20 | grep "experiment"
# Shows: all experiment descriptions

# Branch-aware history (원본, Git history usage pattern)
git log --all --oneline
# If working on a branch, see full experiment history
```

git log의 역할 (원본, Phase 1):

```
**Why read git history every time?** Git IS the memory. After rollbacks, 
state may differ from what you expect. The git log shows which experiments 
were kept vs reverted. The git diff of kept changes reveals WHAT specifically 
improved the metric — use this to inform the next iteration. Never assume — always verify.
```

학습 예시 (원본, Git as Memory 섹션):

```
# Agent reads git log and sees:
# a1b2c3d experiment(api): add response caching — KEPT (metric improved)
# d4e5f6g Revert "experiment(api): increase cache TTL to 60s" — REVERTED
# c3d4e5f experiment(api): add cache invalidation on write — KEPT
#
# Agent learns:
# ✓ Caching works (2 kept commits)
# ✗ Increasing TTL didn't help (reverted)
# → Next: try a different cache strategy, NOT longer TTL
```

실패 반복 방지 (원본, Phase 2):

```bash
# Check if this approach was already tried and reverted
if git log --oneline -20 | grep -q "Revert.*$query"; then
  echo "⚠ WARNING: '$query' was tried before and REVERTED — try a different approach"
  return 1
fi
```

**실행 지시 (스킬 md에 복사용):**

```
At the START of every iteration, you MUST read git history:
  git log --oneline -20
  git log --oneline -20 | grep "<PREFIX>"
  If last iteration was "keep": git diff HEAD~1
Before choosing next change, CHECK if this approach was already reverted:
  git log --oneline -20 | grep "Revert.*<approach>"
  If found: try a DIFFERENT approach.
```

### git diff — 성공한 변경 내용 확인

**목적:** 마지막 성공 변경이 정확히 뭘 바꿨는지 확인해서, 같은 방향으로 다음 실험을 설계한다.

**언제:** Phase 1 (직전 이터레이션이 keep이었을 때)

원본 (`autonomous-loop-protocol.md` Phase 1):

```
4. MUST run: git diff HEAD~1 (if last iteration was "keep") to review what worked
```

```bash
# Step 2: Inspect the last successful change
git diff HEAD~1
# Shows: exact diff that improved the metric — informs next experiment

# Step 4: Deep-dive a specific success
git show abc1234 --stat
# Shows: which files were changed in a successful experiment
```

### git status — 현재 상태 확인

**목적:** working tree가 깨끗한지 확인.

**언제:** Phase 0 (루프 진입 전), 크래시 복구시

원본 (`autonomous-loop-protocol.md` Phase 0):

```bash
# 2. Check for dirty working tree
git status --porcelain
# → If dirty: warn user and ask to stash or commit first
#   NEVER proceed with uncommitted user changes
```

이터레이션 흐름에서 읽기 연산이 일어나는 시점:

```
이터레이션 8:
  Phase 1: 
    git log --oneline -20 →
      "experiment(utils): add error boundary tests — KEPT"
      "Revert experiment(utils): inline hot-path functions"
      "experiment(utils): extract helper functions — KEPT"
    → extract와 test 추가는 됐고, inline은 안 됐음.
    
    git diff HEAD~1 →
      src/utils.test.ts에 3개 테스트 추가된 것 확인
    → 테스트 추가 방향이 잘 먹힘. 다른 파일에도 적용.

이터레이션 9:
  Phase 1:
    git log --oneline -20 | grep "experiment" →
      3개의 experiment 커밋 확인
    git show <utils-test-hash> --stat →
      utils.test.ts만 수정됨 확인
    → 패턴: 테스트 파일 단독 추가가 성공 패턴
```

| 연산 | 주입시 변형 | 변형 방법 |
|------|-----------|----------|
| `git log --oneline -20` | 변형 필요 | depth를 태스크 복잡도에 맞게 조정 (기본 20) |
| `git log ... \| grep "experiment"` | 변형 필요 | prefix를 자신의 스킬명으로 (예: `grep "dk-translate"`) |
| `git log --all --oneline` | 변형 불필요 | 브랜치 작업시 그대로 차용 |
| `git diff HEAD~1` | 변형 불필요 | 그대로 차용 |
| `git show <hash> --stat` | 변형 불필요 | 그대로 차용 |
| `git status --porcelain` | 변형 불필요 | 그대로 차용 |

---

## 3. 중간 검증 연산 — 상태를 판단하고 분기한다

### Phase 0 사전 조건 검사

**목적:** 루프 시작 전에 git 환경이 안전한지 확인한다.

원본 (`autonomous-loop-protocol.md` Phase 0):

```bash
# 1. Verify git repo exists
git rev-parse --git-dir 2>/dev/null || echo "FAIL: not a git repo"

# 2. Check for dirty working tree
git status --porcelain
# → If dirty: warn user and ask to stash or commit first

# 3. Check for stale lock files
ls .git/index.lock 2>/dev/null && echo "WARN: stale lock"

# 4. Check for detached HEAD
git symbolic-ref HEAD 2>/dev/null || echo "WARN: detached HEAD"

# 5. Check for git hooks that might interfere
ls .git/hooks/pre-commit .git/hooks/commit-msg 2>/dev/null && echo "INFO: git hook detected"
```

```
**If any FAIL:** Stop and inform user. Do not enter the loop with broken preconditions.
**If any WARN:** Log the warning, proceed with caution, inform user.
```

**실행 지시 (스킬 md에 복사용):**

```
Before starting ANY work, you MUST run precondition checks:
  git rev-parse --git-dir → if fails: STOP, not a git repo
  git status --porcelain → if output: STOP, ask user to stash/commit first
  git symbolic-ref HEAD → if fails: WARN detached HEAD
If any check FAILs: do NOT proceed.
```

### Phase 3 원자성 검증

**목적:** 변경이 1개의 의도에 집중되었는지 확인한다.

원본 (`autonomous-loop-protocol.md` Phase 3):

```bash
# After modifying but before committing, validate atomicity:
FILES_CHANGED=$(git diff --name-only | wc -l)

# Heuristic: >5 files likely means multiple changes — review
if [ "$FILES_CHANGED" -gt 5 ]; then
  echo "WARN: ${FILES_CHANGED} files changed — verify single intent"
fi
```

### Phase 4 커밋 전 검증

**목적:** 실제로 변경이 있는지 확인. 없으면 no-op으로 처리.

원본 (`autonomous-loop-protocol.md` Phase 4):

```bash
# Check if there's actually something to commit
git diff --cached --quiet
# → If exit code 0 (no staged changes): skip commit, log as "no-op", go to next iteration
# → If exit code 1 (changes exist): proceed with commit
```

### 크래시 복구 판정

**목적:** 에이전트가 죽은 후 재시작할 때, 어느 Phase에서 죽었는지 판단한다.

원본 (`autonomous-loop-protocol.md` Session crash):

```bash
# 1. Uncommitted changes in working tree?
DIRTY=$(git status --porcelain)

# 2. Last commit is an unverified experiment?
LAST_MSG=$(git log --oneline -1)
# If it starts with "experiment(" and there's no corresponding results log entry,
# the agent crashed after commit but before verify/decide.
```

```
IF working tree is dirty (changes not yet committed):
    # Agent crashed during Phase 3 (modify) — before commit
    git checkout -- <in-scope files>
    LOG "Recovered from session crash: discarded uncommitted modifications"
    Resume loop from Phase 1

IF last commit is "experiment(...)" with no matching results log entry:
    # Agent crashed after Phase 4 (commit) but before Phase 6 (decide)
    safe_revert()
    LOG "Recovered from session crash: reverted unverified experiment"
    Resume loop from Phase 1

IF working tree is clean AND last commit has a results log entry:
    # Agent crashed after Phase 7 (log) — clean state
    # Nothing to recover. Resume normally.
    Resume loop from Phase 1
```

**실행 지시 (스킬 md에 복사용):**

```
On restart after crash, you MUST check git state:
  IF git status --porcelain shows dirty files → git checkout -- <in-scope files>
  IF git log -1 shows "<PREFIX>(...)" with no results log entry → safe_revert()
  IF clean and log exists → resume normally
```

크래시 복구 분기 다이어그램:

```
재시작시:
  git status --porcelain 실행
    ├── 출력 있음 (dirty) → Phase 3에서 죽음
    │     → git checkout -- <in-scope files>
    │     → Phase 1부터 재개
    └── 출력 없음 (clean)
          → git log --oneline -1 확인
            ├── "<PREFIX>(...)" + results log에 없음 → Phase 4~6에서 죽음
            │     → safe_revert()
            │     → Phase 1부터 재개
            └── results log에 있음 → Phase 7 이후에 죽음 (정상)
                  → 그대로 Phase 1부터 재개
```

| 연산 | 주입시 변형 | 변형 방법 |
|------|-----------|----------|
| Phase 0 전체 (5개 검사) | 변형 필요 | 프로젝트 환경에 맞게 조정 |
| `git diff --name-only \| wc -l` | 변형 불필요 | 그대로 차용 (원자성 검증) |
| `git diff --cached --quiet` | 변형 불필요 | 그대로 차용 |
| 크래시 복구 로직 | 변형 필요 | 커밋 메시지 prefix만 자신의 것으로 변경 |

---

## Scope 결정 가이드

커밋 메시지 `<PREFIX>(<scope>): <description>`에서 scope를 어떻게 정하는가.

autoresearch 원본에서 scope는 유저가 지정한 Scope 필드에서 파생된다:

원본 예시 (`autonomous-loop-protocol.md` Phase 4):
```
experiment(<scope>): <description>
Example: experiment(auth): increase timeout from 5s to 30s
```

원본 시뮬레이션에서 관찰되는 패턴 (참고용 — 원본에 규칙이 명시되어 있지는 않음):
- `Scope: src/api/**/*.ts` → 커밋에서 `experiment(api): ...` 사용
- `Scope: src/auth/**/*.ts` → 커밋에서 `experiment(auth): ...` 사용
- 파일이 1개 (`src/utils.ts`) → `experiment(utils): ...`

주입시: `<PREFIX>`는 자신의 스킬명으로, `<scope>`는 작업 대상의 주요 식별자로 설정한다.

예시:
```
# autoresearch 원본
experiment(auth): add middleware tests

# 번역 스킬
dk-translate(chapter3): revise introduction paragraph

# 디자인 스킬
dk-design(header): update navigation layout
```

---

## 축소 버전 — 비루프/비메트릭 태스크용

루프가 아닌 단발성 작업에서도 git 단계 검증의 일부를 쓸 수 있다. Phase 1(학습)과 Phase 6(keep/discard)은 루프 전용이므로 기본적으로 제외하되, 이전 작업 히스토리가 있는 경우 Phase 1을 선택적으로 포함할 수 있다.

```
필수:
  Phase 0: 사전 조건 검사 (작업 전 1회)
  Phase 4: 변경 후 커밋 (작업 완료 시점)
  크래시 복구: 재시작시 상태 판정

선택:
  Phase 1: 이전 히스토리 학습 (이전 작업이 있는 경우)
```

비루프 흐름 예시:

```
작업 시작:
  git rev-parse --git-dir → OK
  git status --porcelain → clean → OK

작업 수행:
  chapter3.md 번역 완료

작업 완료:
  git add content/chapter3.md
  git commit -m "dk-translate(chapter3): complete Korean translation"

(크래시 복구가 필요한 경우):
  git status --porcelain → "M content/chapter3.md" (dirty)
  → git checkout -- content/chapter3.md
  → 처음부터 다시
```

---

## 전체 시뮬레이션 예시

아래는 "테스트 커버리지 72% → 90% 개선" 루프에서, 위의 모든 git 연산이 실제로 어떤 순서로 일어나는지 보여주는 시뮬레이션이다. 각 이터레이션에서 쓰기/읽기/검증 연산이 어디서 쓰이는지 `[쓰기]` `[읽기]` `[검증]` 태그로 표시한다.

**설정:**
- Goal: 테스트 커버리지 72% → 90%
- Scope: `src/**/*.ts`
- Verify: `npx jest --coverage 2>&1 | grep 'All files' | awk '{print $4}'`
- Guard: `npm run typecheck`

```
=== Phase 0 (1회, 루프 진입 전) ===

[검증] git rev-parse --git-dir → .git (OK)
[검증] git status --porcelain → 출력 없음 (clean, OK)
[검증] git symbolic-ref HEAD → refs/heads/feature/coverage (OK)
[검증] ls .git/index.lock → 없음 (OK)
[검증] ls .husky/pre-commit → 있음 (INFO: husky hook detected)

→ 사전 조건 통과. 루프 진입.
→ 베이스라인 측정: npx jest --coverage → 72.0%

=== 이터레이션 1 ===

Phase 1 (학습):
  [읽기] git log --oneline -20 → 실험 히스토리 없음 (첫 회)
  → 방향: auth 모듈에 테스트가 없으므로 여기부터 시작

Phase 3 (변경):
  auth.test.ts 생성, 미들웨어 테스트 3개 작성
  [검증] git diff --name-only | wc -l → 1 (원자적, OK)

Phase 4 (기록):
  [쓰기] git add src/auth.test.ts
  [검증] git diff --cached --quiet → exit 1 (변경 있음)
  [검증] git diff --cached --name-only → src/auth.test.ts (in-scope 확인)
  [쓰기] git commit -m "experiment(auth): add middleware unit tests"

Phase 5 (검증):
  npx jest --coverage → 75.3% (+3.3%)
  npm run typecheck → exit 0 (guard 통과)

Phase 6 (판정):
  메트릭 올랐고 + guard 통과 → keep
  → 커밋 유지. git 연산 없음.

=== 이터레이션 2 ===

Phase 1 (학습):
  [읽기] git log --oneline -20 →
    "a1b2c3d experiment(auth): add middleware unit tests"
  [읽기] git diff HEAD~1 →
    src/auth.test.ts: +45 lines (테스트 3개)
  → 학습: auth 테스트 추가가 +3.3% 올림. 같은 방향으로 API 테스트 추가.

Phase 3 (변경):
  api.test.ts 생성, 라우트 테스트 4개 작성
  [검증] git diff --name-only | wc -l → 1 (원자적)

Phase 4 (기록):
  [쓰기] git add src/api.test.ts
  [쓰기] git commit -m "experiment(api): add route handler tests"

Phase 5-6:
  커버리지 75.3% → 79.1% (+3.8%) + guard 통과 → keep

=== 이터레이션 3 ===

Phase 1 (학습):
  [읽기] git log --oneline -20 →
    "b2c3d4e experiment(api): add route handler tests"
    "a1b2c3d experiment(auth): add middleware unit tests"
  [읽기] git diff HEAD~1 → api.test.ts에 라우트 테스트 추가 확인
  → 학습: 테스트 추가 패턴이 2연속 성공 (+3.3%, +3.8%). 계속 이 방향.

Phase 3 (변경):
  db.ts를 리팩토링해서 테스트 가능하게 변경
  [검증] git diff --name-only | wc -l → 3 (db.ts, db.test.ts, types.ts)

Phase 4 (기록):
  [쓰기] git add src/db.ts src/db.test.ts src/types.ts
  [쓰기] git commit -m "experiment(db): refactor for testability + add tests"

Phase 5-6:
  커버리지 79.1% → 77.5% (-1.6%)
  → 떨어짐 → discard
  [쓰기] safe_revert() → git revert HEAD --no-edit
  → 히스토리에 "Revert experiment(db): refactor for testability + add tests" 남음

=== 이터레이션 4 ===

Phase 1 (학습):
  [읽기] git log --oneline -20 →
    "c3d4e5f Revert "experiment(db): refactor for testability + add tests""
    "b2c3d4e experiment(api): add route handler tests"
    "a1b2c3d experiment(auth): add middleware unit tests"
  → 학습: DB 리팩토링은 실패. 리팩토링 없이 기존 구조에 테스트만 추가하는 방향으로.
  
  [읽기] git log --oneline -20 | grep "Revert" →
    "Revert experiment(db): refactor for testability"
  → DB 리팩토링 접근은 회피.

Phase 3 (변경):
  기존 db.ts 구조 그대로, db.test.ts만 추가 (리팩토링 없이)
  [검증] git diff --name-only | wc -l → 1 (원자적)

Phase 4 (기록):
  [쓰기] git add src/db.test.ts
  [쓰기] git commit -m "experiment(db): add query builder tests without refactoring"

Phase 5-6:
  커버리지 79.1% → 82.4% (+3.3%) + guard 통과 → keep
  → 학습 성공: 리팩토링 없이 테스트만 추가가 정답이었음.

=== 이터레이션 5 ===

Phase 1 (학습):
  [읽기] git log --oneline -20 →
    "d4e5f6g experiment(db): add query builder tests without refactoring"
    "c3d4e5f Revert "experiment(db): refactor for testability + add tests""
    "b2c3d4e experiment(api): add route handler tests"
    "a1b2c3d experiment(auth): add middleware unit tests"
  → 패턴 인식: 테스트만 추가 = 성공 (3/3), 리팩토링 = 실패 (1/1)

Phase 3 (변경):
  utils.test.ts 추가
  [검증] git diff --name-only | wc -l → 1

Phase 4 (기록):
  [쓰기] git add src/utils.test.ts
  [쓰기] git commit -m "experiment(utils): add string helper tests"
  → husky pre-commit hook이 lint 에러로 블록!
  → lint 수정, re-stage
  [쓰기] git add src/utils.test.ts
  [쓰기] git commit -m "experiment(utils): add string helper tests"
  → 성공

Phase 5-6:
  커버리지 82.4% → 85.7% (+3.3%) + guard 통과 → keep

=== 이터레이션 6 (guard 실패 케이스) ===

Phase 1 (학습):
  [읽기] git log --oneline -20 | grep "experiment" → 4개의 성공 확인
  → 남은 uncovered 영역: validation 모듈

Phase 3-4:
  validation.test.ts 추가 + validation.ts에서 타입 변경
  [쓰기] git add src/validation.test.ts src/validation.ts
  [쓰기] git commit -m "experiment(validation): add input validation tests"

Phase 5:
  커버리지 85.7% → 88.2% (+2.5%) ← 올랐음

Phase 5.5 (Guard):
  npm run typecheck → exit 1 (타입 에러!) ← guard 실패

Phase 6:
  메트릭은 올랐지만 guard 실패 → rework 시도 (최대 2회)
  [쓰기] safe_revert() → git revert HEAD --no-edit
  
  Rework 1회차:
    validation.ts 타입 수정 방식 변경 + 테스트 유지
    [쓰기] git add src/validation.test.ts src/validation.ts
    [쓰기] git commit -m "experiment(validation): rework — fix type signature"
    커버리지 88.0% + typecheck 통과 → keep (reworked)

=== (에이전트 크래시 발생 — 이터레이션 7 도중 죽음) ===

Phase 3에서 src/cache.ts를 수정하던 중 API 타임아웃으로 에이전트 죽음.
커밋은 아직 안 됨.

=== 재시작시 복구 ===

[검증] git status --porcelain → "M src/cache.ts" (dirty!)
→ Phase 3에서 죽은 것으로 판단
[쓰기] git checkout -- src/cache.ts
→ 복구 완료. Phase 1부터 재개.

=== 이터레이션 7 (재시작) ===

Phase 1:
  [읽기] git log --oneline -20 →
    가장 최근이 "experiment(validation): rework — fix type signature — KEPT"
  → cache.ts 시도는 히스토리에 없음 (커밋 전에 죽었으므로)
  → cache 모듈 테스트 추가 재시도

Phase 3-4:
  cache.test.ts 생성
  [쓰기] git add src/cache.test.ts
  [쓰기] git commit -m "experiment(cache): add cache invalidation tests"

Phase 5-6:
  커버리지 88.0% → 90.3% (+2.3%) + guard 통과 → keep

=== 목표 달성 (90% 초과) → 루프 종료 ===

최종 git log:
  experiment(cache): add cache invalidation tests — KEPT
  experiment(validation): rework — fix type signature — KEPT
  Revert "experiment(validation): add input validation tests"
  experiment(utils): add string helper tests — KEPT
  experiment(db): add query builder tests without refactoring — KEPT
  Revert "experiment(db): refactor for testability + add tests"
  experiment(api): add route handler tests — KEPT
  experiment(auth): add middleware unit tests — KEPT

결과: 8 이터레이션, 6 keep, 2 discard (1 rework 성공)
베이스라인 72.0% → 최종 90.3% (+18.3%)
```

이 시뮬레이션에서 참조한 원본 소스의 해당 섹션:

| 시뮬레이션 요소 | 원본 위치 |
|----------------|----------|
| Phase 0 사전 조건 5개 검사 | `autonomous-loop-protocol.md` Phase 0 |
| Phase 1 git log + git diff 학습 | `autonomous-loop-protocol.md` Phase 1, Git as Memory |
| Phase 3 원자성 검증 (git diff --name-only) | `autonomous-loop-protocol.md` Phase 3, Enforcing Atomicity |
| Phase 4 커밋 전 검증 (git diff --cached --quiet) | `autonomous-loop-protocol.md` Phase 4 |
| Phase 4 커밋 메시지 포맷 (experiment prefix) | `autonomous-loop-protocol.md` Phase 4, Commit message format |
| Phase 4 hook 실패 처리 (lint 수정 후 재시도) | `autonomous-loop-protocol.md` Phase 4, Hook failure handling |
| Phase 6 discard → safe_revert() | `autonomous-loop-protocol.md` Phase 6, safe_revert() |
| Phase 6 guard 실패 → rework (최대 2회) | `autonomous-loop-protocol.md` Phase 5.5, Guard failure recovery |
| 크래시 복구 (dirty tree → checkout) | `autonomous-loop-protocol.md` Session crash, Recovery rules |
| git log에서 Revert 패턴으로 실패 학습 | `autonomous-loop-protocol.md` Git as Memory, Example: Memory in Action |

---

## 주입 템플릿 — 스킬 md에 복사용

아래를 자신의 스킬 md에 붙여넣고, `<PREFIX>`와 `<SCOPE_GLOB>`만 변경한다.

예시: autoresearch는 `<PREFIX>` = `experiment`, 번역 스킬이면 `<PREFIX>` = `dk-translate`.

### 루프형 스킬용 (전체 버전)

```
## Git 단계 검증 프로토콜

이 스킬은 매 이터레이션에서 git을 통한 단계 검증을 수행한다.

### 루프 진입 전 (1회)
You MUST complete ALL precondition checks before entering the loop:
  git rev-parse --git-dir || STOP — not a git repo
  git status --porcelain → if any output, STOP and ask user to stash/commit
  git symbolic-ref HEAD || WARN detached HEAD

### 매 이터레이션 시작
You MUST read git history before deciding the next change:
  git log --oneline -20
  git log --oneline -20 | grep "<PREFIX>"
  If last iteration was keep: git diff HEAD~1
Before choosing next change, CHECK for reverted approaches:
  git log --oneline -20 | grep "Revert.*<approach>" → if found, try DIFFERENT approach

### 변경 후 (검증 전)
You MUST commit before verification:
  git add <specific files only> — NEVER git add -A
  git diff --cached --quiet → if exit 0, log "no-op" and skip
  git commit -m "<PREFIX>(<scope>): <one-sentence description>"
  If hook blocks: fix and retry. NEVER use --no-verify.
  If hook blocks 2x: git checkout -- <files>, log "hook-blocked", move on.

### 판정 후
IF keep: do nothing (commit stays)
IF discard or crash:
  safe_revert() {
    git revert HEAD --no-edit || { git revert --abort; git reset --hard HEAD~1; }
  }

### 크래시 복구
On restart, you MUST check git state before resuming:
  IF git status --porcelain shows dirty files → git checkout -- <in-scope files>
  IF git log -1 shows "<PREFIX>(...)" with no results log entry → safe_revert()
  IF clean + log exists → resume normally
```

### 비루프 스킬용 (축소 버전)

```
## Git 단계 검증 (경량)

### 작업 전 (1회)
You MUST check preconditions:
  git rev-parse --git-dir || STOP
  git status --porcelain → if dirty, STOP

### 작업 완료 후
You MUST commit your changes:
  git add <modified files> — NEVER git add -A
  git commit -m "<PREFIX>(<scope>): <description>"

### 크래시 복구
On restart:
  IF git status --porcelain shows dirty → git checkout -- <files>

### 선택: 이전 히스토리 학습
If previous work exists in this repo:
  git log --oneline -20 | grep "<PREFIX>" — review what was done before
```
