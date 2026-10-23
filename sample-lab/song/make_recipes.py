#!/usr/bin/env python3
"""Writes the six song recipes to ../workflows/song-*.json. Skill ids are resolved by unique prefix against mcp-publish/skills,
so a typo fails here. Edit this file, re-run, then `build_song.py --validate` / `build_song.py recipe out.wav`."""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); LAB = os.path.dirname(HERE); LIB = os.path.dirname(LAB)
IDS = sorted(os.path.basename(p)[:-5] for p in glob.glob(LIB + "/mcp-publish/skills/*.json"))
def S(prefix):
    m = [i for i in IDS if i.startswith(prefix)]; assert len(m) == 1, (prefix, m); return m[0]
def chain_skills(system): return [st["skill"] for st in json.load(open(f"{LAB}/systems/{system}/chain.json"))["steps"]]
def layer(kind, system=None, **kw):
    d = dict(kind=kind, **kw)
    if system: d["system"] = system; d["chainSkillIds"] = chain_skills(system); d["skillIds"] = list(dict.fromkeys(d["chainSkillIds"] + kw.get("skillIds", [])))
    return d
GATES = lambda lo=-18.0, hi=-13.0: {"targetVersion": "TARGET.md v1.3 (the parts that apply to a full-length mix; per-note metrics M3/M4/M6-M11/M13/M15 are not used)",
    "G1_truePeakMaxDb": -1.0, "G2_clippedSamples": 0, "G3_dcMax": 0.001, "G4_determinism": "a rendered clip re-renders bit-identical", "G5_cleanTailRmsMaxDb": -60,
    "G6_cleanStartPeakMax": 0.003, "G7_finite": True, "M1_loudnessLufsBand": [lo, hi], "M2_monoFoldLossMaxDb": 3.0, "M5_sideMidBelow150HzMaxDb": -15,
    "M12_energyAbove12kMaxDb": -24, "M14_limiterGainReductionMaxDb": 4,
    "seams": {"stepVsP999Max": 8, "note": "section boundaries are intentional changes: their flux and loudness steps are reported, not gated"},
    "plannedCurve": {"spearmanLufsVsPlannedEnergyMin": 0.7, "note": "section loudness should follow the planned 1-10 energy order; reported with each render"}}
def table(R):
    prev = set(); rows = ["| # | section | bars | bpm | key / chords | layers entering | layers leaving | energy | transition into next |", "|---|---|---|---|---|---|---|---|---|"]
    for i, s in enumerate(R["sections"], 1):
        cur = {k for k, v in (s.get("layers") or {}).items() if v is not None}
        tr = ", ".join(t["type"] + (f" {t['bars']}b" if "bars" in t else "") + (f" {t['beats']}beat" if "beats" in t else "") for t in s.get("transitions", [])) or "-"
        rows.append(f"| {i} | {s['name']} | {s['bars']} | {s.get('bpm', R['bpm'])} | {s.get('keyLabel', '')} | {', '.join(sorted(cur - prev)) or '-'} | {', '.join(sorted(prev - cur)) or '-'} | {s['energy']} | {tr} |")
        prev = cur
    return "\n".join(rows)
def finish(R, name):
    R["totalBars"] = sum(s["bars"] for s in R["sections"]); R["sectionTableMd"] = table(R)
    secs = sum(s["bars"] * 4 * 60 / s.get("bpm", R["bpm"]) for s in R["sections"]); R["lengthSecPlanned"] = round(secs + R.get("tailSec", 4), 1)
    json.dump(R, open(f"{LAB}/workflows/{name}.json", "w"), indent=1); print(name, R["totalBars"], "bars", R["lengthSecPlanned"], "s")

# =============================================================== 1. Ambient arc (44-bar map)
def r1():
    cl = lambda root, mid, high, full: dict(voices=dict(root=root, mid=mid, high=high, full=full), bars=4)
    R = dict(id="song-ambient-arc-44", form="Ambient arc: staggered entry -> full -> strip-back -> return with new chords -> coda (through-composed layers, 44 bars)",
        version=1, note="Original sound. Skills define the layer roles and the bar map; tempo 70 BPM and C Lydian come from the Lydian layering skill. Pad parts follow the chord-tone split skill (root / mid / high).",
        bpm=70, seed=44, targetLufs=-16, peakCeilDb=-1.0, tailSec=6.0, xfadeSec=2.0, masterFade=dict(inSec=3.0, outSec=5.0), drumBusDb=12, drumLevelDb=dict(rim=-24, ohat=-26, shaker=-26, hat=-28),
        targetLengthSec=[140, 160], skillIds=[S("ambient-44-bar"), S("ambient-chord-arrangement"), S("lydian-ambient"), S("ambient-multi-section")],
        chordLoops=dict(
            A=[cl([36, 43], [55, 59, 64], [60, 64, 67, 71], [48, 52, 55, 59]),      # Cmaj7
               cl([36, 43], [54, 64, 67], [60, 64, 66, 71], [48, 52, 54, 59]),       # Cadd#11 (F# and G a semitone apart)
               cl([36, 43], [55, 62, 64], [60, 62, 64, 67], [48, 52, 55, 62]),       # Cadd9
               cl([36, 43], [55, 59, 64], [60, 64, 67, 71], [48, 52, 55, 59])],      # Cmaj7
            B=[cl([40, 47], [55, 59, 62], [64, 67, 71, 74], [52, 55, 59, 62]),      # Em7 (new chords for the return)
               cl([38, 45], [54, 57, 62], [62, 66, 69, 73], [50, 54, 57, 62])]),     # D6
        layers=dict(
            lowPad=layer("chords", "drone-wavetable-artifact-drone", voice="root", levelDb=-6, tailSec=6.0, skillIds=[S("ambient-44-bar")], role="low pad: chord roots + fifths"),
            highPad=layer("chords", "pad-wide-supersaw-chord-pad", voice="high", levelDb=2, tailSec=6.0, seedOff=3, skillIds=[S("ambient-chord-arrangement")], role="high pad: upper chord tones"),
            choir=layer("chords", "swell-multi-envelope-morph-swell", voice="mid", levelDb=0, tailSec=6.0, seedOff=5, skillIds=[S("ambient-chord-arrangement")], role="mid swell pad: third / fifth (choir stand-in)"),
            piano=layer("chords", "pluck-organic-velocity-pluck", voice="full", levelDb=1, tailSec=5.0, seedOff=7, rhythm=[[0, 3.0, 0.7]], arp=None, skillIds=[S("ambient-44-bar")], role="piano stand-in: whole chord replayed every bar"),
            air=layer("noise", lpHz=1800, panPeriodSec=40, levelDb=0, skillIds=[S("lydian-ambient")], role="quiet noise bed (field-recording stand-in)")),
        sections=[
            dict(name="Intro", bars=4, keyLabel="C Lydian: Cmaj7", chords="A", chordStart=0, energy=2, layers=dict(lowPad=0, air=-30), drums=dict(rim="rim_sparse", ohat="x...............", levelDb=dict(rim=-26, ohat=-28)),
                 skillIds=[S("ambient-44-bar")], transitions=[dict(type="whoosh", sec=2.0, gainDb=-26, dir="up")]),
            dict(name="Rising: high pad", bars=8, keyLabel="Cadd#11 -> Cadd9", chords="A", chordStart=1, energy=3, layers=dict(lowPad=0, highPad=-7, air=-28), drums=dict(rim="rim_sparse", ohat="x..............."),
                 skillIds=[S("ambient-44-bar"), S("ambient-chord-arrangement")], transitions=[dict(type="reverse_swell", source="piano", trim=[0.2, 3.5], irSec=4.0, gainDbRel=-6, skillIds=[S("reverse-reverb-swell")])]),
            dict(name="Piano enters", bars=4, keyLabel="Cmaj7", chords="A", chordStart=3, energy=4, layers=dict(lowPad=0, highPad=-7, choir=-10, piano=-8, air=-28), drums=dict(rim="rim_sparse", ohat="x..............."),
                 skillIds=[S("ambient-44-bar")], transitions=[dict(type="whoosh", sec=1.5, gainDb=-26, dir="up")]),
            dict(name="Full track: shaker", bars=8, keyLabel="Cmaj7 -> Cadd#11", chords="A", chordStart=0, energy=6, layers=dict(lowPad=0, highPad=-6, choir=-8, piano=-7, air=-26), drums=dict(rim="rim_sparse", ohat="x...............", shaker="shaker16"),
                 skillIds=[S("ambient-44-bar"), S("lydian-ambient")], transitions=[dict(type="downlifter", sec=3.0, gainDb=-18, skillIds=[S("noise-layer-whoosh")])]),
            dict(name="Strip-back: shaker + hat", bars=8, keyLabel="Cadd9 -> Cmaj7", chords="A", chordStart=2, energy=3, layers=dict(lowPad=None, highPad=-4, choir=None, piano=None, air=-20), drums=dict(shaker="shaker16", hat="eighth_hat"),
                 skillIds=[S("ambient-44-bar"), S("ambient-multi-section")], transitions=[dict(type="riser", bars=2, fHz=[300, 3000], gainDb=-16, tailSec=3.0, skillIds=[S("one-bar-transition-riser")]),
                      dict(type="reverse_swell", source="lowPad", trim=[0.3, 4.3], irSec=5.0, gainDbRel=-4, skillIds=[S("reverse-reverb-swell")])]),
            dict(name="Return: new chords", bars=8, keyLabel="Em7 -> D6 (new)", chords="B", chordStart=0, energy=7, layers=dict(lowPad=0, highPad=-5, choir=-7, piano=-6, air=-26), drums=dict(rim="rim_sparse", ohat="x...............", shaker="shaker16"),
                 skillIds=[S("ambient-44-bar")], transitions=[dict(type="downlifter", sec=3.0, gainDb=-18, skillIds=[S("noise-layer-whoosh")])]),
            dict(name="Coda: piano ending", bars=4, keyLabel="Cmaj7", chords="A", chordStart=0, energy=2, layers=dict(lowPad={"db": -3, "toDb": -14}, highPad={"db": -8, "toDb": -16}, choir=None, piano=-8, air=-30), drums=dict(shaker="shaker16", stopAtBeat=14),
                 skillIds=[S("ambient-44-bar")], transitions=[])],
        qualityGates=GATES(-19, -13))
    finish(R, "song-ambient-arc-44")

# =============================================================== 2. Cinematic cue
def r2():
    def cl(r, mid, high, full, bars=2): return dict(voices=dict(root=r, mid=mid, high=high, full=full), bars=bars)
    motif = dict(bars=8, notes=[[0, 76, 3, .9], [3, 74, 1, .7], [4, 72, 2, .8], [6, 69, 2, .75], [8, 72, 3, .85], [11, 69, 1, .7], [12, 77, 2, .85], [14, 76, 2, .8],
                                [16, 79, 3, .95], [19, 76, 1, .7], [20, 72, 2, .8], [22, 76, 2, .8], [24, 74, 3, .85], [27, 71, 1, .7], [28, 74, 2, .8], [30, 71, 2, .7]])
    dialog = dict(bars=4, notes=[[0, 69, 3, .6], [6, 72, 2, .5], [10, 76, 4, .5], [14, 69, 2, .45]])
    R = dict(id="song-cinematic-cue", form="Cinematic cue: intro (nothing -> warmth) -> build (add layers) -> climax (the only melody) -> fade outro; 48 bars",
        version=1, note="Original sound. Chord loop is a familiar vi-IV-I-V in C (A minor tonic) as the arrangement-arc skill suggests; the melody is written from chord tones.",
        bpm=72, seed=48, targetLufs=-16, peakCeilDb=-1.0, tailSec=7.0, xfadeSec=3.0, masterFade=dict(inSec=6.0, outSec=8.0), drumLevelDb=dict(kick=-12, shaker=-26),
        targetLengthSec=[150, 175], skillIds=[S("emotional-cinematic"), S("hybrid-score-role-first"), S("one-bar-transition-riser"), S("reverse-reverb-swell"), S("sub-drop-sine")],
        chordLoops=dict(
            L=[cl([33, 40], [57, 60, 64], [64, 69, 72], [57, 60, 64, 69]), cl([29, 36], [57, 60, 65], [65, 69, 72], [57, 60, 65, 69]),
               cl([36, 43], [55, 60, 64], [64, 67, 72], [55, 60, 64, 67]), cl([31, 38], [55, 59, 62], [62, 67, 71], [55, 59, 62, 67])]),
        motifs=dict(theme=motif, dialogue=dialog),
        layers=dict(
            drone=layer("chords", "drone-wavetable-artifact-drone", voice="root", levelDb=0, tailSec=8.0, skillIds=[S("hybrid-score-role-first")], role="low drone: the role that enters first"),
            strings=layer("chords", "swell-multi-envelope-morph-swell", voice="full", levelDb=-4, tailSec=7.0, seedOff=2, skillIds=[S("emotional-cinematic")], role="string-like swells (slow attack)"),
            pad=layer("chords", "pad-wide-supersaw-chord-pad", voice="mid", levelDb=-6, tailSec=7.0, seedOff=4, skillIds=[S("emotional-cinematic")], role="warm pad body"),
            piano=layer("chords", "pluck-organic-velocity-pluck", voice="full", levelDb=-9, tailSec=5.0, seedOff=6, rhythm=[[i * 0.5, 0.45, 0.45 + 0.25 * (i % 2)] for i in range(8)], arp="updown",
                        skillIds=[S("emotional-cinematic")], role="piano stand-in: chord arpeggio forward/backward (the melody-from-chords method)"),
            motor=layer("chords", "gated-fifth-swell-trance-gate", voice="full", levelDb=-14, tailSec=6.0, seedOff=8, gateFloorDb=-10, skillIds=[S("hybrid-score-role-first")], role="motor: soft gated pulse that tightens the build"),
            melody=layer("melody", "pluck-organic-velocity-pluck", levelDb=-5, tailSec=6.0, seedOff=9, skillIds=[S("emotional-cinematic")], role="the climax melody (nowhere else)"),
            dialogue=layer("melody", "pluck-organic-velocity-pluck", levelDb=-8, tailSec=7.0, seedOff=11, octave=0, skillIds=[S("emotional-cinematic")], role="outro piano dialogue"),
            sub=layer("noise", lpHz=300, panPeriodSec=60, levelDb=-26, role="low air under the intro")),
        sections=[
            dict(name="Intro", bars=8, keyLabel="Am F C G (2 bars each)", chords="L", energy=2, layers=dict(drone={"db": -24, "toDb": -2}, strings={"db": -30, "toDb": -10}, sub=-20), skillIds=[S("emotional-cinematic"), S("hybrid-score-role-first")],
                 transitions=[dict(type="whoosh", sec=3.0, gainDb=-28, dir="up")]),
            dict(name="Build A: pad joins", bars=8, keyLabel="Am F C G", chords="L", energy=3, layers=dict(drone=-2, strings={"db": -10, "toDb": -5}, pad={"db": -18, "toDb": -7}, sub=-22), skillIds=[S("hybrid-score-role-first")],
                 transitions=[dict(type="reverse_swell", source="piano", trim=[0.2, 3.5], irSec=4.5, gainDbRel=-8, skillIds=[S("reverse-reverb-swell")])]),
            dict(name="Build B: arpeggio + motor", bars=8, keyLabel="Am F C G", chords="L", energy=5, layers=dict(drone=-2, strings=-5, pad=-7, piano={"db": -16, "toDb": -8}, motor={"db": -24, "toDb": -12}),
                 drums=dict(kick="half", levelDb=dict(kick=-20)), skillIds=[S("hybrid-score-role-first")],
                 transitions=[dict(type="riser", bars=3, fHz=[250, 4200], gainDb=-12, tailSec=4.0, skillIds=[S("one-bar-transition-riser")]),
                              dict(type="reverse_swell", source="strings", trim=[0.3, 4.3], irSec=6.0, gainDbRel=-4, skillIds=[S("reverse-reverb-swell")]),
                              dict(type="gap", beats=1.0, floorDb=-40), dict(type="impact", lengthSec=6, hz=[70, 26], noiseSec=3.5, gainDb=-9, skillIds=[S("sub-drop-sine"), S("synthesized-noise-impact")])]),
            dict(name="Climax A: melody", bars=8, keyLabel="Am F C G", chords="L", energy=8, layers=dict(drone=0, strings=-2, pad=-5, piano=-7, motor=-12, melody=-4), drums=dict(kick="half", levelDb=dict(kick=-14)),
                 melody=dict(layer="melody", motif="theme"), skillIds=[S("emotional-cinematic")], transitions=[]),
            dict(name="Climax B: melody up", bars=8, keyLabel="Am F C G", chords="L", energy=9, layers=dict(drone=0, strings=-1, pad=-4, piano=-6, motor=-11, melody=-3), drums=dict(kick="half", shaker="shaker16", levelDb=dict(kick=-12, shaker=-28)),
                 melody=dict(layer="melody", motif="theme", transpose=12, velScale=1.0), skillIds=[S("emotional-cinematic")],
                 transitions=[dict(type="downlifter", sec=4.0, gainDb=-14, skillIds=[S("noise-layer-whoosh")]), dict(type="sub_drop", lengthSec=6, hz=[60, 24], gainDb=-14, skillIds=[S("sub-drop-sine")])]),
            dict(name="Outro: fade", bars=8, keyLabel="Am F C G", chords="L", energy=1, layers=dict(drone={"db": -2, "toDb": -26}, strings={"db": -6, "toDb": -30}, pad={"db": -9, "toDb": -30}, dialogue=-6), melody=dict(layer="dialogue", motif="dialogue", transpose=0),
                 skillIds=[S("emotional-cinematic")], transitions=[dict(type="whoosh", sec=5.0, gainDb=-26, dir="up")])],
        qualityGates=GATES(-19, -13))
    finish(R, "song-cinematic-cue")

# =============================================================== 3. Electronic build/drop/breakdown/drop
def r3():
    def cl(r, full, high): return dict(voices=dict(root=[r], full=full, high=high, mid=full[:3]), bars=2)
    hook = dict(bars=4, notes=[[0, 81, .75, .9], [1, 84, .75, .8], [2, 88, 1.5, .95], [4, 84, .75, .8], [5, 81, .75, .8], [6, 79, 1.5, .85], [8, 77, .75, .9], [9, 81, .75, .8], [10, 84, 1.5, .9], [12, 83, .75, .8], [13, 79, .75, .8], [14, 76, 1.5, .85]])
    prev = dict(bars=4, notes=[n for n in hook["notes"] if n[0] < 7])
    prev2 = dict(bars=4, notes=[n for n in hook["notes"] if n[0] < 12])
    bass_rhythm = [[0.5, 0.4, 0.95], [1.5, 0.4, 0.8], [2.5, 0.4, 0.9], [3.5, 0.4, 0.8]]
    R = dict(id="song-electronic-build-drop", form="Electronic: intro -> build -> drop -> break/breakdown -> build -> drop 2 -> outro (dance-leaning, 76 bars @128)",
        version=1, note="Short demo version: the intro and outro are 8 bars (club mixes use 16-32). Drums are engine-built synth voices (no drum skill in the library). Original sound.",
        bpm=128, seed=76, targetLufs=-14, peakCeilDb=-1.0, tailSec=5.0, xfadeSec=0.05, masterFade=dict(inSec=0.1, outSec=6.0), drumBusDb=0,
        drumLevelDb=dict(kick=-4, clap=-10, snare=-10, hat=-18, ohat=-20, shaker=-24, rim=-20),
        targetLengthSec=[130, 150], skillIds=[S("eight-bar-build-up"), S("breakdown-arrangement"), S("sidechain-compressor"), S("one-bar-transition-riser"), S("sub-drop-sine"), S("synthesized-noise-impact"), S("reverse-reverb-swell"), S("noise-layer-whoosh")],
        chordLoops=dict(M=[cl(33, [57, 60, 64, 69], [69, 72, 76]), cl(29, [57, 60, 65, 69], [69, 72, 77]), cl(36, [55, 60, 64, 67], [67, 72, 76]), cl(31, [55, 59, 62, 67], [67, 71, 74])]),
        motifs=dict(hook=hook, preview4=prev, preview9=prev2),
        layers=dict(
            bass=layer("chords", "bass-velocity-hybrid-bass", voice="root", levelDb=0, tailSec=3.0, rhythm=bass_rhythm, sidechainDb=9, skillIds=[S("sidechain-compressor"), S("keysol-venus-velocity-hybrid-bass")], role="rolling off-beat bass, ducked by the kick"),
            stabs=layer("chords", "gated-fifth-swell-trance-gate", voice="full", levelDb=-6, tailSec=3.0, seedOff=2, sidechainDb=6, gateFloorDb=-14, skillIds=[S("trance-gate-sidechain"), S("classic-house-pad")], role="gated chord texture"),
            pad=layer("chords", "pad-wide-supersaw-chord-pad", voice="high", levelDb=-8, tailSec=4.0, seedOff=4, sidechainDb=6, skillIds=[S("sidechain-compressor")], role="wide chord pad / held note for builds"),
            soft=layer("chords", "pluck-organic-velocity-pluck", voice="full", levelDb=-9, tailSec=4.0, seedOff=6, rhythm=[[0, 6.0, 0.6]], skillIds=[S("breakdown-arrangement")], role="soft piano stand-in: drop chords as long chords"),
            hook=layer("melody", "pluck-organic-velocity-pluck", levelDb=-4, tailSec=3.0, seedOff=8, skillIds=[S("breakdown-arrangement")], role="drop melody"),
            air=layer("noise", lpHz=2500, panPeriodSec=20, levelDb=-14, role="quiet ambience bed for the break")),
        sections=[
            dict(name="Intro", bars=8, keyLabel="A minor: Am F C G (2 bars each)", chords="M", energy=4, layers=dict(pad={"db": -14, "toDb": -8}), drums=dict(kick="four", hat="offbeat", byBar=dict(hat=["off", "off", "offbeat", "offbeat", "offbeat", "offbeat", "offbeat", "offbeat"]), shaker="off", levelDb=dict(kick=-4)), skillIds=[S("eight-bar-build-up")], transitions=[]),
            dict(name="Build 1 (bars 1-7)", bars=7, keyLabel="Am F C G", chords="M", chordStart=0, energy=6, layers=dict(pad=-8, stabs={"db": -18, "toDb": -8}), drums=dict(kick="four", hat="offbeat", shaker="shaker16", clap="off",
                 byBar=dict(kick=["four", "four", "four", "four", "eighth", "eighth", "sixteenth"], clap=["off", "off", "off", "off", "off", "backbeat", "backbeat"])), skillIds=[S("eight-bar-build-up")],
                 transitions=[dict(type="riser", bars=7, fHz=[250, 5000], gainDb=-11, tailSec=0, skillIds=[S("one-bar-transition-riser")]), dict(type="lowcut", bars=4, hz=[30, 350], skillIds=[S("eight-bar-build-up")])]),
            dict(name="Pre-drop (bar 8)", bars=1, keyLabel="Am", chords="M", chordStart=0, energy=4, layers=dict(pad=-10), drums=dict(), skillIds=[S("eight-bar-build-up")],
                 transitions=[dict(type="snare_roll", bars=1, voice="snare", gapBeats=0.5), dict(type="gap", beats=0.5, floorDb=-60)]),
            dict(name="Drop 1", bars=16, keyLabel="Am F C G", chords="M", chordStart=0, energy=9, layers=dict(bass=0, stabs=-8, pad=-12, hook=-4), drums=dict(kick="four", clap="backbeat", hat="offbeat", shaker="shaker16", levelDb=dict(kick=-4)),
                 melody=dict(layer="hook", motif="hook", skillIds=[]), skillIds=[S("eight-bar-build-up"), S("sidechain-compressor")],
                 transitions=[dict(type="impact", lengthSec=5, hz=[70, 26], noiseSec=3.0, gainDb=-8, skillIds=[S("synthesized-noise-impact"), S("sub-drop-sine")])]),
            dict(name="Break (4 bars)", bars=4, keyLabel="Am F", chords="M", chordStart=0, energy=3, layers=dict(pad=-10, air=-18), drums=dict(), skillIds=[S("breakdown-arrangement")], transitions=[dict(type="downlifter", sec=3.0, gainDb=-14, skillIds=[S("noise-layer-whoosh")])]),
            dict(name="Breakdown", bars=8, keyLabel="Am F C G (long chords)", chords="M", chordStart=0, energy=2, layers=dict(pad=-4, soft=0, hook={"db": -10, "toDb": -4, "lp": [500, 12000]}, air=-20),
                 drums=dict(shaker="shaker16", hat="sixteenth_hat", levelDb=dict(shaker=-28, hat=-30)), melody=dict(layer="hook", motif="preview4", startBar=0, endBar=4),
                 skillIds=[S("breakdown-arrangement")], transitions=[dict(type="reverse_swell", source="pad", trim=[0.3, 4.3], irSec=4.0, gainDbRel=-6, skillIds=[S("reverse-reverb-swell")])]),
            dict(name="Build 2 (bars 1-7)", bars=7, keyLabel="Am F C G", chords="M", chordStart=0, energy=6, layers=dict(pad=-8, soft=-10, stabs={"db": -20, "toDb": -8}, hook={"db": -9, "toDb": -3, "lp": [900, 14000]}),
                 drums=dict(kick="four", hat="offbeat", shaker="shaker16", byBar=dict(kick=["off", "four", "four", "four", "eighth", "eighth", "sixteenth"], clap=["off", "off", "off", "backbeat", "backbeat", "backbeat", "backbeat"])),
                 melody=dict(layer="hook", motif="preview9", startBar=0, endBar=8), skillIds=[S("breakdown-arrangement"), S("eight-bar-build-up")],
                 transitions=[dict(type="riser", bars=7, fHz=[250, 5500], gainDb=-10, tailSec=0, skillIds=[S("one-bar-transition-riser")]), dict(type="lowcut", bars=4, hz=[30, 380], skillIds=[S("eight-bar-build-up")])]),
            dict(name="Pre-drop 2 (bar 8)", bars=1, keyLabel="Am", chords="M", chordStart=0, energy=4, layers=dict(pad=-10), drums=dict(), skillIds=[S("eight-bar-build-up")],
                 transitions=[dict(type="snare_roll", bars=1, voice="snare", gapBeats=0.5), dict(type="gap", beats=0.5, floorDb=-60)]),
            dict(name="Drop 2", bars=16, keyLabel="Am F C G", chords="M", chordStart=0, energy=10, layers=dict(bass=0, stabs=-7, pad=-10, hook=-3, soft=-14),
                 drums=dict(kick="four", clap="backbeat", hat="offbeat", ohat="offbeat", shaker="shaker16", levelDb=dict(kick=-3.5)), melody=dict(layer="hook", motif="hook", transpose=0),
                 skillIds=[S("eight-bar-build-up"), S("sidechain-compressor")], transitions=[]),
            dict(name="Outro", bars=8, keyLabel="Am F C G", chords="M", chordStart=0, energy=3, layers=dict(bass={"db": 0, "toDb": -24}, stabs=None, pad={"db": -10, "toDb": -24}),
                 drums=dict(kick="four", hat="offbeat", byBar=dict(kick=["four"] * 6 + ["half", "half"], hat=["offbeat"] * 4 + ["off"] * 4), levelDb=dict(kick=-12)), skillIds=[S("eight-bar-build-up")], transitions=[])],
        qualityGates=GATES(-18, -12))
    finish(R, "song-electronic-build-drop")

# =============================================================== 4. Verse-chorus-bridge instrumental pop
def r4():
    def cl(r, full, high, bars=2): return dict(voices=dict(root=[r], full=full, high=high, mid=full[1:]), bars=bars)
    C, Am, F, G, Em, Dm = (cl(36, [48, 52, 55, 60], [64, 67, 72]), cl(33, [45, 52, 57, 60], [64, 69, 72]), cl(41, [48, 53, 57, 60], [65, 69, 72]), cl(31, [47, 50, 55, 62], [62, 67, 71]),
                           cl(40, [47, 52, 55, 59], [64, 67, 71]), cl(38, [50, 53, 57, 62], [65, 69, 74]))
    verse = dict(bars=8, notes=[[0, 67, 1.5, .7], [2, 72, 1, .7], [4, 71, 2, .7], [8, 69, 1.5, .7], [10, 67, 1, .7], [12, 64, 2, .7], [16, 65, 1.5, .7], [18, 69, 1, .7], [20, 72, 2, .7], [24, 71, 1.5, .7], [26, 67, 1, .7], [28, 67, 3, .7]])
    chorus = dict(bars=8, notes=[[0, 72, 1, .95], [1, 76, 1, .9], [2, 79, 2, 1.0], [4, 76, 1, .85], [5, 74, 1, .85], [6, 72, 2, .9], [8, 74, 1, .95], [9, 77, 1, .9], [10, 81, 2, 1.0], [12, 79, 1, .85], [13, 77, 1, .85], [14, 74, 2, .9],
                                [16, 72, 1, .95], [17, 76, 1, .9], [18, 79, 2, 1.0], [20, 84, 2, .95], [22, 83, 2, .9], [24, 81, 1, .9], [25, 79, 1, .85], [26, 76, 2, .9], [28, 74, 1, .85], [29, 72, 3, .9]])
    bridge = dict(bars=8, notes=[[0, 76, 4, .75], [4, 74, 2, .7], [6, 72, 2, .7], [8, 77, 4, .75], [12, 76, 2, .7], [14, 74, 2, .7], [16, 79, 3, .8], [19, 76, 1, .7], [20, 74, 3, .75], [24, 71, 4, .8], [28, 74, 3, .8]])
    tag = dict(bars=4, notes=[[0, 72, 1, .8], [1, 76, 1, .75], [2, 79, 4, .75]])
    kit = lambda **k: dict(**k)
    R = dict(id="song-verse-chorus-bridge", form="Verse-chorus-bridge instrumental pop: Intro, V1, C1, V2, C2, Bridge, C3 (up a whole step), Outro (56 bars @100)",
        version=1, note="Instrumental: the 'vocal' role is a plucked lead. Original sound. Form after the Ableton Making Music forms chapter and open music theory texts (see research/song-structure.md).",
        bpm=100, seed=56, targetLufs=-14, peakCeilDb=-1.0, tailSec=5.0, xfadeSec=0.4, masterFade=dict(inSec=0.1, outSec=4.0), drumLevelDb=dict(kick=-5, snare=-9, clap=-12, hat=-20, ohat=-22, shaker=-24, rim=-20),
        targetLengthSec=[120, 150], skillIds=[S("sidechain-compressor"), S("one-bar-transition-riser"), S("reverse-reverb-swell"), S("noise-layer-whoosh"), S("synthesized-noise-impact"), S("emotional-cinematic")],
        chordLoops=dict(V=[C, Am, F, G], Ch=[F, C, G, Am], Br=[Am, Dm, Em, G], Out=[C, Am]),
        motifs=dict(verse=verse, chorus=chorus, bridge=bridge, tag=tag),
        layers=dict(
            bass=layer("chords", "bass-velocity-hybrid-bass", voice="root", levelDb=-1, tailSec=3.0, rhythm=[[0, 0.9, 0.95], [1.5, 0.4, 0.75], [2, 0.9, 0.9], [3.5, 0.4, 0.7]], skillIds=[S("sidechain-compressor"), S("keysol-venus-velocity-hybrid-bass")], role="bass: root pattern"),
            pad=layer("chords", "pad-wide-supersaw-chord-pad", voice="high", levelDb=-8, tailSec=4.0, seedOff=3, sidechainDb=3, skillIds=[S("sidechain-compressor")], role="chord pad"),
            keys=layer("chords", "pluck-organic-velocity-pluck", voice="full", levelDb=-8, tailSec=4.0, seedOff=5, rhythm=[[0, 0.9, 0.7], [1.5, 0.5, 0.55], [3, 0.9, 0.6]], skillIds=[S("emotional-cinematic")], role="chord comping"),
            counter=layer("chords", "swell-multi-envelope-morph-swell", voice="mid", levelDb=-10, tailSec=5.0, seedOff=7, skillIds=[S("emotional-cinematic")], role="counter-layer: slow swell pads (added on repeats = variation)"),
            lead=layer("melody", "pluck-organic-velocity-pluck", levelDb=-4, tailSec=4.0, seedOff=9, skillIds=[S("emotional-cinematic")], role="lead / vocal stand-in")),
        sections=[
            dict(name="Intro", bars=4, keyLabel="C: C Am F G (2 bars each)", chords="V", energy=2, layers=dict(pad=-2, keys=-3), drums=dict(hat="offbeat", rim="rim_sparse", levelDb=dict(hat=-24)), skillIds=[S("emotional-cinematic")],
                 transitions=[dict(type="snare_roll", bars=1, voice="snare", gapBeats=0)]),
            dict(name="Verse 1", bars=8, keyLabel="C Am F G", chords="V", energy=4, layers=dict(bass=-2, pad=-10, keys=-8, lead=-4), drums=dict(kick="kick_pop", snare="backbeat", hat="eighth_hat", levelDb=dict(kick=-7, snare=-12, hat=-24)),
                 melody=dict(layer="lead", motif="verse"), skillIds=[], transitions=[dict(type="snare_roll", bars=1, voice="snare"), dict(type="riser", bars=2, fHz=[300, 4000], gainDb=-18, tailSec=0, skillIds=[S("one-bar-transition-riser")])]),
            dict(name="Chorus 1", bars=8, keyLabel="C: F C G Am", chords="Ch", energy=7, layers=dict(bass=0, pad=-8, keys=-7, lead=-3), drums=dict(kick="four", snare="backbeat", hat="eighth_hat", shaker="shaker16", levelDb=dict(kick=-5)),
                 melody=dict(layer="lead", motif="chorus"), skillIds=[], transitions=[dict(type="impact", lengthSec=3, hz=[60, 34], noiseSec=2.0, gainDb=-20, skillIds=[S("synthesized-noise-impact")])]),
            dict(name="Verse 2", bars=8, keyLabel="C Am F G", chords="V", energy=5, layers=dict(bass=-1, pad=-9, keys=-8, counter=-14, lead=-4), drums=dict(kick="kick_pop", snare="backbeat", hat="eighth_hat", shaker="shaker16", levelDb=dict(kick=-6, snare=-11, hat=-23, shaker=-28)),
                 melody=dict(layer="lead", motif="verse", transpose=0, velScale=1.0), skillIds=[], transitions=[dict(type="snare_roll", bars=1, voice="snare"), dict(type="riser", bars=2, fHz=[300, 4500], gainDb=-17, tailSec=0, skillIds=[S("one-bar-transition-riser")])]),
            dict(name="Chorus 2", bars=8, keyLabel="C: F C G Am", chords="Ch", energy=8, layers=dict(bass=0, pad=-8, keys=-7, counter=-9, lead=-3), drums=dict(kick="four", snare="backbeat", hat="eighth_hat", ohat="offbeat", shaker="shaker16", levelDb=dict(kick=-4.5)),
                 melody=dict(layer="lead", motif="chorus"), skillIds=[], transitions=[dict(type="downlifter", sec=3.0, gainDb=-18, skillIds=[S("noise-layer-whoosh")])]),
            dict(name="Bridge", bars=8, keyLabel="C: Am Dm Em G (new chords, thinner)", chords="Br", energy=3, layers=dict(pad=-7, keys={"db": -12, "toDb": -8}, counter=-10, lead=-4), drums=dict(rim="rim_sparse", shaker="shaker16", levelDb=dict(shaker=-28)),
                 melody=dict(layer="lead", motif="bridge"), skillIds=[S("emotional-cinematic")],
                 transitions=[dict(type="riser", bars=2, fHz=[250, 5000], gainDb=-12, tailSec=0, skillIds=[S("one-bar-transition-riser")]), dict(type="reverse_swell", source="pad", trim=[0.3, 4.3], irSec=4.0, gainDbRel=-6, skillIds=[S("reverse-reverb-swell")]),
                              dict(type="snare_roll", bars=1, voice="snare", gapBeats=0.5), dict(type="gap", beats=0.5, floorDb=-50)]),
            dict(name="Chorus 3 (up a whole step)", bars=8, keyLabel="D: G D A Bm (C chorus +2 semitones)", chords="Ch", transpose=2, energy=10, layers=dict(bass=0, pad=-7, keys=-6, counter=-8, lead=-2), drums=dict(kick="four", snare="backbeat", hat="sixteenth_hat", ohat="offbeat", shaker="shaker16", levelDb=dict(kick=-4)),
                 melody=dict(layer="lead", motif="chorus", transpose=0, velScale=1.0), skillIds=[], transitions=[dict(type="downlifter", sec=3.0, gainDb=-16, skillIds=[S("noise-layer-whoosh")])]),
            dict(name="Outro", bars=4, keyLabel="D: tag over G D (loop A Bm)", chords="Ch", transpose=2, energy=3, layers=dict(pad={"db": -8, "toDb": -20}, keys={"db": -8, "toDb": -20}, lead=-5), drums=dict(kick="half", levelDb=dict(kick=-12), stopAtBeat=8),
                 melody=dict(layer="lead", motif="tag"), skillIds=[], transitions=[])],
        qualityGates=GATES(-18, -12))
    finish(R, "song-verse-chorus-bridge")

# =============================================================== 5. Game adaptive loop (boreal stems)
def r5():
    stems = "/workspace/share/boreal-stems"
    R = dict(id="song-game-adaptive-boreal", form="Game adaptive music: one key (A minor pentatonic) and tempo (90 BPM); vertical layers (night bed, day layer, tension layer) with state changes quantised to bars; demo = scripted play session",
        version=1, note="No new synthesis: the layers are the existing boreal stems (build_stems.py, 32-bar loops = 85.333 s). The demo timeline is a stand-in for what the game's state machine would do; the recipe's gameStates table is the real deliverable.",
        bpm=90, seed=90, targetLufs=-16, peakCeilDb=-1.0, tailSec=3.0, xfadeSec=2.667, masterFade=dict(inSec=1.0, outSec=3.0),
        targetLengthSec=[120, 140], skillIds=[S("hybrid-score-role-first")],
        stemFiles=dict(night="/workspace/share/boreal-stems/boreal-night.wav", day="/workspace/share/boreal-stems/boreal-day.wav", weather="/workspace/share/boreal-stems/boreal-weather.wav", tension="/workspace/share/boreal-stems/boreal-tension.wav"),
        gameStates=dict(
            calm_night=dict(layers=dict(night=0, day=None, weather=None, tension=None), switchOn="next bar", fadeBars=1),
            day_explore=dict(layers=dict(night=-12, day=0, weather=None, tension=None), switchOn="next bar", fadeBars=1),
            rain=dict(layers=dict(night=-10, day=-8, weather=-3, tension=None), switchOn="next bar", fadeBars=2),
            threat=dict(layers=dict(night=-8, day=-12, weather=None, tension=-1), switchOn="next bar", fadeBars=1, note="the game has no threat signal yet (see boreal INTEGRATION.md)"),
            hunt=dict(layers=dict(night=-10, day=-16, weather=None, tension=0), switchOn="next beat", fadeBars=0.5)),
        layers=dict(
            night=layer("file", None, path=stems + "/boreal-night.wav", levelDb=0, skillIds=chain_skills("drone-wavetable-artifact-drone"), role="night bed (shimmer-drone chain)"),
            day=layer("file", None, path=stems + "/boreal-day.wav", levelDb=0, skillIds=chain_skills("pad-wide-supersaw-chord-pad"), role="day layer (supersaw chord pad chain)"),
            weather=layer("file", None, path=stems + "/boreal-weather.wav", levelDb=0, skillIds=chain_skills("swell-multi-envelope-morph-swell"), role="weather swell"),
            tension=layer("file", None, path=stems + "/boreal-tension.wav", levelDb=0, skillIds=chain_skills("gated-fifth-swell-trance-gate"), role="tension layer (gated fifth swell)")),
        sections=[
            dict(name="Calm night", bars=8, keyLabel="A minor pentatonic", energy=2, layers=dict(night=-8), skillIds=[S("hybrid-score-role-first")], transitions=[]),
            dict(name="Day explore", bars=8, keyLabel="A minor pentatonic", energy=4, layers=dict(night=-16, day=-3), skillIds=[S("hybrid-score-role-first")], transitions=[]),
            dict(name="Rain", bars=8, keyLabel="A minor pentatonic", energy=3, layers=dict(night=-12, day=-10, weather=-4), skillIds=[S("hybrid-score-role-first")], transitions=[]),
            dict(name="Threat", bars=8, keyLabel="A minor pentatonic", energy=6, layers=dict(night=-8, day=-14, tension=-1), xfadeSec=2.667, skillIds=[S("hybrid-score-role-first")], transitions=[]),
            dict(name="Hunt", bars=8, keyLabel="A minor pentatonic", energy=9, layers=dict(night=-8, day=-18, tension=2), xfadeSec=1.33, skillIds=[S("hybrid-score-role-first")], transitions=[]),
            dict(name="Release", bars=8, keyLabel="A minor pentatonic", energy=3, layers=dict(night=-10, day=-12), xfadeSec=5.33, skillIds=[S("hybrid-score-role-first")], transitions=[])],
        qualityGates=GATES(-19, -13))
    finish(R, "song-game-adaptive-boreal")

# =============================================================== 6. Meditation / isochronic session arc (recipe only; renderer = isochronic/render_flow_state_v2.py)
def r6():
    R = dict(id="song-meditation-session-arc", form="Meditation / entrainment session arc: settle -> descend -> deep hold -> gentle rise -> integrate -> close (extends isochronic-flow-state-v2)",
        version=1, note="Recipe only. Rendered by isochronic/render_flow_state_v2.py once a v3 JSON carries this rate map (the engine in song/ does not synthesise the pulse). Band names are convention only; no health claims. The research found the evidence for entrainment is mixed (see research/song-structure.md).",
        delegate=dict(renderer="isochronic/render_flow_state_v2.py", extends="workflows/isochronic-flow-state-v2.json", carrierHz=432, binauralLevel=0.2),
        bpm=60, seed=61, targetLufs=-14, peakCeilDb=-1.0, tailSec=0, targetLengthSec=[480, 900],
        skillIds=[S("isochronic-tone-layer"), S("binaural-beat-meditation"), S("layered-binaural-plus-isochronic"), S("hybrid-score-role-first"), S("one-bar-transition-riser"), S("reverse-reverb-swell"), S("sub-drop-sine"), S("risset-rhythm")],
        layers=dict(
            drone=layer("chords", "drone-wavetable-artifact-drone", voice="root", skillIds=[S("hybrid-score-role-first")], role="drone bed (enters first)"),
            pad=layer("chords", "pad-wide-supersaw-chord-pad", voice="full", skillIds=[S("hybrid-score-role-first")], role="warm pad"),
            isoPulse=layer("delegate", skillIds=[S("isochronic-tone-layer"), S("layered-binaural-plus-isochronic")], role="isochronic pulse, rate automated (see pulseRateHz per section)"),
            binaural=layer("delegate", skillIds=[S("binaural-beat-meditation"), S("layered-binaural-plus-isochronic")], role="binaural layer: carrier L, carrier+beat R")),
        sections=[
            dict(name="Settle", bars=24, keyLabel="A minor drone", energy=2, pulseRateHz=[14, 12], layers=dict(drone=0, pad=None, isoPulse={"db": -30, "toDb": -17}, binaural=None), skillIds=[S("isochronic-tone-layer"), S("hybrid-score-role-first")], transitions=[dict(type="riser", bars=1, skillIds=[S("one-bar-transition-riser")])]),
            dict(name="Descend", bars=36, keyLabel="A minor", energy=3, pulseRateHz=[12, 8], layers=dict(drone=0, pad=-8, isoPulse=-17, binaural=-20), skillIds=[S("layered-binaural-plus-isochronic"), S("risset-rhythm")], transitions=[dict(type="reverse_swell", source="pad", skillIds=[S("reverse-reverb-swell")])]),
            dict(name="Deep hold", bars=48, keyLabel="A minor", energy=2, pulseRateHz=[8, 6], layers=dict(drone=0, pad=-12, isoPulse=-19, binaural=-18), skillIds=[S("binaural-beat-meditation"), S("layered-binaural-plus-isochronic")], transitions=[dict(type="riser", bars=2, skillIds=[S("one-bar-transition-riser")])]),
            dict(name="Gentle rise", bars=24, keyLabel="A minor", energy=4, pulseRateHz=[6, 10], layers=dict(drone=0, pad=-6, isoPulse=-17, binaural=-20), skillIds=[S("isochronic-tone-layer")], transitions=[]),
            dict(name="Integrate", bars=24, keyLabel="A minor", energy=3, pulseRateHz=[10, 10], layers=dict(drone=0, pad=-6, isoPulse=-18, binaural=-22), skillIds=[S("hybrid-score-role-first")], transitions=[]),
            dict(name="Close", bars=24, keyLabel="A minor", energy=1, pulseRateHz=[10, 8], layers=dict(drone={"db": 0, "toDb": -30}, pad={"db": -6, "toDb": -30}, isoPulse={"db": -18, "toDb": -40}, binaural=None), skillIds=[S("sub-drop-sine")],
                 transitions=[dict(type="sub_drop", lengthSec=9, hz=[72, 24], skillIds=[S("sub-drop-sine")])])],
        qualityGates=GATES(-18, -12))
    finish(R, "song-meditation-session-arc")

if __name__ == "__main__":
    for f in (r1, r2, r3, r4, r5, r6): f()
