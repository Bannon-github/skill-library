cd /workspace/skill-library
W=batches/work-2026-10-19
i=4
for b in "MjijB6ExetI JC-UA2C-sZU Zgwxh3VrQZQ" "m6wfGX7rwiQ rVRMgLa9Y9E P_bIEn8FGzI" "e1AMHtuuuTQ nbS1pT8V7YU b2zwGqefZw8" "pO5BOqCS9mo 17OGg5CrJ-g 7OatKTrtmJ8"; do
  timeout 600 .venv/bin/python pipeline/route.py -- $b > $W/route$i.log 2>&1
  grep OUTCOME $W/route$i.log
  i=$((i+1)); sleep 45
done
