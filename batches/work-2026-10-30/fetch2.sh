#!/bin/bash
cd /workspace/skill-library
for v in "$@"; do
  echo "## $v"
  .venv/bin/python pipeline/fetch_youtube_transcript.py -- "$v" 2>&1 | tail -4
  [ -f raw/$v/raw.txt ] && wc -w raw/$v/raw.txt || echo "NO_TRANSCRIPT $v"
  sleep 20
done
