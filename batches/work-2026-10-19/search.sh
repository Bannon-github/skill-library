cd /workspace/skill-library
for q in "phaser pad synth sound design" "vocoder pad synth tutorial" "phase distortion oscillator sound design" "wavetable pad sound design tutorial 2026" "cinematic texture sound design synth tutorial" "stereo width pad synth sound design tutorial" "hybrid synthesis cinematic pad tutorial"; do
  echo "### $q"; timeout 400 .venv/bin/python pipeline/search_youtube_topics.py "$q" --per-query 15 --top 6 --min-dur 180 --max-dur 3600 --within year --precheck --require-transcript --skip-known 2>&1 | tail -12
  sleep 40
done
