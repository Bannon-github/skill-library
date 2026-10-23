# Song structure: findings and how the song engine uses them

Researched 2026-10-23 (America/Vancouver) for the Polyrhythm Studio / sample-lab project. Facts from the web carry a source name and URL. Anything marked **[synthesis]** is my own reasoning, not a sourced claim. Several pages were read only through search summaries rather than opened in full; those are marked **(summary only)**.

## 1. Forms

| Form | Typical shape | Source |
|---|---|---|
| AABA / 32-bar | four 8-bar sections; B is the "middle eight" or bridge; sections can be dropped on repeats | Open Music Theory, Univ. of Puget Sound: https://musictheory.pugetsound.edu/mt21c/AABAForm.html ; Wikipedia "Thirty-two bar form": https://en.wikipedia.org/wiki/AABA_form |
| Verse-chorus | verse and chorus usually 16 or 32 bars; the bridge happens once and often differs in key, chords or density; ABABCB is common | Ableton Making Music, "Common Forms 1": https://makingmusic.ableton.com/common-forms-1-elements-of-song-form ; Native Instruments "Song structure 101": https://blog.native-instruments.com/song-structure-101/ |
| Verse-chorus history | dominated pop from the 1960s; sections may be shortened or lengthened by a measure or two | OERTX "A Survey of Form in Music": https://oertx.highered.texas.gov/courseware/lesson/3975/student/?section=9 |
| EDM (intro-build-drop-breakdown) | intro 16-32 bars, build 8-16, drop 16-32, breakdown 16-32, outro 16-32; at 128 BPM 16 bars is about 30 s | Mixelite: https://mixelite.com/blog/edm-song-structure/ ; EDM Ghost Production: https://edm-ghost-production.com/dj-knowledge-base/electronic-song-structure ; InspiredByBeatz (8-bar phrases, build by taking things away): https://www.inspiredbybeatz.com/en/edm-arrangement-from-loop-to-exciting-track/ |
| Rondo (ABACA...) | a refrain returns between contrasting episodes | Open Music Theory: https://openmusictheory.github.io/rondo.html |
| Ternary (ABA) | statement, contrast, return | Open Music Theory: https://viva.pressbooks.pub/openmusictheory/chapter/ternary-form/ |
| Binary (AB) | two parts, often both repeated | Open Music Theory 2e on LibreTexts: https://human.libretexts.org/Bookshelves/Music/Music_Theory/Open_Music_Theory_2e_(Gotham_et_al.)/03%3A_Form/3.06%3A_Binary_Form |
| Through-composed | no returning sections (definition seen in the OMT glossary search summary only, **(summary only)**): https://viva.pressbooks.pub/openmusictheorycopy/back-matter/glossary/ |
| Layering as form | form comes from layers entering and leaving rather than from new material (Ableton Making Music book, chapter "Common Forms 2: Layering as Form"; the web chapter returned 404 when fetched, so this is **(summary only)**; book PDF: https://cdn-resources.ableton.com/resources/uploads/makingmusic/MakingMusic_DennisDeSantis.pdf) |
| Ambient loop arcs | Eno's *Music for Airports* uses tape loops of unequal lengths so the combination rarely repeats: https://blog.oup.com/2018/12/brian-eno-music-for-airports/ ; https://reverbmachine.com/blog/deconstructing-brian-eno-music-for-airports/ |
| Cinematic cue | phrases of 2, 4, 8, 16 bars between sync points; do not cut a phrase in half: Berklee Online https://online.berklee.edu/takenote/5-film-scoring-concepts-to-know-for-your-first-movie-score/ . Leave space before the climax: Nymly Studio https://nymlystudio.com/blogs/journal/how-to-make-cinematic-music-for-film-trailers . Build from the bottom up, with restraint: Songer https://songer.co/blog/posts/how-to-create-cinematic-music-scoring-without-a-studio . Also https://www.masterthescore.com/article/how-to-write-cinematic-music |
| Game adaptive music | stems = vertical layering; states = switching sections on the bar. Austin Haynes: https://www.austinhaynesmusic.com/adaptive-game-music-stems-states-sections ; GDC 2021 "Pure vertical layering" (Game Developer): https://www.gamedeveloper.com/game-platforms/pure-vertical-layering-for-game-music-composers-from-spyder-to-sackboy-gdc-2021- ; TheOvermare: https://theovermare.com/ingame-adaptive-music/ ; tono::adaptive docs: https://docs.rs/tono/latest/tono/adaptive/struct.AdaptiveMusic.html ; gamedev-skills adaptive-music note (0.5-1.5 s fades, quantised switches, stingers): https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/main/skills/disciplines/audio-design/references/adaptive-music.md |
| Meditation / entrainment arcs | the evidence is mixed. A 2023 PLOS One systematic review counted 5 supportive, 8 not supportive and 1 mixed study: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0286023 . A 2022 Springer meta-analysis on memory/attention found g = 0.40 overall with conflicting studies: https://link.springer.com/article/10.1007/s00426-022-01706-7 . PMC4428073 "Auditory Beat Stimulation and its Effects on Cognition and Mood States". Evidence for isochronic tones specifically is limited. We make no health claims; the arc is a listening-session shape only. |

## 2. Transitions

| Technique | What the sources say | Source |
|---|---|---|
| Riser / build | build with risers, drum fills, filter sweeps; subtractive builds (take layers away) | Ableton Lessons "Composition & Arrangement in Ableton Live", ch. 6: https://abletonlessons.com/composition-and-arrangement-in-ableton-live/ ; InspiredByBeatz (above) |
| Pull the low end / kick before the drop, then a "breath" of near-silence | Red Star Media: https://redstar.media/guides/production/structuring-your-edm-tracks (also: an 8-bar intro is unusable for DJs; drop 2 must not disappoint) |
| Reverse swell | reverse reverb | Unison: https://unison.audio/time-based-effects/ |
| Breaking the loop | change something every 4-8 bars so the loop does not stall | Cookingtechno "escape the loop": https://cookingtechno.com/escape-the-loop/ |
| Game transitions | switch on the next bar or beat, 0.5-1.5 s fades, stingers | gamedev-skills (above) |

## 3. Harmonic rhythm and key change
- Harmonic rhythm is how fast chords change; slower in ambient, one chord per 1-2 bars in most pop/EDM loops: neirocca https://neirocca.com/en/learn/function/harmonic-rhythm ; Open Music Theory "Harmonic Syntax" (LibreTexts, 1e).
- A key change (modulation) is most often used to lift the last chorus; up a whole step or half step is the common move: Orphiq https://orphiq.com/resources/what-is-a-key-change ; Horton School musicianship resources https://kshaffer.github.io/musicianshipResources/Modulation.html . **(partly summary only)**

## 4. What the library's own skills say (mcp-publish/skills)
- `ambient-44-bar-arrangement-map`: low pad plus light percussion; high pad at bar 5; piano at bar 13; shaker about bar 17; about 8 bars of strip-back to shaker/hat; return about bar 33 with new chords; coda, percussion stops half a bar early, ends on piano at bar 45.
- `ambient-multi-section-arrangement`: cues at section changes (tiny hats, whoosh, snare), tempo change per section, a final push then a taper.
- `ambient-chord-arrangement`: about 55 BPM; sub on the root, a pad on the third, a choir pad on the fifth, a frozen string; parallel motion and spread voicing.
- `lydian-ambient-soundscape-layering`: 70 BPM C Lydian, 16-bar cadence (Cmaj7, Cadd#11, Cadd9), layers split by frequency range, mute test.
- `eight-bar-build-up`: 8 bars (16 for drum and bass); bars 1-7 risers and drums, bar 8 is the pre-drop with everything else cut; kick every beat, doubled, doubled again; low end removed toward the drop.
- `breakdown-arrangement`: break (4) then breakdown 1 (8), breakdown 2 (8), build-up (8), drop; the melody is foreshadowed with low-pass automation.
- `emotional-cinematic-arrangement-arc`: subtle intro; add layers a little at a time; melody only at the climax; continuous fade-out outro; melody grown from chord arpeggios.

## 5. Rules the song engine uses **[synthesis]**
1. Work in 4-bar and 8-bar blocks; change something at every block boundary.
2. Repeat sections with a variation: a new layer, a new fill, or a transposed key. Do not repeat a section unchanged more than once.
3. Energy is shaped by layer count and level, not by loudness normalisation. The section map carries an energy number 1-10, and the render reports how well measured section loudness follows it (Spearman correlation).
4. Every section boundary gets a transition (riser, reverse swell, sub drop, impact, downlifter, gap, low-cut or snare roll) or an intentional hard cut.
5. A pre-drop gap of about half a beat gives the "breath".
6. Keep lows mono (side channel high-passed at 120 Hz) and keep true peak at or below -1 dBTP.
7. Total length targets: ambient 140-160 s, cinematic 150-175 s, electronic 130-150 s, pop 120-150 s, game loop demo 120-140 s, meditation 480-900 s.

## 6. Engine and recipes
- Engine: `sample-lab/song/build_song.py` (recipe in, WAV out plus a stats JSON). Recipe generator: `sample-lab/song/make_recipes.py`. Recipes: `sample-lab/workflows/song-*.json`.
- Renders and measurements: `/workspace/share/songs/stats.md` (audio is not committed to git).

## 7. Gaps (hunt topics)
- No drum or percussion skills: the engine uses built-in numpy kick/clap/snare/hat voices. Topics: "drum synthesis kick snare hat", "drum programming patterns".
- No melody-writing or motif-development skills: melodies are hand-written note lists.
- No vocal skills: ElevenLabs TTS or music as optional sources (see the plan Page).
- No song-structure skill in the library: the seven arrangement skills are all ambient/cinematic/EDM specific; none cover verse-chorus, bridge or key-change lifts.
- No per-layer filter-sweep, pitch-automation or tempo-lane renderer: the build-up skill's pitch-bent held note is not reproduced.
- No mixing or mastering skills beyond limiting; no sidechain skill that actually renders (the engine does its own kick-driven duck).
