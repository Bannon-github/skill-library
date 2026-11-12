# Morning synth YouTube hunt: 2026-11-12

Mode: compact library (fold-in). No standalone skills were published. All 4 new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, 0.91–0.93). I hand-checked each against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json went 265 → 269 entries (merge_log batch `2026-11-12-morning-hunt`). `mcp-publish/index.json` was refreshed (33 skills) and the new ids resolve through `mcp-publish/aliases.json`. All transcripts are YouTube-provided captions (pipeline fetcher). No Whisper/ASR was used.

No rate limiting today: all 10 fetches succeeded on the first try, including carry-over NAEyg_eXP14 (auto-generated captions). `route.py` returned CANDIDATES_READY for all 9 routed ids, including clear rejects (false-novel pattern continues), so every result was hand-checked.

## Folded in (4)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| TSiH9MUh4Ec | phaser-drums-ping-allpass-bank-short-impulse-feedback-ring-poles-sequenced-sweep-and-resonance | pad-phaser-notch-comb-movement | Phaser as a drum synth: ping the all-pass bank with a very short impulse, raise feedback until it rings like a tom, add poles for liquid timbres, and sequence sweep (pitch) and resonance (accent) per step. |
| sNdpvcQqrP8 | ambient-dub-techno-kit-sub-50hz-crushed-kick-pitched-down-rim-clap-phaser-ghosts-hard-pan-dusty-hat-crushed-break-hp-2k | drum-groove-programming-swing-and-ghosts | Ambient dub-techno kit: a kick peaking just below 50 Hz, bit-crushed and mid-cut; a −2 st rim-like clap on the last beat of every second bar into a huge parallel verb; phasered hard-panned ghosts/shakers; a dusty noise hat; a crushed break HP'd above 2–3 kHz; a 50%-wet bus saturator; plus the m9 drone, square bass and filtered crushed chords. |
| q6TxzspNL9Q | reverb-rumble-kick-parallel-aux-ny-comp-release-between-16th-8th-drive-short-verb-ducked-by-kick-synced-lowpass | drum-synthesis-and-hybrid-percussion | Rumble kick from any kick: parallel returns for NY compression (release between 1/16 and 1/8 = 15000–30000/BPM ms), a 100%-wet light drive and a 100%-wet short high-cut reverb ducked by the kick and low-passed with a synced LFO. Kept soft, it works as an ambient sub bed. |
| NZJ9bvuyII4 | looper-drone-clips-sine-utility-fade-overdub-clusters-faders-capped-0db-group-8s-verb-pingpong-resample-commit | generative-ambient-drones-and-soundscapes | Hand-built drone loops: a sine → gain → long low-cut verb → one-bar looper, overdubbing notes and clusters with gain fades into four clips, faded live on mapped faders capped at 0 dB through a group with an 8 s verb, ping-pong delay, tape and glue, then committed by resampling. |

Matt's preferences are written into each skill's constraints: steady pitch (dropped the dub video's flutter/wow and randomised velocity deviation, plus the looper video's re-pitch tempo knob), fixed sequenced phaser pitches (no random sweep), no rapid clicking or rolls, drums early (~8 counts / ~12 s), Ableton/MIDI-friendly, and portable module mapping.

## Rejected (6)
- **NAEyg_eXP14**: 3 types of ambient from one concept (carry-over). Beginner preset-browsing overview (six layer types, synth presets) with sample-pack and masterclass promo. Layering is already in arrangement-ambient.
- **1VlYGttVbxE**: Ableton swells. Overlapping notes with ~1.8 s glide. Built on pitch glide (against the steady-pitch preference) and thin.
- **8ZerPdrCs-4**: hybrid orchestral deep dive S01E05. Rambling session built on commercial library patch names. No portable procedure.
- **hlJ9t7MbJjY**: electronic hybrid film score. Near-duplicate of the hybrid-orchestra four-synth-roles variant (electronics first, orchestra creeps in). No sample manipulation.
- **y5cMngcIUMc**: techno kick & bass fundamentals (kick at ~48 Hz, click layer, EQ sandwich, low-band sidechain, dynamic EQ). Covered by the bass cluster (kick-bass four-level lock, interval-aware low end) and the sidechain cluster.
- **JDVu6GvoMuw**: Two Lanes-style downtempo. A track remake built on guitar recordings and presets, with no ambient breakdown procedure.

Not fetched: none.

Seen but skipped (beginner, product, off-genre or duplicate titles): 2d3Fu9vuPPI (jungle break editing), ebSTdCWZoVU (video editing), DIz67iurpXQ / veMIOXVSJZU / dMzMmnRT_HE / tzfzkTAQsnE (transition listicles), y0mfaQpWYQw / _bLQ262qA7I (pitch risers, against steady pitch), JVxj5nB3mlw, JOm_EqBoW0M, IghRZY1VWqk / mPJEfc6xqLA / pIiAicy5pjc / rttwq2onLxQ (static binaural/solfeggio, already covered), sRMRtJ8Ces8, paRevQ5JffU, Ea0b9jgbFhI, Eyqgu4N9rho, 0u_deCFwE7o, 3oO0xLxEbfU / wcDIW_oDBc8 (techno kicks, close to existing kick variants), _BRr5OeOurk, IdYvw1CvV40, t3hJ0BtK37o / nRKE4rllwBY / lHsO6m9d7qQ (EDM kick synthesis, covered), APljvOxetas / 0FmzFpHdwrc / gFPoITY_ioA (lo-fi overviews), CqFnOsymyNk, 1Vv7vUT5BQ0, ccwxv5OzwRU, 5dQMClgMLyw, tDNr50UUaIk, QMndfcntCHw / 1V69vIt4yX4 / i3GLybBxeEg / Y9s26ldOImQ / m46MIMeUiPY / QZdGb-7GBsk (synth manuals/presets), 7NrRhHKp0n8, ezuUuP_DJAI, Bzvn_6toM6M, uAQA7mPAI2g (orchestral composing, not sample manipulation), 8CEZiu8efrs / ZdKxOsK4nQ8 / uhC-5pwVHLw / bZjzOSqWn1s / CgdRPHKa5Gw (phaser plugin manuals), ARNEww5nBl4, ioOj_92LTxw, nOWcSJVJIss, s_UFhvl3Zpo / m8zYnm8dRuE / aLOYhVQbhp8 / cDwgGD4PsCM / mvuV9M0NM1k / IHgFpWYyaqQ (wavetable manuals), zEkCere2A_Y / zjrjf6gr1dg / VaqMag-CG04 / byZFpzg5LFI / xy_NbX2SNSc / W7EK9Y7io88 (bass/hats, covered or off-genre), U62kTICYqjQ / vSAnEJpSBjU (trance), hU1gCqYmMjw, Ha5E5VfOKtk, XdGN8BJe6WI, hR31DQrxfT4 / gbkT7y0ZgTc (Nord layering), mxNff8JD7wY, 6VFNnAAI3O0, 7qQX6YGBQEA, vYYp7KRqih8.

## Searches (2026-11-12)
`search_youtube_topics.py --skip-known` (240–3600 s): ambient build/breakdown transitions; cinematic swell/riser transitions; binaural frequency ramp automation; felt kick ambient techno; lo-fi soft kick synthesis; ambient kick + sub; exciter/noise air on pads; orchestral-sample manipulation hybrid; phaser pad; ambient loop making; wavetable pad modulation; punchy bass. Second pass: isochronic frequency sweep automation; ambient breakdown without drums; white-noise layer pad brightness. Logs are in `batches/work-2026-11-12/`.

## Gaps still open
- **Brainwave rate-ramp automation (e.g. 8 → 4 Hz over a section):** still open. Searches return only static binaural/solfeggio videos. This is probably best authored in-house from existing monaural/tremolo variants (automate the tremolo Hz or the second sine's offset) rather than found on YouTube.
- **Ambient/cinematic build/breakdown transitions:** still open. Results are EDM/trance listicles or pitch-glide risers.
- **Soft ambient kick + sub:** improved. Today added a sub-50 Hz crushed, mid-cut dub kick and a ducked, low-passed reverb rumble bed. A dedicated felt/soft synthesized ambient kick walkthrough is still wanted.
- **Synth-native noise/exciter air on pads:** still open. Hits were synth manuals and Nord layering.
- **Orchestral-sample manipulation hybrid:** still open. Hits were orchestral composing walkthroughs, not sample mangling.
- **Phaser:** improved with phaser drums (pinging). Pure phaser-pad hits were still plugin manuals.
- **Loops:** improved with looper drone clips.

## Carry-overs
- None to refetch. NAEyg_eXP14 was fetched and rejected.
