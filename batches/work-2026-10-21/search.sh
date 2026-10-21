cd /workspace/skill-library
for q in "sample and hold random modulation synth tutorial" "vocoder chords synth pad tutorial" "spectral morphing synth sound design tutorial" "paulstretch extreme time stretch ambient tutorial" "euclidean rhythm generative ambient synth tutorial" "phaser pad synth sound design tutorial" "shepard tone riser sound design tutorial"; do
  echo "### $q"; timeout 400 .venv/bin/python pipeline/search_youtube_topics.py "$q" --per-query 15 --top 6 --min-dur 180 --max-dur 3600 --within year --precheck --require-transcript --skip-known 2>&1 | tail -10
  if tail -3 batches/work-2026-10-21/search.log | grep -q rate_limited; then echo RATE_LIMIT_STOP; break; fi
  sleep 40
done
