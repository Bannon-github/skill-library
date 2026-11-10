import json
from pathlib import Path
R=Path('/workspace/skill-library')
AFF="Original synthesis/processing recipe; not affiliated with Ableton, Reason, Bitwig, Soundtoys, FabFilter, Eventide or any vendor. Map product devices to generic modules (sampler, noise osc, filter, envelope, LFO, EQ, saturator, compressor, delay, reverb) in any DAW, hardware or Web Audio."
STEADY="Steady pitch: no random pitch wobble or randomised notes; no rapid clicking textures (Matt's preference)."
def S(vid,title,sid,name,goal,pre,inputs,outputs,cons,steps,ver,tags):
    d={"schema_version":"1.0","id":sid,"name":name,"goal":goal,"domain":"cinematic-synth",
       "source":{"kind":"youtube-transcript","video_id":vid,"url":f"https://www.youtube.com/watch?v={vid}","title":title,"transcript":"youtube-provided",
                 "distilled_path":f"distilled/{vid}/agent-skill-{sid}.json","batch":"2026-11-10-morning-hunt"},
       "prerequisites":pre,"inputs":[dict(zip(("name","type","description","required"),i)) for i in inputs],
       "outputs":[dict(zip(("name","type","description"),o)) for o in outputs],
       "constraints":cons+[AFF,STEADY],
       "steps":[{"n":n+1,"action":a,"tool":t,"expect":e} for n,(a,t,e) in enumerate(steps)],
       "verification":ver,"tags":tags+["portable","cinematic-synth"],"curriculum_ids":["curriculum-cinematic-hybrid-synth"],"mcp_resource":f"skill://{sid}"}
    p=R/'distilled'/vid; p.mkdir(parents=True,exist_ok=True)
    (p/f'agent-skill-{sid}.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n"); print(p/f'agent-skill-{sid}.json')

S("N60Jcn9zfBo","Disclosure's Signature Kick (How To Make It & Why It Sounds So Good)",
 "dark-short-kick-behind-busy-bass-transient-body-tail-73hz-start-eighth-note-length",
 "Dark, short house kick that sits behind a busy bassline: think in transient / body / tail, keep the transient dark (not clicky), start the body pitch near 73 Hz and fall to the sub, cut the tail to an eighth (or sixteenth) note, tune to the key, layer only what's missing, and mix the kick a few dB lower than the bass",
 "Synthesize and place a kick in the Disclosure style (pop-leaning house mix) so the bass carries the groove. Delta vs drum-synthesis cluster (synth kit from basic synth, trailer hits, taiko noise): this is a kick-length/level/darkness recipe for leaving room for a busy bass, and a reference-curve check; it also suits softer, less clicky kicks.",
 ["A kick synth (sine body with pitch envelope, attack, decay) or a drum sampler with pitch and amp envelopes","EQ and a spectrum analyser; reference tracks in the target style"],
 [("song_key","string","Key to tune the kick to",True),("bassline","midi/audio","Busy bassline the kick must leave room for",True),("reference_tracks","audio","Target-style records for a frequency guide",False)],
 [("kick","audio","Short, dark, tuned kick sitting a few dB under the bass")],
 ["Dark transient: avoid bright clicky EDM transients (also Matt's preference: no clicky textures).","Kick length about an eighth note at the song tempo, sometimes as short as a sixteenth.","Layer only to fix a missing part; extra layers can cause phase issues.","Steady tuned pitch; the pitch envelope is a fixed fast drop, not modulation."],
 [("Split the kick into three parts: transient (the tiny start), body (the chest punch) and tail (the sub). Judge and fix each part separately.","Listening / analyser","Know which part needs work"),
  ("Synthesize the kick: a sine body tuned to the song key, with a pitch envelope starting higher, around 73 Hz, and falling to a lower sub note. Add a short pitch-envelope punch (around 100 Hz) for pop if needed.","Kick synth: osc pitch + pitch env","Punchy body that settles on the key's sub note"),
  ("Keep the transient dark: low-pass or choose a soft attack rather than a bright click.","Kick synth attack / EQ","Less clicky start than an EDM kick"),
  ("Set decay so the whole kick lasts about an eighth note (sometimes a sixteenth) at the song tempo, leaving space for the bassline.","Amp envelope decay","Short kick, room for the bass between hits"),
  ("Layer only if something is missing: e.g. a sub layer for the felt low end, a body layer with its sub removed for punch, and a quiet top layer. Check for phase issues after layering.","Layers + EQ","Each layer covers one part without cancellation"),
  ("Mix the kick a few dB lower than a typical melodic-house kick so the bass is the focus, with the kick still audible.","Fader","Bass leads, kick supports"),
  ("Make a frequency guide from reference records: compare the kick and sub curve on an analyser and EQ the kick (e.g. trim excess around 50 Hz or deep sub) toward the reference.","Analyser + EQ","Kick and sub curve close to the target")],
 ["Kick decay ends within about an eighth note at the song tempo.","Kick body pitch starts near 73 Hz and settles on a key-related sub note.","Kick peak level sits a few dB below the bass bus; analyser curve is close to the reference."],
 ["kick","drum-synthesis","house","pitch-envelope","tuning","low-end","soft-kick","mix"])

S("RPzAJFC_JkI","How to Build Evolving Cinematic Pads with Wavetable Synths",
 "three-band-wavetable-rack-counter-lfo-position-glue-reverb-saturate-reverb-macro-drive",
 "Evolving cinematic pad/drone from a three-instance wavetable rack split by register (lows / mids / highs), each with two very slow free-running LFOs moving the two oscillators' wavetable positions in opposite directions, glue compression, a reverb→gentle saturation→long reverb sandwich, and one macro that opens filters and adds drive",
 "Build a pad that keeps changing under one held chord or note. Delta vs wavetable cluster (four-layer wave-sequenced pad, self-evolving WT rack): the register-split three-instance rack with counter-moving position LFOs per instance, and the reverb–saturation–reverb chain with a single drive/filter macro.",
 ["A wavetable synth with 2 oscillators, filters with drive, unison modes and free-running LFOs","An instrument rack/group to hold three instances; glue compressor, algorithmic reverb, saturator/waveshaper, long reverb, limiter"],
 [("chord","midi","Held chord or single note (e.g. G minor)",True)],
 [("pad_rack","synth rack","Three-layer evolving pad/drone with one expression macro")],
 ["Use slow free-running LFOs (e.g. around 0.04 Hz or slower) for steady evolving motion; avoid random pitch or random parameter jumps (Matt's preference). Use a second slow LFO instead of the source's random amount on filter cutoff.","Each band covers its own register: low-cut the mids layer, keep the lows layer simple (saw + sub, no unison) and controlled.","Keep a limiter at the end while designing; levels jump when all three play."],
 [("Mids layer: wavetable osc 1 with a warm table, filter closed a little (drive-capable filter type), low cut to keep it in the mids. Two very slow LFOs at slightly different rates, retrigger off: LFO 1 + and LFO 2 − on osc 1 position.","Wavetable synth","Slowly morphing mid pad"),
  ("Osc 2 on the mids: a different table (e.g. sweep saw) with the same two LFOs in the opposite directions, so the movements sometimes cancel. Add shimmer-style unison.","Osc 2 + unison","Floating, wide mid layer"),
  ("Filter 1 movement on the mids: a small amount of both LFOs and of a slow envelope (about 2 s decay, 3 s release) on cutoff.","Filter mod","Filter opens then drifts slowly"),
  ("Group into a rack, duplicate the instance twice and name them lows / mids / highs.","Instrument rack","Three parallel instances"),
  ("Highs: brighter, more aggressive tables, filter more open with light drive, noise-style unison with more voices; make its LFOs different speeds from the mids (one slower, around 0.04 Hz); keep mod amounts delicate. Osc 2 slightly detuned and optionally an octave down.","Highs instance","Rich shimmering top layer moving on its own timeline"),
  ("Lows: simple saw an octave down without unison plus a sub; cut the lowest rumble with a steeper, low-resonance filter; one very slow LFO with a small amount on filter frequency.","Lows instance","Stable warm floor"),
  ("Set about 1 s attack on all three and balance their levels (turn highs down if they dominate).","Amp env + rack levels","Balanced three-band pad"),
  ("FX chain after the rack: glue compressor (4:1, threshold just catching peaks), algorithmic reverb 100% wet with a vintage character, gentle soft-clip saturation, then a long lush reverb at 50% mix, and a limiter catching 2-3 dB.","Compressor, reverb, saturator, reverb, limiter","Long, lush, controlled tail"),
  ("Map one macro (mod wheel) on each instance to open filter 1 (or close it on the highs) and add filter drive, with only a small wavetable-position offset.","Macro / mod wheel","One control for intensity and grit"),
  ("Hold one chord, then a single note, and check that the sound keeps evolving with no loud jumps.","Playback","Self-evolving drone/pad usable under a cue")],
 ["Each instance's two oscillators move in opposite position directions at different slow rates.","Lows, mids and highs each occupy their own band on an analyser.","Holding one chord for 30 s gives continuous slow change with no clipping at the limiter."],
 ["wavetable","pad","drone","cinematic","evolving","lfo","layering","reverb","saturation","macro"])
