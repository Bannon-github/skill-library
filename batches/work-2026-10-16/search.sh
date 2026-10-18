cd /workspace/skill-library
for q in "spectral freeze pad sound design tutorial" "folded bass patch wavefolder synth tutorial" "phase distortion synth pad tutorial" "barber pole phaser pad synth tutorial" "physical modelling string pad synth tutorial" "cinematic riser sound design synth tutorial"; do
  echo "### $q"; timeout 400 .venv/bin/python pipeline/search_youtube_topics.py "$q" --per-query 15 --top 6 --min-dur 180 --max-dur 3600 --within year --precheck --require-transcript --skip-known 2>&1 | tail -12
  sleep 20
done
