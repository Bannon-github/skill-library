#!/usr/bin/env python3
"""Parse an English Show-transcript into a refined JSON graph of useful data.

Input : raw/<id>/transcript.txt (panel style; '#' header lines ignored)
Output: raw/<id>/graph.json  (local; evidence quotes are creators' words, gitignored)

Nodes  (id = "<type>:<canonical>"):
  concept | module | param | value | tool | step | phrase
Edges:
  sets      param/module -> value       ("cutoff ... 500 Hz", "+7 semitones")
  affects   mod source   -> param/module ("LFO to the cutoff", "velocity controls ...")
  precedes  step -> next step           (ordered procedure)
  part-of   param -> module (lexicon), module -> tool (co-mentioned in one window)
  mentions  step -> term                (which terms a step uses)
Every node/edge carries evidence [{t, quote<=160 chars}] (max 5) and a count.

Domain lexicons: pipeline/lexicons/<domain>.json (synth, blender, crypto,
sidehustle, drone). Domain auto-detected by lexicon hit density unless --domain.
Phrase/collocation extraction (bigram/trigram, frequency + PMI) surfaces
repeated multi-word terms the lexicon doesn't know yet (type "phrase").
Stdlib only, deterministic. Never invents text: quotes are verbatim slices.

Usage:
  python3 pipeline/extract_terms_graph.py <video_id> [--domain synth] [--print-stats]
  python3 pipeline/extract_terms_graph.py --text-file some.txt --video-id X
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/workspace/skill-library")
RAW = ROOT / "raw"
LEX_DIR = Path(__file__).resolve().parent / "lexicons"
TS = re.compile(r"^\d{1,2}(:\d{2}){1,2}$")

STOP = set("""a an the and or but so to of in on at for with from by as is are was were be been being it its
this that these those i you he she we they me my your our their them us just like really very kind sort
gonna wanna gotta going go get got do does did done have has had can could would should will shall may
might must not no yes okay ok um uh yeah right now then here there what which who how when where why all
any some more most much many little bit lot also too into out up down over again about if than because
let lets let's see look make made thing things way one two three really actually basically something
want need think know mean say said little pretty good great nice cool awesome guys everyone today video channel subscribe gonna i'm it's that's we're you're don't we'll i'll you'll
""".split())

ACTION_VERBS = re.compile(
    r"\b(set|sets|setting|turn|turning|add|adding|increase|increasing|raise|raising|lower|lowering|"
    r"drop|dropping|bring|bringing|route|routing|drag|dragging|assign|assigning|select|choose|"
    r"enable|enabling|switch|switching|copy|duplicate|automate|automating|pan|panning|detune|"
    r"layer|layering|apply|insert|load|loading|press|click|use|using|put|putting|boost|cut|cutting|"
    r"dial|dialing|push|pushing|pull|reduce|reducing|open|opening|map|mapping|modulate|modulating|"
    r"sweep|change|changing|move|moving|stack|stacking|bounce|resample|record)\b", re.I)
STEP_CUES = re.compile(r"\b(first|then|next|now|after that|finally|step|start by|let's|we'll|go ahead)\b", re.I)
CONNECT = re.compile(r"\b(to|into|onto|on|controls?|controlling|modulat\w*|drives?|driving|affects?|mapped|assign\w*|rout\w*)\b", re.I)

NUMWORDS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
            "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fifteen": 15, "sixteen": 16, "twenty": 20,
            "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
            "hundred": 100}
UNITS = (r"(hz|hertz|khz|kilohertz|ms|milliseconds?|seconds?|sec|%|percent|db|decibels?|semitones?|"
         r"semis?|cents?|voices?|bpm|octaves?|bars?|beats?|steps?|degrees?|mm|millimeters?|meters?|"
         r"fps|iterations?|samples?)")
VALUE_RE = re.compile(r"(?<![\w.])([-+]?\d+(?:[.,]\d+)?|" + "|".join(NUMWORDS) + r")\s*" + UNITS + r"\b", re.I)
VALUE_RE2 = re.compile(r"(?<![\w.])(\d+(?:[.,]\d+)?)\s*(%|ms|hz|khz|db)", re.I)


def fmt_t(sec: float) -> str:
    sec = int(sec)
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def parse_ts(s: str) -> float:
    parts = [int(x) for x in s.split(":")]
    v = 0
    for p in parts:
        v = v * 60 + p
    return float(v)


def load_segments(path: Path) -> list[tuple[float, str]]:
    segs, t = [], 0.0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if TS.match(s):
            t = parse_ts(s)
            continue
        s = re.sub(r"\[(music|applause|laughter|música|音楽)\]", " ", s, flags=re.I).strip()
        if s:
            segs.append((t, s))
    return segs


def windows(segs: list[tuple[float, str]], max_chars: int = 240) -> list[tuple[float, str]]:
    out: list[tuple[float, str]] = []
    for t, s in segs:
        if out and len(out[-1][1]) + len(s) + 1 <= max_chars and not re.search(r"[.!?]$", out[-1][1]):
            out[-1] = (out[-1][0], out[-1][1] + " " + s)
        else:
            out.append((t, s))
    return out


# ------------------------------------------------------------------ lexicons
def load_lexicons() -> dict[str, dict]:
    lex = {}
    for p in sorted(LEX_DIR.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if "domain" in d:
            lex[d["domain"]] = d
    return lex


class Matcher:
    """Alias -> (type, canonical) matcher with word boundaries, longest-first."""

    def __init__(self, lex: dict):
        self.lex = lex
        entries: list[tuple[str, str, str]] = []
        for canon, aliases in lex.get("modules", {}).items():
            entries += [(a, "module", canon) for a in aliases]
        for canon, spec in lex.get("params", {}).items():
            entries += [(a, "param", canon) for a in spec["aliases"]]
        for canon, aliases in lex.get("tools", {}).items():
            entries += [(a, "tool", canon) for a in aliases]
        for canon, aliases in lex.get("concepts", {}).items():
            entries += [(a, "concept", canon) for a in aliases]
        seen = {}
        for a, ty, c in entries:  # first definition wins for an alias
            seen.setdefault(a.lower(), (ty, c))
        self.alias = seen
        alts = sorted(seen, key=len, reverse=True)
        self.rx = re.compile(r"(?<![\w-])(" + "|".join(re.escape(a) for a in alts) + r")(?![\w-])", re.I)
        self.param_module = {c: s.get("module") for c, s in lex.get("params", {}).items()}
        ms = {}
        for canon, aliases in lex.get("mod_sources", {}).items():
            for a in aliases:
                ms[a.lower()] = canon
        self.mod_alias = ms
        self.unit_targets = lex.get("unit_targets", {})

    def find(self, text: str) -> list[dict]:
        hits = []
        for m in self.rx.finditer(text):
            a = m.group(1).lower()
            ty, c = self.alias[a]
            hits.append({"alias": a, "type": ty, "canon": c, "start": m.start(), "end": m.end(),
                         "mod_source": self.mod_alias.get(a)})
        return hits


def detect_domain(text: str, lexicons: dict[str, dict]) -> tuple[str, dict[str, int]]:
    scores = {}
    for d, lx in lexicons.items():
        scores[d] = len(Matcher(lx).find(text))
    best = max(scores, key=scores.get) if scores else "synth"
    return best, scores


def norm_value(num: str, unit: str) -> str:
    n = num.lower().replace(",", ".")
    if n in NUMWORDS:
        n = str(NUMWORDS[n])
    u = unit.lower()
    u = {"hertz": "hz", "kilohertz": "khz", "milliseconds": "ms", "millisecond": "ms", "percent": "%",
         "decibels": "db", "decibel": "db", "semitone": "semitones", "semis": "semitones", "semi": "semitones",
         "cent": "cents", "voice": "voices", "octave": "octaves", "second": "s", "seconds": "s", "sec": "s",
         "bar": "bars", "beat": "beats", "step": "steps", "degree": "degrees", "millimeter": "mm",
         "millimeters": "mm", "meter": "m", "meters": "m", "iteration": "iterations", "sample": "samples"}.get(u, u)
    return f"{n} {u}"


# ------------------------------------------------------------------ graph
class Graph:
    def __init__(self, video_id: str):
        self.video_id = video_id
        self.nodes: dict[str, dict] = {}
        self.edges: dict[tuple[str, str, str], dict] = {}

    @staticmethod
    def _ev(lst: list, t: float, quote: str) -> None:
        if len(lst) < 5 and not any(e["t"] == fmt_t(t) for e in lst):
            lst.append({"t": fmt_t(t), "quote": quote[:160]})

    def node(self, ty: str, canon: str, label: str, t: float, quote: str, **attrs) -> str:
        nid = f"{ty}:{canon}"
        n = self.nodes.setdefault(nid, {"id": nid, "type": ty, "label": label, "count": 0, "evidence": [], **attrs})
        n["count"] += 1
        self._ev(n["evidence"], t, quote)
        return nid

    def edge(self, src: str, dst: str, ty: str, t: float, quote: str, **attrs) -> None:
        if src == dst:
            return
        k = (src, dst, ty)
        e = self.edges.setdefault(k, {"src": src, "dst": dst, "type": ty, "count": 0, "evidence": [], **attrs})
        e["count"] += 1
        self._ev(e["evidence"], t, quote)

    def to_json(self) -> dict:
        return {"nodes": list(self.nodes.values()), "edges": list(self.edges.values())}


def collocations(segs: list[tuple[float, str]], known: set[str], min_count: int = 3, top: int = 25) -> list[dict]:
    toks_all: list[str] = []
    first_t: dict[str, float] = {}
    for t, s in segs:
        toks = re.findall(r"[a-z][a-z0-9'+-]*", s.lower())
        toks_all += toks + ["|"]
    uni = Counter(toks_all)
    total = max(1, len(toks_all))
    grams = Counter()
    for n in (2, 3):
        for i in range(len(toks_all) - n + 1):
            g = toks_all[i:i + n]
            if "|" in g or g[0] in STOP or g[-1] in STOP or any(len(x) < 3 for x in (g[0], g[-1])):
                continue
            if sum(1 for x in g if x in STOP) > (n - 2):
                continue
            grams[" ".join(g)] += 1
    out = []
    for g, c in grams.items():
        if c < min_count or g in known:
            continue
        parts = g.split()
        pmi = math.log((c / total) / math.prod(uni[p] / total for p in parts) + 1e-12)
        out.append({"phrase": g, "count": c, "pmi": round(pmi, 2)})
    out.sort(key=lambda r: (r["count"] * max(r["pmi"], 0.1)), reverse=True)
    # drop phrases contained in a higher-ranked longer phrase with same count
    kept = []
    for r in out:
        if any(r["phrase"] in k["phrase"] and k["count"] >= r["count"] for k in kept):
            continue
        kept.append(r)
    for r in kept[:top]:
        for t, s in segs:
            if r["phrase"] in s.lower():
                first_t[r["phrase"]] = t
                r["quote"] = s[:160]
                break
        r["t"] = fmt_t(first_t.get(r["phrase"], 0))
    return kept[:top]


def build_graph(video_id: str, segs: list[tuple[float, str]], domain: str | None = None,
                meta: dict | None = None) -> dict:
    lexicons = load_lexicons()
    full = " ".join(s for _, s in segs)
    det, scores = detect_domain(full, lexicons)
    domain = domain or det
    lx = lexicons[domain]
    M = Matcher(lx)
    G = Graph(video_id)
    wins = windows(segs)
    step_ids: list[str] = []
    for t, w in wins:
        hits = M.find(w)
        ids = []
        for h in hits:
            ids.append(G.node(h["type"], h["canon"], h["canon"].replace("_", " "), t, w))
            if h["type"] == "param":
                mod = M.param_module.get(h["canon"])
                if mod:
                    mid = G.node("module", mod, mod.replace("_", " "), t, w)
                    G.edge(f"param:{h['canon']}", mid, "part-of", t, w, source="lexicon")
        # module -> tool co-mention
        tools = [h for h in hits if h["type"] == "tool"]
        for tl in tools:
            for h in hits:
                if h["type"] == "module":
                    G.edge(f"module:{h['canon']}", f"tool:{tl['canon']}", "part-of", t, w, source="co-mention")
        # values -> nearest preceding param/module within 70 chars
        for vm in list(VALUE_RE.finditer(w)) + [m for m in VALUE_RE2.finditer(w)]:
            val = norm_value(vm.group(1), vm.group(2))
            unit = val.split(" ", 1)[1]
            allowed = M.unit_targets.get(unit)
            ok = (lambda h: allowed is None or h["canon"] in allowed)
            prev = [h for h in hits if h["type"] in ("param", "module") and h["end"] <= vm.start()
                    and vm.start() - h["end"] <= 70 and ok(h)]
            nxt = [h for h in hits if h["type"] in ("param", "module") and h["start"] >= vm.end(1)
                   and h["start"] - vm.end() <= 25 and ok(h)]
            # an immediately following noun ("24 dB slope", "24 decibel slope") beats an earlier mention
            if nxt and nxt[0]["start"] - vm.end() <= 3:
                tgt = nxt[0]
            else:
                tgt = prev[-1] if prev else (nxt[0] if nxt else None)
            if not tgt:
                continue
            vid = G.node("value", f"{tgt['canon']}={val}", val, t, w, of=f"{tgt['type']}:{tgt['canon']}")
            G.edge(f"{tgt['type']}:{tgt['canon']}", vid, "sets", t, w, value=val)
        # affects: mod source ... connector ... target param/module
        for i, s in enumerate(hits):
            if not s["mod_source"]:
                continue
            for tg in hits[i + 1:]:
                if tg["type"] not in ("param", "module") or tg["start"] - s["end"] > 60:
                    continue
                if tg["canon"] == s["canon"] or (tg["type"] == "module" and tg["canon"] == s["mod_source"]):
                    continue
                if tg["type"] == "param" and M.param_module.get(tg["canon"]) == s["mod_source"]:
                    continue  # envelope -> attack is part-of, not modulation
                between = w[s["end"]:tg["start"]]
                if CONNECT.search(between):
                    G.edge(f"{s['type']}:{s['canon']}", f"{tg['type']}:{tg['canon']}", "affects", t, w,
                           via=s["mod_source"])
                    break
        # steps
        terms = {f"{h['type']}:{h['canon']}" for h in hits if h["type"] in ("param", "module", "concept")}
        if terms and ACTION_VERBS.search(w) and (STEP_CUES.search(w) or len(terms) >= 2):
            sid = G.node("step", f"{video_id}@{fmt_t(t)}", w[:140], t, w, at=fmt_t(t))
            for term in sorted(terms):
                G.edge(sid, term, "mentions", t, w)
            if step_ids:
                G.edge(step_ids[-1], sid, "precedes", t, w)
            step_ids.append(sid)
    known = set(M.alias)
    phrases = collocations(segs, known)
    for p in phrases:
        G.node("phrase", p["phrase"].replace(" ", "_"), p["phrase"], parse_ts(p["t"]), p.get("quote", ""),
               pmi=p["pmi"], freq=p["count"])
        G.nodes[f"phrase:{p['phrase'].replace(' ', '_')}"]["count"] = p["count"]
    gj = G.to_json()
    by_type = Counter(n["type"] for n in gj["nodes"])
    e_type = Counter(e["type"] for e in gj["edges"])
    return {
        "schema": "yt-knowledge-graph/v1",
        "video_id": video_id,
        "domain": domain,
        "domain_scores": scores,
        "source": {k: (meta or {}).get(k) for k in ("title", "route", "translated", "translation_method",
                                                    "language_code", "original_language", "is_generated")},
        "stats": {"segments": len(segs), "windows": len(wins), "nodes": len(gj["nodes"]),
                  "edges": len(gj["edges"]), "nodes_by_type": dict(by_type), "edges_by_type": dict(e_type),
                  "words": len(full.split())},
        **gj,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a term/relation graph from a transcript")
    ap.add_argument("vid", nargs="?", metavar="video_id")
    ap.add_argument("--text-file", help="panel transcript path (default raw/<id>/transcript.txt)")
    ap.add_argument("--video-id", dest="vid_opt")
    ap.add_argument("--domain")
    ap.add_argument("--out")
    ap.add_argument("--print-stats", action="store_true")
    a = ap.parse_args()
    vid = a.vid or a.vid_opt
    if not vid:
        ap.error("video_id required")
    path = Path(a.text_file) if a.text_file else RAW / vid / "transcript.txt"
    meta_p = RAW / vid / "meta.json"
    meta = json.loads(meta_p.read_text()) if meta_p.exists() else {}
    segs = load_segments(path)
    g = build_graph(vid, segs, a.domain, meta)
    out = Path(a.out) if a.out else RAW / vid / "graph.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(g, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({"video_id": vid, "domain": g["domain"], "out": str(out), **g["stats"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
