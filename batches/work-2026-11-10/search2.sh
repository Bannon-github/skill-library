#!/bin/bash
cd /workspace/skill-library
while IFS= read -r q; do
  [ -z "$q" ] && continue
  echo "## $q $(date -Iseconds)"
  timeout 400 .venv/bin/python pipeline/search_youtube_topics.py "$q" --per-query 12 --top 6 --min-dur 240 --max-dur 3600 --skip-known 2>&1 | tee -a batches/work-2026-11-10/search2.log | tail -12
  sleep 15
done < batches/work-2026-11-10/queries2.txt
echo "SEARCH_DONE $(date -Iseconds)"
