"""Skill appliers: each library skill's procedure mapped to concrete renderer parameters.

Every knob carries (range/choices, cite). `cite` quotes the skill step (s<n>) or constraint (C) the range comes
from. Where a skill gives only a qualitative instruction, it is mapped through ENGINE CONVENTIONS (below) and the
cite says so explicitly ("conv"). Params a skill does not mention are left to module defaults or other skills.

ENGINE CONVENTIONS (qualitative words -> numbers, used consistently):
  detune knob 0..1 = outer unison voice at +/-(knob*50) cents. Vendor % values map 1:1 (e.g. "~3%" -> 0.03,
      Serum "0.16" -> 0.16). "light/low" = 0.03-0.10, "moderate/near mid/reduced from max" = 0.10-0.30.
  "slow attack" (pads) = 1.5-4 s; "long release" = 2.5-5 s (bounded so the 12 s sample can decay to silence).
  "subtle/slow LFO" = 0.03-0.3 Hz, cutoff depth 0.15-0.6 oct. "quiet/low level" layer = 0.02-0.10.
  "width ~50%" = 0.5; "100% stereo" = 1.0.  "moderate mix" (FX) = 0.15-0.35.
  reverb "long/space" rt60 capped at 8 s (sample-length limit; skill asks longer -> noted as a limitation).
"""
import numpy as np

class K:  # float range
    def __init__(self, lo, hi, cite): self.lo, self.hi, self.cite = lo, hi, cite
    def default(self): return round((self.lo + self.hi) / 2, 4)
    def sample(self, rng): return round(float(rng.uniform(self.lo, self.hi)), 4)
    def clamp(self, v): return float(min(self.hi, max(self.lo, v)))
    def spec(self): return {"range": [self.lo, self.hi], "cite": self.cite}

class KI(K):
    def default(self): return int(round((self.lo + self.hi) / 2))
    def sample(self, rng): return int(rng.integers(self.lo, self.hi + 1))
    def clamp(self, v): return int(min(self.hi, max(self.lo, round(v))))

class KC:
    def __init__(self, choices, cite): self.choices, self.cite = choices, cite
    def default(self): return self.choices[0]
    def sample(self, rng): return self.choices[int(rng.integers(len(self.choices)))]
    def clamp(self, v): return v if v in self.choices else self.choices[0]
    def spec(self): return {"choices": self.choices, "cite": self.cite}

REGISTRY = {}

def skill(sid, role, knobs):
    def deco(fn):
        REGISTRY[sid] = {"id": sid, "role": role, "knobs": knobs, "apply": fn}
        return fn
    return deco

MODE = {"mode": KC(["base", "layer"], "chain mode: base=init voice, layer=add as extra layer"),
        "layer_gain": K(0.3, 0.6, "chain layer gain")}

def init_patch(category):
    return {"category": category, "layers": [], "filters": [], "amp_env": {"a": 0.01, "d": 0.3, "s": 1.0, "r": 0.5, "curve": 1.0},
            "envs": {}, "lfos": {}, "ctracks": {}, "mods": [], "fx": [], "velocity": {}, "drift_c": 0.0,
            "master": {"target_lufs": {"bass": -14.5}.get(category, -15.5)}}

def place_voice(patch, layers, filters, amp_env, envs, lfos, mods, mode, gain=1.0, tag="v"):
    """mode 'base' = init the voice (replace layers/filters/envs/mods, keep FX); 'layer' = add as an extra layer group
    through its own filters, levels scaled by gain; the existing amp env is kept."""
    base = (mode == "base") or not patch["layers"]
    if base:
        patch["layers"], patch["filters"], patch["envs"], patch["lfos"], patch["mods"], patch["ctracks"] = [], [], {}, {}, [], {}
        if amp_env:
            patch["amp_env"] = amp_env
        gain = 1.0
    gmap = {}
    lo, fo = len(patch["layers"]), len(patch["filters"])
    uid = f"{tag}{lo}"
    rn = {name: (name if base else f"{name}_{uid}") for name in list(envs) + list(lfos)}
    G = lambda g: g if base else gmap.setdefault(g, f"{g}_{uid}")
    for ly in layers:
        ly = dict(ly)
        ly["group"] = G(ly.get("group", "A"))
        ly["level"] = ly.get("level", 1.0) * gain
        if ly.get("am") and ly["am"].get("depth_src") in rn:
            ly["am"] = dict(ly["am"], depth_src=rn[ly["am"]["depth_src"]])
        patch["layers"].append(ly)
    for f in filters:
        f = dict(f)
        f["groups"] = [G(g) for g in f.get("groups", ["A"])]
        if f.get("env"):
            f["env"] = rn.get(f["env"], f["env"])
        patch["filters"].append(f)
    for name, e in envs.items():
        patch["envs"][rn[name]] = e
    for name, l in lfos.items():
        patch["lfos"][rn[name]] = l
    for m in mods:
        m = dict(m)
        m["src"] = rn.get(m["src"], m["src"])
        d = m["dst"]
        if ":" in d:
            kind, idx = d.split(":")
            if kind in ("pan", "level", "pitch", "wt_pos"):
                d = f"{kind}:{int(idx) + lo}"
            elif kind in ("cutoff", "vowel"):
                d = f"{kind}:{int(idx) + fo}"
        m["dst"] = d
        patch["mods"].append(m)
    return lo, fo

def rack_set(patch, fx, before=(), after=(), new_instance=False):
    """Insert/update an FX module. Same type already in rack -> update in place (a later skill refines the same rack
    slot) unless new_instance. `before`/`after`: the skill's own FX-order constraints."""
    for i, f in enumerate(patch["fx"]):
        if f["type"] == fx["type"] and not new_instance:
            patch["fx"][i] = {**f, **fx}
            return
    pos = len(patch["fx"])
    for i, f in enumerate(patch["fx"]):
        if f["type"] in before:
            pos = i
            break
    for i, f in enumerate(patch["fx"]):
        if f["type"] in after and i >= pos:
            pos = i + 1
    patch["fx"].insert(pos, fx)

SPACE = ("delay", "reverb", "shimmer")

def first_filter(patch):
    for i, f in enumerate(patch["filters"]):
        if f["type"] in ("ladder", "diode", "svf_lp"):
            return i, f
    return None, None

def groups_of(patch, tonal_only=False):
    return sorted({ly.get("group", "A") for ly in patch["layers"] if not (tonal_only and ly["osc"] == "noise")}) or ["A"]

# ================================================================== VOICE SKILLS (part A)
@skill("unison-odd-even-detune-width-clean-supersaw", "voice", {
    "voices": KC([7, 9, 11, 6, 8, 10, 12], "s8: unison ~6-12; s4/C1: odd keeps a centered voice; even = ultra-wide"),
    "detune": K(0.10, 0.30, "s6/s8/C3: modest (~0.16 demo), near mid, conservative for chords"),
    "blend": K(0.4, 0.6, "s8: blend near mid"),
    "width": K(0.45, 0.55, "s13/C3: global unison width ~50% for chord phase correlation"),
    "oscb": KC([True, False], "s9: optional Osc B"), "oscb_oct": KC([1, -1], "s9: pitch +/-octaves"),
    "oscb_level": K(0.3, 0.5, "s9: lower level, fewer voices"),
    "sub_level": K(0.2, 0.4, "s10: optional centered saw sub one octave down (no unison)"),
    "noise_level": K(0.02, 0.06, "s10 + conv: quiet noise"),
    "eq_hp": K(80, 150, "s11: EQ cut lows (freq conv)"), "eq_hi_shelf_db": K(1.0, 3.0, "s11: EQ lift highs (amount conv)"),
    "comp_ratio": K(2.0, 4.0, "s11: compression (ratio conv)"),
    "attack": K(0.8, 2.0, "conv: pad attack (skill gives none)"), "release": K(2.0, 3.5, "conv: pad release"), **MODE})
def supersaw(patch, k):
    lay = [{"osc": "saw", "unison": k["voices"], "detune": k["detune"], "blend": k["blend"], "width": k["width"], "level": 1.0}]
    if k["oscb"]:
        lay.append({"osc": "saw", "oct": k["oscb_oct"], "unison": 3, "detune": k["detune"] * 0.7, "width": k["width"], "level": k["oscb_level"]})
    lay.append({"osc": "saw", "oct": -1, "unison": 1, "level": k["sub_level"]})
    lay.append({"osc": "noise", "noise_color": "white", "width": 0.5, "level": k["noise_level"]})
    place_voice(patch, lay, [], {"a": k["attack"], "d": 0.5, "s": 1.0, "r": k["release"], "curve": 1.0}, {}, {}, [], k["mode"], k["layer_gain"])
    rack_set(patch, {"type": "eq", "bands": [{"kind": "hp", "f": k["eq_hp"]}, {"kind": "highshelf", "f": 6000, "gain": k["eq_hi_shelf_db"]}]}, before=SPACE + ("comp", "chorus"))
    rack_set(patch, {"type": "comp", "ratio": k["comp_ratio"], "thresh_rel_db": 2.0}, before=SPACE)
    rack_set(patch, {"type": "delay", "mode": "pingpong", "sync_l": "1/4", "feedback": 0.45, "mix": 0.2, "hp_hz": 100, "lp_hz": 3000}, before=("reverb", "shimmer"))
    rack_set(patch, {"type": "reverb", "rt60": 2.5, "size": 1.2, "send": 0.25, "return_hp": 200})

@skill("warm-heavenly-supersaw-pad-keytrack-fx", "voice", {
    "voices": KI(5, 7, "s1: saw unison ~5-7"), "detune": K(0.10, 0.25, "s1: reduce detune from max (conv moderate)"),
    "attack": K(1.5, 3.0, "s1: slow attack (conv)"), "release": K(2.5, 4.0, "s1: long release (conv)"),
    "cutoff": K(600, 1500, "s3: 24 dB LP, cutoff for warm lows (Hz conv)"), "keytrack": K(0.5, 1.0, "s3/C1: key track until high notes audible"),
    "filter_model": KC(["ladder", "diode"], "s3: compare analog/ladder/diode"),
    "lfo_rate": K(0.08, 0.3, "s5: subtle slow irregular LFO"), "lfo_amt": K(0.15, 0.5, "s5: subtle -> cutoff"),
    "chorus_mix": K(0.35, 0.5, "s4: rich chorus"), "rev_rt60": K(2.5, 3.5, "s4: reverb ~3s"), "rev_hp": K(150, 300, "s4: reverb low cut"),
    "rev_send": K(0.2, 0.35, "conv moderate"), "dly_fb": K(0.3, 0.45, "s4: controlled feedback"), "dly_mix": K(0.12, 0.2, "conv moderate"),
    "pwm_layer": KC([False, True], "s6: optional PWM layer, less unison"), "serial_hp": KC([True, False], "s6: serial HP after LP if subs build"),
    "sine_reinforce": KC([False, True], "s6: optional unfiltered sine reinforce"), **MODE})
def warm_heavenly(patch, k):
    lay = [{"osc": "saw", "unison": k["voices"], "detune": k["detune"], "width": 0.8, "level": 1.0}]
    if k["pwm_layer"]:
        lay.append({"osc": "pulse", "pw": 0.35, "unison": 3, "detune": k["detune"] * 0.5, "width": 0.6, "level": 0.5})
    filt = [{"type": k["filter_model"], "mode": "lp24", "cutoff": k["cutoff"], "res": 0.0, "keytrack": k["keytrack"]}]
    if k["serial_hp"]:
        filt.append({"type": "svf_hp", "cutoff": 90, "res": 0.0, "keytrack": 0.0})
    if k["sine_reinforce"]:
        lay.append({"osc": "sine", "level": 0.3, "group": "S"})
    lfos = {"lfo_irr": {"shape": "random", "rate_hz": k["lfo_rate"]}}
    mods = [{"src": "lfo_irr", "dst": "cutoff:0", "amt": k["lfo_amt"]}]
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 1.0, "s": 1.0, "r": k["release"], "curve": 1.0}, {}, lfos, mods, k["mode"], k["layer_gain"])
    rack_set(patch, {"type": "chorus", "mode": "ensemble", "rate": 0.35, "depth_ms": 3.5, "mix": k["chorus_mix"], "wet_hp_hz": 200}, before=SPACE)
    rack_set(patch, {"type": "delay", "mode": "pingpong", "sync_l": "1/8d", "feedback": k["dly_fb"], "mix": k["dly_mix"], "hp_hz": 120, "lp_hz": 4000}, before=("reverb", "shimmer"))
    rack_set(patch, {"type": "reverb", "rt60": k["rev_rt60"], "size": 1.1, "send": k["rev_send"], "return_hp": k["rev_hp"]})
    rack_set(patch, {"type": "eq", "bands": [{"kind": "hp", "f": 50}]}, after=("reverb",), new_instance=True)

@skill("evolving-pad-unison-filter-swell-fifth", "voice", {
    "amp_attack": K(0.05, 0.4, "s1: amp can be quicker"), "release": K(2.0, 3.5, "conv"),
    "env2_attack": K(2.0, 5.0, "s1: env2 slow attack -> cutoff"), "cutoff": K(250, 700, "s1: tone arrives then opens (low base conv)"),
    "env_amt": K(2.0, 4.0, "s1: env2 depth (oct conv)"), "res": K(0.0, 0.2, "s1: low resonance"),
    "voices": KI(5, 9, "s2: unison"), "width": K(0.7, 1.0, "s2: noticeable stereo spread"), "detune": K(0.12, 0.3, "conv moderate"),
    "lfo_amt": K(0.0, 0.5, "s2: optional slow LFO->cutoff"), "fifth_voices": KI(3, 5, "s3: similar/less unison"),
    "fifth_level": K(0.5, 0.8, "s3: fifth (+7) into same filter"), "third_voice": KC([False, True], "s3: optional higher voice with LFO->level"),
    "comp_ratio": K(2.0, 3.0, "s4: glue compression"), "rev_rt60": K(3.0, 5.0, "s4: large size/decay reverb"), "rev_send": K(0.25, 0.4, "s4: rising mix"),
    "chorus": KC([False, True], "s4: optional chorus"), **MODE})
def evolving_fifth(patch, k):
    lay = [{"osc": "saw", "unison": k["voices"], "detune": k["detune"], "width": k["width"], "level": 1.0},
           {"osc": "saw", "semi": 7, "unison": k["fifth_voices"], "detune": k["detune"] * 0.8, "width": k["width"] * 0.8, "level": k["fifth_level"]}]
    lfos = {"lfo_cut": {"shape": "sine", "rate_hz": 0.08}}
    mods = [{"src": "lfo_cut", "dst": "cutoff:0", "amt": k["lfo_amt"]}]
    if k["third_voice"]:
        lay.append({"osc": "saw", "oct": 1, "unison": 3, "detune": k["detune"] * 0.6, "width": k["width"], "level": 0.3})
        lfos["lfo_lvl"] = {"shape": "sine", "rate_hz": 0.1}
        mods.append({"src": "lfo_lvl", "dst": "level:2", "amt": 0.8})
    filt = [{"type": "ladder", "mode": "lp24", "cutoff": k["cutoff"], "res": k["res"], "keytrack": 0.5, "env": "env2", "env_amt_oct": k["env_amt"]}]
    envs = {"env2": {"a": k["env2_attack"], "d": 2.0, "s": 0.8, "r": k["release"], "curve": 1.0}}
    place_voice(patch, lay, filt, {"a": k["amp_attack"], "d": 0.5, "s": 1.0, "r": k["release"], "curve": 1.0}, envs, lfos, mods, k["mode"], k["layer_gain"])
    rack_set(patch, {"type": "comp", "ratio": k["comp_ratio"], "thresh_rel_db": 2.0}, before=SPACE)
    if k["chorus"]:
        rack_set(patch, {"type": "chorus", "mode": "classic", "mix": 0.3, "wet_hp_hz": 200}, before=SPACE)
    rack_set(patch, {"type": "reverb", "rt60": k["rev_rt60"], "size": 1.4, "send": k["rev_send"], "return_hp": 150})

@skill("cinematic-warm-analog-pad-drift-stereo", "voice", {
    "drift_c": K(2.0, 8.0, "s1: slow chaos -> master tune, gentle drift (cents conv)"),
    "attack": K(0.6, 1.5, "s2: soften amp attack"), "release": K(1.5, 3.0, "s2: soften release"),
    "detune": K(0.08, 0.2, "conv moderate"), "b_level": K(0.6, 0.85, "s3: Osc B +1 oct triangle, slightly under A"),
    "lfo_rate": K(0.03, 0.1, "s5: very slow free LFO"), "pan_amt": K(0.3, 0.6, "s5: opposite pan depths"),
    "noise_level": K(0.0, 0.08, "s6: optional quiet noise air"), "cutoff": K(1500, 4000, "s7: 12 dB LP tames A+noise highs (Hz conv)"),
    "filter_pan": K(0.1, 0.5, "s7: LFO filter pan/offset (oct conv)"), "rev_rt60": K(3.0, 5.0, "s8: spacious reverb"),
    "rev_send": K(0.25, 0.4, "conv"), "post_from": K(800, 1500, "s8: post-reverb filter slowly opens"), "post_to": K(6000, 12000, "s8/C2: open, not fully"), **MODE})
def warm_analog(patch, k):
    lay = [{"osc": "saw", "unison": 5, "detune": k["detune"], "width": 0.5, "level": 1.0, "group": "A"},
           {"osc": "triangle", "oct": 1, "unison": 5, "detune": k["detune"], "width": 0.5, "level": k["b_level"], "group": "B"}]
    if k["noise_level"] > 0.005:
        lay.append({"osc": "noise", "level": k["noise_level"], "width": 0.6, "group": "A"})
    lfos = {"lfo_pan": {"shape": "sine", "rate_hz": k["lfo_rate"]}, "lfo_fpan": {"shape": "sine", "rate_hz": k["lfo_rate"] * 1.3, "stereo_phase": np.pi}}
    mods = [{"src": "lfo_pan", "dst": "pan:0", "amt": k["pan_amt"]}, {"src": "lfo_pan", "dst": "pan:1", "amt": -k["pan_amt"]},
            {"src": "lfo_fpan", "dst": "cutoff:0", "amt": k["filter_pan"]}]
    filt = [{"type": "ladder", "mode": "lp12", "cutoff": k["cutoff"], "res": 0.1, "keytrack": 0.3, "groups": ["A"]}]
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 0.5, "s": 1.0, "r": k["release"], "curve": 1.0}, {}, lfos, mods, k["mode"], k["layer_gain"])
    patch["drift_c"] = max(patch.get("drift_c", 0), k["drift_c"])
    rack_set(patch, {"type": "reverb", "rt60": k["rev_rt60"], "size": 1.3, "send": k["rev_send"], "return_hp": 150,
                     "post_filter_open": {"from_hz": k["post_from"], "to_hz": k["post_to"], "time_s": 6.0}})

@skill("lush-stereo-saw-pad-random-pitch-texture", "voice", {
    "pan": K(0.6, 1.0, "s1: saws panned opposite"), "fine_c": K(4.0, 6.0, "s1: fine-tune ~+/-5 cents"),
    "detune": K(0.02, 0.05, "s2: ~4 voices @ ~3% (conv 1:1)"), "drive": K(0.3, 0.6, "s3: dirty 12 dB filter drive"),
    "res": K(0.15, 0.4, "s3: resonance"), "cutoff": K(500, 1200, "conv base cutoff"),
    "a1": K(0.3, 1.0, "s3: env1 mid attack"), "s1": K(0.6, 0.85, "s3: mid sustain"), "r1": K(2.0, 3.5, "s3: longer release"),
    "d2": K(2.0, 4.0, "s4: env2 long decay"), "s2": K(0.2, 0.45, "s4: sustain <50%"), "env2_amt": K(1.5, 3.0, "s4: env2 -> cutoff (oct conv)"),
    "rand_amt": K(0.2, 0.6, "s4: stereo random (1 bar) -> cutoff"), "osc3_level": K(0.12, 0.3, "s5: osc3 texture +12 st"),
    "detune_drift": K(2.0, 6.0, "s6: slow stereo random -> global voice detune (cents conv)"),
    "noise_level": K(0.02, 0.06, "s7: noise sample bed (pink noise stand-in)"), "rev_send": K(0.35, 0.5, "s7: reverb ~50% mix"),
    "dly_mix": K(0.15, 0.25, "s7: ping-pong 1/4 (mix per delay skill)"), **MODE})
def lush_stereo(patch, k):
    lay = [{"osc": "saw", "unison": 4, "detune": k["detune"], "width": 0.4, "pan": -k["pan"], "fine_c": -k["fine_c"], "level": 1.0},
           {"osc": "saw", "unison": 4, "detune": k["detune"], "width": 0.4, "pan": k["pan"], "fine_c": k["fine_c"], "level": 1.0},
           {"osc": "sine", "oct": 1, "level": k["osc3_level"], "group": "T"},
           {"osc": "noise", "level": k["noise_level"], "width": 0.7, "group": "T"}]
    rng = np.random.default_rng(int(k["fine_c"] * 1000))   # scale-snapped random transpose (deterministic per chain)
    deg = [0, 3, 7, 10, 12]
    steps = [100.0 * deg[int(i)] for i in rng.integers(0, len(deg), 8)]
    filt = [{"type": "ladder", "mode": "lp12", "cutoff": k["cutoff"], "res": k["res"], "drive": k["drive"], "keytrack": 0.4,
             "env": "env2", "env_amt_oct": k["env2_amt"]},
            {"type": "svf_lp", "cutoff": 3000, "res": 0.1, "groups": ["T"]}]
    envs = {"env2": {"a": 0.05, "d": k["d2"], "s": k["s2"], "r": k["r1"], "curve": 1.0}}
    lfos = {"rnd_cut": {"shape": "random", "sync": "1bar", "stereo_phase": 1.7}, "rnd_pan3": {"shape": "random", "rate_hz": 1 / 5.2},
            "rnd_det": {"shape": "random", "rate_hz": 0.15}}
    mods = [{"src": "rnd_cut", "dst": "cutoff:0", "amt": k["rand_amt"]}, {"src": "rnd_pan3", "dst": "pan:2", "amt": 0.7},
            {"src": "rnd_det", "dst": "detune", "amt": k["detune_drift"]}, {"src": "ct_osc3", "dst": "pitch:2", "amt": 1.0}]
    place_voice(patch, lay, filt, {"a": k["a1"], "d": 1.5, "s": k["s1"], "r": k["r1"], "curve": 1.0}, envs, lfos, mods, k["mode"], k["layer_gain"])
    patch["ctracks"]["ct_osc3"] = {"steps": steps, "sync": "1bar", "direction": "fwd"}
    rack_set(patch, {"type": "delay", "mode": "pingpong", "sync_l": "1/4", "feedback": 0.45, "mix": k["dly_mix"], "hp_hz": 100, "lp_hz": 3000}, before=("reverb", "shimmer"))
    rack_set(patch, {"type": "reverb", "rt60": 3.0, "size": 1.2, "send": k["rev_send"], "return_hp": 200})

@skill("granular-dual-saw-ambient-epic-pad", "voice", {
    "sub_level": K(0.2, 0.25, "s1: second saw -1 oct at ~20-25%"), "attack": K(3.5, 4.5, "s2: amp attack ~4s"), "release": K(4.0, 5.0, "s2: release ~4-5s"),
    "filter_model": KC(["ladder", "diode"], "s3: ladder/diode"), "cutoff": K(300, 600, "s3: low cutoff (Hz conv)"),
    "env2_attack": K(2.0, 3.0, "s3: env2 attack ~2-3s"), "env2_sus": K(0.2, 0.4, "s3: low sustain"), "env_amt": K(2.0, 3.5, "s3: -> cutoff slow open (oct conv)"),
    "mud_cut_hz": K(120, 150, "s4: gentle cut ~120-150 Hz"), "mud_cut_db": K(2.0, 4.0, "s4: gentle (conv)"),
    "chorus_mix": K(0.5, 0.7, "s5: chorus 3 taps high mix"), "chorus_rate": K(0.2, 0.5, "s5: slow rate"),
    "rev_send": K(0.35, 0.40, "s5: large reverb ~35-40% mix"), "rev_rt60": K(3.0, 4.5, "s5: large (conv)"),
    "grain_level": K(0.08, 0.2, "s6: granular layer blended under saws"), "grain_jitter_c": K(10, 40, "s6: small pitch variation"), **MODE})
def granular_dual(patch, k):
    lay = [{"osc": "saw", "level": 1.0, "unison": 1}, {"osc": "saw", "oct": -1, "level": k["sub_level"]},
           {"osc": "sine", "oct": 1, "level": k["grain_level"], "unison": 3, "detune": 0.05, "width": 0.9}]   # C1: particle-layer approximation
    lfos = {"grain_j": {"shape": "random", "rate_hz": 3.0, "stereo_phase": 2.0}}
    mods = [{"src": "grain_j", "dst": "pitch:2", "amt": k["grain_jitter_c"]}, {"src": "grain_j", "dst": "pan:2", "amt": 0.8}]
    filt = [{"type": k["filter_model"], "mode": "lp24", "cutoff": k["cutoff"], "res": 0.15, "keytrack": 0.3, "env": "env2", "env_amt_oct": k["env_amt"]}]
    envs = {"env2": {"a": k["env2_attack"], "d": 5.0, "s": k["env2_sus"], "r": k["release"], "curve": 2.0}}
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 0.5, "s": 1.0, "r": k["release"], "curve": 1.0}, envs, lfos, mods, k["mode"], k["layer_gain"])
    rack_set(patch, {"type": "eq", "bands": [{"kind": "hp", "f": 60}, {"kind": "peak", "f": k["mud_cut_hz"], "q": 1.0, "gain": -k["mud_cut_db"]}]}, before=SPACE + ("chorus",))
    rack_set(patch, {"type": "chorus", "mode": "ensemble", "rate": k["chorus_rate"], "depth_ms": 3.0, "mix": k["chorus_mix"], "wet_hp_hz": 150}, before=SPACE)
    rack_set(patch, {"type": "delay", "mode": "pingpong", "sync_l": "1/4", "feedback": 0.4, "mix": 0.18}, before=("reverb", "shimmer"))
    rack_set(patch, {"type": "reverb", "rt60": k["rev_rt60"], "size": 1.4, "send": k["rev_send"], "return_hp": 200})

# ================================================================== VOICE SKILLS (part B)
@skill("digital-wt-morph-bandpass-chorus-echo-space", "voice", {
    "wt_pos": K(0.4, 0.6, "s1: set mid position"), "env2_attack": K(3.0, 5.0, "s1: long attack env2 -> WT position"), "wt_amt": K(0.25, 0.45, "s1: env2 depth (conv)"),
    "attack": K(2.5, 3.0, "s2: attack ~2.8s"), "release": K(3.5, 5.0, "s2: release ~5s+ (bounded by sample length)"),
    "detune": K(0.015, 0.02, "s3: ~1.5-2% detune (conv 1:1)"), "sine_level": K(0.4, 0.7, "s4: sine engine blended under"),
    "lp_cut": K(250, 500, "s5: LP24 cutoff low hundreds"), "lp_res": K(0.1, 0.25, "s5: light resonance"), "lp_env": K(2.0, 3.5, "s5: env2 opens LP (oct conv)"),
    "hp_env": K(0.5, 1.5, "s5: env2 moves HP (oct conv)"), "chorus_depth": K(2.0, 4.0, "s7: depth a few ms"),
    "echo_mix": K(0.3, 0.5, "s7: echo ~50% wet on aux"), "rev_rt60": K(4.0, 6.0, "s7: long reverb"), "rev_predelay": K(0.04, 0.1, "s7: long predelay"),
    "rev_send": K(0.3, 0.45, "s7: 100% wet aux, send level conv"), **MODE})
def digital_wt(patch, k):
    lay = [{"osc": "wt", "wt_table": "digital_additive", "wt_pos": k["wt_pos"], "unison": 3, "detune": k["detune"], "width": 1.0, "level": 1.0},
           {"osc": "sine", "unison": 3, "detune": 0.01, "width": 1.0, "level": k["sine_level"]}]
    envs = {"env2": {"a": k["env2_attack"], "d": 4.0, "s": 0.8, "r": k["release"], "curve": 1.0}}
    filt = [{"type": "ladder", "mode": "lp24", "cutoff": k["lp_cut"], "res": k["lp_res"], "keytrack": 0.4, "env": "env2", "env_amt_oct": k["lp_env"]},
            {"type": "svf_hp", "cutoff": 50, "res": 0.0, "env": "env2", "env_amt_oct": k["hp_env"]}]
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 0.5, "s": 1.0, "r": k["release"], "curve": 1.0}, envs, {},
                [{"src": "env2", "dst": "wt_pos:0", "amt": k["wt_amt"]}], k["mode"], k["layer_gain"])
    patch["velocity"]["to_amp"] = 0.2
    rack_set(patch, {"type": "chorus", "mode": "classic", "rate": 0.25, "depth_ms": k["chorus_depth"], "offset": np.pi, "mix": 0.4, "wet_hp_hz": 150}, before=SPACE)
    rack_set(patch, {"type": "delay", "mode": "pingpong", "sync_l": "1/4", "feedback": 0.35, "mix": k["echo_mix"], "hp_hz": 150, "lp_hz": 4000, "sat": 0.2}, before=("reverb", "shimmer"))
    rack_set(patch, {"type": "reverb", "rt60": k["rev_rt60"], "size": 1.5, "predelay_s": k["rev_predelay"], "send": k["rev_send"], "return_hp": 200, "return_lp": 9000, "damp_hz": 5000})

@skill("ambient-organic-pluck-pad-ladder-chorus-space", "voice", {
    "decay": K(0.6, 1.2, "s1: raised decay"), "sustain": K(0.3, 0.5, "s1: mid sustain (not zero)"), "release": K(0.4, 1.0, "s1: some release"),
    "warp": K(0.15, 0.4, "s2: sine warped toward saw-sine hybrid (WT position conv)"),
    "cutoff": K(400, 900, "s3: ladder base (Hz conv)"), "env_amt": K(1.8, 2.0, "s3: env2 -> cutoff ~+24 semitones"), "res": K(0.05, 0.15, "s3: low resonance"),
    "env2_decay": K(0.25, 0.6, "s3: pluck contour (conv)"),
    "dist_drive": K(0.3, 0.5, "s4: moderate drive"), "dist_mix": K(0.15, 0.3, "s4: reduced mix"),
    "noise_level": K(0.02, 0.06, "s5: low pink noise -> BP"), "drift_c": K(2.0, 5.0, "s6: slow pitch drift"),
    "vel_amp": K(0.3, 0.5, "s7: velocity -> level"), "vel_cut": K(1.0, 2.0, "s7: velocity -> cutoff (oct conv)"),
    "chorus_fb": K(0.5, 0.7, "s8/C2: high feedback for long decay, metallic risk"), "chorus_depth": K(4.0, 7.0, "s8: raise depth/delay"),
    "chorus_hp": K(200, 400, "s8: high-pass"), "rev_send": K(0.25, 0.35, "s8: ~30% mix"), "rev_hp": K(150, 250, "s8: low cut"),
    "dly_mix": K(0.25, 0.35, "s8: dotted-quarter delay ~30%"), **MODE})
def organic_pluck(patch, k):
    lay = [{"osc": "wt", "wt_table": "soft_to_complex", "wt_pos": k["warp"], "level": 1.0, "unison": 1},
           {"osc": "noise", "noise_color": "pink", "level": k["noise_level"], "width": 0.5, "group": "N"}]
    envs = {"env2": {"a": 0.002, "d": k["env2_decay"], "s": 0.0, "r": 0.3, "curve": 1.0}}
    filt = [{"type": "ladder", "mode": "lp24", "cutoff": k["cutoff"], "res": k["res"], "drive": 0.0, "keytrack": 1.0, "env": "env2", "env_amt_oct": k["env_amt"]},
            {"type": "svf_bp", "cutoff": 1200, "res": 0.1, "keytrack": 1.0, "groups": ["N"]}]
    place_voice(patch, lay, filt, {"a": 0.004, "d": k["decay"], "s": k["sustain"], "r": k["release"], "curve": 1.0}, envs, {}, [], k["mode"], k["layer_gain"])
    patch["drift_c"] = max(patch.get("drift_c", 0), k["drift_c"])
    patch["velocity"].update({"to_amp": k["vel_amp"], "to_cutoff_oct": k["vel_cut"]})
    rack_set(patch, {"type": "dist", "drive": k["dist_drive"], "mix": k["dist_mix"], "post_lp": 9000}, before=SPACE + ("chorus",))
    rack_set(patch, {"type": "chorus", "mode": "classic", "rate": 0.3, "depth_ms": k["chorus_depth"], "base_ms": 12, "feedback": k["chorus_fb"], "mix": 0.4, "wet_hp_hz": k["chorus_hp"]}, before=SPACE)
    rack_set(patch, {"type": "reverb", "rt60": 3.0, "size": 1.2, "send": k["rev_send"], "return_hp": k["rev_hp"]})
    rack_set(patch, {"type": "delay", "mode": "pingpong", "sync_l": "1/4d", "feedback": 0.35, "mix": k["dly_mix"]}, before=("reverb",))

@skill("traveler-walkthrough-super-unison-wide-lead", "voice", {
    "wave_pos": K(0.0, 0.25, "s1: continuous waveform saw->sine->thin pulse (near saw)"), "voices": KI(5, 7, "s2: stack up to ~7"),
    "detune": K(0.2, 0.4, "s2: increase detune until gigantic"), "width": K(0.8, 1.0, "s2: stereo spread"),
    "drive": K(0.1, 0.3, "s4: mild drive into filter"), "cutoff": K(3000, 7000, "s5: cutoff high enough to keep width"),
    "slope": KC(["lp12", "lp24"], "s5: 12-24 dB ladder"), "res": K(0.1, 0.25, "s5: modest resonance"),
    "attack": K(0.3, 1.0, "s6: medium attack for pads"), "sustain": K(0.7, 0.9, "s6: sustain mid-high"), "release": K(0.5, 2.0, "s6: release 0.5-2s"), **MODE})
def super_unison(patch, k):
    lay = [{"osc": "wt", "wt_table": "saw_tri_square_sine", "wt_pos": k["wave_pos"], "unison": k["voices"], "detune": k["detune"], "width": k["width"], "level": 1.0}]
    filt = [{"type": "ladder", "mode": k["slope"], "cutoff": k["cutoff"], "res": k["res"], "drive": k["drive"], "keytrack": 0.3}]
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 1.0, "s": k["sustain"], "r": k["release"], "curve": 1.0}, {}, {}, [], k["mode"], k["layer_gain"])

@skill("traveler-walkthrough-wavetable-morph-filter-motion", "voice", {
    "table": KC(["soft_to_complex", "digital_additive"], "s1: original/free WT"), "wt_pos": K(0.2, 0.5, "conv"),
    "detune": K(0.05, 0.15, "s2: 2-voice stack detune"), "width": K(0.5, 0.8, "s2: stereo spread"),
    "wt_lfo_amt": K(0.1, 0.25, "s4: subtle WT-position depth"), "wt_lfo_rate": K(0.05, 0.2, "s4: slow (conv)"),
    "slope": KC(["lp12", "lp24", "lp6"], "s5: ladder 6-24 dB"), "cutoff": K(800, 2500, "conv"), "hp": K(60, 180, "s5: HP linkable"),
    "cut_lfo_amt": K(0.2, 0.6, "s5: LFO -> cutoff"), "noise_level": K(0.0, 0.04, "s6: noise sparingly"), "drive": K(0.05, 0.2, "s6: light drive"),
    "attack": K(1.0, 3.0, "conv pad"), "release": K(2.0, 4.0, "conv pad"), **MODE})
def wt_morph_motion(patch, k):
    lay = [{"osc": "wt", "wt_table": k["table"], "wt_pos": k["wt_pos"], "unison": 2, "detune": k["detune"], "width": k["width"], "level": 1.0}]
    if k["noise_level"] > 0.005:
        lay.append({"osc": "noise", "level": k["noise_level"], "width": 0.5})
    lfos = {"lfo_wt": {"shape": "sine", "rate_hz": k["wt_lfo_rate"]}, "lfo_cut": {"shape": "tri", "rate_hz": k["wt_lfo_rate"] * 0.7, "stereo_phase": 0.8}}
    mods = [{"src": "lfo_wt", "dst": "wt_pos:0", "amt": k["wt_lfo_amt"]}, {"src": "lfo_cut", "dst": "cutoff:0", "amt": k["cut_lfo_amt"]}]
    filt = [{"type": "ladder", "mode": k["slope"], "cutoff": k["cutoff"], "res": 0.15, "drive": k["drive"], "keytrack": 0.4},
            {"type": "svf_hp", "cutoff": k["hp"], "res": 0.0}]
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 1.0, "s": 1.0, "r": k["release"], "curve": 1.0}, {}, lfos, mods, k["mode"], k["layer_gain"])

@skill("wavetable-crossfade-morph-modulate-pad", "voice", {
    "smooth": KC([1, 0], "s1: smooth crossfade vs hard switch"), "wt_pos": K(0.2, 0.6, "conv"),
    "lfo_amt": K(0.2, 0.45, "s2: depth musical for pads"), "lfo_rate": K(0.04, 0.15, "s2: slowly morphing (conv)"),
    "cutoff": K(1000, 3000, "s5: ladder/LP + envelopes (Hz conv)"), "attack": K(1.0, 3.0, "conv pad"), "release": K(2.0, 4.0, "conv pad"),
    "voices": KI(1, 3, "conv"), **MODE})
def wt_crossfade(patch, k):
    lay = [{"osc": "wt", "wt_table": "saw_tri_square_sine", "wt_smooth": k["smooth"], "wt_pos": k["wt_pos"], "unison": k["voices"], "detune": 0.08, "width": 0.6, "level": 1.0}]
    filt = [{"type": "ladder", "mode": "lp24", "cutoff": k["cutoff"], "res": 0.1, "keytrack": 0.5}]
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 1.0, "s": 1.0, "r": k["release"], "curve": 1.0}, {}, {"lfo_wt": {"shape": "sine", "rate_hz": k["lfo_rate"]}},
                [{"src": "lfo_wt", "dst": "wt_pos:0", "amt": k["lfo_amt"]}], k["mode"], k["layer_gain"])
    rack_set(patch, {"type": "eq", "bands": [{"kind": "hp", "f": 80}]}, before=SPACE + ("chorus",))
    rack_set(patch, {"type": "chorus", "mode": "classic", "mix": 0.3, "wet_hp_hz": 200}, before=SPACE)
    rack_set(patch, {"type": "delay", "mode": "pingpong", "sync_l": "1/4", "feedback": 0.42, "mix": 0.18}, before=("reverb", "shimmer"))
    rack_set(patch, {"type": "reverb", "rt60": 3.0, "size": 1.2, "send": 0.3, "return_hp": 200})

@skill("cinematic-multi-envelope-osc-level-morph", "voice", {
    "release": K(4.0, 5.0, "s1: amp release ~5s"), "a1": K(0.1, 0.6, "s3: staggered attacks"), "a2": K(1.2, 2.5, "s3: staggered attacks"), "a3": K(2.5, 4.5, "s3: staggered attacks"),
    "oct3": KC([1, -1], "s4: octave-shift layers"), "pan_amt": K(0.2, 0.5, "s4: pan layers"),
    "res": K(0.0, 0.15, "s5: reduce resonance"), "noise_level": K(0.03, 0.1, "s6: noise wash own envelope"),
    "wt_sync": KC(["1bar", "2bar"], "s7: synced LFO -> WT position"), "rev_rt60": K(5.0, 8.0, "s8: long ambient reverb (capped 8s)"),
    "rev_send": K(0.25, 0.4, "conv"), **MODE})
def multi_env(patch, k):
    lay = [{"osc": "saw", "unison": 3, "detune": 0.1, "width": 0.5, "pan": -k["pan_amt"], "level": 0.9, "level_env": {"a": k["a1"], "d": 1.0, "s": 0.7, "r": k["release"], "curve": 1.0}, "group": "A"},
           {"osc": "wt", "wt_table": "soft_to_complex", "wt_pos": 0.3, "unison": 2, "detune": 0.06, "width": 0.6, "pan": k["pan_amt"], "level": 0.8,
            "level_env": {"a": k["a2"], "d": 1.0, "s": 0.9, "r": k["release"], "curve": 1.5}, "group": "B"},
           {"osc": "triangle", "oct": k["oct3"], "level": 0.6, "level_env": {"a": k["a3"], "d": 1.0, "s": 1.0, "r": k["release"], "curve": 2.0}, "group": "B"},
           {"osc": "noise", "level": k["noise_level"], "width": 0.8, "level_env": {"a": 0.4, "d": 1.5, "s": 0.0, "r": 1.0, "curve": 1.0}, "group": "N"}]
    filt = [{"type": "ladder", "mode": "lp24", "cutoff": 1200, "res": k["res"], "keytrack": 0.4, "env": "fenv", "env_amt_oct": 1.5, "groups": ["A"]},
            {"type": "svf_lp", "cutoff": 2500, "res": k["res"], "keytrack": 0.3, "groups": ["B"]},
            {"type": "svf_bp", "cutoff": 1500, "res": 0.1, "groups": ["N"]}]
    envs = {"fenv": {"a": 0.2, "d": 2.5, "s": 0.2, "r": 2.0, "curve": 1.0}}
    place_voice(patch, lay, filt, {"a": 0.05, "d": 0.5, "s": 1.0, "r": k["release"], "curve": 1.0}, envs, {"lfo_wt": {"shape": "sine", "sync": k["wt_sync"]}},
                [{"src": "lfo_wt", "dst": "wt_pos:1", "amt": 0.3}], k["mode"], k["layer_gain"])
    rack_set(patch, {"type": "reverb", "rt60": k["rev_rt60"], "size": 1.6, "send": k["rev_send"], "return_hp": 200})

@skill("audio-rate-am-wave-shape-texture", "voice", {
    "carrier": KC(["triangle", "sine", "saw"], "s2/goal: soft carrier sine/triangle/saw"), "am_mode": KC(["self", "dual"], "s2 self-AM vs s4 second osc"),
    "ratio": KC([1.5, 2.0, 3.0, 0.5], "s4: second osc at a different frequency"), "depth": K(0.3, 0.8, "s3/s5: depth under envelope; modest for pads"),
    "depth_src": KC(["amp_env", "lfo"], "s3 env vs s5 LFO for continuous motion"), "lfo_rate": K(0.05, 0.3, "s5: LFO motion (conv slow)"),
    "cutoff": K(1500, 5000, "s5: gentle filter if needed"), "attack": K(1.0, 3.0, "conv pad/texture"), "release": K(2.0, 4.0, "conv"),
    "voices": KI(1, 3, "conv"), **MODE})
def am_texture(patch, k):
    am = {"shape": "pulse" if k["am_mode"] == "self" else "sine", "ratio": 1.0 if k["am_mode"] == "self" else k["ratio"], "depth": k["depth"]}
    lfos = {}
    if k["depth_src"] == "amp_env":
        am["depth_src"] = "amp_env"
    else:
        lfos["lfo_am"] = {"shape": "sine", "rate_hz": k["lfo_rate"], "unipolar": True}
        am["depth_src"] = "lfo_am"
    lay = [{"osc": k["carrier"], "am": am, "unison": k["voices"], "detune": 0.06, "width": 0.6, "level": 1.0}]
    filt = [{"type": "svf_lp", "cutoff": k["cutoff"], "res": 0.1, "keytrack": 0.3}]
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 1.0, "s": 1.0, "r": k["release"], "curve": 1.0}, {}, lfos, [], k["mode"], k["layer_gain"])

@skill("fm-carrier-modulator-ratio-basics", "voice", {
    "ratio": KC([1.0, 2.0], "s5: simple ratios 1:1, 2:1"), "index": K(0.5, 3.0, "s2-s3: depth = modulator amplitude"),
    "slow_mod_amt": K(0.1, 0.5, "s4: slower operator modulates depth"), "slow_mod_rate": K(0.05, 0.4, "s4: slow (conv)"),
    "attack": K(0.003, 1.5, "conv role-dependent"), "decay": K(0.3, 1.5, "conv"), "sustain": K(0.3, 1.0, "conv"), "release": K(0.5, 3.0, "conv"),
    "voices": KI(1, 3, "conv"), **MODE})
def fm_basic(patch, k):
    lay = [{"osc": "fm", "fm_ratio": k["ratio"], "fm_index": k["index"], "unison": k["voices"], "detune": 0.05, "width": 0.5, "level": 1.0}]
    place_voice(patch, lay, [], {"a": k["attack"], "d": k["decay"], "s": k["sustain"], "r": k["release"], "curve": 1.0}, {},
                {"lfo_fm": {"shape": "sine", "rate_hz": k["slow_mod_rate"]}}, [{"src": "lfo_fm", "dst": "fm_index", "amt": k["slow_mod_amt"]}], k["mode"], k["layer_gain"])

# ================================================================== VOICE SKILLS (part C: bass/impact/hybrid)
@skill("hybrid-noise-distortion-separate-sub-layer", "voice", {
    "noise_level": K(0.35, 0.55, "s1: noise ~50%"), "noise_drive": K(0.4, 0.6, "s2: asymmetric distortion ~50%"),
    "noise_cut": K(2000, 5000, "s2: filter noise path mid-high"), "noise_hp": K(200, 450, "s3: HP into low-mid region"),
    "sub_wave": KC(["pulse", "wt"], "s4: square favoured, or WT"), "sub_oct": KC([0, -1], "s4: low tones"),
    "attack": K(0.003, 0.05, "conv bass"), "decay": K(0.3, 1.0, "conv"), "sustain": K(0.5, 0.8, "conv"), "release": K(0.3, 1.0, "conv"),
    "sub_cut": K(300, 900, "conv"), "for_pads": KC([False, True], "s5/C1: for pads lower distortion, lengthen amps"), **MODE})
def hybrid_noise_sub(patch, k):
    nd = k["noise_drive"] * (0.5 if k["for_pads"] else 1.0)
    sub = {"osc": "pulse", "pw": 0.5} if k["sub_wave"] == "pulse" else {"osc": "wt", "wt_table": "saw_tri_square_sine", "wt_pos": 0.66}
    lay = [dict(sub, oct=k["sub_oct"], level=1.0, group="S"), {"osc": "noise", "noise_color": "white", "level": k["noise_level"], "width": 0.2, "group": "N"}]
    filt = [{"type": "ladder", "mode": "lp24", "cutoff": k["sub_cut"], "res": 0.1, "keytrack": 0.5, "groups": ["S"]},
            {"type": "diode", "mode": "lp12", "cutoff": k["noise_cut"], "res": 0.1, "drive": nd, "groups": ["N"]},
            {"type": "svf_hp", "cutoff": k["noise_hp"], "res": 0.0, "groups": ["N"]}]
    env = {"a": k["attack"], "d": k["decay"], "s": k["sustain"], "r": k["release"], "curve": 1.0}
    if k["for_pads"]:
        env = {"a": 1.0, "d": 1.0, "s": 1.0, "r": 2.5, "curve": 1.0}
    place_voice(patch, lay, filt, env, {}, {}, [], k["mode"], k["layer_gain"])
    rack_set(patch, {"type": "eq", "bands": [{"kind": "highshelf", "f": 8000, "gain": -2.5}]}, before=SPACE + ("chorus",))

@skill("keysol-venus-velocity-hybrid-bass-impact", "voice", {
    "osc": KC(["saw", "pulse"], "s1: dark saw/pulse"), "wt_spice": K(0.0, 0.3, "s1: optional WT"),
    "decay": K(0.3, 0.8, "s1: punchy decay"), "sustain": K(0.4, 0.65, "s1: moderate sustain"), "release": K(0.3, 0.8, "conv"),
    "cutoff": K(150, 350, "s1: dark (Hz conv)"), "vel_cut": K(2.0, 3.5, "s2: strong velocity -> cutoff"), "env_amt": K(1.0, 2.5, "s1/s2: transient bloom"),
    "sub_level": K(0.3, 0.5, "s4: optionally underscore with sub"), "bass_mode": KC(["deep", "atmos"], "s3 atmospheric vs s4 deep"), **MODE})
def velocity_bass(patch, k):
    lay = [{"osc": k["osc"], "pw": 0.4, "unison": 1, "level": 1.0}, {"osc": "sine", "oct": -1 if k["bass_mode"] == "deep" else 0, "level": k["sub_level"], "group": "S"}]
    if k["wt_spice"] > 0.02:
        lay.append({"osc": "wt", "wt_table": "digital_additive", "wt_pos": 0.5, "level": k["wt_spice"]})
    envs = {"fenv": {"a": 0.002, "d": k["decay"], "s": 0.2, "r": k["release"], "curve": 1.0}}
    filt = [{"type": "ladder", "mode": "lp24", "cutoff": k["cutoff"], "res": 0.2, "drive": 0.2, "keytrack": 0.5, "env": "fenv", "env_amt_oct": k["env_amt"]}]
    place_voice(patch, lay, filt, {"a": 0.003, "d": k["decay"], "s": k["sustain"], "r": k["release"], "curve": 1.0}, envs, {}, [], k["mode"], k["layer_gain"])
    patch["velocity"]["to_cutoff_oct"] = k["vel_cut"]
    if k["bass_mode"] == "atmos":
        rack_set(patch, {"type": "eq", "bands": [{"kind": "hp", "f": 250}]}, before=SPACE)
        rack_set(patch, {"type": "reverb", "rt60": 5.0, "size": 1.6, "send": 0.4, "return_hp": 200})

@skill("keysol-helpling-keytrack-bass-split-delay", "voice", {
    "low_osc": KC(["sine", "triangle", "saw"], "s1: dedicated low oscillator"), "top_osc": KC(["saw", "triangle", "wt"], "s1: mid/high tonal osc"),
    "kt_full": KI(36, 48, "s2: strong in low register"), "kt_zero": KI(55, 67, "s2: fades as you play higher"),
    "dly_mix": K(0.5, 0.9, "s3: delay wet very high"), "dly_fb": K(0.35, 0.55, "s3: filter delay feedback to taste"),
    "attack": K(0.3, 1.5, "conv"), "release": K(1.0, 3.0, "conv"), **MODE})
def keytrack_split(patch, k):
    top = {"osc": k["top_osc"], "level": 0.8, "unison": 3, "detune": 0.08, "width": 0.6}
    if k["top_osc"] == "wt":
        top.update(wt_table="soft_to_complex", wt_pos=0.4)
    lay = [top, {"osc": k["low_osc"], "oct": -1, "level": 0.8, "keytrack_low": {"full_below": k["kt_full"], "zero_above": k["kt_zero"]}, "group": "L"}]
    filt = [{"type": "ladder", "mode": "lp24", "cutoff": 1800, "res": 0.1, "keytrack": 0.5}]
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 1.0, "s": 0.9, "r": k["release"], "curve": 1.0}, {}, {}, [], k["mode"], k["layer_gain"])
    rack_set(patch, {"type": "delay", "mode": "dual", "sync_l": "1/4", "sync_r": "1/8d", "fb_l": k["dly_fb"], "fb_r": k["dly_fb"] * 0.8, "mix": k["dly_mix"], "hp_hz": 150, "lp_hz": 3500}, before=("reverb", "shimmer"))

@skill("keysol-venus-fifths-pulsar-wt-impact", "voice", {
    "core": KC(["pulse", "saw"], "s1: pulse/saw core"), "fifth_level": K(0.4, 0.8, "s1: Osc2 +7 balance"),
    "detune": K(0.08, 0.25, "s2: duo detune"), "width": K(0.5, 0.9, "s2: scatter/spread"),
    "wt_level": K(0.15, 0.35, "s3: WT as spice, not replacement"), "wt_lfo": K(0.1, 0.3, "s3: animate WT position"),
    "attack": K(0.003, 1.0, "conv"), "release": K(0.5, 3.0, "conv"), "cutoff": K(1200, 4000, "conv"), **MODE})
def fifths_pulsar(patch, k):
    lay = [{"osc": k["core"], "pw": 0.4, "unison": 2, "detune": k["detune"], "width": k["width"], "level": 1.0},
           {"osc": k["core"], "pw": 0.4, "semi": 7, "unison": 2, "detune": k["detune"], "width": k["width"], "level": k["fifth_level"]},
           {"osc": "wt", "wt_table": "digital_additive", "wt_pos": 0.4, "level": k["wt_level"]}]
    filt = [{"type": "ladder", "mode": "lp24", "cutoff": k["cutoff"], "res": 0.15, "keytrack": 0.4}]
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 1.0, "s": 0.8, "r": k["release"], "curve": 1.0}, {}, {"lfo_wt": {"shape": "tri", "rate_hz": 0.12}},
                [{"src": "lfo_wt", "dst": "wt_pos:2", "amt": k["wt_lfo"]}], k["mode"], k["layer_gain"])

@skill("cinematic-formant-comb-pad-phaser-fx", "voice", {
    "voices_a": KI(3, 7, "s1: unison/detune for width"), "voices_b": KI(8, 12, "s2: higher unison (~14, capped 12)"), "detune": K(0.1, 0.25, "s1-s2 (conv)"),
    "formant_res": K(0.2, 0.5, "s3: formant cutoff/resonance on C"), "comb_fb": K(0.2, 0.5, "s4: comb-minus resonance"), "comb_mix": K(0.2, 0.4, "s4"),
    "attack": K(1.0, 2.5, "s5: raise attack"), "release": K(2.0, 4.0, "s5: raise release"), "lfo_rate": K(0.05, 0.15, "s6: free slow LFO -> cutoff"),
    "phaser_mix": K(0.15, 0.3, "s7: phaser lower mix"), "chorus_mix": K(0.15, 0.3, "s7: chorus mix down"), "rev_send": K(0.2, 0.35, "s7: moderate"), **MODE})
def formant_comb(patch, k):
    lay = [{"osc": "saw", "unison": k["voices_a"], "detune": k["detune"], "width": 0.7, "level": 0.8, "group": "AB"},
           {"osc": "saw", "oct": -1, "unison": k["voices_b"], "detune": k["detune"], "width": 0.5, "level": 0.6, "group": "AB"},
           {"osc": "pulse", "pw": 0.4, "unison": 2, "detune": 0.08, "width": 0.5, "level": 0.5, "group": "C"}]
    filt = [{"type": "formant", "vowel_a": "A", "vowel_b": "O", "res": k["formant_res"], "mix": 0.8, "groups": ["C"]},
            {"type": "ladder", "mode": "lp24", "cutoff": 1500, "res": 0.1, "keytrack": 0.3, "groups": ["AB", "C"]},
            {"type": "comb", "keytrack": 1.0, "minus": True, "res": k["comb_fb"], "mix": k["comb_mix"], "groups": ["AB", "C"]}]
    lfos = {"lfo_cut": {"shape": "sine", "rate_hz": k["lfo_rate"], "stereo_phase": 0.5}, "lfo_v": {"shape": "sine", "rate_hz": k["lfo_rate"] * 0.5}}
    mods = [{"src": "lfo_cut", "dst": "cutoff:1", "amt": 0.5}, {"src": "lfo_v", "dst": "vowel:0", "amt": 0.8}]
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 1.0, "s": 1.0, "r": k["release"], "curve": 1.0}, {}, lfos, mods, k["mode"], k["layer_gain"])
    rack_set(patch, {"type": "phaser", "rate": 0.12, "mix": k["phaser_mix"]}, before=SPACE + ("chorus",))
    rack_set(patch, {"type": "chorus", "mode": "classic", "mix": k["chorus_mix"], "wet_hp_hz": 200}, before=SPACE)
    rack_set(patch, {"type": "delay", "mode": "pingpong", "sync_l": "1/4", "feedback": 0.4, "mix": 0.15}, before=("reverb",))
    rack_set(patch, {"type": "reverb", "rt60": 3.5, "size": 1.3, "send": k["rev_send"], "return_hp": 200})

@skill("ambient-wavetable-scratch-spectral-morph-pad", "voice", {
    "wt_lfo_amt": K(0.5, 0.9, "s2: synced LFO 4 bars -> WT position, high depth"), "detune2": K(0.03, 0.04, "s3: octave-stack low detune ~3-4%"),
    "attack": K(3.5, 4.5, "s4: ~4s attack"), "release": K(4.0, 6.0, "s4: ~6s release (bounded)"), "curve": K(1.0, 2.0, "s4: optional curve bend"),
    "lp_cut": K(800, 2500, "s5: osc1 LP 12 dB (Hz conv)"), "hp_cut": K(150, 500, "s5: osc2 HP"), "stereo_split": K(0.1, 0.4, "s5: random stereo-split"),
    "dly_mix": K(0.15, 0.3, "s7: dotted delay with feedback"), "rev_rt60": K(6.0, 8.0, "s7: ~10-11s requested, capped 8s"), "rev_send": K(0.2, 0.35, "conv"),
    "pan_rand": K(0.2, 0.5, "s7: bipolar random -> pan"), **MODE})
def ambient_wt_scratch(patch, k):
    lay = [{"osc": "wt", "wt_table": "soft_to_complex", "wt_pos": 0.1, "unison": 1, "level": 1.0, "group": "A"},
           {"osc": "wt", "wt_table": "digital_additive", "wt_pos": 0.5, "unison": 3, "detune": k["detune2"], "width": 0.8, "level": 0.6, "group": "B"},
           {"osc": "wt", "wt_table": "digital_additive", "oct": 1, "wt_pos": 0.5, "unison": 2, "detune": k["detune2"], "width": 0.8, "level": 0.3, "group": "B"}]
    lfos = {"lfo_wt4": {"shape": "tri", "sync": "4bar", "unipolar": True}, "rnd_pan": {"shape": "random", "rate_hz": 0.2, "stereo_phase": 2.0}}
    mods = [{"src": "lfo_wt4", "dst": "wt_pos:0", "amt": k["wt_lfo_amt"]}, {"src": "rnd_pan", "dst": "pan:0", "amt": k["pan_rand"]},
            {"src": "rnd_pan", "dst": "pan:1", "amt": -k["pan_rand"]}]
    envs = {"fenv": {"a": 3.0, "d": 3.0, "s": 0.7, "r": k["release"], "curve": 1.0}}
    filt = [{"type": "svf_lp", "cutoff": k["lp_cut"], "res": 0.1, "env": "fenv", "env_amt_oct": 1.0, "stereo_off_oct": k["stereo_split"], "groups": ["A"]},
            {"type": "svf_hp", "cutoff": k["hp_cut"], "res": 0.0, "env": "fenv", "env_amt_oct": 0.5, "stereo_off_oct": k["stereo_split"], "groups": ["B"]}]
    place_voice(patch, lay, filt, {"a": k["attack"], "d": 1.0, "s": 1.0, "r": k["release"], "curve": k["curve"]}, envs, lfos, mods, k["mode"], k["layer_gain"])
    rack_set(patch, {"type": "comp", "ratio": 2.0, "thresh_rel_db": 3.0}, before=SPACE)
    rack_set(patch, {"type": "delay", "mode": "pingpong", "sync_l": "1/4d", "feedback": 0.45, "mix": k["dly_mix"]}, before=("reverb", "shimmer"))
    rack_set(patch, {"type": "reverb", "rt60": k["rev_rt60"], "size": 1.8, "send": k["rev_send"], "return_hp": 200})

# ================================================================== LAYER / FILTER / MOD MODIFIERS
@skill("keysol-venus-high-wt-artifact-pulse-layer", "layer", {
    "oct": KC([2, 3], "s2: tuned very high until artifact-like"), "level": K(0.04, 0.12, "s4: mix low under the bed"),
    "wt_lfo_amt": K(0.15, 0.4, "s3: slow WT-position modulation"), "wt_lfo_rate": K(0.03, 0.15, "s3: slow")})
def high_artifact(patch, k):
    li = len(patch["layers"])
    patch["layers"].append({"osc": "wt", "wt_table": "artifact_high", "oct": k["oct"], "wt_pos": 0.3, "level": k["level"], "group": "HA"})
    patch["lfos"]["lfo_art"] = {"shape": "sine", "rate_hz": k["wt_lfo_rate"]}
    patch["mods"].append({"src": "lfo_art", "dst": f"wt_pos:{li}", "amt": k["wt_lfo_amt"]})
    patch["filters"].append({"type": "svf_lp", "cutoff": 9000, "res": 0.0, "groups": ["HA"]})

@skill("keysol-venus-polyrhythmic-control-track-pitch", "layer", {
    "bed_oct": KC([-1, -2], "s1: bed an octave or two below"), "high_level": K(0.08, 0.2, "s5: high oscs blended underneath"),
    "depth_c": K(15, 60, "s3: small depth so pitch breaks subtly (cents conv)"), "high_oct": KC([1, 2], "s2: much higher registers")})
def poly_ctrack(patch, k):
    li = len(patch["layers"])
    patch["layers"] += [{"osc": "pulse", "pw": 0.45, "oct": k["bed_oct"], "level": 0.7, "group": "BED"},
                        {"osc": "triangle", "oct": k["high_oct"], "level": k["high_level"], "pan": -0.4, "group": "HI"},
                        {"osc": "sine", "oct": k["high_oct"], "semi": 7, "level": k["high_level"], "pan": 0.4, "group": "HI"}]
    rng = np.random.default_rng(int(k["depth_c"] * 100))
    patch["ctracks"]["ctA_poly"] = {"steps": [float(x) for x in rng.uniform(-1, 1, 15).round(3)], "sync": "1/4d"}   # s3: length 15, dotted quarter
    patch["ctracks"]["ctB_poly"] = {"steps": [float(x) for x in rng.uniform(-1, 1, 14).round(3)], "sync": "1/4"}    # s3: length 14, quarter
    patch["mods"] += [{"src": "ctA_poly", "dst": f"pitch:{li+1}", "amt": k["depth_c"]}, {"src": "ctB_poly", "dst": f"pitch:{li+2}", "amt": k["depth_c"]}]
    patch["filters"] += [{"type": "ladder", "mode": "lp24", "cutoff": 500, "res": 0.1, "keytrack": 0.3, "groups": ["BED"]},
                         {"type": "svf_lp", "cutoff": 5000, "res": 0.0, "groups": ["HI"]}]
    rack_set(patch, {"type": "delay", "mode": "pingpong", "sync_l": "1/4d", "feedback": 0.4, "mix": 0.15}, before=("reverb", "shimmer"))

@skill("osc-as-granular-pitch-step-delay", "layer", {
    "sync": KC(["1/4", "1/8"], "s3/s6: tempo-synced LFO sets delay time; faster eighths optional"),
    "pitch_steps": KC([[0, 1200, 2400], [0, 1200], [0, 700, 1200, 1900, 2400]], "s5: +24 st over steps, each repeat rises"),
    "echo_level": K(0.3, 0.6, "s3: echo-shaped level LFO"), "fade_in_s": K(0.15, 0.5, "s4: fade-in ramp so repeats don't pile on dry attack")})
def granular_step_delay(patch, k):
    if not patch["layers"]:
        return
    src = dict(patch["layers"][0])
    li = len(patch["layers"])
    src.update(level=k["echo_level"] * src.get("level", 1.0), unison=1,
               level_env={"a": k["fade_in_s"], "d": 0.5, "s": 1.0, "r": patch["amp_env"]["r"], "curve": 1.0})
    patch["layers"].append(src)
    sub = "1/16" if k["sync"] == "1/8" else "1/8"
    # echo-shaped taps: level = 1 + (step) -> 0 between taps, decaying taps (s3)
    patch["ctracks"]["ct_echo"] = {"steps": [-1.0, 0.0, -1.0, -0.3, -1.0, -0.5, -1.0, -0.65], "sync": sub}
    patch["ctracks"]["ct_echopitch"] = {"steps": [float(x) for x in k["pitch_steps"]], "sync": k["sync"]}
    patch["mods"] += [{"src": "ct_echo", "dst": f"level:{li}", "amt": 1.0}, {"src": "ct_echopitch", "dst": f"pitch:{li}", "amt": 1.0}]

@skill("filter-ladder-diode-comb-formant-flavors", "filter", {
    "design": KC(["ladder", "diode", "comb", "formant"], "s2-s5: ladder/diode/comb/formant designs"),
    "drive": K(0.0, 0.4, "s2: raise drive then resonance"), "res": K(0.05, 0.35, "s2/s3: resonance (retune for diode)"),
    "comb_mix": K(0.2, 0.45, "s5: comb remix"), "comb_fb": K(0.3, 0.6, "s5: comb resonance +/-"),
    "vowel_pair": KC([["A", "O"], ["E", "I"], ["O", "U"]], "s4: vowel sets"), "vowel_lfo": K(0.05, 0.2, "s4: XY vowel morph (rate conv)")})
def filter_flavor(patch, k):
    i, f = first_filter(patch)
    if k["design"] in ("ladder", "diode"):
        if f is not None:
            f["type"] = k["design"]
            f["drive"] = k["drive"]
            f.setdefault("mode", "lp24")
            if f["mode"] not in ("lp24", "lp12", "lp6"):
                f["mode"] = "lp24"
            f["res"] = k["res"] * (0.8 if k["design"] == "diode" else 1.0)
        else:
            patch["filters"].append({"type": k["design"], "mode": "lp24", "cutoff": 2000, "res": k["res"], "drive": k["drive"], "keytrack": 0.4, "groups": groups_of(patch, True)})
    elif k["design"] == "comb":
        patch["filters"].append({"type": "comb", "keytrack": 1.0, "res": k["comb_fb"], "mix": k["comb_mix"], "groups": groups_of(patch, True)})
    else:
        fi = len(patch["filters"])
        patch["filters"].append({"type": "formant", "vowel_a": k["vowel_pair"][0], "vowel_b": k["vowel_pair"][1], "res": k["res"], "mix": 0.5, "groups": groups_of(patch, True)})
        patch["lfos"]["lfo_vowel"] = {"shape": "sine", "rate_hz": k["vowel_lfo"], "stereo_phase": 1.0}
        patch["mods"].append({"src": "lfo_vowel", "dst": f"vowel:{fi}", "amt": 1.0})

@skill("traveler-walkthrough-stereo-ladder-lf-width", "filter", {
    "slope": KC(["lp24", "lp12", "lp6"], "s1: ladder 6-24 dB"), "stereo_off": K(0.1, 0.4, "s2: L/R cutoff offset, subtle"),
    "hp": K(40, 120, "s3: dedicated HP (conv)"), "pan_spread": K(0.2, 0.6, "s4: pan-spread fans successive voices"),
    "lf_width_hz": K(180, 280, "s5: mono below ~middle C (262 Hz)")})
def stereo_ladder(patch, k):
    i, f = first_filter(patch)
    if f is not None and f["type"] in ("ladder", "diode"):
        f["mode"] = k["slope"]; f["stereo_off_oct"] = k["stereo_off"]
    else:
        patch["filters"].append({"type": "ladder", "mode": k["slope"], "cutoff": 3000, "res": 0.1, "keytrack": 0.4, "stereo_off_oct": k["stereo_off"], "groups": groups_of(patch)})
    patch["filters"].append({"type": "svf_hp", "cutoff": k["hp"], "res": 0.0, "groups": groups_of(patch)})
    patch["note_spread"] = k["pan_spread"]
    patch["lf_width_hz"] = k["lf_width_hz"]

@skill("velocity-filter-cutoff-envelope-amount", "filter", {
    "floor": K(300, 900, "s2: darkest tone with EG amount 0"), "eg_amt": K(1.5, 3.5, "s3: EG amount to bright ceiling (oct conv)"),
    "vel_amt": K(1.0, 2.5, "s4-s5: velocity -> cutoff so soft hits darker")})
def velocity_filter(patch, k):
    i, f = first_filter(patch)
    if f is None:
        patch["filters"].insert(0, {"type": "ladder", "mode": "lp24", "cutoff": k["floor"], "res": 0.0, "keytrack": 0.0, "groups": groups_of(patch, True)})
        f = patch["filters"][0]
        for m in patch["mods"]:
            if m["dst"].startswith(("cutoff:", "vowel:")):
                kind, idx = m["dst"].split(":"); m["dst"] = f"{kind}:{int(idx)+1}"
    f.update(cutoff=k["floor"], res=0.0, env="venv", env_amt_oct=k["eg_amt"])
    patch["envs"]["venv"] = {"a": 0.005, "d": 0.4, "s": 1.0, "r": patch["amp_env"]["r"], "curve": 1.0}
    patch["velocity"]["to_cutoff_oct"] = k["vel_amt"]

@skill("modulation-lfo-envelope-mod-matrix-routing", "mod", {
    "dests": KC([["cutoff"], ["cutoff", "pan"], ["cutoff", "wt_pos"], ["cutoff", "pan", "level"]], "s2/s11: stack routes to several destinations"),
    "lfo_rate": K(0.05, 0.3, "s2: slow free rate for subtle drift"), "cut_amt": K(0.2, 0.6, "s2: LFO -> cutoff wobble (oct conv subtle)"),
    "pan_amt": K(0.1, 0.35, "s11: -> pan"), "lvl_amt": K(0.1, 0.25, "s11: -> volume"), "shape": KC(["sine", "tri", "random"], "s1: shape")})
def mod_matrix(patch, k):
    patch["lfos"]["mm_lfo"] = {"shape": k["shape"], "rate_hz": k["lfo_rate"], "stereo_phase": 0.6}
    patch["lfos"]["mm_lfo2"] = {"shape": "sine", "rate_hz": round(k["lfo_rate"] * 0.61, 4)}
    i, f = first_filter(patch)
    if "cutoff" in k["dests"] and i is not None:
        patch["mods"].append({"src": "mm_lfo", "dst": f"cutoff:{i}", "amt": k["cut_amt"]})
    if "pan" in k["dests"]:
        for li, ly in enumerate(patch["layers"]):
            if ly.get("oct", 0) >= 0 and ly["osc"] != "noise":
                patch["mods"].append({"src": "mm_lfo2", "dst": f"pan:{li}", "amt": k["pan_amt"] * (1 if li % 2 == 0 else -1)})
    if "wt_pos" in k["dests"]:
        patch["mods"].append({"src": "mm_lfo2", "dst": "wt_pos", "amt": 0.2})
    if "level" in k["dests"] and len(patch["layers"]) > 1:
        patch["mods"].append({"src": "mm_lfo2", "dst": "level:1", "amt": k["lvl_amt"]})

@skill("traveler-walkthrough-curved-envelope-evolving-pad", "mod", {
    "attack": K(2.5, 5.0, "s2: long stages (up to ~20s; bounded by 6 s note)"), "curve": K(1.5, 2.5, "s1: curve handles (convex)"),
    "release": K(3.0, 5.0, "s2: long (bounded)"), "fenv_amt": K(0.8, 2.0, "s3: filter env -> stereo LPF moderate"),
    "fenv_attack": K(3.0, 6.0, "s2/s3: long bloom"), "menv_dest": KC(["wt_pos", "pan", "cutoff2"], "s3: mod env -> WT pos/pan/second cutoff"),
    "vib_c": K(2.0, 8.0, "s5: pitch vibrato (cents conv)"), "chorus_mix": K(0.15, 0.25, "s6: light chorus"),
    "rev_rt60": K(4.0, 7.0, "s6: long space/hall"), "rev_send": K(0.2, 0.35, "conv")})
def curved_env(patch, k):
    patch["amp_env"] = {"a": k["attack"], "d": 1.5, "s": 1.0, "r": k["release"], "curve": k["curve"]}
    patch["envs"]["cfenv"] = {"a": k["fenv_attack"], "d": 2.0, "s": 0.85, "r": k["release"], "curve": k["curve"]}
    patch["envs"]["cmenv"] = {"a": k["fenv_attack"] * 0.8, "d": 3.0, "s": 0.6, "r": k["release"], "curve": 1.0}
    i, f = first_filter(patch)
    if f is not None:
        f["env"] = "cfenv"; f["env_amt_oct"] = k["fenv_amt"]; f["stereo_off_oct"] = f.get("stereo_off_oct", 0.15)
    if k["menv_dest"] == "wt_pos":
        patch["mods"].append({"src": "cmenv", "dst": "wt_pos", "amt": 0.3})
    elif k["menv_dest"] == "pan" and patch["layers"]:
        patch["mods"].append({"src": "cmenv", "dst": "pan:0", "amt": 0.3})
    else:
        for j, ff in enumerate(patch["filters"]):
            if j != i and ff["type"] in ("svf_lp", "ladder", "diode"):
                patch["mods"].append({"src": "cmenv", "dst": f"cutoff:{j}", "amt": 1.0})
                break
    patch["lfos"]["vib"] = {"shape": "sine", "rate_hz": 4.5}
    patch["mods"].append({"src": "vib", "dst": "pitch", "amt": k["vib_c"]})
    rack_set(patch, {"type": "eq", "bands": [{"kind": "peak", "f": 300, "q": 0.7, "gain": -1.5}]}, before=SPACE + ("chorus",))
    rack_set(patch, {"type": "chorus", "mode": "classic", "mix": k["chorus_mix"], "wet_hp_hz": 200}, before=SPACE)
    rack_set(patch, {"type": "reverb", "rt60": k["rev_rt60"], "size": 1.6, "send": k["rev_send"], "return_hp": 200})

@skill("traveler-walkthrough-control-track-filter-wt-animation", "mod", {
    "len_a": KI(8, 16, "s1: up to 16 steps"), "dir_a": KC(["fwd", "pingpong"], "s1: forward or ping-pong"),
    "sync_a": KC(["1/16", "1/8", "1/4"], "s1: tempo-synced note value"), "depth_a": K(0.4, 1.5, "s2: depth to cutoff (oct conv)"),
    "len_b": KI(5, 15, "s3: different length"), "sync_b": KC(["1/8", "1/4", "1/8d"], "s3: different rate"),
    "dest_b": KC(["wt_pos", "pan", "level"], "s3: complementary destination"), "depth_b": K(0.1, 0.4, "s3 (conv)"), "seed": KI(1, 999, "s4: randomize then refine")})
def control_tracks(patch, k):
    rng = np.random.default_rng(k["seed"])
    patch["ctracks"]["ctA"] = {"steps": [float(x) for x in rng.uniform(-1, 1, k["len_a"]).round(3)], "sync": k["sync_a"], "direction": k["dir_a"]}
    patch["ctracks"]["ctB"] = {"steps": [float(x) for x in rng.uniform(-1, 1, k["len_b"]).round(3)], "sync": k["sync_b"], "direction": "fwd"}
    i, f = first_filter(patch)
    if i is not None:
        patch["mods"].append({"src": "ctA", "dst": f"cutoff:{i}", "amt": k["depth_a"]})
    if k["dest_b"] == "wt_pos":
        patch["mods"].append({"src": "ctB", "dst": "wt_pos", "amt": k["depth_b"]})
    elif k["dest_b"] == "pan" and patch["layers"]:
        patch["mods"].append({"src": "ctB", "dst": "pan:0", "amt": k["depth_b"]})
    elif patch["layers"]:
        patch["mods"].append({"src": "ctB", "dst": "level:0", "amt": k["depth_b"]})

# ================================================================== FX / MIX SKILLS
@skill("soft-tape-saturation-pads-before-space", "fx", {
    "drive": K(0.15, 0.5, "s3: input toward ~0 VU, not into red"), "option": KC(["console", "tape_delay0"], "s2 A zero-time tape delay vs s3 B console")})
def tape_sat(patch, k):
    rack_set(patch, {"type": "tape", "drive": k["drive"], "hf_roll": 15000 if k["option"] == "tape_delay0" else 18000}, before=SPACE + ("chorus", "eq"))   # s5/C1: before space

@skill("chorus-ensemble-classic-vibrato-pad-modes", "fx", {
    "mode": KC(["ensemble", "classic"], "s1: classic (2 copies) vs ensemble (3)"), "rate": K(0.2, 0.8, "s2: warm sweet spot"),
    "depth_ms": K(2.0, 5.0, "s2: amount (ms conv)"), "feedback": K(0.0, 0.3, "s2: feedback; extreme turns metallic"),
    "wet_hp": K(150, 400, "s3: high-pass the processed path"), "width": K(0.8, 1.0, "s4: width (up to ~200%)"),
    "mix": K(0.25, 0.5, "s4: blend so pad stays present")})
def chorus_skill(patch, k):
    rack_set(patch, {"type": "chorus", "mode": k["mode"], "rate": k["rate"], "depth_ms": k["depth_ms"], "feedback": k["feedback"],
                     "wet_hp_hz": k["wet_hp"], "width": k["width"], "mix": k["mix"]}, before=SPACE, after=("eq",))   # C: after EQ, before delay/reverb

@skill("stereo-delay-pingpong-dual-parallel-two-tap", "fx", {
    "topology": KC(["pingpong", "dual"], "s1: ping-pong vs dual-parallel"), "sync": KC(["1/4", "1/8", "1/8d"], "s2: quarter or eighth"),
    "feedback": K(0.40, 0.50, "s3: ~40-50%"), "mix": K(0.15, 0.25, "s3: wet ~15-25%"), "sat": K(0.0, 0.2, "s4: tiny saturation"),
    "cross": K(0.0, 0.3, "s8: cross-feedback"), "mod_depth": K(0.0, 0.003, "s9: delay modulation (~20% conv)")})
def delay_skill(patch, k):
    if k["topology"] == "pingpong":
        fx = {"type": "delay", "mode": "pingpong", "sync_l": k["sync"], "feedback": k["feedback"], "mix": k["mix"], "hp_hz": 100, "lp_hz": 3000, "sat": k["sat"]}
    else:
        fx = {"type": "delay", "mode": "dual", "sync_l": "1/8d", "sync_r": "1/4", "fb_l": 0.45, "fb_r": 0.30, "x_lr": k["cross"], "x_rl": k["cross"],
              "mix": k["mix"] * 0.8, "hp_hz": 100, "lp_hz": 3000, "sat": k["sat"], "mod_depth": k["mod_depth"], "mod_rate": 0.4}
    rack_set(patch, fx, before=("reverb", "shimmer"))   # C: after EQ/chorus, before reverb

@skill("reverb-pads-type-choice-and-send-setup", "fx", {
    "type": KC(["hall", "plate", "room"], "s3-s6: hall lush 2-3s+, plate ~6.2s, room ~1s"),
    "hall_rt60": K(2.5, 4.0, "s3: hall ~2-3s+, longer for cinematic"), "plate_rt60": K(5.5, 6.5, "s6: long ambient plate ~6.2s"),
    "room_rt60": K(0.8, 1.2, "s6: room ~1s"), "predelay": K(0.01, 0.04, "s2: pre-delay for clarity"),
    "return_hp": K(200, 300, "s8: HP return ~200 Hz+"), "send": K(0.15, 0.4, "s7/s10: send level; longer decays need less"),
    "high_cut": KC([0, 8000, 10000], "s9: optional high-cut darkens")})
def reverb_skill(patch, k):
    t = k["type"]
    rt = {"hall": k["hall_rt60"], "plate": k["plate_rt60"], "room": k["room_rt60"]}[t]
    send = k["send"] * {"hall": 1.0, "plate": 0.7, "room": 1.3}[t]   # s10: longer -> quieter send
    rack_set(patch, {"type": "reverb", "rt60": rt, "size": {"hall": 1.4, "plate": 0.8, "room": 0.5}[t], "diffusion": {"hall": 0.6, "plate": 0.75, "room": 0.5}[t],
                     "er": {"hall": 0.5, "plate": 0.2, "room": 0.9}[t], "damp_hz": {"hall": 6000, "plate": 9000, "room": 7000}[t],
                     "predelay_s": k["predelay"], "return_hp": k["return_hp"], "return_lp": k["high_cut"], "send": send, "dry": 1.0,
                     "post_filter_open": None})

@skill("shimmer-reverb-pitchshift-plus12-feedback", "fx", {
    "rt60": K(4.0, 7.0, "s2: long lush reverb (capped by sample length)"), "feedback": K(0.25, 0.55, "s3: feedback for endless bloom"),
    "delay_s": K(0.1, 0.4, "s3: short = rapid, long = slower bloom"), "echo_hp": K(200, 400, "s4: cut lows on echoes"),
    "echo_lp": K(4000, 7000, "s4: shave brittle highs"), "wet_hp": K(200, 350, "s5: HP the shimmer wet"), "send": K(0.12, 0.3, "s5: blend via send")})
def shimmer_skill(patch, k):
    rack_set(patch, {"type": "shimmer", "semis": 12, "rt60": k["rt60"], "feedback": k["feedback"], "delay_s": k["delay_s"], "echo_hp": k["echo_hp"],
                     "echo_lp": k["echo_lp"], "wet_eq": [{"kind": "hp", "f": k["wet_hp"]}], "send": k["send"]})

@skill("midside-eq-bass-focus-width-depth", "mix", {
    "side_hp": K(100, 220, "s2: high-pass the side channel"), "mid_cut_db": K(1.0, 3.0, "s3/C2: cut mid problem band, small moves"),
    "restore": KC([False, True], "s4: optionally boost same band on sides"), "side_um_db": K(0.5, 1.5, "s5: subtle upper-mid side boost"),
    "side_um_hz": K(2000, 4000, "s5: upper midrange")})
def ms_eq_skill(patch, k):
    rack_set(patch, {"type": "ms_eq", "side_hp": k["side_hp"], "mid_cut_db": k["mid_cut_db"], "side_restore_same_band": k["restore"],
                     "side_uppermid_db": k["side_um_db"], "side_uppermid_hz": k["side_um_hz"]})

@skill("pad-width-no-phase-smear-highband-pan-or-chord-split", "mix", {
    "method": KC(["A_highband_pan", "B_chord_split"], "s1: method A or B"), "sync": KC(["1bar", "1/16"], "s3: bar-length or 16th"),
    "amount": K(0.3, 0.8, "s4: pull amount down if distracting"), "xover": K(1500, 4000, "s2: high band only (xover conv)"),
    "split_amt": K(0.6, 1.0, "s8: hard-pan L/R")})
def width_skill(patch, k):
    if k["method"] == "A_highband_pan":
        amt = k["amount"] * (0.6 if k["sync"] == "1/16" else 1.0)
        rack_set(patch, {"type": "hb_pan", "sync": k["sync"], "amount": amt, "xover_hz": k["xover"]})
    else:
        patch["chord_split"] = True
        patch["chord_split_amt"] = k["split_amt"]

@skill("trance-gate-sidechain-chop-texture", "fx", {
    "pattern": KC([[1, 1, 1, 0], [1], [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0]], "s2: clusters of 3 sixteenths, or every 16th"),
    "release": K(0.02, 0.12, "s4: release for snap (shorter = choppier)"), "hold": K(0.45, 0.7, "s3: threshold/open time (conv)"),
    "power_chord": KC([False, True], "s1: optional root+octave+fifth thickening"), "post_reverb": KC([True, False], "s5: reverb after the gate"),
    "post_send": K(0.15, 0.3, "s5 (conv)")})
def gate_skill(patch, k):
    if k["power_chord"] and patch["layers"]:
        base = dict(patch["layers"][0]); base.update(semi=base.get("semi", 0) + 7, level=base.get("level", 1.0) * 0.5)
        patch["layers"].append(base)
    pre = [f for f in patch["fx"] if f["type"] in ("reverb", "shimmer")]
    rack_set(patch, {"type": "gate", "pattern": k["pattern"], "release_s": k["release"], "hold_frac": k["hold"]})
    if k["post_reverb"]:
        rack_set(patch, {"type": "reverb", "rt60": 1.6, "size": 0.8, "send": k["post_send"], "return_hp": 200}, new_instance=bool(pre))

@skill("sidechain-compressor-duck-synth-pads", "fx", {
    "ratio": K(5.0, 7.0, "s4: ~6:1"), "attack": K(0.0005, 0.002, "s4: very fast attack"), "release": K(0.15, 0.35, "s4: slower release"),
    "thresh_db": K(-36, -24, "s5: tune threshold (key-relative conv)")})
def duck_skill(patch, k):
    rack_set(patch, {"type": "duck", "ratio": k["ratio"], "attack_s": k["attack"], "release_s": k["release"], "thresh_db": k["thresh_db"]}, before=("reverb", "shimmer"))   # s2: before reverb

@skill("parallel-filter-rhythmic-pad-chains", "fx", {
    "sync": KC(["1bar", "1/2"], "s3: 1-bar tempo-synced shape"), "lp_hz": K(600, 1500, "s2: low-pass path (conv)"), "bp_hz": K(500, 1500, "s2: band-pass path"),
    "depth_oct": K(1.0, 2.5, "s3 (conv)"), "mix": K(0.4, 0.8, "s1: parallel rack blend"), "post_hp": K(80, 150, "s5: EQ lows after stack")})
def parallel_filter(patch, k):
    rack_set(patch, {"type": "parallel_filter", "sync": k["sync"], "lp_hz": k["lp_hz"], "bp_hz": k["bp_hz"], "depth_oct": k["depth_oct"],
                     "mix": k["mix"], "post_hp": k["post_hp"], "lr_offset": float(np.pi / 2)}, before=SPACE)

@skill("traveler-walkthrough-fx-eq-chorus-delay-reverb", "fx", {
    "low_db": K(-3.0, -0.5, "s1: sculpt low end"), "mid_db": K(0.0, 2.0, "s1: mid presence"), "high_db": K(-2.0, 1.0, "s1: highs"),
    "chorus_mix": K(0.15, 0.3, "s2: chorus wet modest"), "delay": KC(["pingpong", "dual"], "s3: dual or ping-pong modulated"),
    "dly_mix": K(0.12, 0.22, "s3 (conv moderate)"), "rev": KC(["hall", "room", "space"], "s4: room/hall/space"), "rev_send": K(0.2, 0.35, "conv")})
def traveler_fx(patch, k):
    rack_set(patch, {"type": "eq", "bands": [{"kind": "lowshelf", "f": 200, "gain": k["low_db"]}, {"kind": "peak", "f": 1500, "q": 0.8, "gain": k["mid_db"]},
                                             {"kind": "highshelf", "f": 6000, "gain": k["high_db"]}]}, before=SPACE + ("chorus",))
    rack_set(patch, {"type": "chorus", "mode": "classic", "mix": k["chorus_mix"], "wet_hp_hz": 200}, before=SPACE, after=("eq",))
    if k["delay"] == "pingpong":
        d = {"type": "delay", "mode": "pingpong", "sync_l": "1/4", "feedback": 0.42, "mix": k["dly_mix"], "hp_hz": 150, "lp_hz": 3500}
    else:
        d = {"type": "delay", "mode": "dual", "sync_l": "1/8d", "sync_r": "1/4", "fb_l": 0.4, "fb_r": 0.3, "mix": k["dly_mix"], "mod_depth": 0.002, "hp_hz": 150, "lp_hz": 3500}
    rack_set(patch, d, before=("reverb", "shimmer"))
    rt = {"hall": 3.0, "room": 1.0, "space": 7.0}[k["rev"]]
    rack_set(patch, {"type": "reverb", "rt60": rt, "size": {"hall": 1.4, "room": 0.5, "space": 1.8}[k["rev"]],
                     "send": k["rev_send"] * (0.7 if k["rev"] == "space" else 1.0), "return_hp": 200})

@skill("mix-pads-role-eq-width-clarity", "mix", {
    "role": KC(["lead_bed", "background"], "s1: pad role"), "hp": K(80, 160, "s3: HP pad to protect kick/bass"),
    "return_hp": K(100, 200, "s3: HP reverb/delay returns ~100 Hz"), "narrow_hz": K(150, 300, "s6: multiband-narrow conflicting bands")})
def mix_pads(patch, k):
    rack_set(patch, {"type": "eq", "bands": [{"kind": "hp", "f": k["hp"]}]}, before=SPACE + ("chorus",))
    for f in patch["fx"]:
        if f["type"] == "reverb":
            f["return_hp"] = max(f.get("return_hp", 0), k["return_hp"])
        if f["type"] == "delay":
            f["hp_hz"] = max(f.get("hp_hz", 0), k["return_hp"])
    if k["role"] == "background":
        patch["lf_width_hz"] = max(patch.get("lf_width_hz") or 0, k["narrow_hz"])

# ------------------------------------------------------------------ chain builder
NOT_IMPLEMENTED = {
    "spectral-warp-vocode-formant-stretch-smear": "no per-harmonic spectral-warp oscillator in the renderer",
    "organic-looped-sample-unison-voicing-pad": "needs original acoustic samples (none on the box; original-synthesis-only rule)",
    "keysol-venus-fm-lfo-evolving-chase-sequence": "arp/sequence performance skill; partially covered by control-track + FM skills",
    "keysol-venus-noise-audiorate-filter-texture": "audio-rate filter FM + aftertouch performance; intentionally unstable",
}

def fill_knobs(sid, knobs=None):
    spec = REGISTRY[sid]["knobs"]
    out = {}
    for name, kn in spec.items():
        v = (knobs or {}).get(name, kn.default())
        out[name] = (v if v in kn.choices else kn.default()) if isinstance(kn, KC) else kn.clamp(v)
    return out

def build_patch(chain):
    patch = init_patch(chain["category"])
    for step in chain["steps"]:
        REGISTRY[step["skill"]]["apply"](patch, fill_knobs(step["skill"], step.get("knobs")))
    patch["fx"] = [f for f in patch["fx"]]
    for f in patch["fx"]:
        if f.get("type") == "reverb" and f.get("post_filter_open") is None:
            f.pop("post_filter_open", None)
    return patch
