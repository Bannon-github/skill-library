# Morning synth YouTube hunt: 2026-11-10

Mode: compact library (fold-in). No standalone skills were published. All 6 new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, 0.90–0.94). I checked each against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json went 254 → 260 entries (merge_log batch `2026-11-10-morning-hunt`). `mcp-publish/index.json` was refreshed (33 skills) and new ids resolve through `mcp-publish/aliases.json`. All transcripts are YouTube-provided (pipeline fetcher: youtube-transcript-api / yt-dlp captions). No Whisper/ASR was used.

YouTube rate-limited the fetcher (`rate_limited_or_ip_blocked`) on about every other video. I retried once with a 45 s sleep and no cookies. 4 videos were still not fetched (listed below) and nothing was invented for them.

## Folded in (6)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| 27ewHn5SAiI | kick-bass-interval-aware-low-end-saturate-octave-harmonic-exciter-transient | bass-design-sub-reese-808-and-layering | Interval-aware low end: keep bass notes off semitone neighbours of the kick fundamental (move up an octave), EQ out kick overtones that crowd the bass, saturate the kick so harmonics fall on octaves, then exciter + mild transient expander (~50 ms). |
| u4tg0u-THS8 | hybrid-orchestra-four-synth-roles-sub-pulse-pad-chord-tone-pluck-ostinati | arrangement-ambient-cinematic-score | Hybrid orchestral cue: sine sub an octave under the bass, straight 1/4–1/8 pulse bass, quick-attack poly pads, then 2–3 staccato chord-tone-only pluck ostinati (1–2 beat loops, rising complexity). |
| N60Jcn9zfBo | dark-short-kick-behind-busy-bass-transient-body-tail-73hz-start-eighth-note-length | drum-synthesis-and-hybrid-percussion | Disclosure-style kick: transient/body/tail thinking, dark non-clicky transient, body pitch from ~73 Hz down to the key's sub, ~1/8-note length, minimal layering, mixed a few dB under the bass, reference-curve check. |
| RPzAJFC_JkI | three-band-wavetable-rack-counter-lfo-position-glue-reverb-saturate-reverb-macro-drive | wavetable-and-vector-morph-pads | Evolving cinematic pad: 3 wavetable instances split lows/mids/highs, each with two very slow LFOs moving the two osc positions in opposite directions, glue comp → reverb → soft-clip → long reverb, one macro for filter + drive. Random cutoff swapped for a slow LFO. |
| 3zIsQfKtUno | organic-downtempo-groove-kick-tom-from-kick-layered-offset-claps-shaker-family-room-sends | drum-groove-programming-swing-and-ghosts | Löffler-style 115–120 BPM organic groove: kick + tom made from the kick (shorter, softer attack, band-passed), rim in a small room, clap crowd with offset pre-claps, transposed shaker family, frequency-split hats, noise ambience, warm sidechained piano/pad bed. |
| 6x1_XZDcI8I | hypnotic-drone-arrangement-phrase-layer-fade-ins-sequence-instrument-swap-drone-only-break | arrangement-loop-to-song-build-drop | Drone-led minimal arrangement: recorded cutoff automation and added dissonant drone notes, phrase-by-phrase layers with fade-in curves, climax = cutoff rise + high noise, drone-only break for 2–3 phrases, the same sequence swapped onto other instruments to keep energy up. |

Matt's preferences are written into each skill's constraints: no random pitch, no rapid clicking (claps are offset flams, not rolls), drums early.

## Rejected (7)
- **XqmRJNH3b4w**: Audacity binaural/isochronic. Beginner-level and rambling, with no in-track production.
- **P-BV9Fa0e3Q**: binaural beats in any DAW (two panned tone generators / paid plugin). Sound-healing framing and promo; the method is already in the brainwave cluster.
- **e-y_F4sv6fA**: Zimmer-style "Cinematic Synthesis". Course presale promo with no reproducible recipe.
- **vv4LdpuvH5U**: Ableton Wavetable dreamy pad. Near-duplicate of existing wavetable variants, plus variation on every note.
- **aceTs5aSDZU**: Kiasmos orchestral downtempo decode. Locked to Kontakt libraries and a sample pack, with randomised percussion. Its kick→tom idea is covered by the 3zIs fold.
- **TTIon9_pRHQ**: organic house warm/wide bass. Near-duplicate of the bass cluster's wide-bass and M/S variants.
- **WFGs91vSpIw**: Serum drum basics. Overlaps the whole-kit variant; random delay automation; promo.

Not fetched (YouTube 429/IP block after retry, no transcript saved): _MgJJpqxcn8 (filtered drums for ambient mixes), NAEyg_eXP14 (3 types of ambient from 1 concept), X_yfys8wAJ4 (first ambient track full build, Logic), P--40MYlGuI (hybrid score from manipulated orchestral samples). These are good candidates for the next hunt.

Seen but skipped (beginner, product or off-scope): vieGTqd3uhQ, vr0DHvuQX8E, lfL9TMFhXUE, JhZU6JGvoHw, dwHjLxpNBlw, pLR874EgF9Y (KICK 3 promo), Wcxw3BPSt3A / 8LV1bqf8ZVo / 4cGCL4KVXhA (film/video sound design, not music), kgdE6pEfP0s, 3QfkNIw_qLQ, NkuBRIA96j4, Pb8TAyJT5ws, exciter plugin breakdowns (p20qRHbuxQI, Ib09MRj-Xzw, -HDM5IZARyg), rZnxiE7u7ns, RzjsPIr49PU, rgSL418cv2I (808 trap).

## Router / lexicon fix
- **Root cause of yesterday's -yzW0DZuo40 OFF_LEXICON:** this was not the lexicon. `route.py` passed the video id positionally to `extract_terms_graph.py` and `graph_gap_merge.py`, so any id starting with `-` was parsed as an option. The graph step failed and the scores came back None, which reads as OFF_LEXICON. Fixed: both calls now pass `-- <vid>` after the options. Re-routing -yzW0DZuo40 (with --no-kg-update) now returns CANDIDATES_READY.
- **Also added to `pipeline/lexicons/synth.json`:** noise terms (brown noise, noise osc, tape hiss, hiss, noise layer/sample/generator), filter terms (low/high shelf, split/parallel/serial filter routing, dual filter, SVF, band reject), `filter cutoff`, and envelope-follower terms (erosion, tuned noise, gated noise, noise burst).

## Searches (2026-11-10)
`search_youtube_topics.py --skip-known` (240–3600 s): soft kick for ambient; soft round kick + sub; binaural/isochronic in a DAW; ambient track structure intro/build/breakdown/outro; cinematic transitions and builds; hybrid synthesis samples + synths cinematic; ambient drum loops from synth sounds; wavetable cinematic pad; analog evolving pad; exciter on pads; isochronic tremolo gate on a pad; deep warm downtempo kick; ambient-techno arrangement automation; punchy bass from scratch; stereo width M/S mono compatibility. Logs are in `batches/work-2026-11-10/`.

## Gaps still open
- **Soft ambient kick + sub:** partly addressed. The dark, short, non-clicky kick placed under the bass (Disclosure) and the kick→tom reuse help, but there's still no long, rounded, felt-not-heard ambient kick recipe.
- **DAW isochronic/brainwave production:** still open. Hits are all healing/solfeggio or Audacity tutorials. Next time, try a tremolo/gate-on-pad walkthrough by id.
- **Ambient/cinematic arrangement:** improved with the hybrid four-role layering and the drone-led phrase arrangement. Ambient-specific full builds (NAEyg_eXP14, X_yfys8wAJ4) are queued because of rate limits.
- **Hybrid synthesis (synth + sample manipulation):** partly addressed by the orchestra + synth role recipe. P--40MYlGuI is queued.
- **Loops/drums:** improved with the organic downtempo groove. _MgJJpqxcn8 (filtered ambient drums) is queued.
- **Synth-native exciter on pads:** still thin. Searches return only plugin breakdowns.

## Carry-overs
- Refetch when not rate-limited: _MgJJpqxcn8, NAEyg_eXP14, X_yfys8wAJ4, P--40MYlGuI.
