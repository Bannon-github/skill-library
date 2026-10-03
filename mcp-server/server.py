#!/usr/bin/env python3
"""MCP server: YouTube Practical Skills Library (MCP SDK 2.x)."""
from __future__ import annotations

import json
from pathlib import Path

from mcp.server.mcpserver import MCPServer

ROOT = Path("/workspace/skill-library/mcp-publish")
SKILLS = ROOT / "skills"
ALIASES = ROOT / "aliases.json"


def _resolve(skill_id: str) -> str:
    """Map retired (merged-away) ids to their current id."""
    try:
        return json.loads(ALIASES.read_text()).get("aliases", {}).get(skill_id, skill_id)
    except (OSError, json.JSONDecodeError):
        return skill_id

mcp = MCPServer(
    "youtube-skills",
    instructions=(
        "Agent-consumable skills extracted from YouTube how-to transcripts. "
        "Tools: list_skills, get_skill, search_skills. Resources: skill://{id}."
    ),
)


def _load_all():
    skills = []
    for p in sorted(SKILLS.glob("*.json")):
        skills.append(json.loads(p.read_text()))
    return skills


@mcp.tool()
def list_skills() -> str:
    """List all published skills (id, name, goal, domain, mcp URI)."""
    rows = [
        {
            "id": s["id"],
            "name": s["name"],
            "goal": s["goal"],
            "domain": s.get("domain"),
            "mcp_resource": s.get("mcp_resource", f"skill://{s['id']}"),
            "curriculum_ids": s.get("curriculum_ids", []),
        }
        for s in _load_all()
    ]
    return json.dumps({"count": len(rows), "skills": rows}, indent=2)


@mcp.tool()
def get_skill(skill_id: str) -> str:
    """Fetch one AgentConsumableSkill v1 document by id."""
    path = SKILLS / f"{_resolve(skill_id)}.json"
    if not path.exists():
        return json.dumps({"error": "not_found", "skill_id": skill_id})
    return path.read_text()


@mcp.tool()
def search_skills(query: str) -> str:
    """Search skills by substring in id, name, goal, domain, or tags."""
    q = query.lower().strip()
    hits = []
    for s in _load_all():
        blob = " ".join(
            [
                s.get("id", ""),
                s.get("name", ""),
                s.get("goal", ""),
                s.get("domain", ""),
                " ".join(s.get("tags", [])),
                " ".join(s.get("aliases", [])),
            ]
        ).lower()
        if q in blob:
            hits.append(
                {
                    "id": s["id"],
                    "name": s["name"],
                    "goal": s["goal"],
                    "domain": s.get("domain"),
                }
            )
    return json.dumps({"query": query, "count": len(hits), "skills": hits}, indent=2)


@mcp.resource("skill://{skill_id}")
def skill_resource(skill_id: str) -> str:
    """Read a published skill as an MCP resource."""
    path = SKILLS / f"{_resolve(skill_id)}.json"
    if not path.exists():
        return json.dumps({"error": "not_found", "skill_id": skill_id})
    return path.read_text()


if __name__ == "__main__":
    mcp.run()
