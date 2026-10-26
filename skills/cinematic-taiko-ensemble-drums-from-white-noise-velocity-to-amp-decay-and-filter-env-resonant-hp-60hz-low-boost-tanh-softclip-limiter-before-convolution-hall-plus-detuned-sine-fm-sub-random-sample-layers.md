# Cinematic taiko-style ensemble drums from white noise: velocity sets the amp and filter decay, a resonant 60 Hz high-pass plus low boost adds weight, a tanh soft clip and limiter go before a large-hall convolution reverb, with optional detuned sine, FM sub and round-robin sample layers

Goal: Make big cinematic ensemble drums (taiko-like) with no recordings, using any synth with a noise oscillator, a filter, two envelopes and velocity sensitivity. Think in four categories: frequency, amplitude, time and timbre. Start with white noise; amp envelope with no sustain and a short decay, with velocity routed to decay (soft hits short, hard hits long and ringing) and a wide velocity-to-level range. Add a low-pass filter (about 1 kHz) with its own short envelope on cutoff, also scaled by velocity, so each hit starts bright and closes darker; add a little filter drive. EQ: resonant high-pass at about 60 Hz plus a low bell boost for weight, a mud cut, presence, a slight high shelf; add a little release so hits breathe. Soft clip (tanh waveshaper) driven a little by that low boost to mimic an overloaded ensemble, trim the output and the extreme sub. Put a limiter or maximizer, then a convolution reverb with a cathedral or large-hall impulse (shortened, low end tamed, highs damped, about 5 kHz lifted). Layers: several detuned sines with a pitch envelope for tone, an FM sub at 20-50 Hz, and a round-robin layer of rattly found-object hits with slight random pitch to avoid machine-gunning.

Source: [EPIC Cinematic Drums from White Noise | A Sound Design Tutorial](https://www.youtube.com/watch?v=6CWmImkHDgs)

1. Load white noise in a fresh patch; set the amp envelope to sustain 0 and a short decay; widen the velocity-to-level range.
2. Route velocity to amp decay so soft hits are short and hard hits ring out long.
3. Add a low-pass (about 1 kHz) and a second envelope on cutoff with a short decay, opening bright at the attack and closing darker; scale its amount or decay by velocity and add a little filter drive.
4. EQ for weight: resonant high-pass at about 60 Hz plus a low bell boost; cut mud, add some presence and a slight high shelf; add a little amp release.
5. Soft clip with a tanh waveshaper (small drive), trim the output, filter a little extreme sub.
6. Add a limiter, THEN a convolution reverb with a cathedral or large-hall impulse; shorten the decay, tame the low end, damp the highs and lift about 5 kHz.
7. Optional layers: 3 detuned sines with a pitch-drop envelope (tone), an FM or sine sub at 20-50 Hz, and a round-robin layer of found-object or rattle hits with slight random pitch.

Batch: `2026-10-26-morning-hunt` · transcript: YouTube-provided (Show transcript) · Auto-generated YouTube Show transcript; partly garbled, values approximate from transcript description.
