# Vocoder as an insert effect on any synth patch: the patch itself is the carrier and a microphone is the modulator, with mode (clean, vintage, narrow, gated), decay, formant (neutral or higher) and dry-mic controls, placement in the effects chain (before or after distortion and chorus), arpeggiated carriers and a slow square LFO on formant

Goal: Turn any existing pad, bass or lead patch into a vocoder voice by putting the vocoder in an effect slot instead of building a special vocoder patch. The synth patch is the carrier (all its oscillators, voice mode, unison, envelopes and pitch bend still apply) and an external microphone is the modulator, so the patch goes silent until you speak or sing. Choose the vocoder mode (clean, vintage, narrow, gated; the presenter prefers clean), set decay (how long bands hold after the voice stops), set formant (neutral or higher; low settings sounded worse) and mix in some dry mic if wanted. Then experiment with where the vocoder sits in the chain (first, before distortion, with chorus after distortion, or replacing an EQ slot), add long reverb after it, run the arpeggiator so the vocoder speaks in rhythm, and modulate formant with a slow, deep square LFO. Rich carriers work best: e.g. a pluck oscillator plus a 2-operator FM oscillator, or a mono virtual-analog patch an octave down with filter envelope movement, chorus and distortion. Our first dedicated vocoder skill; the existing ones only borrow a 'vocode' spectral-warp mode.

Source: [The Minifreak Vocoder is Awesome!](https://www.youtube.com/watch?v=MjijB6ExetI)

1. Start from an init patch or any existing preset. Put the vocoder (external input) in a free effect slot, replacing a less important effect such as EQ or delay if needed. Connect a microphone to the audio input.
2. Pick the vocoder mode (clean, vintage, narrow, gated). Set decay for how long the bands hang on, formant at neutral or a bit higher, and the dry-mic amount to taste.
3. Make the carrier rich: e.g. oscillator 1 a plucked-string type, oscillator 2 a 2-operator FM type; or a mono virtual-analog patch an octave down with filter-envelope movement. Use unison or mono as needed and play lead lines with pitch bend.
4. Try different slot positions: vocoder first, then distortion, then chorus after the distortion; or vocoder after a chorus and distortion carrier. Add a long reverb after.
5. Turn on the arpeggiator with a held chord so the vocoded voice is re-triggered rhythmically.
6. Modulate formant with an LFO: square shape, slow rate, deep (even maximum) depth. Reduce unison spread if the result gets too smeared.

Batch: `2026-10-20-morning-hunt` · transcript: YouTube-provided (Show transcript) · Hardware walkthrough; mounting tip, patron and preset-pack talk dropped.
