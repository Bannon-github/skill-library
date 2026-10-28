#!/bin/bash
cd /workspace/skill-library
while IFS= read -r q; do
  [ -z "$q" ] && continue
  echo "## $q"; timeout 400 .venv/bin/python pipeline/search_youtube_topics.py "$q" --per-query 15 --top 7 --min-dur 240 --max-dur 3600 --skip-known 2>&1 | tail -9
  sleep 18
done
