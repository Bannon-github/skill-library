#!/usr/bin/env python3
"""Translate an original-language Show-transcript panel into English (or --tgt).

Used by fetch_youtube_transcript.py / route.py when no English track and no
YouTube-translated (tlang) track could be fetched, or when forced.

Input : raw/<id>/transcript.orig.<lang>.txt  (panel: "m:ss" line, then text line)
Output: raw/<id>/transcript.txt   (# header marks it machine-translated; timestamps kept)
        raw/<id>/raw.txt + raw    (English prose for distill)
        raw/<id>/translation.json (backend, model, glossary hits, segment count)
The original file is never modified. Nothing is invented: each output segment is
the backend's translation of exactly one source segment, same timestamp.

Backends (pluggable, --backend):
  argos           offline, free (argostranslate in .venv-translate). Default.
  libretranslate  HTTP; set LIBRETRANSLATE_URL (self-hosted) [+ LIBRETRANSLATE_KEY].
  none            passthrough (copies original; marks untranslated) for testing.
Add a backend: write `def _backend_x(segments, src, tgt) -> list[str]` and register it in BACKENDS.

Domain glossary (post-edit, never pre-injection): when a source segment contains a
known synth/DAW term (es "envolvente", de "Hüllkurve", ja "リバーブ") and the MT output
contains a known bad rendering ("cover", "hull curve", "riverb"), that rendering is
replaced with the English term. Pre-injecting English words into the source made
argos emit garbage (tested), so we only correct after translation. Term hits per
segment are saved in translation.json for the graph extractor.

Usage:
  .venv-translate/bin/python pipeline/translate_transcript.py raw/ID/transcript.orig.ja.txt --src ja
  .venv-translate/bin/python pipeline/translate_transcript.py --install-langs de,es,ja,fr,pt,it
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
GLOSSARY = HERE / "lexicons" / "translation_glossary.json"
TS = re.compile(r"^\d{1,2}(:\d{2}){1,2}$")


def parse_panel(text: str) -> list[tuple[str, str]]:
    rows, ts = [], None
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if TS.match(s):
            ts = s
            continue
        rows.append((ts or "0:00", s))
    return rows


def load_glossary(src: str) -> dict[str, str]:
    if not GLOSSARY.exists():
        return {}
    g = json.loads(GLOSSARY.read_text(encoding="utf-8"))
    return g.get(src, {})


def _has_term(src_text: str, term: str) -> bool:
    if all(ord(c) < 0x3000 for c in term):  # latin/cyrillic: word-ish, case-insensitive
        return re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", src_text, re.IGNORECASE) is not None
    return term in src_text


def post_edit(src_text: str, out_text: str, gloss: dict, hits: dict[str, int]) -> tuple[str, list[str]]:
    """Fix known MT mistranslations of domain terms present in the source segment."""
    seg_terms = []
    present = [t for t in gloss if _has_term(src_text, t)]
    legit = {gloss[t][0].lower() for t in present}
    for term in sorted(present, key=len, reverse=True):
        en, bads = gloss[term][0], gloss[term][1]
        seg_terms.append(en)
        hits[term] = hits.get(term, 0) + 1
        for b in sorted(bads, key=len, reverse=True):
            if b.lower() == en.lower() or b.lower() in legit:
                continue
            out_text = re.sub(r"(?<!\w)" + re.escape(b) + r"(?!\w)", en, out_text, flags=re.IGNORECASE)
    return out_text, seg_terms


# ---------------------------------------------------------------- backends
def _backend_argos(segments: list[str], src: str, tgt: str) -> list[str]:
    import argostranslate.translate as at
    langs = {l.code: l for l in at.get_installed_languages()}
    if src not in langs or tgt not in langs:
        raise RuntimeError(f"argos language pack {src}->{tgt} not installed (run --install-langs {src})")
    tr = langs[src].get_translation(langs[tgt])
    if tr is None:
        raise RuntimeError(f"no argos translation {src}->{tgt}")
    return [tr.translate(s) if s.strip() else s for s in segments]


def _backend_libretranslate(segments: list[str], src: str, tgt: str) -> list[str]:
    import urllib.request
    url = os.environ.get("LIBRETRANSLATE_URL")
    if not url:
        raise RuntimeError("LIBRETRANSLATE_URL not set")
    out = []
    for s in segments:
        body = {"q": s, "source": src, "target": tgt, "format": "text"}
        if os.environ.get("LIBRETRANSLATE_KEY"):
            body["api_key"] = os.environ["LIBRETRANSLATE_KEY"]
        req = urllib.request.Request(url.rstrip("/") + "/translate", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            out.append(json.loads(r.read())["translatedText"])
    return out


def _backend_none(segments: list[str], src: str, tgt: str) -> list[str]:
    return list(segments)


BACKENDS = {"argos": _backend_argos, "libretranslate": _backend_libretranslate, "none": _backend_none}


# Pinned packages: argos es->en 1.9 (BPE, 314 MB) emits garbage with argostranslate
# 1.11 / ctranslate2 4.8 (tested 2026-10-03); 1.0 is fine.
PINNED = {("es", "en"): "https://argos-net.com/v1/translate-es_en-1_0.argosmodel"}


def install_langs(codes: list[str], tgt: str = "en") -> list[str]:
    import tempfile
    import urllib.request
    import argostranslate.package as p
    p.update_package_index()
    av = p.get_available_packages()
    installed = {(x.from_code, x.to_code) for x in p.get_installed_packages()}
    done = []
    for c in codes:
        if (c, tgt) in installed:
            done.append(c)
            continue
        if (c, tgt) in PINNED:
            with tempfile.NamedTemporaryFile(suffix=".argosmodel") as f:
                urllib.request.urlretrieve(PINNED[(c, tgt)], f.name)
                p.install_from_path(f.name)
            done.append(c)
            continue
        m = [x for x in av if x.from_code == c and x.to_code == tgt]
        if m:
            p.install_from_path(m[0].download())
            done.append(c)
    return done


def looks_garbled(lines: list[str], tgt: str) -> float:
    """Share of output segments with foreign-script junk (MT model failure)."""
    if tgt != "en" or not lines:
        return 0.0
    bad = 0
    for l in lines:
        junk = sum(1 for ch in l if ord(ch) > 0x2E80 or 0x0370 <= ord(ch) <= 0x1FFF)
        if junk >= 2 or (l and junk / max(1, len(l)) > 0.05):
            bad += 1
    return bad / len(lines)


def group_segments(rows: list[tuple[str, str]], src: str, max_chars: int) -> list[tuple[str, str]]:
    """Auto tracks (esp. ja/zh) come as tiny fragments; group a few consecutive
    fragments under the first timestamp so the MT model sees a whole clause."""
    out: list[tuple[str, str]] = []
    sep = "" if src in ("ja", "zh") else " "
    for ts, txt in rows:
        if out and len(out[-1][1]) + len(txt) < max_chars and not re.search(r"[.!?。！？]$", out[-1][1]):
            out[-1] = (out[-1][0], out[-1][1] + sep + txt)
        else:
            out.append((ts, txt))
    return out


def translate_file(path: Path, src: str, tgt: str = "en", backend: str = "argos",
                   max_chars: int = 160) -> dict:
    dest = path.parent
    rows = parse_panel(path.read_text(encoding="utf-8"))
    if not rows:
        return {"ok": False, "error": "empty_original"}
    rows = group_segments(rows, src, max_chars)
    gloss = load_glossary(src)
    hits: dict[str, int] = {}
    t0 = time.time()
    out = BACKENDS[backend]([t for _, t in rows], src, tgt)
    if len(out) != len(rows):
        return {"ok": False, "error": "segment_count_mismatch"}
    seg_terms = []
    for i, ((ts, srctxt), o) in enumerate(zip(rows, out)):
        out[i], terms = post_edit(srctxt, o, gloss, hits)
        if terms:
            seg_terms.append({"t": ts, "terms": terms})
    garbled = looks_garbled(out, tgt)
    if garbled > 0.2:
        return {"ok": False, "error": "mt_output_garbled", "garbled_share": round(garbled, 2),
                "hint": "translation model failure; try another backend/package version. Nothing written."}
    header = (f"# MACHINE-TRANSLATED transcript ({src} -> {tgt}, backend={backend}). "
              f"Original words: {path.name}. Timestamps are from the original track.")
    panel = header + "\n" + "\n".join(f"{ts}\n{txt.strip()}" for (ts, _), txt in zip(rows, out)) + "\n"
    prose = "\n\n".join(t.strip() for t in out if t.strip()) + "\n"
    (dest / "transcript.txt").write_text(panel, encoding="utf-8")
    (dest / "raw.txt").write_text(prose, encoding="utf-8")
    (dest / "raw").write_text(prose, encoding="utf-8")
    info = {
        "ok": True,
        "backend": backend,
        "src": src,
        "tgt": tgt,
        "segments": len(rows),
        "glossary_hits": hits,
        "garbled_share": round(garbled, 3),
        "segment_terms": seg_terms,
        "seconds": round(time.time() - t0, 1),
        "original_path": str(path),
        "output_path": str(dest / "transcript.txt"),
        "translated": backend != "none",
        "at": datetime.now(timezone.utc).isoformat(),
    }
    (dest / "translation.json").write_text(json.dumps(info, indent=2, ensure_ascii=False) + "\n")
    return info


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path", nargs="?", help="transcript.orig.<lang>.txt")
    ap.add_argument("--src", help="source language code (default: from filename)")
    ap.add_argument("--tgt", default="en")
    ap.add_argument("--backend", default="argos", choices=sorted(BACKENDS))
    ap.add_argument("--max-chars", type=int, default=160)
    ap.add_argument("--install-langs", help="comma list of source langs to install (argos)")
    ap.add_argument("--json", action="store_true", help="print one JSON line result")
    a = ap.parse_args()
    if a.install_langs:
        print(json.dumps({"installed": install_langs(a.install_langs.split(","), a.tgt)}))
        return 0
    if not a.path:
        ap.error("path required")
    p = Path(a.path)
    src = a.src or (re.search(r"orig\.([a-z]{2,3})", p.name) or [None, None])[1]
    if not src:
        ap.error("--src required")
    try:
        info = translate_file(p, src.split("-")[0], a.tgt, a.backend, a.max_chars)
    except Exception as e:  # noqa: BLE001
        info = {"ok": False, "error": f"{type(e).__name__}: {e}"}
    print(json.dumps(info, ensure_ascii=False))
    return 0 if info.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
