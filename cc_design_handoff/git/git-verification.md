# Git 단계 검증 — project_discovery 스킬용

커밋 prefix는 `design`으로 통일한다. 예: `design(intent-brief): ...`

## Dirty 체크 스코프 규칙 (공통)

```
git status --porcelain 결과를 두 부류로 나눈다:
  스킬 출력 경로(산출물 출력 경로) 안의 dirty → STOP (이전 실행 잔재 — 정리 후 시작)
  출력 경로 밖의 dirty (무관한 파일) → WARN 후 진행. 단, 그 파일들을 절대 stage하지 않는다.
```

## 커밋 전 staged 검증 (공통 — 모든 커밋에 적용)

```
git commit 직전에 반드시:
  git diff --cached --name-only
  → 목록이 이번에 의도한 파일과 정확히 일치하는지 확인
  → 예상 밖 파일이 있으면 git restore --staged <file>로 내리고 커밋
이유: git commit은 "방금 add한 파일"이 아니라 인덱스 전체를 커밋한다.
      이전에 스테이징된 파일이 쓸려 들어가는 사고를 이 한 줄이 막는다.
NEVER use git commit -a.
```

## 루프형 스킬용 (전체 버전)

```
## Git 단계 검증 프로토콜

이 스킬은 매 이터레이션에서 git을 통한 단계 검증을 수행한다.

### 루프 진입 전 (1회)
You MUST complete ALL precondition checks before entering the loop:
  git rev-parse --git-dir || STOP — not a git repo
  git status --porcelain → 상단 "Dirty 체크 스코프 규칙" 적용
  git symbolic-ref HEAD || WARN detached HEAD

### 매 이터레이션 시작
You MUST read git history before deciding the next change:
  git log --oneline -20
  git log --oneline -20 | grep "design"
  If last iteration was keep: git diff HEAD~1
Before choosing next change, CHECK for reverted approaches:
  git log --oneline -20 | grep "Revert.*<approach>" → if found, try DIFFERENT approach

### 변경 후 (검증 전)
You MUST commit before verification:
  git add <specific files only> — NEVER git add -A
  git diff --cached --name-only → 상단 "커밋 전 staged 검증" 적용
  git diff --cached --quiet → if exit 0, log "no-op" and skip
  git commit -m "design(<scope>): <one-sentence description>"
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
  IF git log -1 shows "design(...)" with no results log entry → safe_revert()
  IF clean + log exists → resume normally
```

## 비루프 스킬용 (축소 버전)

```
## Git 단계 검증 (경량)

### 작업 전 (1회)
You MUST check preconditions:
  git rev-parse --git-dir || STOP
  git status --porcelain → 상단 "Dirty 체크 스코프 규칙" 적용

### 작업 완료 후
You MUST commit your changes:
  git add <modified files> — NEVER git add -A
  git diff --cached --name-only → 상단 "커밋 전 staged 검증" 적용
  git commit -m "design(<scope>): <description>"

### 크래시 복구
On restart:
  IF git status --porcelain shows dirty → git checkout -- <files>

### 선택: 이전 히스토리 학습
If previous work exists in this repo:
  git log --oneline -20 | grep "design" — review what was done before
```
