# Three-layer ambient starter in about 30 minutes: a slow-envelope wavetable pad with a 4-bar bipolar position LFO and random cutoff drift, a saw-plus-sine bass pad through a 24 dB low-pass, and a sustain-less detail voice whose filter is stepped by a sample-and-hold style modulator into heavy delay and reverb, all composed by frequency region

Goal: Build the core of an ambient track (70-80 BPM, one minor key, 32-bar canvas) from three complementary layers. Pad: wavetable osc with attack about 3-5 s (4 s), decay about 4 s, sustain a few dB down, long release; 5 unison voices with moderate detune; wavetable position on a bipolar LFO synced to 4 bars; low-pass cutoff set to the 'sweet spot' where partials just peek through, with a random (chaos) modulator on cutoff at a low depth; a sub osc one octave down kept quiet; a second wavetable osc routed around the filter at low level and auto-panned by a 2-bar LFO for width. Send (not insert) to a dotted-eighth dual delay and a very long room/hall reverb (about 55 s decay, 100% wet on the return). Write only a few sustained notes over 32 bars, then pull the cutoff down and let the reverb do the opening. Bass pad: faster envelope, saw through a 24 dB/oct low-pass plus a sine, a touch of reverb, one long root note. Detail voice: attack-decay envelope with zero sustain (a key that rises and falls regardless of hold), 24 dB low-pass whose cutoff is moved by a stepped random (sample-and-hold) modulator at a slow rate, cranked delay and reverb. Check the layers on a spectrum analyser and place each in a different frequency region.

Source: [30 min Ambient Track for Beginners - Get Inspired & Find Your Sound](https://www.youtube.com/watch?v=CRWBHFIikqc)

1. Set tempo to about 75 BPM and pick one minor key; set a 32-bar loop.
2. Pad amp envelope: attack about 4 s (3-5 s range), decay about 4 s, sustain a couple of dB down, long release. Gain-stage the synth output down.
3. Load a soft wavetable in osc A, set 5 unison voices and adjust detune between wild (wide) and tight. Modulate wavetable position with an LFO synced to 4 bars in bipolar mode.
4. Turn on a low-pass filter and find the sweet spot where partials just peek out; put a random/chaos modulator on cutoff and lower its depth in the mod matrix.
5. Send the pad to a dotted-eighth dual delay and a very long reverb (about 55 s decay, 100% wet on its return track).
6. Add a sub osc one octave down at low level. Add osc B with a second wavetable bypassing the filter at low level, and auto-pan it with a 2-bar LFO (optionally its own bipolar WT-position LFO).
7. In a 32-bar MIDI clip, place a minimal chord shape and only a few slow sustained notes; then lower the pad cutoff slightly and let the reverb open it.
8. Bass pad: new instance, saw through a 24 dB/oct low-pass, faster envelope with some decay, add a sine (or sine sub) layer and a touch of reverb; write one long root note.
9. Detail voice: attack-decay envelope with sustain at zero, 24 dB low-pass with cutoff stepped by a slow sample-and-hold/step modulator; send heavily to delay and reverb; write a few sparse notes.
10. Check the master spectrum: confirm pad, bass pad and detail voice occupy different frequency regions; adjust levels or filters where they collide.

Batch: `2026-10-27-morning-hunt` · transcript: YouTube-provided (Show transcript) · Auto-generated YouTube Show transcript; values are as spoken and approximate where the speaker says 'about' or 'around'.
