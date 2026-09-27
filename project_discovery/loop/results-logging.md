# Results Logging Protocol

Track every iteration in a structured log. Enables pattern recognition and prevents repeating failed experiments.

> **적용 범위 (project_discovery에서 읽을 때 — 먼저 읽을 것)**
>
> 이 문서에서 가져갈 원칙: ① 매 이터레이션을 TSV 한 줄로 기록, ② 시작 시 최근 로그를
> 읽어 패턴 인식·중복 방지, ③ 로그는 로컬 파일 — .gitignore로 제외하고 커밋하지 않는다.
>
> **TSV 파일명과 컬럼 스키마는 각 워크플로 문서가 정의하며, 그것이 이 문서보다 우선한다:**
> - research: `research-results.tsv` (research-workflow.md Phase 7)
> - service-recording: `recording-results.tsv` (service-recording-workflow.md Phase 7)
>
> 아래 본문의 `planner-results.tsv` 파일명과 metric/delta/guard 컬럼은 코드-실험 루프용
> 예시다 — 조사 루프에 그대로 쓰지 않는다.

## Setup & Initialization

Autoresearch creates the log automatically at Phase 0 (baseline). The agent runs these commands during initialization:

```bash
# 1. Create log file with metric direction and header
echo "# metric_direction: higher_is_better" > planner-results.tsv
echo -e "iteration\tcommit\tmetric\tdelta\tguard\tguard-metric\tstatus\tdescription" >> planner-results.tsv

# 2. Add to .gitignore (log is local, not committed)
echo "planner-results.tsv" >> .gitignore

# 3. Run verify command to establish baseline metric
BASELINE=$(npx jest --coverage 2>&1 | grep 'All files' | awk '{print $4}')

# 4. Record baseline as iteration 0
COMMIT=$(git rev-parse --short HEAD)
echo -e "0\t${COMMIT}\t${BASELINE}\t0.0\tpass\tbaseline\tinitial state — coverage ${BASELINE}%" >> planner-results.tsv
```

## Logging Function

Called at Phase 7 of every iteration after the keep/discard/crash decision:

```bash
# Function: log_iteration
log_iteration() {
  local iteration=$1 commit=$2 metric=$3 delta=$4 guard=$5 guard_metric=$6 status=$7 description=$8
  echo -e "${iteration}\t${commit}\t${metric}\t${delta}\t${guard}\t${guard_metric}\t${status}\t${description}" \
    >> planner-results.tsv
}

# Usage examples:
log_iteration 1 "b2c3d4e" "87.1" "+1.9" "pass" "-" "keep" "add tests for auth middleware"
log_iteration 2 "-" "86.5" "-0.6" "-" "-" "discard" "refactor test helpers (broke 2 tests)"
log_iteration 3 "-" "0.0" "0.0" "-" "-" "crash" "add integration tests (DB connection failed)"
log_iteration 4 "-" "-" "-" "-" "-" "no-op" "attempted to modify read-only config"
log_iteration 5 "-" "-" "-" "-" "-" "hook-blocked" "pre-commit lint rejected formatting"
log_iteration 6 "-" "-" "-" "-" "-" "metric-error" "verify output was 'PASS' — not a number"
```

## Reading & Using the Log

```bash
# Phase 1 (Review): Read recent entries for pattern recognition
tail -20 planner-results.tsv

# Count outcomes for progress tracking
KEEPS=$(grep -c 'keep' planner-results.tsv || echo 0)
DISCARDS=$(grep -c 'discard' planner-results.tsv || echo 0)
CRASHES=$(grep -c 'crash' planner-results.tsv || echo 0)

# Detect stuck state: >5 consecutive discards triggers recovery
LAST_5=$(tail -5 planner-results.tsv | awk -F'\t' '{print $6}')
# If all 5 are "discard" → trigger "When Stuck" protocol (re-read all files, try radical change)

# Pattern recognition: which file changes succeed?
# Cross-reference "keep" rows with git log to find winning patterns
grep 'keep' planner-results.tsv | awk -F'\t' '{print $7}'
# → Shows descriptions of all successful changes
```

## Integration with the Autoresearch Loop

Where logging fits in the loop lifecycle:

```
Phase 0 (Setup):    → CREATE log file, record baseline (iteration 0)
Phase 1 (Review):   → READ last 10-20 log entries for pattern recognition
Phase 3-6 (Loop):   → Modify, Commit, Verify, Decide
Phase 7 (Log):      → APPEND new row after keep/discard/crash decision
Phase 8 (Repeat):   → Back to Phase 1 (reads updated log)
```

Complete end-to-end example:

```
/autoresearch
Goal: Increase test coverage from 72% to 90%
Scope: src/**/*.ts
Verify: npx jest --coverage 2>&1 | grep 'All files' | awk '{print $4}'
Guard: npm run typecheck

# Internal lifecycle:
# 1. Agent creates planner-results.tsv with baseline 72.0
# 2. Agent reads log (empty except baseline) → decides first experiment
# 3. Agent modifies code, commits, runs verify → gets 74.5
# 4. Agent appends: "1  b2c3d4e  74.5  +2.5  pass  keep  add auth middleware tests"
# 5. Next iteration: agent reads log, sees auth tests worked → tries similar pattern
# 6. Continues until coverage reaches 90% or iterations exhausted
```

## Log Format (TSV)

Create `planner-results.tsv` in the working directory (gitignored):

```tsv
iteration	commit	metric	delta	guard	guard-metric	status	description
```

### Columns

| Column | Type | Description |
|--------|------|-------------|
| iteration | int | Sequential counter starting at 0 (baseline) |
| commit | string | Short git hash (7 chars), "-" if reverted |
| metric | float | Measured value from verification |
| delta | float | Change from previous best (negative = improved for "lower is better") |
| guard | enum | `pass`, `fail`, or `-` (no guard configured) |
| guard-metric | float or `-` | Measured guard-metric value (metric-valued guards only). `-` for pass/fail guards or no guard. |
| status | enum | `baseline`, `keep`, `keep (reworked)`, `discard`, `crash`, `no-op`, `hook-blocked`, `metric-error` |
| description | string | One-sentence description of what was tried |

### Example (pass/fail guard)

```tsv
iteration	commit	metric	delta	guard	guard-metric	status	description
0	a1b2c3d	85.2	0.0	pass	-	baseline	initial state — test coverage 85.2%
1	b2c3d4e	87.1	+1.9	pass	-	keep	add tests for auth middleware edge cases
2	-	86.5	-0.6	-	-	discard	refactor test helpers (broke 2 tests)
3	-	0.0	0.0	-	-	crash	add integration tests (DB connection failed)
4	-	88.9	+1.8	fail	-	discard	inline hot-path functions (guard: 3 tests broke)
5	c3d4e5f	88.3	+1.2	pass	-	keep	add tests for error handling in API routes
6	d4e5f6g	89.0	+0.7	pass	-	keep	add boundary value tests for validators
```

### Example (metric-valued guard — bundle size with 5% threshold)

```tsv
iteration	commit	metric	delta	guard	guard-metric	status	description
0	a1b2c3d	85.2	0.0	pass	48200	baseline	coverage 85.2%, bundle 48200 bytes
1	b2c3d4e	87.1	+1.9	pass	48500	keep	add auth tests (bundle +300 bytes, within 5%)
2	-	88.0	+0.9	fail	51500	discard	add integration tests (bundle +3300, exceeds 5% of 48200)
3	c3d4e5f	87.8	+0.7	pass	47900	keep	add unit tests (bundle decreased)
```

**Note:** When guard fails, the metric may have improved but the change is still discarded. The guard column makes this visible in the log. For metric-valued guards, the guard-metric column lets you track drift over time even when individual iterations stay within threshold.

## Log Management

- Create at setup (iteration 0 = baseline)
- Append after EVERY iteration (including crashes)
- Do NOT commit this file to git (add to .gitignore)
- Read last 10-20 entries at start of each iteration for context
- Use to detect patterns: what kind of changes tend to succeed?

## Summary Reporting

Every 10 iterations (or at loop completion in bounded mode), print a brief summary:

```
=== Autoresearch Progress (iteration 20) ===
Baseline: 85.2% → Current best: 92.1% (+6.9%)
Keeps: 8 | Discards: 10 | Crashes: 2
Last 5: keep, discard, discard, keep, keep
```

## Metric Direction

Clarify at setup whether lower or higher is better:
- **Lower is better:** val_bpb, response time (ms), bundle size (KB), error count
- **Higher is better:** test coverage (%), lighthouse score, throughput (req/s)

Record direction in first line of results log as a comment:
```
# metric_direction: higher_is_better
```
