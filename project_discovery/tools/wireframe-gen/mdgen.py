import json, os, re, sys
sys.dont_write_bytecode = True   # 플러그인 폴더와 DATA 폴더에 __pycache__를 만들지 않는다
sys.path.insert(0, os.path.dirname(__file__))  # gen.py를 찾기 위함
os.environ.setdefault("SCOPE", "all")
import gen, dsl
D = gen.DATA
STATUS = os.environ["STATUS"]
WARN = [w for w in os.environ.get("WARN", "").split("||") if w]
info = json.load(open(f"{D}/info.json"))
cand = json.load(open(f"{D}/candidates.json"))
dec = json.load(open(f"{D}/decisions.json"))
extra = json.load(open(f"{D}/pageextra.json"))  # page -> dict(below=..., comp=...)
# run마다 다른 문장: first_batch = 첫 묶음 설명 한 줄, notice = 머리 아래 인용 안내 줄들 (없으면 빈 목록)
meta = json.load(open(f"{D}/meta.json")) if os.path.exists(f"{D}/meta.json") else {}
notice = meta.get("notice", [])

L = []
L.append(f"# 와이어프레임 기록 — {gen.title_line}\n")
L.append(f"기준 문서: sitemap/sitemap.md · user-flow/user-flow.md · 플랫폼: {gen.platform}")
L.append(f"진행 상태: {STATUS}")
for w in WARN: L.append(w)
L.append("그림 파일: wireframe/wireframe.html\n")
for i, n in enumerate(notice):
    L.append(f"> {n}" + ("\n" if i == len(notice) - 1 else ""))
L.append("## 그린 범위")
L.append(f'첫 묶음: {meta.get("first_batch", "—")}\n')
L.append("### 페이지 프레임")
L.append("| 페이지 | 유형 | 섹션 수 | 박스 수 | 첫 화면 경계 아래의 핵심 행동 버튼 | 경쟁사 참조 | 그림 |")
L.append("|--------|------|--------|--------|------------------------------|-----------|------|")
for p in gen.order:
    pg = gen.pages[p]
    typ = pg["heading"][len(p) + 1 + len(pg["name"]) + 1:].strip("()")
    got = info["pages"].get(p)
    e = extra.get(p, {})
    L.append(f'| {p} {pg["name"]} | {typ} | {len(pg["sections"])} | {got["nbox"] if got else "—"} | {e.get("below", "없음")} | {e.get("comp", "없음")} | {"완료" if got else "미완"} |')
L.append("")
L.append("### 상태 화면")
L.append("| 페이지 | 상태 | 언제 생기는가 | 나온 흐름 | 바뀐 섹션 | 그림 |")
L.append("|--------|------|-------------|----------|----------|------|")
drawn = {(s["page"], s["state"]): s for s in info["states"]}
for s in gen.states:
    d = drawn.get((s["page"], s["state"]))
    L.append(f'| {s["page"]} {s["pname"]} | {s["state"]} | {s["when"]} | {s["src"]} | {", ".join(d["changed"]) if d else "—"} | {"완료" if d else "미완"} |')
L.append("")
L.append("### 와이어플로")
L.append("| 흐름 | 이름 | 흐름 그림의 노드 수 | 옮긴 노드 수 | 흐름 그림의 선 라벨 수 | 옮긴 선 라벨 수 | 그림 |")
L.append("|------|------|------------------|------------|---------------------|---------------|------|")
fm = {m["num"]: m for m in info["flows"]}
for f in gen.flows:
    m = fm.get(f["num"])
    if m: L.append(f'| {f["num"]} | {f["name"]} | {m["nodes"]} | {m["moved"]} | {m["labels"]} | {m["moved_labels"]} | 완료 |')
    else: L.append(f'| {f["num"]} | {f["name"]} | — | — | — | — | 미완 |')
L.append("\n(노드 수는 주석 노드를 포함해 셌다. 유저 입력 노드는 화살표 위 문구로, 상태 화면이 있는 시스템 결과는 상태 화면 프레임으로 옮겼다.)\n")
L.append("## 추가 후보")
L.append("| 종류 | 내용 | 나온 곳 | 반영 방법 | 유저 결정 | 반영 결과 |")
L.append("|------|------|--------|----------|----------|----------|")
for c in cand:
    L.append(f'| {c["kind"]} | {c["content"]} | {c["from"]} | {c["method"]} | {c["decision"]} | {c["result"]} |')
if not cand: L.append("| — | 없음 | — | — | — | — |")
L.append("")
L.append("## 결정 기록")
L.append("| 단계 | 무엇을 | 유저 답변 원문 |")
L.append("|------|--------|---------------|")
for d in dec:
    L.append(f'| {d[0]} | {d[1]} | {d[2]} |')
open(f"{gen.RUN}/wireframe/wireframe.md", "w").write("\n".join(L) + "\n")
print("md ok")
