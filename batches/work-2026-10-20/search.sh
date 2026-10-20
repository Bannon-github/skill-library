cd /workspace/skill-library
for q in "paulstretch extreme time stretch ambient tutorial" "euclidean rhythm generative ambient synth tutorial" "sample and hold random modulation synth tutorial" "vocoder chords synth pad tutorial" "spectral morphing synth sound design tutorial"; do
  echo "### $q"; timeout 400 .venv/bin/python pipeline/search_youtube_topics.py "$q" --per-query 15 --top 6 --min-dur 180 --max-dur 3600 --within year --precheck --require-transcript --skip-known 2>&1 | tail -10
  sleep 40
done
