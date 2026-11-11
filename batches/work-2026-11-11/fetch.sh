#!/bin/bash
cd /workspace/skill-library
for v in "$@"; do
  echo "## $v $(date -Iseconds)"
  .venv/bin/python pipeline/fetch_youtube_transcript.py -- "$v" 2>&1 | tee -a batches/work-2026-11-11/fetch.log | tail -6
  if [ -f raw/$v/raw.txt ]; then wc -w raw/$v/raw.txt; else echo "NO_TRANSCRIPT $v"; fi
  sleep 45
done
echo "FETCH_DONE $(date -Iseconds)"
