#!/usr/bin/env bash
# Idempotent: recreate the skill-library venvs and the /tmp/ytvenv symlink the
# youtube-skills MCP spawns (/tmp/ytvenv/bin/python mcp-server/server.py).
# Safe to run any time (boot, before routines, after /tmp is wiped).
set -euo pipefail
ROOT="${SKILL_LIBRARY_ROOT:-/workspace/skill-library}"
PY="${PYTHON:-python3}"

mkvenv() { # <venv dir> <requirements file> <import check>
  local dir="$1" req="$2" check="$3"
  if [ -x "$dir/bin/python" ] && "$dir/bin/python" -c "$check" >/dev/null 2>&1; then
    echo "ok: $dir"; return 0
  fi
  echo "building: $dir"
  rm -rf "$dir"
  "$PY" -m venv "$dir"
  "$dir/bin/python" -m pip install -q --upgrade pip
  "$dir/bin/python" -m pip install -q -r "$req"
}

# 1) MCP server venv
mkvenv "$ROOT/mcp-server/.venv" "$ROOT/mcp-server/requirements.txt" "import mcp.server.mcpserver"
# 2) Pipeline venv (fetch_youtube_transcript.py uses $ROOT/.venv/bin/yt-dlp and python3)
mkvenv "$ROOT/.venv" "$ROOT/pipeline/requirements.txt" "import youtube_transcript_api, yt_dlp"
# 3) sample-lab venv (only if sample-lab exists)
if [ -d "$ROOT/sample-lab" ]; then
  mkvenv "$ROOT/sample-lab/.venv" "$ROOT/scripts/requirements-sample-lab.txt" "import numpy, scipy, soundfile, pyloudnorm"
fi

# 4) /tmp/ytvenv -> mcp-server/.venv (MCP config spawns /tmp/ytvenv/bin/python)
TARGET="$ROOT/mcp-server/.venv"
if [ "$(readlink /tmp/ytvenv 2>/dev/null || true)" != "$TARGET" ]; then
  rm -rf /tmp/ytvenv
  ln -s "$TARGET" /tmp/ytvenv
  echo "linked: /tmp/ytvenv -> $TARGET"
else
  echo "ok: /tmp/ytvenv -> $TARGET"
fi
/tmp/ytvenv/bin/python -c "import mcp.server.mcpserver" && echo "youtube-skills MCP python ready"
