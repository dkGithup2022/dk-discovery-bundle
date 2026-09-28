# wireframe-gen — 와이어프레임 HTML 생성기

discovery-wireframe 스킬이 wireframe.html과 wireframe.md를 만들 때 쓰는 생성기다.
예시 run(크루 매거진 커뮤니티 앱) 테스트 실행에서 에이전트가 즉석으로 짠 스크립트를 가져와,
경로만 인자로 바꿨다. 같은 데이터로 돌리면 테스트 실행 때와 바이트 단위로 같은 HTML이 나온다.

## 왜 고정해 두는가

생성기가 없으면 에이전트가 실행할 때마다 그림 코드를 새로 짠다. 그러면 결과 모양이 매번 달라지고,
실행 시간과 토큰의 대부분이 그림 코드 작성에 쓰인다. 생성기를 고정해 두면 에이전트는
**무엇을 그릴지(데이터)만** 만들고, 그림은 매번 같은 스크립트가 그린다.

## 무엇을 읽고 무엇을 쓰는가

```
읽는 것:
  {RUN}/sitemap/sitemap.md        — 페이지 목록, 공통 섹션, 페이지별 섹션 목록, 이동 표
  {RUN}/user-flow/user-flow.md    — 화면 상태 목록, 흐름별 mermaid 그림
  {DATA}/dsl.py                   — 섹션 안에 무엇을 그릴지 (에이전트가 run마다 새로 쓴다)
  {DATA}/candidates.json          — 추가 후보 (사이트맵 대조 결과)
  {DATA}/decisions.json           — 결정 기록 (mdgen.py만)
  {DATA}/pageextra.json           — 페이지별 덧붙임: 첫 화면 경계 아래 핵심 행동, 경쟁사 참조 (mdgen.py만)
쓰는 것:
  {RUN}/wireframe/wireframe.html  — gen.py
  {RUN}/wireframe/wireframe.md    — mdgen.py
  {DATA}/info.json                — gen.py가 센 페이지·상태·흐름 수 (mdgen.py가 읽는다)
```

## 실행

```bash
# 첫 묶음만 (유저 확인 1 전)
RUN=discovery/{run-id} SCOPE=first FIRST=P1,P2,P5 STATUS="첫 묶음 확인 전" \
  python3 ${CLAUDE_PLUGIN_ROOT}/project_discovery/tools/wireframe-gen/gen.py

# 전체
RUN=discovery/{run-id} STATUS="전체 확정" \
  python3 ${CLAUDE_PLUGIN_ROOT}/project_discovery/tools/wireframe-gen/gen.py
RUN=discovery/{run-id} STATUS="전체 확정" \
  python3 ${CLAUDE_PLUGIN_ROOT}/project_discovery/tools/wireframe-gen/mdgen.py
```

| 환경 변수 | 뜻 | 기본값 |
|----------|-----|-------|
| `RUN` | run 디렉토리 | 없음 (필수) |
| `DATA` | 이 run의 그림 데이터 폴더 | `{RUN}/wireframe/.gen` |
| `SCOPE` | `first`면 공통 섹션과 첫 묶음만, `all`이면 전부 | `all` |
| `FIRST` | 첫 묶음 페이지 번호, 쉼표 구분 | 없음 |
| `STATUS` | 진행 상태 문구. "유저 확인 전 초안"이면 상단에 초안 표시 | `전체 확정` |
| `WARN` | 상단 경고 문구, `\|\|`로 구분 | 없음 |

## dsl.py 쓰는 법

`example/dsl.py`가 예시 run의 전체 데이터다. 새 run에서는 이 파일을 본보기로 `{DATA}/dsl.py`를 새로 쓴다.

```
COMMON       = { "공통 섹션 이름": [요소, …] }
PAGES        = { "P1": { 섹션번호: [요소, …] | C("공통 섹션 이름", [주석], 핵심버튼여부) } }
STATES       = { ("P5", "비로그인"): { 바뀐 섹션번호: [요소, …] } }
EXTRA_STATES = [ ("P11", "빈 목록", "언제 생기는가") ]   # 와이어프레임 단계에서 추가한 상태
```

요소는 튜플이고 첫 값이 종류다 (전체 목록은 gen.py의 `el_html`):

| 종류 | 모양 | 예 |
|------|------|-----|
| `t` / `s` | 제목 막대 / 작은 글 막대 + 이름 | `("t", "제목")` |
| `l` | 글 줄 N개 | `("l", 3, "소개")` |
| `img` / `imgs` | X자 이미지 자리 (높이) / 작은 이미지 N개 | `("img", "표지 사진", 120)` |
| `btn` / `btnp` / `btns` | 버튼 / 핵심 행동 버튼(진한 회색) / 버튼 묶음(몇 번째가 핵심) | `("btns", ["팔로우", "가입 신청"], 1)` |
| `in` | 입력칸 (높이) | `("in", "짧은 글", 70)` |
| `tabs` / `tabbar` / `chips` | 탭(선택 번호) / 하단 탭 바 / 칩 | `("tabs", ["아카이브", "이벤트"], 0)` |
| `h` | 가로 한 줄 (안에 `ic` 아이콘, `tb` 제목 등) | `("h", [("ic", "뒤로 가기"), ("tb", "페이지 제목")])` |
| `card` / `list` | 카드 N개 / 목록 줄 N개 | `("card", [요소…], 2, "매거진 카드")` |
| `empty` / `err` / `load` | 빈 목록 안내 / 오류 표시 / 불러오는 중 막대 | `("empty", "글이 없다는 안내")` |
| `note` | 동작 주석 (··· 로 시작) | `("note", "누르면 M1")` |

요소 이름은 사이트맵 섹션의 "담는 내용"에 적힌 말만 쓴다 (wireframe-guide.md 규칙).

## 와이어플로를 그리는 방식

user-flow.md의 mermaid 코드를 직접 파싱한다 (`parse_mer`). 노드마다 열 순위를 매겨 왼쪽에서 오른쪽으로 놓고,
사람이 둘인 흐름은 사람별 가로 칸으로 나눈다. 선은 SVG path로 그리고, 한 칸을 넘는 선은 위 통로,
되돌아가는 선은 아래 통로로 돌린다. 노드 모양은 user-flow-guide.md의 도형 규칙을 따른다.

## 알려진 한계

- 흐름 노드가 20개를 넘으면 폭이 2000~4300px로 늘어나고, 몇 곳에서 선이 겹친다 (예: F3의 M1 닫기 선)
- mdgen.py에 예시 run 전용 문장이 남아 있다 — "첫 묶음: P1, P2, P5 …" 줄과 "테스트 실행 산출물이다" 안내 두 줄.
  새 run에서 쓰기 전에 이 세 줄을 데이터(pageextra.json 등)에서 읽도록 바꿔야 한다
- sitemap.md와 user-flow.md의 표 형식(제목 줄, 표 칸 순서)에 기대어 파싱한다. 두 스킬의 산출물 구조가 바뀌면 함께 고친다
- `dsl.py`의 `STAGE` 값(draft/final)은 예시 run에서 사이트맵 갱신 전후를 나누려고 쓴 것이다. 새 run에서는 쓰지 않아도 된다
