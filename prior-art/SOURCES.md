# Prior-art sources

Collections relevant to agent skills. Relevance is relative to **our** domains: synth/cinematic, blender/3d, crypto tooling, side-hustle procedures, general agent how-tos.

_Last reviewed: 2026-09-24 (PT)._

| # | Name | URL | License (known) | Rough size / scope | How to re-fetch | Relevance |
|---|------|-----|-----------------|--------------------|-----------------|-----------|
| 1 | **Anthropic skills** | https://github.com/anthropics/skills · https://agentskills.io | Apache-2.0 (examples); document skills source-available | ~19 example skills (docx/pdf/pptx/xlsx, frontend-design, mcp-builder, skill-creator, …) | `git -C vendors/anthropics-skills pull` or re-list `skills/`; rebuild index | **High** for general-agent (do not restate); **Low** for synth/blender |
| 2 | **skills.sh** (Agent Skills Directory) | https://www.skills.sh/ | Directory (upstream licenses vary) | Leaderboard of installable skills across orgs (Anthropic, Vercel, Microsoft, Remotion, Matt Pocock, …) | Re-fetch homepage / org pages; merge into `index.json` via build script | **High** awareness hub |
| 3 | **VoltAgent awesome-agent-skills** | https://github.com/VoltAgent/awesome-agent-skills · https://officialskills.sh/ | MIT (list) | **1497+** curated official/community skills (Stripe, Cloudflare, Binance, HF, Trail of Bits, OpenAI, …) | `curl -o raw/voltagent-awesome-agent-skills-README.md` raw README; rebuild | **High** mega-index |
| 4 | **Hugging Face skills** | https://github.com/huggingface/skills · Hub Agents docs | Apache-2.0 | ~25 SKILL.md (hf-cli, datasets, trainers, Gradio, transformers.js, SageMaker, …) + HF MCP | `git -C vendors/huggingface-skills pull` | **Med** ML/agent; **Low** synth/blender |
| 5 | **obra/superpowers** | https://github.com/obra/superpowers | MIT | ~15 engineering workflow skills (brainstorming, TDD, systematic-debugging, code-review, …) | Pull vendor clone | **High** general-agent (avoid cloning) |
| 6 | **mattpocock/skills** | https://github.com/mattpocock/skills | Check repo LICENSE | ~38 skills (grill-me, codebase-design, implement, wayfinder, …) | Pull `vendors/mattpocock-skills` | **High** general-agent |
| 7 | **vercel-labs/agent-skills** | https://github.com/vercel-labs/agent-skills | Check repo | React/Next/web-design/deploy skills | Pull vendor clone | **Med–High** web; **Low** our creative domains |
| 8 | **microsoft/azure-skills** | https://github.com/microsoft/azure-skills | MIT | Dozens of Azure/Foundry skills (also large Microsoft listings in VoltAgent ~133) | Pull vendor clone | **Med** infra; **Low** synth/blender |
| 9 | **PatrickJS/awesome-cursorrules** | https://github.com/PatrickJS/awesome-cursorrules | CC0 / see LICENSE | **250+** `.mdc` Cursor rules (incl. `blender-python-addon`) | Pull `vendors/awesome-cursorrules` | **High** Cursor/agent how-tos; **Med** blender (addon ≠ modeling how-to) |
| 10 | **coreyhaines31/marketingskills** | https://github.com/coreyhaines31/marketingskills | MIT | ~50 marketing/SEO/CRO/copy skills | Pull vendor clone | **High** side-hustle prior-art (do not clone narratives) |
| 11 | **remotion-dev/skills** | https://github.com/remotion-dev/skills | Check repo | ~12 Remotion video skills | Pull vendor clone | **Med** cinematic/video adjacent |
| 12 | **AliasgharArabi/agentic-awesome-skills** | https://github.com/AliasgharArabi/agentic-awesome-skills | Check repo | **1900+** installable SKILL.md playbooks + CLI | Index from README/CLI catalog; avoid full clone if huge | **High** breadth; index-from-listing |
| 13 | **alirezarezvani/claude-skills** | https://github.com/alirezarezvani/claude-skills | Check repo | **380+** multi-agent skills/plugins | README/API listing | **Med–High** general |
| 14 | **Composio MCP plugin / skills** | https://github.com/ComposioHQ/composio-mcp-plugin | Check repo | MCP meta-tools + skills for 1000+ app actions | Re-read README; skills.sh listing | **Med** MCP actions ≠ YouTube how-tos |
| 15 | **agentskills/agentskills** (spec) | https://github.com/agentskills/agentskills · https://agentskills.io/specification | Apache-2.0 | Spec + docs for `SKILL.md` format | Pull `vendors/agentskills-spec` | **High** format peer (not content) |
| 16 | **OpenAI skills** (via VoltAgent / skills.sh) | Listed under OpenAI in awesome-agent-skills | Upstream | doc/pdf/speech/sora/playwright/security/figma/… | Re-parse VoltAgent README | **High** general; avoid re-distilling |
| 17 | **Binance / Venice.ai / fal.ai skills** | Via VoltAgent + skills.sh | Upstream | Crypto market/spot/token-audit; audio/music gen; fal-3d/audio | Re-parse VoltAgent README | **High** crypto-tooling & synth-adjacent APIs — distill YouTube **UI deltas only** |
| 18 | **youtube-skills (ours)** | MCP `user-youtube-skills` · `/workspace/skill-library/mcp-publish/` | Internal | ~50 published AgentConsumableSkill v1 JSON | `list_skills` / rebuild mcp index | **Peer de-dupe** (not external skip list) |

## Intentionally not fully cloned

- **agentic-awesome-skills** (~2k playbooks): too large; catalog via README/CLI next refresh.
- **VoltAgent** list itself: indexed from README bullets into `index.json` (1000+ rows), no vendor clone of every upstream.
- Proprietary preset banks / closed courseware: never vendor.

## Re-fetch recipe (box)

```bash
curl -sL https://raw.githubusercontent.com/VoltAgent/awesome-agent-skills/main/README.md \
  -o /workspace/skill-library/prior-art/raw/voltagent-awesome-agent-skills-README.md
# optional: git -C vendors/<slug> pull
python /workspace/skill-library/pipeline/build_prior_art_index.py
```

## Coverage notes for our domains

| Domain | Prior-art density | Distill implication |
|--------|-------------------|---------------------|
| general-agent | Very high | Novelty gate strict; delta-only |
| side-hustle / marketing | High (Corey Haines et al.) | Tool procedures only |
| crypto-tooling | High (Binance, Coinbase listings) | UI/ops only; finance-risk constraints |
| synth-cinematic | Low (Remotion/fal/Venice APIs ≠ DAW recipes) | **Moat** — keep specific |
| blender-3d modeling how-tos | Low–med (cursorrules addon, fal-3d) | **Moat** for transcript procedures |
| gaussian splat / drone | Near-empty | **Moat** |
