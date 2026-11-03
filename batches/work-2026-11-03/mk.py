import json
from pathlib import Path
R=Path('/workspace/skill-library')
AFF="Original synthesis/processing recipe; not affiliated with any vendor named in the source. Recreate in browser/Web Audio (Polyrhythm Studio) or any DAW/synth with comparable modules; no presets, banks, impulse responses or samples copied."
DRUMS="Drums early (Matt's taste): if the track has drums, the kick/drum loop enters by about count 8 (roughly 10-12 s), with only the pad before that."
def S(n,a,t,e): return {"n":n,"action":a,"tool":t,"expect":e}
def mk(vid,title,sid,name,goal,pre,inp,out,cons,steps,ver,tags):
    d={"schema_version":"1.0","id":sid,"name":name,"goal":goal,"domain":"cinematic-synth",
       "source":{"kind":"youtube-transcript","video_id":vid,"url":f"https://www.youtube.com/watch?v={vid}","title":title,"transcript":"youtube-provided",
                 "distilled_path":f"distilled/{vid}/agent-skill-{sid}.json","batch":"2026-11-03-morning-hunt"},
       "prerequisites":pre,"inputs":inp,"outputs":out,"constraints":[AFF]+cons+[DRUMS],"steps":steps,"verification":ver,
       "tags":tags+["portable","steady-pitch","cinematic-synth"],"curriculum_ids":["curriculum-cinematic-hybrid-synth"],"mcp_resource":f"skill://{sid}"}
    p=R/'distilled'/vid; p.mkdir(parents=True,exist_ok=True)
    (p/f'agent-skill-{sid}.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n"); print(p/f'agent-skill-{sid}.json')

mk("ZsbcQZtklGI",'Sylenth 1 Tutorial "Phasing" Pad',"phaser-chorus-pure-wave-octave-pad",
 "Phaser + chorus pad from pure waves: triangle and sine unison stacks on one note in three octaves, slow filter-envelope opening, triplet-synced phaser, deep feedback chorus, notch the phaser whistle, dark church-style reverb",
 "Make a soft trance/ambient background pad whose movement comes almost entirely from a phaser and a feedback chorus rather than modulation: soft triangle and sine unison stacks play the same note in three octaves, a slow filter envelope opens the tone as notes hold, and the space comes from a dark, low-cut convolution-style reverb. Delta vs the phaser cluster: pure-wave (triangle/sine) source, phaser + chorus in series as the only motion, and cutting the resonant 'whistle' the phaser creates.",
 ["Any synth with 2 oscillators (triangle, sine), unison, 24 dB low-pass and a mod envelope","Phaser and chorus effects (or all-pass chain + modulated short delay)","Reverb with EQ on the return (convolution or algorithmic hall)"],
 [{"name":"progression","type":"midi","description":"Chord roots or the bass progression to follow","required":True}],
 [{"name":"phasing_pad","type":"audio","description":"Soft, slowly opening pad with phaser/chorus movement that sits behind the mix"}],
 ["Unison detune stays small and static (no random pitch); movement comes from phaser and chorus only.","Prefer triangle/sine sources for this pad; they are the softest and leave room for effects to add motion.","Keep the pad in the background: no extra modulation, simple levels."],
 [S(1,"Write the clip as the same note in three octaves (e.g. B0, B1, B2) following the progression of the bass.","Piano roll","Octave-stacked single-note pad line"),
  S(2,"Osc 1: triangle, 6 unison voices, small static detune, wide stereo, centre pan, retrigger on. Osc 2: sine, 8 unison voices, slightly more detune, phase offset (~85 degrees), retrigger on. Raise polyphony since several notes play.","Synth oscillators","Soft, thick but steady-pitched tone"),
  S(3,"Amp envelope: back the attack off so each note fades in slowly; keep sustain high.","Amp envelope","Notes swell in"),
  S(4,"24 dB/oct low-pass with a mod envelope on cutoff: cutoff a little below full (about 70% of range), slow envelope attack (about 65% of its range) and medium sustain (about 50%), so the filter opens gradually while notes hold.","Filter + mod envelope","Tone warms and brightens slowly during each note"),
  S(5,"Phaser: spread at maximum, left/right offset centred, width about half, default feedback, dry/wet about 38-40%, LFO rate tempo-synced slightly slower than 1/8 (the source uses a 4/1-triplet style setting).","Phaser","Audible sweeping notches"),
  S(6,"Chorus after the phaser: delay about 4 ms, rate about 0.25 Hz, depth about 60%, feedback on (chorus feeds back into itself), width maximum, dry/wet about 40%.","Chorus","Deep, wide movement"),
  S(7,"Solo the pad and listen for a resonant whistle the phaser creates; cut that band with a narrow, deep EQ notch.","EQ","No whistling peak"),
  S(8,"Reverb as an insert or send at about 35% wet: slow, large hall/church-type space, pre-delay about 10 ms, size and decay at maximum; on the reverb's EQ cut everything below 150 Hz and roll the highs off around 4.5 kHz. Add a light compressor after it (shorter release) to bring the reverb up.","Reverb + EQ + compressor","Rich, dark space that does not muddy the bass"),
  S(9,"Sidechain-compress the pad to the kick for gentle pump and automate the pad filter so it comes in and out across sections.","Sidechain compressor / automation","Pad breathes with the kick and the arrangement")],
 ["The pad is the same note in three octaves following the bass roots.","Only phaser and chorus move the sound; pitch is steady.","Filter opens audibly over each held note.","No resonant whistle peak remains after the notch.","Reverb return has nothing below about 150 Hz."],
 ["pad","phaser","chorus","trance","ambient","filter-envelope","reverb"])

mk("3rCUdTDodrc","Sound Design Tutorial: Cinematic Whoosh hit","whoosh-into-hit-layer-resample-chain",
 "Cinematic whoosh-hit: layer sub-whoosh, whoosh and three hit layers, edit the whoosh quieter than the hit and tighten the flam, resample at milestones, dark dual reverbs, upward/parallel compression, clipping, sub removed from the whoosh only, multiband then true-peak limiting",
 "Build a punchy cinematic whoosh-into-hit impact by layering (a reversed sub-kick tail plus a resonant whoosh leading into three short metallic/wooden hits), then editing so the whoosh is quieter than the hit and the hit transients are only slightly flammed, and finishing with a resample-by-milestone processing chain. Delta vs our riser/whoosh variants: the whoosh-to-hit contrast rules (quieter whoosh, no sub in the whoosh) and the clip/limit finishing chain for impacts.",
 ["DAW with audio editing, resampling/bounce and return tracks","Source layers: a synth or recorded sub kick, noise/foley whooshes, 2-3 short impact hits (own recordings or synthesized)","Tape saturation, two reverbs, EQ, multiband/upward compressor, clipper, multiband limiter, true-peak limiter (any brands)"],
 [{"name":"layers","type":"audio","description":"Sub layer, 1-2 whoosh layers, 2-3 hit layers","required":True}],
 [{"name":"whoosh_hit","type":"audio","description":"Mastered whoosh-into-hit impact, true-peak safe"}],
 ["The whoosh must be quieter than the hit transient so the hit feels loud by contrast.","Remove sub (below ~60 Hz) from the whoosh so the low end arrives with the hit.","Pitch moves are fixed transpositions of hit layers (lowered pitch), not wobble.","Keep a copy at each resample milestone so you can always go back."],
 [S(1,"Layer: a sub layer made from the reversed tail of a sub kick, a resonant whoosh layer (e.g. noise or foley swept past a resonant body), and three short hit layers lightly pitched down, each with a small whoosh into a clean transient and a tail.","Arrangement / sampler","Five layers that read as whoosh -> hit"),
  S(2,"Resample the sum at the first milestone and keep the original; work on a duplicate.","Bounce / resample","Safe restore point"),
  S(3,"Edit without plugins: chop the whoosh and lower its level below the hit; trim the hit layers so the transients flam only slightly (a small flam lengthens the body, too much sounds messy).","Clip editing / gain","Quieter whoosh, cleaner single hit"),
  S(4,"Resample again, add gentle tape saturation to glue the layers.","Tape saturation","Layers sit together"),
  S(5,"Send to two dark reverbs on returns: a room with about 2.75 s decay and a low filter, and a plate with about 3.6 s decay low-passed around 1.4 kHz; sum dry and reverbs into one bus.","Reverb returns","Deep, low tail with two characters"),
  S(6,"On the bus: tame the high-end noise in the tail after the transient (adaptive denoise or a dynamic high-shelf cut that acts after the hit), then two upward/downward multiband compressors in series at low mix, then aggressive parallel compression at 50% wet.","Dynamics","Denser, more energetic body without hissy tail"),
  S(7,"Clip the peak hard (about 6 dB of clipping) to square off and prolong the transient, then limit lightly. Resample (milestone 3).","Clipper + limiter","Heavier, boxier transient"),
  S(8,"Final pass: re-edit any unwanted whoosh section with fades; high-pass only the whoosh portion at about 60 Hz; a few EQ notches/boosts by ear; light clipping (~1.5 dB); a multiband limiter (lowest band ~0-100 Hz) with some transient emphasis; then a true-peak limiter as a safety net.","EQ + clipper + multiband limiter + true-peak limiter","Punchy, heavy impact that cuts through without digital clipping")],
 ["Whoosh peak level is clearly below the hit transient level.","No energy below ~60 Hz before the hit; the sub arrives with the hit.","Hit transient shows at most a slight flam.","Final file has no true-peak overs."],
 ["impact","whoosh","hit","transition-fx","trailer","layering","clipping","resampling"])

mk("eDErfMlnh7c","Fix a Thin Mix: Easy Parallel Bass Trick for Ambient Music","parallel-octave-down-bass-from-stereo-mix",
 "Parallel octave-down bass for a thin ambient stereo take: duplicate the mix, pitch it down an octave at the same tempo, low-pass it at ~100 Hz (12 dB/oct), high-pass the original at the same point (24 dB/oct), squash the copy with a limiter and blend it in quietly, checking phase correlation",
 "Add weight to a thin one-take ambient/modular stereo recording (or a bounced pad/drone stem) without writing a new bass part: derive a sub layer by pitching a copy of the mix down one octave, crossover it against the original at about 100 Hz, remove its dynamics and tuck it underneath. Delta vs our bass-design variants: a sub generated from the existing material by octave transposition plus a complementary crossover, for when there are no multitracks.",
 ["DAW with pitch shifting/warping that keeps tempo","EQ/filters, a limiter, a spectrum analyzer and a phase-correlation meter"],
 [{"name":"stereo_mix","type":"audio","description":"Finished stereo take or stem whose low end rolls off steeply around 100 Hz","required":True}],
 [{"name":"parallel_sub","type":"audio","description":"Octave-down, low-passed, flattened copy blended under the original"}],
 ["Octave shift is a fixed -12 semitone transposition; no pitch modulation.","The added layer supports the track; keep it quiet so it does not take over.","Crossover the two paths at the same frequency to avoid doubled frequencies and phase problems."],
 [S(1,"Analyse the mix: find where the low end rolls off (e.g. steeply below ~100 Hz).","Spectrum analyzer","Roll-off frequency noted"),
  S(2,"Duplicate the track and pitch the copy down one octave while keeping the playback speed (warp/time-stretch). Energy at 100 Hz now appears at 50 Hz.","Pitch shift / warp","Octave-down copy in time with the original"),
  S(3,"Turn the copy well down, then low-pass it gently (12 dB/oct) at about the original's roll-off (~100 Hz).","Low-pass filter","Copy contributes only sub/bass"),
  S(4,"High-pass the original (24 dB/oct) at the same point so the two paths do not overlap.","High-pass filter","Complementary crossover"),
  S(5,"Check a phase-correlation meter around 100 Hz; adjust the crossover if correlation drops.","Correlation meter","No phase problems at the crossover"),
  S(6,"Limit the copy aggressively (several dB of gain reduction, e.g. ~6-7 dB) so its dynamics are flattened, then set its level low and A/B on and off.","Limiter + fader","Steady, quiet sub support; mix feels heavier, not boomy")],
 ["Sub band (~40-80 Hz) shows new, steady energy after blending.","Correlation stays positive around the crossover.","Bypassing the copy makes the mix sound noticeably thinner, but enabling it does not mask the original."],
 ["bass","sub-bass","punchy-bass","parallel-processing","ambient","mastering","crossover"])
