#!/usr/bin/env bash
# Re-fetch third-party prior-art (excluded from git: size + upstream licenses).
# Pinned commits are what the prior-art index was built from (2026-09-24).
set -euo pipefail
ROOT="${SKILL_LIBRARY_ROOT:-/workspace/skill-library}"
V="$ROOT/prior-art/vendors"; mkdir -p "$V" "$ROOT/prior-art/raw"
while read -r slug url sha; do
  [ -z "$slug" ] && continue
  if [ -d "$V/$slug/.git" ]; then git -C "$V/$slug" fetch -q origin; else git clone -q "$url" "$V/$slug"; fi
  git -C "$V/$slug" checkout -q "$sha" 2>/dev/null || echo "warn: $slug pin $sha missing, staying on default branch"
done <<'LIST'
agentskills-spec https://github.com/agentskills/agentskills.git 69ef37e9424c0a7ea9dd2293b559e43ec8176379
anthropics-skills https://github.com/anthropics/skills.git 34040c9c568585f6929bedeaad110ad08f079624
awesome-cursorrules https://github.com/PatrickJS/awesome-cursorrules.git b044f956f021b6e8877f16781bcfc466a6a120e9
coreyhaines-marketingskills https://github.com/coreyhaines31/marketingskills.git 5b2c0007766c6a1cf1d53fd8fc73e979e0821022
huggingface-skills https://github.com/huggingface/skills.git 80f9fa530e46f4ae642fcb9e1725bad0e1979395
mattpocock-skills https://github.com/mattpocock/skills.git c55ee46073ed923f86ce59a5eb3b6d895095d1b7
microsoft-azure-skills https://github.com/microsoft/azure-skills.git 9184881885141eccbf8f6477db9689f861608a68
obra-superpowers https://github.com/obra/superpowers.git 5bf4e78011075bcfc0dc295f0724994cd123ee71
remotion-skills https://github.com/remotion-dev/skills.git 41b22eec767aa77eb31df62ccb3bacf52ed771fb
vercel-agent-skills https://github.com/vercel-labs/agent-skills.git 063bee94c3f4df8453406c830b0a7df0f2860278
LIST
curl -sL https://raw.githubusercontent.com/VoltAgent/awesome-agent-skills/main/README.md -o "$ROOT/prior-art/raw/voltagent-awesome-agent-skills-README.md"
curl -sL https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/README.md -o "$ROOT/prior-art/raw/awesome-cursorrules-README.md"
echo "prior-art re-fetched. Rebuild index: $ROOT/.venv/bin/python $ROOT/pipeline/build_prior_art_index.py"
