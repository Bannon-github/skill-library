#!/usr/bin/env python3
"""Build prior-art/index.json from vendored clones + awesome README listings."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/workspace/skill-library/prior-art")
VENDORS = ROOT / "vendors"
RAW = ROOT / "raw"
OUT = ROOT / "index.json"
RETRIEVED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

DOMAIN_HINTS = [
    (re.compile(r"blender|3d|gaussian|splat|mesh|geometry|viewport|donut|lowpoly", re.I), "blender-3d"),
    (re.compile(r"synth|audio|music|pad|osc|wavetable|daw|fm\b|sound|remotion|video|cinematic|fal-audio|venice-audio", re.I), "synth-cinematic"),
    (re.compile(r"crypto|binance|coinbase|wallet|token|trading|defi|web3|blockchain|spot\b", re.I), "crypto-tooling"),
    (re.compile(r"side.?hustle|marketing|seo|ads?|copywrit|cold-email|launch|pricing|growth|sales|referral", re.I), "side-hustle"),
    (re.compile(r"agent|skill|mcp|debug|code.?review|plan|tdd|git|pr\b|claude|cursor|openai", re.I), "general-agent"),
]


def domains_for(*texts: str) -> list[str]:
    blob = " ".join(t for t in texts if t)
    found = []
    for rx, name in DOMAIN_HINTS:
        if rx.search(blob):
            found.append(name)
    return found or ["general-agent"]


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[3:end]
    meta: dict = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def add(entries: list, seen: set, *, id: str, name: str, goal: str, source: str, url: str, domains: list[str] | None = None):
    key = f"{source}::{id}".lower()
    if key in seen:
        return
    seen.add(key)
    entries.append(
        {
            "id": id,
            "name": name,
            "goal_or_summary": goal[:400],
            "source_collection": source,
            "url": url,
            "domains": domains or domains_for(id, name, goal),
            "retrieved_at": RETRIEVED,
        }
    )


def harvest_vendors(entries: list, seen: set):
    mapping = {
        "anthropics-skills": ("anthropics/skills", "https://github.com/anthropics/skills/tree/main/skills/{id}"),
        "huggingface-skills": ("huggingface/skills", "https://github.com/huggingface/skills/tree/main/skills/{id}"),
        "obra-superpowers": ("obra/superpowers", "https://github.com/obra/superpowers/tree/main/skills/{id}"),
        "vercel-agent-skills": ("vercel-labs/agent-skills", "https://github.com/vercel-labs/agent-skills/tree/main/skills/{id}"),
        "microsoft-azure-skills": ("microsoft/azure-skills", "https://github.com/microsoft/azure-skills/tree/main/skills/{id}"),
        "remotion-skills": ("remotion-dev/skills", "https://github.com/remotion-dev/skills/tree/main/skills/{id}"),
        "coreyhaines-marketingskills": ("coreyhaines31/marketingskills", "https://github.com/coreyhaines31/marketingskills/tree/main/skills/{id}"),
    }
    for slug, (source, url_tmpl) in mapping.items():
        base = VENDORS / slug / "skills"
        if not base.exists():
            continue
        for skill_md in base.rglob("SKILL.md"):
            # id = immediate parent of SKILL.md if under skills/, else relative
            rel = skill_md.relative_to(base)
            parts = rel.parts
            sid = parts[0] if len(parts) >= 2 else skill_md.parent.name
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            meta = parse_frontmatter(text)
            name = meta.get("name") or sid.replace("-", " ")
            goal = meta.get("description") or ""
            if not goal:
                # first non-empty markdown heading/paragraph after frontmatter
                body = text.split("---", 2)[-1] if text.startswith("---") else text
                for line in body.splitlines():
                    line = line.strip()
                    if line and not line.startswith("#"):
                        goal = line[:400]
                        break
                    if line.startswith("# "):
                        goal = line[2:][:400]
                        break
            add(
                entries,
                seen,
                id=sid,
                name=name,
                goal=goal or f"Agent skill: {sid}",
                source=source,
                url=url_tmpl.format(id=sid),
            )

    # mattpocock nested under skills/{category}/{id}
    mp = VENDORS / "mattpocock-skills" / "skills"
    if mp.exists():
        for skill_md in mp.rglob("SKILL.md"):
            sid = skill_md.parent.name
            cat = skill_md.parent.parent.name if skill_md.parent.parent != mp else ""
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            meta = parse_frontmatter(text)
            name = meta.get("name") or sid.replace("-", " ")
            goal = meta.get("description") or f"Matt Pocock skill ({cat}): {sid}"
            add(
                entries,
                seen,
                id=sid,
                name=name,
                goal=goal,
                source="mattpocock/skills",
                url=f"https://github.com/mattpocock/skills/tree/main/skills/{cat}/{sid}" if cat else f"https://github.com/mattpocock/skills/tree/main/skills/{sid}",
            )

    # cursorrules
    rules = VENDORS / "awesome-cursorrules" / "rules"
    if rules.exists():
        for p in sorted(rules.glob("*.mdc")):
            sid = p.stem
            # skim first ~2k for description
            text = p.read_text(encoding="utf-8", errors="replace")[:2500]
            meta = parse_frontmatter(text)
            goal = meta.get("description") or meta.get("globs") or f"Cursor rule: {sid}"
            name = meta.get("description") or sid.replace("-", " ").replace("_", " ")
            if len(name) > 80:
                name = sid.replace("-", " ")
            add(
                entries,
                seen,
                id=sid,
                name=name if isinstance(name, str) else sid,
                goal=str(goal)[:400],
                source="PatrickJS/awesome-cursorrules",
                url=f"https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/{p.name}",
            )


def harvest_voltagent_readme(entries: list, seen: set):
    path = RAW / "voltagent-awesome-agent-skills-README.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    # - **[owner/name](url)** - summary
    pat = re.compile(
        r"-\s+\*\*\[([^\]]+)\]\(([^)]+)\)\*\*\s*[-–—]\s*(.+)"
    )
    for m in pat.finditer(text):
        label, url, summary = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        # skip non-skill noise links
        if "become a sponsor" in label.lower():
            continue
        sid = label.split("/")[-1].lower().replace(" ", "-")
        # normalize id from path if officialskills
        if "/skills/" in url:
            sid = url.rstrip("/").split("/skills/")[-1].split("?")[0]
        elif "tree/main/" in url:
            sid = url.rstrip("/").split("/")[-1]
        add(
            entries,
            seen,
            id=sid,
            name=label,
            goal=summary,
            source="VoltAgent/awesome-agent-skills",
            url=url,
        )


def harvest_skills_sh_leaderboard(entries: list, seen: set):
    # Curated from skills.sh fetch (2026-09-24) — names + known repos
    board = [
        ("find-skills", "Discover and install agent skills", "vercel-labs/skills", "https://www.skills.sh/", ["general-agent"]),
        ("grill-me", "Socratic grilling for requirements", "mattpocock/skills", "https://github.com/mattpocock/skills", ["general-agent"]),
        ("agent-browser", "Browser automation for agents", "vercel-labs/agent-browser", "https://github.com/vercel-labs/agent-browser", ["general-agent"]),
        ("frontend-design", "Frontend design and UI/UX", "anthropics/skills", "https://github.com/anthropics/skills/tree/main/skills/frontend-design", ["general-agent"]),
        ("vercel-react-best-practices", "React best practices for Vercel", "vercel-labs/agent-skills", "https://github.com/vercel-labs/agent-skills", ["general-agent"]),
        ("video-edit", "Video editing workflows", "genmedia-labs/skills", "https://www.skills.sh/", ["synth-cinematic"]),
        ("remotion-best-practices", "Programmatic video with Remotion", "remotion-dev/skills", "https://github.com/remotion-dev/skills", ["synth-cinematic"]),
        ("ai-video-generation", "AI video generation pipelines", "101-skills/superpowers", "https://www.skills.sh/", ["synth-cinematic"]),
        ("ai-image-generation", "AI image generation", "101-skills/superpowers", "https://www.skills.sh/", ["general-agent"]),
        ("supabase-postgres-best-practices", "Postgres best practices for Supabase", "supabase/agent-skills", "https://github.com/supabase/agent-skills", ["general-agent"]),
        ("microsoft-foundry", "Microsoft Azure AI Foundry", "microsoft/azure-skills", "https://github.com/microsoft/azure-skills", ["general-agent"]),
        ("brainstorming", "Structured brainstorming", "obra/superpowers", "https://github.com/obra/superpowers", ["general-agent"]),
        ("systematic-debugging", "Systematic debugging workflow", "obra/superpowers", "https://github.com/obra/superpowers", ["general-agent"]),
        ("test-driven-development", "TDD workflow skill", "obra/superpowers", "https://github.com/obra/superpowers", ["general-agent"]),
        ("seo-audit", "Technical and on-page SEO audit", "coreyhaines31/marketingskills", "https://github.com/coreyhaines31/marketingskills", ["side-hustle"]),
        ("pdf", "PDF create/edit/extract", "anthropics/skills", "https://github.com/anthropics/skills/tree/main/skills/pdf", ["general-agent"]),
        ("docx", "Word document skills", "anthropics/skills", "https://github.com/anthropics/skills/tree/main/skills/docx", ["general-agent"]),
        ("xlsx", "Excel spreadsheet skills", "anthropics/skills", "https://github.com/anthropics/skills/tree/main/skills/xlsx", ["general-agent"]),
        ("skill-creator", "Create new agent skills", "anthropics/skills", "https://github.com/anthropics/skills/tree/main/skills/skill-creator", ["general-agent"]),
        ("fal-3d", "Generate 3D models from text/images via fal.ai", "fal-ai-community", "https://www.skills.sh/", ["blender-3d"]),
        ("fal-audio", "TTS/STT via fal.ai", "fal-ai-community", "https://www.skills.sh/", ["synth-cinematic"]),
        ("venice-audio-music", "Music generation via Venice API", "veniceai/skills", "https://github.com/veniceai/skills", ["synth-cinematic"]),
        ("binance-spot", "Binance spot trading via API", "binance", "https://www.skills.sh/", ["crypto-tooling"]),
        ("query-token-audit", "Token security audit (honeypot/scam)", "binance", "https://www.skills.sh/", ["crypto-tooling"]),
        ("composio", "Connect agents to 1000+ apps via Composio MCP", "composiohq", "https://github.com/ComposioHQ/composio-mcp-plugin", ["general-agent"]),
        ("blender-python-addon", "Blender Python addon Cursor rule", "PatrickJS/awesome-cursorrules", "https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/blender-python-addon.mdc", ["blender-3d"]),
    ]
    for sid, goal, source, url, domains in board:
        add(entries, seen, id=sid, name=sid.replace("-", " "), goal=goal, source=f"skills.sh/{source}", url=url, domains=domains)


def harvest_peers(entries: list, seen: set):
    peers = [
        ("agentskills-spec", "Agent Skills open format (SKILL.md)", "agentskills/agentskills", "https://agentskills.io/specification", ["general-agent"]),
        ("skills-sh-directory", "Public agent skills directory / leaderboard", "skills.sh", "https://www.skills.sh/", ["general-agent"]),
        ("officialskills-sh", "Official skills mirror used by VoltAgent listings", "officialskills.sh", "https://officialskills.sh/", ["general-agent"]),
        ("agentic-awesome-skills", "Installable library of 1900+ SKILL.md playbooks", "AliasgharArabi/agentic-awesome-skills", "https://github.com/AliasgharArabi/agentic-awesome-skills", ["general-agent"]),
        ("alirezarezvani-claude-skills", "380+ Claude Code / multi-agent skills pack", "alirezarezvani/claude-skills", "https://github.com/alirezarezvani/claude-skills", ["general-agent"]),
        ("youtube-skills-mcp", "Our YouTube Practical Skills Library (de-dupe peer, not external prior-art to skip wholesale)", "youtube-skills", "skill://", ["synth-cinematic", "blender-3d", "crypto-tooling", "side-hustle", "general-agent"]),
    ]
    for sid, goal, source, url, domains in peers:
        add(entries, seen, id=sid, name=sid.replace("-", " "), goal=goal, source=source, url=url, domains=domains)


def main():
    entries: list = []
    seen: set = set()
    harvest_vendors(entries, seen)
    harvest_voltagent_readme(entries, seen)
    harvest_skills_sh_leaderboard(entries, seen)
    harvest_peers(entries, seen)
    entries.sort(key=lambda e: (e["source_collection"], e["id"]))
    doc = {
        "schema_version": "1.0",
        "title": "YouTube Distillery Prior-Art Index",
        "retrieved_at": RETRIEVED,
        "count": len(entries),
        "notes": (
            "Machine-readable catalog of external agent skills / Cursor rules / MCP skill packs. "
            "Distill runs must novelty-check candidates against this index + local mcp-publish. "
            "youtube-skills entries are peers for de-dupe, not reasons to skip the domain."
        ),
        "skills": entries,
    }
    OUT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    # domain tallies
    from collections import Counter
    c = Counter()
    for e in entries:
        for d in e["domains"]:
            c[d] += 1
    print(f"Wrote {OUT} with {len(entries)} entries")
    print("domains:", dict(c))
    src = Counter(e["source_collection"] for e in entries)
    print("top sources:", src.most_common(12))


if __name__ == "__main__":
    main()
