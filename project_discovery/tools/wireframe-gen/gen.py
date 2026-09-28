import re, json, os, sys, math, html
# RUN  = run 디렉토리 (sitemap/, user-flow/ 가 있는 곳) — 필수
# DATA = 이 run의 그림 데이터 폴더 (dsl.py, candidates.json …) — 기본: {RUN}/wireframe/.gen
RUN = os.environ["RUN"]
DATA = os.environ.get("DATA", os.path.join(RUN, "wireframe", ".gen"))
sys.path.insert(0, DATA)
import dsl

SCOPE = os.environ.get("SCOPE", "all")          # "first" = 공통 섹션 + 첫 묶음만
STATUS = os.environ.get("STATUS", "전체 확정")
FIRST = [p for p in os.environ.get("FIRST", "").split(",") if p]   # 첫 묶음 페이지 번호, 쉼표 구분
WARN = os.environ.get("WARN", "")
E = html.escape

# ---------------- 사이트맵 읽기 ----------------
sm = open(f"{RUN}/sitemap/sitemap.md").read()
title_line = sm.splitlines()[0].replace("# 사이트맵 — ", "")
platform = re.search(r"플랫폼: (\S+)", sm).group(1)

pages = {}   # num -> dict(name, type, heading, sections=[...])
order = []
for m in re.finditer(r"^\| ([PMX]\d+) \| (.+?) \| (.+?) \|", sm, re.M):
    num, name, typ = m.group(1), m.group(2), m.group(3)
    if num in pages: continue
    pages[num] = dict(name=name, type=typ, sections=[], heading=None)
    order.append(num)

common = {}
cm = re.search(r"## 공통 섹션\n\n\|.*\n\|.*\n((?:\|.*\n)+)", sm)
for row in cm.group(1).strip().splitlines():
    c = [x.strip() for x in row.strip("|").split("|")]
    common[c[0]] = dict(content=c[1], pages=c[2])

sec_part = sm.split("## 페이지별 섹션 목록")[1].split("## 이동 표")[0]
cur = None
for line in sec_part.splitlines():
    h = re.match(r"^### (([PMX]\d+) .+)$", line)
    if h:
        cur = h.group(2); pages[cur]["heading"] = h.group(1); continue
    s = re.match(r"^(\d+)\. (.+)$", line)
    if s and cur:
        n, rest = int(s.group(1)), s.group(2)
        feats = re.findall(r"\(기능 ([^)]+)\)", rest)
        feat = feats[0] if feats else ""
        name = rest.split(" — ")[0]
        name = re.sub(r"\s*\(기능 [^)]+\)", "", name)
        name = re.sub(r"\s*\(→ [^)]+\)", "", name)
        is_common = "[공통]" in name
        name = name.replace("[공통]", "").strip()
        pages[cur]["sections"].append(dict(n=n, name=name, feat=feat, common=is_common, raw=rest))

moves = {}
mv = sm.split("## 이동 표")[1].split("## 점검 결과")[0]
for row in mv.splitlines():
    if row.startswith("| ") and not row.startswith("| 페이지") :
        c = [x.strip() for x in row.strip("|").split("|")]
        if len(c) == 3 and re.match(r"[PMX]\d+ ", c[0]):
            moves[c[0].split()[0]] = dict(inbound=c[1], outbound=c[2])

# ---------------- 유저 흐름 읽기 ----------------
uf = open(f"{RUN}/user-flow/user-flow.md").read()
states = []
st = uf.split("## 화면 상태 목록")[1].split("## 사이트맵 대조 결과")[0]
for row in st.splitlines():
    if re.match(r"^\| [PMX]\d+ ", row):
        c = [x.strip() for x in row.strip("|").split("|")]
        states.append(dict(page=c[0].split()[0], pname=" ".join(c[0].split()[1:]), state=c[1], when=c[2], src=c[3], extra=False))
for p, s, w in dsl.EXTRA_STATES:
    states.append(dict(page=p, pname=pages[p]["name"], state=s, when=w, src="와이어프레임 단계에서 추가", extra=True))
state_by_node = {}
for s in states:
    for fm in re.finditer(r"(F\d+) \(([^)]*)\)", s["src"]):
        if "→" in fm.group(2): continue
        for nid in re.split(r",\s*", fm.group(2)):
            state_by_node.setdefault((fm.group(1), nid.strip()), []).append(s)

flows = []
fl_part = uf.split("## 흐름별 그림")[1].split("## 화면 상태 목록")[0]
for block in re.split(r"^### ", fl_part, flags=re.M)[1:]:
    head = block.splitlines()[0]
    fnum = head.split()[0]
    info = {k: re.search(rf"^- {k}: (.+)$", block, re.M).group(1) for k in ["누가", "시작", "목표"]}
    mer = re.search(r"```mermaid\n(.+?)```", block, re.S).group(1)
    flows.append(dict(num=fnum, name=head[len(fnum)+1:], info=info, mer=mer, block=block))

# ---------------- 요소 자리 그리기 ----------------
XSVG = '<svg class="x" preserveAspectRatio="none" viewBox="0 0 100 100"><line x1="0" y1="0" x2="100" y2="100"/><line x1="100" y1="0" x2="0" y2="100"/></svg>'
def el_html(e):
    k = e[0]
    if k == "t": return f'<div class="el"><span class="bar t"></span><span class="nm">{E(e[1])}</span></div>'
    if k == "s": return f'<div class="el"><span class="bar s"></span><span class="nm">{E(e[1])}</span></div>'
    if k == "l":
        ls = "".join(f'<span class="line{" short" if i == e[1]-1 and e[1] > 1 else ""}"></span>' for i in range(e[1]))
        return f'<div class="el col"><span class="nm">{E(e[2])}</span>{ls}</div>'
    if k == "img": return f'<div class="el col"><div class="img" style="height:{e[2]}px">{XSVG}<span class="nm">{E(e[1])}</span></div></div>'
    if k == "img_s": return f'<span class="img sq">{XSVG}</span>'
    if k == "imgs": return '<div class="el"><span class="nm">' + E(e[2]) + '</span>' + "".join(f'<span class="img sq">{XSVG}</span>' for _ in range(e[1])) + '</div>'
    if k == "btn": return f'<div class="el"><span class="btn">{E(e[1])}</span></div>'
    if k == "btnp": return f'<div class="el"><span class="btn primary">{E(e[1])}</span></div>'
    if k == "btns":
        return '<div class="el">' + "".join(f'<span class="btn{" primary" if i == e[2] else ""}">{E(b)}</span>' for i, b in enumerate(e[1])) + '</div>'
    if k == "in": return f'<div class="el col"><span class="nm">{E(e[1])}</span><div class="input" style="height:{e[2]}px"></div></div>'
    if k == "inl": return f'<span class="input inl"><span class="nm">{E(e[1])}</span></span>'
    if k == "tabs":
        return '<div class="el"><div class="tabs">' + "".join(f'<span class="tab{" sel" if i == e[2] else ""}">{E(t)}</span>' for i, t in enumerate(e[1])) + '</div></div>'
    if k == "tabbar":
        return '<div class="el"><div class="tabs">' + "".join(f'<span class="tab"><span class="icon"></span> ({E(t)})</span>' for t in e[1]) + '</div></div>'
    if k == "chips": return '<div class="el">' + "".join(f'<span class="chip">{E(c)}</span>' for c in e[1]) + '</div>'
    if k == "ic": return f'<span class="ico"><span class="icon"></span>({E(e[1])})</span>'
    if k == "tb": return f'<span class="tb"><span class="bar t"></span><span class="nm">{E(e[1])}</span></span>'
    if k == "h":
        inner = "".join(el_html(x) if x[0] in ("ic", "tb", "img_s", "inl") else el_html(x).replace('<div class="el">', '').replace('</div>', '') for x in e[1])
        return f'<div class="el h">{inner}</div>'
    if k == "card":
        inner = "".join(el_html(x) for x in e[1])
        return "".join(f'<div class="card"><span class="nm cardname">{E(e[3])}</span>{inner}</div>' for _ in range(e[2]))
    if k == "more": return '<div class="more">…</div>'
    if k == "list":
        return "".join(f'<div class="card row"><span class="bar s"></span><span class="nm">{E(e[2])}</span><span class="line"></span></div>' for _ in range(e[1]))
    if k == "stat": return '<div class="el">' + "".join(f'<span class="stat"><span class="bar t"></span><span class="nm">{E(n)}</span></span>' for n in e[1]) + '</div>'
    if k == "tog": return "".join(f'<div class="el"><span class="tog"></span><span class="nm">{E(e[2])}</span></div>' for _ in range(e[1]))
    if k == "empty": return f'<div class="empty">{E(e[1])}</div>'
    if k == "err": return f'<div class="el"><span class="errmark">!</span><span class="line"></span><span class="nm">{E(e[1])}</span></div>'
    if k == "load": return "".join('<span class="loadbar"></span>' for _ in range(e[1]))
    if k == "note": return f'<div class="note">··· {E(e[1])}</div>'
    raise ValueError(e)

def label(page, sec, suffix=""):
    f = f' <small>기능 {E(sec["feat"])}</small>' if sec["feat"] else ""
    c = " [공통]" if sec["common"] else ""
    return f'<span class="label">{page}-{sec["n"]} {E(sec["name"])}{c}{f}{suffix}</span>'

def sec_body(page, sec):
    spec = dsl.PAGES[page][sec["n"]]
    if isinstance(spec, tuple) and spec[0] == "common":
        _, cname, notes, primary = spec
        body = "".join(el_html(e) for e in dsl.COMMON[cname] if e[0] != "note")
        if primary:
            body = body.replace('<span class="btn">완료</span>', '<span class="btn primary">완료</span>')
        body += "".join(el_html(("note", n)) for n in notes)
        return body
    return "".join(el_html(e) for e in spec)

def modal_note(page):
    mvr = moves.get(page)
    if page.startswith("M") and mvr:
        return f'<div class="note callers">··· 부르는 곳: {E(mvr["inbound"])}</div>'
    return ""

def frame_html(page):
    p = pages[page]
    out = [f'<section class="frame" id="{page}"><h3>{E(p["heading"])}</h3>{modal_note(page)}<div class="screen">']
    for s in p["sections"]:
        out.append(f'<div class="sec" id="{page}-{s["n"]}">{label(page, s)}{sec_body(page, s)}</div>')
    out.append('<div class="fold"><span>첫 화면 경계</span></div></div></section>')
    return "".join(out)

def state_html(st):
    page = st["page"]; p = pages[page]
    changed = dsl.STATES[(page, st["state"])]
    sid = f'{page}-{st["state"].replace(" ", "-")}'
    extra = ' <small>와이어프레임 단계에서 추가</small>' if st["extra"] else ""
    out = [f'<section class="frame state" id="{sid}"><h3>{page} {E(p["name"])} · {E(st["state"])}{extra}</h3>',
           f'<div class="note callers">··· 언제: {E(st["when"])}</div><div class="screen">']
    for s in p["sections"]:
        if s["n"] in changed:
            body = "".join(el_html(e) for e in changed[s["n"]])
            out.append(f'<div class="sec changed">{label(page, s)}{body}</div>')
        else:
            out.append(f'<div class="sec same">{label(page, s)}<div class="same-t">(기본 모양과 같음)</div></div>')
    out.append('</div></section>')
    return "".join(out)

def common_html():
    out = []
    for name, c in common.items():
        cid = "공통-" + name.replace(" ", "-")
        body = "".join(el_html(e) for e in dsl.COMMON[name])
        f = ' <small>기능 s6</small>' if name == "상세 상단 바" else ""
        out.append(f'<section class="frame common-frame"><h3>{E(name)} [공통]</h3><div class="screen short"><div class="sec" id="{cid}"><span class="label">{E(name)} [공통]{f}</span>{body}</div></div>'
                   f'<div class="note">··· 쓰이는 페이지: {E(c["pages"])}</div></section>')
    return "".join(out)

# ---------------- 와이어플로 ----------------
NODE_RE = [
    ("circle", re.compile(r"^\s*([AB]\d+)\(\((.+)\)\)\s*$")),
    ("result", re.compile(r"^\s*([AB]\d+)\(\[(.+)\]\)\s*$")),
    ("ext", re.compile(r"^\s*([AB]\d+)\[\[(.+)\]\]\s*$")),
    ("input", re.compile(r"^\s*([AB]\d+)\[/(.+)/\]\s*$")),
    ("note", re.compile(r"^\s*(N\d+)\[(.+)\]:::note\s*$")),
    ("box", re.compile(r"^\s*([AB]\d+)\[(.+)\]\s*$")),
    ("diamond", re.compile(r"^\s*([AB]\d+)\{(.+)\}\s*$")),
]

def parse_mer(mer):
    nodes, edges, lanes, lane = {}, [], [], None
    for line in mer.splitlines():
        t = line.strip()
        if not t or t.startswith("flowchart") or t.startswith("classDef"): continue
        m = re.match(r"subgraph (\w+)\[(.+)\]", t)
        if m: lane = m.group(2); lanes.append(lane); continue
        if t == "end": lane = None; continue
        matched = False
        for kind, rx in NODE_RE:
            m = rx.match(t)
            if m and "-->" not in t and "-.-" not in t:
                txt = m.group(2).strip().strip('"')
                nodes[m.group(1)] = dict(id=m.group(1), kind=kind, text=txt, lane=lane)
                matched = True; break
        if matched: continue
        toks = re.split(r"\s*(-->|-- .+? -->|-\.-)\s*", t)
        for i in range(1, len(toks), 2):
            a, conn, b = toks[i-1].strip(), toks[i], toks[i+1].strip()
            if conn == "-.-": edges.append(dict(a=a, b=b, label="", note=True))
            else:
                lab = conn[3:-4].strip() if conn.startswith("-- ") else ""
                edges.append(dict(a=a, b=b, label=lab, note=False))
    if not lanes: lanes = [None]
    for n in nodes.values():
        if n["kind"] == "box" and re.match(r"^[PMX]\d+ ", n["text"]):
            n["kind"] = "screen"
            n["page"] = n["text"].split()[0]
            n["suffix"] = n["text"].split(" · ", 1)[1] if " · " in n["text"] else None
        if n["kind"] == "input":
            sm_ = re.search(r"\s([PMX]\d+-\d+)(?=(\s*\(선택\))?$)", n["text"])
            n["sec"] = sm_.group(1) if sm_ else None
            n["shown"] = re.sub(r"\s[PMX]\d+-\d+(?=(\s*\(선택\))?$)", "", n["text"])
    return nodes, edges, lanes

MINI_W = 170
def mini_frame(fl, n, confirm):
    """줄인 프레임: 섹션 박스와 라벨만, 화살표가 출발하는 섹션만 요소 자리."""
    page = n["page"]; p = pages[page]
    st = None
    if n["suffix"] is not None:
        cands = state_by_node.get((fl["num"], n["id"]), [])
        cands = [c for c in cands if c["page"] == page]
        if len(cands) == 1: st = cands[0]
        else:
            confirm.append(dict(kind="상태 화면 짝", flow=fl["num"], node=n["id"], text=n["text"],
                                detail="화면 상태 목록에 이 노드를 가리키는 줄이 없어 기본 모양을 놓았다"))
    if n.get("result_state"):
        st = n["result_state"]
    title = f'{page} {p["name"]}' + (f' · {st["state"]}' if st else "")
    changed = dsl.STATES[(page, st["state"])] if st else {}
    origins = n.get("origins", set())
    rows, y = [], 34
    secy = {}
    for s in p["sections"]:
        key = f"{page}-{s['n']}"
        cls = "msec" + (" changed" if s["n"] in changed else "") + (" origin" if key in origins else "")
        h = 17
        inner = ""
        if key in origins:
            spec = changed.get(s["n"]) or dsl.PAGES[page][s["n"]]
            if isinstance(spec, tuple): spec = [e for e in dsl.COMMON[spec[1]] if e[0] != "note"]
            names = []
            for e in spec:
                if e[0] in ("btn", "btnp"): names.append(("b", e[1], e[0] == "btnp"))
                elif e[0] == "btns": names += [("b", b, i == e[2]) for i, b in enumerate(e[1])]
                elif e[0] == "chips": names += [("c", c, False) for c in e[1]]
                elif e[0] == "tabs": names += [("c", t, i == e[2]) for i, t in enumerate(e[1])]
                elif e[0] == "card": names.append(("c", e[3], False))
                elif e[0] == "list": names.append(("c", e[2], False))
                elif e[0] == "in": names.append(("i", e[1], False))
                elif e[0] == "h":
                    for x in e[1]:
                        if x[0] == "btn": names.append(("b", x[1], False))
                        elif x[0] == "ic": names.append(("c", f"({x[1]})", False))
            names = names[:4]
            inner = '<div class="mel">' + "".join(
                f'<span class="{"mbtn" if k=="b" else "mchip"}{" primary" if pr else ""}">{E(t)}</span>' for k, t, pr in names) + '</div>'
            h += 18 * max(1, math.ceil(len(names) / 2))
        secy[key] = y + h / 2
        rows.append(f'<div class="{cls}" style="height:{h}px"><span class="mlabel">{page}-{s["n"]} {E(s["name"])}</span>{inner}</div>')
        y += h + 2
    memo = ""
    if n.get("via"):
        memo = f'<div class="mvia">··· {E(n["via"])}</div>'; y += 16
    H = y + 6
    tcls = "mframe state" if st else "mframe"
    htm = f'<div class="{tcls}" style="left:{{x}}px;top:{{y}}px;width:{MINI_W}px;height:{H}px"><div class="mtitle">{E(title)}</div>{"".join(rows)}{memo}</div>'
    return htm, MINI_W, H, secy

def text_lines(t, per=11):
    return max(1, math.ceil(len(t) / per))

def build_flow(fl):
    nodes, edges, lanes = parse_mer(fl["mer"])
    confirm, diamond_origin = [], []
    flow_edges = [e for e in edges if not e["note"]]
    note_edges = [e for e in edges if e["note"]]
    # 다른 흐름을 거치는 화면: 나가는 선 라벨에 흐름 번호가 있다
    for e in flow_edges:
        m = re.match(r"(F\d+)", e["label"])
        if m and nodes[e["a"]]["kind"] == "screen":
            nodes[e["a"]]["via"] = f'{m.group(1)} 와이어플로에서 그린다'
    for n in nodes.values():
        if n["kind"] == "screen" and n["page"] == "M1" and fl["num"] == "F4":
            n["via"] = "F3 와이어플로에서 그린다 (M1 안의 단계)"
    # 시스템 결과 → 상태 화면
    for n in nodes.values():
        if n["kind"] == "result":
            c = state_by_node.get((fl["num"], n["id"]), [])
            if c:
                n["kind"] = "screen"; n["page"] = c[0]["page"]; n["suffix"] = None; n["result_state"] = c[0]
                n["result_text"] = n["text"]
    # 입력 → 출발 섹션
    preds = {k: [] for k in nodes}; succs = {k: [] for k in nodes}
    for e in flow_edges:
        succs[e["a"]].append(e); preds[e["b"]].append(e)
    for n in nodes.values():
        if n["kind"] != "input": continue
        for e in preds[n["id"]]:
            src = nodes[e["a"]]
            if src["kind"] == "screen" and n["sec"] and n["sec"].split("-")[0] == src["page"]:
                src.setdefault("origins", set()).add(n["sec"])
                e["from_sec"] = n["sec"]
            elif src["kind"] == "input":
                pass
            else:
                reason = ("입력 글자에 섹션 번호가 없다" if not n["sec"] else
                          f"입력의 섹션({n['sec']})이 앞 노드({src['text']})의 페이지에 없다")
                diamond_origin.append(dict(flow=fl["num"], input=n["id"], text=n["shown"], src=src["text"], sec=n["sec"], reason=reason))
    # 순위 (가로 열)
    starts = [k for k in nodes if nodes[k]["kind"] != "note" and not preds[k]]
    back = set(); state = {}
    def dfs(u):
        state[u] = 1
        for i, e in enumerate(succs[u]):
            v = e["b"]
            if state.get(v) == 1: back.add(id(e))
            elif v not in state: dfs(v)
        state[u] = 2
    for s0 in starts: dfs(s0)
    for k in nodes:
        if nodes[k]["kind"] != "note" and k not in state: dfs(k)
    rank = {k: 0 for k in nodes if nodes[k]["kind"] != "note"}
    changed = True
    while changed:
        changed = False
        for e in flow_edges:
            if id(e) in back: continue
            if rank[e["b"]] < rank[e["a"]] + 1:
                rank[e["b"]] = rank[e["a"]] + 1; changed = True
    notes_of = {}
    for e in note_edges:
        notes_of.setdefault(e["a"], []).append(e["b"])
    # 노드 모양과 크기
    shapes = {}
    for k, n in nodes.items():
        if n["kind"] == "screen":
            h, w, H, secy = mini_frame(fl, n, confirm)
            shapes[k] = dict(tpl=h, w=w, h=H, secy=secy)
        elif n["kind"] == "circle":
            L = text_lines(n["text"], 12); shapes[k] = dict(w=150, h=max(54, 22 + 14 * L))
        elif n["kind"] == "diamond":
            L = text_lines(n["text"], 9); shapes[k] = dict(w=140, h=max(80, 50 + 13 * L))
        elif n["kind"] == "input":
            L = text_lines(n["shown"], 11); shapes[k] = dict(w=150, h=14 * L + 8)
        else:
            t = ("결과: " + n["text"]) if n["kind"] == "result" else n["text"]
            L = text_lines(t, 11); shapes[k] = dict(w=150, h=16 + 14 * L)
    # 열 안의 순서 (레인별)
    lane_names = lanes
    lane_of = {k: (nodes[k]["lane"] if nodes[k]["lane"] in lane_names else lane_names[0]) for k in nodes}
    for nid, lst in notes_of.items():
        for x in lst: lane_of[x] = lane_of[nid]
    seq = list(nodes.keys())
    ncol = max(rank.values()) + 1
    cols = {(ln, c): [] for ln in lane_names for c in range(ncol)}
    for k in seq:
        if nodes[k]["kind"] == "note": continue
        cols[(lane_of[k], rank[k])].append(k)
    for k in seq:  # 주석은 붙은 노드 바로 뒤
        if nodes[k]["kind"] == "note":
            owner = next(e["a"] for e in note_edges if e["b"] == k)
            c = cols[(lane_of[owner], rank[owner])]
            c.insert(c.index(owner) + 1, k); rank[k] = rank[owner]
    colw = [max([shapes[k]["w"] for ln in lane_names for k in cols[(ln, c)]] or [60]) for c in range(ncol)]
    GAP = 70
    colx = []; x = 20
    for c in range(ncol): colx.append(x); x += colw[c] + GAP
    W = x
    # 선 분류
    pos = {}
    top_edges = {ln: [] for ln in lane_names}; bot_edges = {ln: [] for ln in lane_names}
    for e in flow_edges:
        a, b = e["a"], e["b"]
        if lane_of[a] != lane_of[b]: e["route"] = "cross"; continue
        if id(e) in back or rank[b] <= rank[a]: e["route"] = "bot"; bot_edges[lane_of[a]].append(e)
        elif rank[b] > rank[a] + 1: e["route"] = "top"; top_edges[lane_of[a]].append(e)
        else: e["route"] = "direct"
    # 세로 배치 — 앞 노드의 순서를 따라 두 번 다듬는다
    def place():
        y0 = 30
        lane_box = {}
        for ln in lane_names:
            top_h = 18 * len(top_edges[ln]) + 20
            ystart = y0 + (26 if ln else 0) + top_h
            maxh = 0
            for c in range(ncol):
                yy = ystart
                for k in cols[(ln, c)]:
                    pos[k] = [colx[c] + (colw[c] - shapes[k]["w"]) / 2, yy]
                    yy += shapes[k]["h"] + 26
                maxh = max(maxh, yy - ystart)
            bot_h = 18 * len(bot_edges[ln]) + 24
            lane_box[ln] = dict(top=y0, ch_top=y0 + (26 if ln else 0) + 10, nodes_bottom=ystart + maxh, bottom=ystart + maxh + bot_h)
            y0 = ystart + maxh + bot_h + 20
        return lane_box, y0
    lane_box, H = place()
    for _ in range(2):
        for ln in lane_names:
            for c in range(1, ncol):
                col = cols[(ln, c)]
                def bc(k):
                    if nodes[k]["kind"] == "note": return None
                    ps = [pos[e["a"]][1] + shapes[e["a"]]["h"] / 2 for e in preds[k] if e["a"] in pos and rank[e["a"]] < rank[k] and lane_of[e["a"]] == ln]
                    return sum(ps) / len(ps) if ps else pos[k][1]
                groups = []
                for k in col:
                    if nodes[k]["kind"] == "note" and groups: groups[-1].append(k)
                    else: groups.append([k])
                groups.sort(key=lambda g: bc(g[0]))
                cols[(ln, c)] = [k for g in groups for k in g]
        lane_box, H = place()
    # 선 그리기
    svg, labels = [], []
    def anchor_out(e):
        a = e["a"]; x0, y0 = pos[a]; s = shapes[a]
        if e.get("from_sec") and e["from_sec"] in s.get("secy", {}):
            return x0 + s["w"], y0 + s["secy"][e["from_sec"]], True
        return x0 + s["w"], y0 + s["h"] / 2, False
    def anchor_in(b):
        x0, y0 = pos[b]; return x0, y0 + shapes[b]["h"] / 2
    def lab(x, y, t, cls=""):
        if t: labels.append(f'<div class="elabel {cls}" style="left:{x:.0f}px;top:{y:.0f}px">{E(t)}</div>')
    ti = {ln: 0 for ln in lane_names}; bi = {ln: 0 for ln in lane_names}
    for e in flow_edges:
        a, b = e["a"], e["b"]
        head = "" if nodes[b]["kind"] == "input" else f' marker-end="url(#ah-{fl["num"]})"'
        x1, y1, fs = anchor_out(e)
        cls = ' class="fromsec"' if fs else ""
        if e["route"] in ("direct", "cross"):
            if e["route"] == "cross" and rank[b] <= rank[a]:
                x2 = pos[b][0] + shapes[b]["w"] / 2; y2 = pos[b][1] + (shapes[b]["h"] if pos[b][1] < y1 else 0)
                svg.append(f'<path d="M{x1:.0f},{y1:.0f} C{x1+60:.0f},{y1:.0f} {x2:.0f},{(y1+y2)/2:.0f} {x2:.0f},{y2:.0f}"{head}{cls}/>')
                lab((x1 + x2) / 2 - 40, (y1 + y2) / 2 - 8, e["label"], "cross")
            else:
                x2, y2 = anchor_in(b)
                dx = max(30, (x2 - x1) / 2)
                svg.append(f'<path d="M{x1:.0f},{y1:.0f} C{x1+dx:.0f},{y1:.0f} {x2-dx:.0f},{y2:.0f} {x2:.0f},{y2:.0f}"{head}{cls}/>')
                lab(x1 + 4, (y1 + y2) / 2 - 16 if abs(y2 - y1) > 20 else y1 - 16, e["label"], "cross" if e["route"] == "cross" else "")
        elif e["route"] == "top":
            ln = lane_of[a]; ch = lane_box[ln]["ch_top"] + 18 * ti[ln]; ti[ln] += 1
            x2 = pos[b][0] + shapes[b]["w"] / 2; y2 = pos[b][1]
            svg.append(f'<path d="M{x1:.0f},{y1:.0f} L{x1+14:.0f},{y1:.0f} L{x1+14:.0f},{ch:.0f} L{x2:.0f},{ch:.0f} L{x2:.0f},{y2:.0f}"{head}{cls}/>')
            lab(x1 + 20, ch - 15, e["label"])
        else:
            ln = lane_of[a]; ch = lane_box[ln]["nodes_bottom"] + 4 + 18 * bi[ln]; bi[ln] += 1
            x2 = pos[b][0] + shapes[b]["w"] / 2 + 10 * (bi[ln] % 3); y2 = pos[b][1] + shapes[b]["h"]
            if fs or nodes[a]["kind"] == "input":
                pts = f"M{x1:.0f},{y1:.0f} L{x1+10:.0f},{y1:.0f} L{x1+10:.0f},{ch:.0f}"
            else:
                xs = pos[a][0] + shapes[a]["w"] / 2 - 10; ys = pos[a][1] + shapes[a]["h"]
                pts = f"M{xs:.0f},{ys:.0f} L{xs:.0f},{ch:.0f}"; x1 = xs
            svg.append(f'<path d="{pts} L{x2:.0f},{ch:.0f} L{x2:.0f},{y2:.0f}"{head}{cls}/>')
            lab(min(x1, x2) + 8, ch - 15, e["label"])
    for e in note_edges:
        a, b = e["a"], e["b"]
        xa, ya = pos[a][0] + shapes[a]["w"] / 2, pos[a][1] + shapes[a]["h"]
        xb, yb = pos[b][0] + shapes[b]["w"] / 2, pos[b][1]
        svg.append(f'<path class="memo-link" d="M{xa:.0f},{ya:.0f} L{xb:.0f},{yb:.0f}"/>')
    # 노드 그리기
    divs = []
    for k, n in nodes.items():
        x0, y0 = pos[k]; s = shapes[k]
        st = f'left:{x0:.0f}px;top:{y0:.0f}px;width:{s["w"]}px;height:{s["h"]:.0f}px'
        if n["kind"] == "screen":
            divs.append(s["tpl"].replace("{x}", f"{x0:.0f}").replace("{y}", f"{y0:.0f}"))
        elif n["kind"] == "circle":
            divs.append(f'<div class="ncircle" style="{st}">{E(n["text"])}</div>')
        elif n["kind"] == "diamond":
            w, h = s["w"], s["h"]
            svg.append(f'<polygon class="dia" points="{x0+w/2:.0f},{y0:.0f} {x0+w:.0f},{y0+h/2:.0f} {x0+w/2:.0f},{y0+h:.0f} {x0:.0f},{y0+h/2:.0f}"/>')
            divs.append(f'<div class="ndia" style="{st}"><span>{E(n["text"])}</span></div>')
        elif n["kind"] == "input":
            divs.append(f'<div class="ninput" style="{st}">{E(n["shown"])}</div>')
        elif n["kind"] == "result":
            divs.append(f'<div class="nbox" style="{st}">결과: {E(n["text"])}</div>')
        elif n["kind"] == "ext":
            divs.append(f'<div class="nbox ext" style="{st}">{E(n["text"])}</div>')
        elif n["kind"] == "note":
            divs.append(f'<div class="nmemo" style="{st}">{E(n["text"])}</div>')
        else:
            divs.append(f'<div class="nbox" style="{st}">{E(n["text"])}</div>')
    lane_html = ""
    for ln in lane_names:
        if ln:
            b = lane_box[ln]
            lane_html += f'<div class="lane" style="top:{b["top"]}px;height:{b["bottom"]-b["top"]}px;width:{W}px"><span>{E(ln)}</span></div>'
    body = (f'<div class="flowcanvas" style="width:{W}px;height:{H}px">{lane_html}'
            f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><marker id="ah-{fl["num"]}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#000"/></marker></defs>{"".join(svg)}</svg>'
            f'{"".join(divs)}{"".join(labels)}</div>')
    # 개수 세기
    all_nodes = len(nodes)
    rendered = sum(1 for n in nodes.values())
    labeled = [e for e in flow_edges if e["label"]]
    shown_labels = sum(1 for e in labeled if f'>{E(e["label"])}<' in "".join(labels))
    meta = dict(num=fl["num"], name=fl["name"], nodes=all_nodes, moved=rendered, labels=len(labeled), moved_labels=shown_labels,
                confirm=confirm, input_other_origin=diamond_origin,
                screens=sorted({n["page"] for n in nodes.values() if n["kind"] == "screen"}),
                states_used=sorted({(n.get("result_state") or {}).get("state", "") for n in nodes.values()} - {""}))
    # 상태 화면으로 옮긴 노드 목록
    meta["state_nodes"] = [f'{k}→{n["page"]} · {n["result_state"]["state"]}' for k, n in nodes.items() if n.get("result_state")]
    lanes_line = ""
    sec = (f'<section class="flow" id="{fl["num"]}"><h3>{fl["num"]} {E(fl["name"])}</h3>'
           f'<p class="meta">누가: {E(fl["info"]["누가"])}</p><p class="meta">시작: {E(fl["info"]["시작"])}</p><p class="meta">목표: {E(fl["info"]["목표"])}</p>'
           f'<div class="flowwrap">{body}</div></section>')
    return sec, meta

CSS = """
*{box-sizing:border-box}
body{margin:0;padding:24px;background:#fff;color:#000;font-family:-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;font-size:12px;line-height:1.4}
header{border-bottom:2px solid #000;padding-bottom:12px;margin-bottom:24px}
header .draft{font-size:22px;font-weight:700;border:2px solid #000;display:inline-block;padding:4px 10px;margin-bottom:8px}
header .warn{border:1px dashed #000;padding:6px 8px;margin:6px 0}
h1{font-size:20px;margin:0 0 8px}
h2{font-size:17px;margin:32px 0 12px;border-bottom:1px solid #000;padding-bottom:4px}
h3{font-size:13px;margin:0 0 6px}
h3 small,.label small{font-weight:400;color:#555;font-size:10px}
nav a{color:#000;margin-right:6px}
.rowwrap{overflow-x:auto;margin-bottom:28px}
.row{display:flex;gap:28px;align-items:flex-start}
.frame{width:360px;flex:0 0 360px}
.frame .screen{position:relative;border:2px solid #000;min-height:660px;background:#fff}
.common-frame .screen.short{min-height:0}
#common{display:flex;gap:28px;flex-wrap:wrap}
#common h2{flex-basis:100%}
.sec{position:relative;border-bottom:1px solid #000;padding:20px 8px 8px}
.sec.changed{border:2px dashed #000;margin:2px}
.sec.same{color:#555}
.same-t{color:#999;font-size:11px}
.label{position:absolute;left:4px;top:3px;font-size:10px;font-weight:700;background:#fff;padding:0 2px}
.el{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:4px 0}
.el.col{flex-direction:column;align-items:stretch;gap:3px}
.el.h{justify-content:space-between;flex-wrap:nowrap}
.bar{display:inline-block;background:#555}
.bar.t{height:10px;width:70px}
.bar.s{height:5px;width:40px;background:#999}
.nm{font-size:10px;color:#555}
.line{display:block;height:3px;background:#ccc;width:100%;margin:2px 0}
.line.short{width:60%}
.img{position:relative;border:1px solid #000;background:#fff}
.img svg.x{position:absolute;left:0;top:0;width:100%;height:100%}
.img svg.x line{stroke:#999;stroke-width:1;vector-effect:non-scaling-stroke}
.img .nm{position:absolute;left:4px;top:2px;background:#fff}
.img.sq{display:inline-block;width:36px;height:36px}
.btn{display:inline-block;border:1px solid #000;padding:3px 10px;font-size:11px;background:#fff}
.btn.primary{background:#444;color:#fff;border-color:#444}
.input{border:1px solid #000;background:#fff}
.input.inl{flex:1;height:26px;padding:4px;margin-left:6px}
.tabs{display:flex;width:100%;border:1px solid #000}
.tab{flex:1;text-align:center;padding:4px 2px;border-right:1px solid #000;font-size:11px}
.tab:last-child{border-right:0}
.tab.sel{background:#444;color:#fff}
.chip{border:1px solid #000;padding:2px 8px;font-size:11px}
.icon{display:inline-block;width:12px;height:12px;border:1px solid #000;border-radius:50%;vertical-align:middle}
.ico{font-size:10px;color:#555;white-space:nowrap}
.tb{display:inline-flex;align-items:center;gap:4px}
.card{border:1px solid #999;padding:14px 6px 6px;margin:4px 0;position:relative}
.card.row{display:flex;align-items:center;gap:6px;padding:6px}
.card.row .line{flex:1}
.cardname{position:absolute;left:4px;top:1px}
.more{color:#555;padding-left:4px}
.stat{flex:1;border:1px solid #999;padding:6px;display:flex;flex-direction:column;gap:3px}
.tog{display:inline-block;width:22px;height:12px;border:1px solid #000}
.empty{border:1px dashed #000;padding:14px 8px;color:#555;font-size:11px;margin:4px 0;text-align:center}
.errmark{display:inline-block;width:14px;height:14px;border:1px solid #000;text-align:center;font-size:10px;line-height:12px}
.loadbar{display:block;height:14px;background:#ccc;margin:6px 0}
.note{color:#555;font-size:10px;margin-top:3px}
.note.callers{margin:0 0 4px}
.fold{position:absolute;left:0;right:0;top:640px;border-top:1px dashed #000;height:0}
.fold span{position:absolute;right:2px;top:-13px;font-size:9px;color:#555;background:#fff}
.flow{margin-bottom:40px}
.flow .meta{margin:0}
.flowwrap{overflow-x:auto;border:1px solid #ccc;margin-top:8px}
.flowcanvas{position:relative}
.flowcanvas svg{position:absolute;left:0;top:0}
.flowcanvas path{fill:none;stroke:#000;stroke-width:1.2}
.flowcanvas path.fromsec{stroke-width:1.6}
.flowcanvas path.memo-link{stroke:#999;stroke-dasharray:3 3}
.flowcanvas polygon.dia{fill:#fff;stroke:#000;stroke-width:1.2}
.lane{position:absolute;left:0;border-top:1px solid #999;border-bottom:1px solid #999}
.lane span{position:absolute;left:6px;top:4px;font-weight:700;font-size:12px}
.ncircle{position:absolute;border:1.5px solid #000;border-radius:50%;display:flex;align-items:center;justify-content:center;text-align:center;padding:6px 14px;font-size:10px;background:#fff}
.ndia{position:absolute;display:flex;align-items:center;justify-content:center;text-align:center;font-size:10px;padding:0 30px}
.ninput{position:absolute;font-size:10px;background:#fff;text-align:center;padding:2px;border-bottom:1px solid #000;display:flex;align-items:center;justify-content:center}
.nbox{position:absolute;border:1px solid #000;font-size:10px;padding:4px;background:#fff;text-align:center;display:flex;align-items:center;justify-content:center}
.nbox.ext{border:3px double #000}
.nmemo{position:absolute;border:1px dashed #999;color:#555;font-size:10px;padding:4px;background:#fff}
.elabel{position:absolute;font-size:10px;background:#fff;padding:0 2px;max-width:150px;color:#000}
.elabel.cross{font-weight:700}
.mframe{position:absolute;border:1.5px solid #000;background:#fff;padding:2px}
.mframe.state .mtitle{font-style:italic}
.mtitle{font-size:10px;font-weight:700;height:30px;line-height:1.3;border-bottom:1px solid #000;margin-bottom:2px}
.msec{border:1px solid #999;margin-bottom:2px;padding:1px 3px;overflow:hidden}
.msec.changed{border:1.5px dashed #000}
.msec.origin{border-color:#000}
.mlabel{font-size:9px;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mel{display:flex;flex-wrap:wrap;gap:2px}
.mbtn,.mchip{font-size:9px;border:1px solid #000;padding:0 3px;height:15px;max-width:78px;white-space:nowrap;overflow:hidden}
.mchip{border-color:#999}
.mbtn.primary,.mchip.primary{background:#444;color:#fff}
.mvia{font-size:9px;color:#555}
table{border-collapse:collapse;margin-top:8px}
td,th{border:1px solid #999;padding:4px 6px;font-size:11px;text-align:left;vertical-align:top}
"""

def build():
    showpages = FIRST if SCOPE == "first" else order
    parts = []
    status_line = STATUS
    draft = '<div class="draft">유저 확인 전 초안</div>' if STATUS == "유저 확인 전 초안" else ""
    warn = "".join(f'<p class="warn">{E(w)}</p>' for w in WARN.split("||") if w)
    flows_out, metas = [], []
    if SCOPE != "first":
        for fl in flows:
            h, m = build_flow(fl); flows_out.append(h); metas.append(m)
    nav = ('<nav><b>목차</b> — <a href="#common">공통 섹션</a> · 페이지별 프레임: ' + " ".join(f'<a href="#{p}">{p}</a>' for p in showpages) +
           (' · 와이어플로: ' + " ".join(f'<a href="#{f["num"]}">{f["num"]}</a>' for f in flows) if SCOPE != "first" else "") + ' · <a href="#candidates">사이트맵 대조 결과</a></nav>')
    parts.append(f'<header>{draft}<h1>와이어프레임 — {E(title_line)}</h1>'
                 f'<p>기준 문서: sitemap/sitemap.md · user-flow/user-flow.md · 플랫폼: {E(platform)} · 진행 상태: {E(status_line)}</p>{warn}'
                 f'<p>읽는 법: 박스 = 사이트맵 섹션, 박스 왼쪽 위 = 섹션 번호와 이름(작은 글자는 기능 번호), 점선 박스 = 상태에 따라 바뀐 섹션, 가로 점선 = 첫 화면 경계, ··· = 동작 주석. '
                 f'진한 회색 버튼 = 그 화면의 핵심 행동 버튼. 와이어플로의 원 = 시작·목표, 마름모 = 분기, 밑줄 글자 = 유저 입력(화살표 위 문구), 가는 테두리 박스 = 단계·시스템 결과, 두 줄 테두리 = 외부 앱, 점선 회색 박스 = 메모.</p>{nav}</header>')
    parts.append(f'<section id="common"><h2>공통 섹션</h2>{common_html()}</section>')
    rows = []
    for p in showpages:
        row = [frame_html(p)]
        if SCOPE != "first":
            for s in states:
                if s["page"] == p: row.append(state_html(s))
        rows.append(f'<div class="rowwrap"><div class="row">{"".join(row)}</div></div>')
    parts.append(f'<section id="pages"><h2>페이지별 프레임</h2>{"".join(rows)}</section>')
    if SCOPE != "first":
        parts.append(f'<section id="flows"><h2>와이어플로</h2>{"".join(flows_out)}</section>')
    cand = json.load(open(os.path.join(DATA, "candidates.json")))
    if cand:
        tr = "".join(f'<tr><td>{E(c["kind"])}</td><td>{E(c["content"])}</td><td>{E(c["from"])}</td><td>{E(c["result"])}</td></tr>' for c in cand)
        ctab = f'<table><tr><th>종류</th><th>내용</th><th>나온 곳</th><th>반영 결과</th></tr>{tr}</table>'
    else:
        ctab = "<p>없음</p>"
    parts.append(f'<section id="candidates"><h2>사이트맵 대조 결과</h2>{ctab}</section>')
    doc = (f'<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           f'<title>와이어프레임 — {E(title_line)}</title>\n<style>{CSS}</style>\n</head>\n<body>\n' + "\n".join(parts) + '\n</body>\n</html>\n')
    os.makedirs(f"{RUN}/wireframe", exist_ok=True)
    open(f"{RUN}/wireframe/wireframe.html", "w").write(doc)
    info = dict(pages={p: dict(heading=pages[p]["heading"], nsec=len(pages[p]["sections"]),
                               nbox=len(re.findall(rf'class="sec" id="{p}-\d+"', doc))) for p in showpages},
                states=[dict(page=s["page"], pname=s["pname"], state=s["state"], when=s["when"], src=s["src"], extra=s["extra"],
                             changed=[f'{s["page"]}-{n}' for n in dsl.STATES[(s["page"], s["state"])]]) for s in states] if SCOPE != "first" else [],
                flows=metas)
    json.dump(info, open(os.path.join(DATA, "info.json"), "w"), ensure_ascii=False, indent=1)
    print("written", len(doc))

if __name__ == "__main__":
    build()
