# Three-band parallel bandpass filter-bank pad with offset, unsynced cutoff LFOs

Goal: Build a pad from bandpass filters instead of low-pass: saw (+ octave-down second osc) into three parallel resonant bandpass filters set low / mid / high, each mixed to the output, each cutoff moved by a slow LFO deliberately offset in phase/value so the three bands never move in sync, then slow-attack pad envelope, ~7-voice unison, chorus and long reverb — a filter-bank pad distinct from parallel rhythmic filter chains and single-bandpass WT pads.

Source: [Sound Design 53: Pads 3 Bandpass](https://www.youtube.com/watch?v=L0IXE_whmso)

1. Route oscillator 1 into filter 1, filter 2 and filter 3 in parallel, each also sent to the output. Change oscillator 1 from sine to saw.
2. Set all three filters to bandpass with a little resonance: filter 1 low frequencies, filter 2 mids, filter 3 highs.
3. Give it a pad envelope: slow attack, sustain, long release.
4. On filter 1 cutoff add a slow LFO (global). Copy it to filters 2 and 3 but change the value/start slightly so they don't start the same or synchronize.
5. Enable oscillator 2 an octave lower, also into all three filters, with the same pad envelope; nudge its speed slightly so the oscillators don't move too evenly.
6. Add unison ~7 voices, raise volume/bass as needed; resonance amount and output mix are to taste.
7. Add chorus for thickness and a long-decay reverb; play chords or a single sustained note.

Batch: `2026-10-13-morning-hunt` · transcript: YouTube-provided (Show transcript) · YouTube English auto transcript of an AI-dubbed track (original audio es-US); route auto-target-from-dub-track.
