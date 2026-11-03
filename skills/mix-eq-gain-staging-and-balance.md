# Mixdown workflow: gain staging, subtractive EQ, dynamic EQ, multiband and saturation

Goal: Mix a track to a reference: gain stage to sensible levels, balance with faders first, subtractive EQ (high-pass non-bass, cut mud 200-400 Hz), the three-questions dynamic EQ approach, mid/side EQ, gentle multiband low control, selective saturation and parallel processing.

**Theory:** Masking happens when parts share frequency and time; cut before boost. Static clashes -> static EQ; dynamic clashes -> dynamic EQ keyed to the focus element; mono clashes -> mid-only cuts.

**Hear it:** `sample-lab/theory/eq_mix_balance.py`

## Workflow
1. Gain stage: each track peaks ~-12 to -6 dBFS, bus headroom ~-6 dB; import a reference track at matched loudness.
2. Balance with faders and pan before any EQ; kick and bass first, then lead/vocal, then the rest.
3. Subtractive EQ: HP everything that isn't bass/kick (100-250 Hz for pads), cut mud 200-400 Hz, harshness 2-5 kHz with narrow Q.
4. Three questions: what is the focus? is the clash static or dynamic (dynamic -> dynamic EQ keyed to the focus)? where in stereo (centre focus -> mid-only cut)? EQ last.
5. Mid/side: keep lows mono (side HP ~120 Hz), boost air on sides lightly; multiband: gently compress/expand the low band only.
6. Saturation: tape/tube on pads before space, selective lo-fi grit on one element, parallel blends level-matched.
7. Check mono, small speakers, and A/B against the reference; leave ~-6 dB for mastering or target loudness (e.g. -14 LUFS stream).
8. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/eq_mix_balance.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### EQ for balance in three questions: what is the focus, is the clash static or dynamic (sidechained dynamic EQ), and where in the stereo field (mid-only)
Source: [I HATED Mixing Until I Learned This Hack](https://www.youtube.com/watch?v=2cR4omOL6p4) · was `eq-balance-three-questions-focus-static-vs-dynamic-sidechained-dynamic-eq-mid-only-when-competitor-is-mono`
- Set general volume, stereo placement and compression first; EQ for balance comes after those.
- Ask what the focus of this section is and which other sounds still compete with it (often the parts you chose to mix louder).
- For each pair, ask whether the overlap is static or dynamic: does it change when the focus pauses, gets louder or quieter, or moves to different notes?
- For a dynamic clash, insert a dynamic EQ on the competitor and set its sidechain input to the focus track. Adjust the depth (how drastic), resolution (detailed vs broad) and any frequency ranges to ignore.
- Ask where in the stereo field the clash happens. If the focus is mono (centre) and the competitor is stereo, switch the dynamic EQ to mid-only (or wrap it in M/S encode/decode) so only the centre is ducked.
- A/B against a static scoop: compare the competitor's level and life in the focus's pauses and in its side channel.

### Mid-side EQ: center the bass, tame mid problems, widen with side mids/highs
Source: [Mid Side EQ Simplified - A Powerful Tool for Stereo Mixing](https://www.youtube.com/watch?v=kEiILPm1VSc) · was `midside-eq-bass-focus-width-depth`
- Enable mid/side on the EQ. Confirm mid ≈ mono sum of L+R and side ≈ L minus R (spatial difference, not merely hard-panned parts).
- If a synth/sample has overly wide bass: solo sides, high-pass the side channel to remove bass so sides keep ambience/air while lows become narrower and centered; A/B with full stereo.
- If a lead/pad resonance is mostly mid-localized: solo mid vs side to locate it, then cut the problem band on the mid channel only.
- Optionally boost a little top end on the sides after mid cuts so width/air remains; for mix problems where stereo EQ mushifies everything, cut only the mid band that holds the squeaky/scratchy energy (example: guitars in mid) and leave lush side reverb/ambience alone — even boost that same band on sides if you want air back.
- For width/depth: try a subtle boost in the upper midrange on the sides (not only extreme high shelves) — transcript finds upper-mid side boosts create more depth/aliveness than highs-alone width tricks. Keep mastering-style moves modest.

### Mix pads for role, EQ clarity, energy, and width control
Source: [5 Tips for Mixing Pads and Synths for a Full, Clear Sound](https://www.youtube.com/watch?v=6NXqV9jWJ1s) · was `mix-pads-role-eq-width-clarity`
- Decide pad role (lead evolving bed vs background atmosphere) — mix moves follow the role.
- View long-average spectrum to see which bands the pad occupies vs vocals/keys.
- High-pass the pad to leave room for kick/bass; stop before the pad thins excessively; likewise HP reverb/delay returns (~100 Hz) to prevent buildup.
- In busy mids/highs, use gentle tonal EQ or dynamic EQ sidechained to conflicting elements (e.g. snare/vocal) only as needed.
- Automate mute/filter/FX across intro/verse/chorus so pads shape energy while staying supportive.
- If pads steal stereo space: collapse toward mono and pan, or multiband-narrow only conflicting bands while keeping air wide.

### Multiband dynamics on a synth/pad bus: gentle low-band control, upward expand for weak lows, slow-attack top band
Source: [Ultimate Compression Tutorial Pt.5 - Multiband Compression quick settings for Drums and 2bus](https://www.youtube.com/watch?v=T2poUGh6qPg) · was `multiband-low-band-gentle-control-and-expand`
- Bypass all bands except the one covering the problem range; solo that band to hear exactly what it acts on.
- Boomy lows: on the low band start aggressive to find it (e.g. -24 dB range, very fast attack), then ease off; a slower attack lets the initial transient/punch through and reduces the range after it, while a very fast attack chokes it.
- Real-world gentle setting: low band only, crossover ~92 Hz (acts like a dynamic low shelf), range ~1.5 dB, opto mode, fairly fast attack—'a couple of dB' makes a big difference.
- Weak lows: raise that band's gain (example +6 dB) and switch to expansion with lower threshold so the band stays down until a hit arrives, then returns to its boosted gain—cleaner low end between hits, bigger on hits.
- Harsh highs: on a top band use a slow attack so fast bright transients pass while sustained splashy energy is reduced; if it gets dark, add band gain to restore controlled brightness.
- Set attack/release as with a wideband compressor: release roughly in time with the music and listen to the breathing. Use a band only for range problems that come and go (a static EQ handles constant ones).
- A/B with the whole unit bypassed: splitting into bands with crossover filters shifts phase and tone even at zero gain reduction, so confirm the change is worth it.

### Frequency- and level-selective saturation, exciter, bit/noise grit and small-speaker transition
Source: [How to use DISTORTION properly in Ableton Live: Tips & tricks for Saturator, Redux, Erosion & more](https://www.youtube.com/watch?v=MWzBoFOOzco) · was `selective-saturation-and-lofi-grit-toolkit`
- Add saturation drive gradually and turn output down by the same amount to compare at matched loudness; decide whether the post-saturation clipper stage is wanted (adds more distortion) or off.
- Weight saturation by band: reduce drive on the low band so subs stay clean while upper harmonics remain (helps 808/sub cut through small speakers); push the high band and width for brighter grit. Avoid cranking the low band—sub content collapses.
- Level-selective: use a threshold/waveshaper mode where only signal above the threshold saturates, or an envelope-follow control that adds more bias/drive on louder parts (tube-style).
- Clipper use: set saturation so peaks are shaved (e.g. peak meter drops ~6 dB with little audible change), then raise the track level by the recovered headroom.
- Exciter: overdrive with its pre-distortion band filter aimed at the highs, low drive, low dry/wet, a touch of tone—adds new harmonics instead of EQ boost to dull or lossy material.
- Vintage grit: subtle bit-depth/sample-rate reduction (old samplers ran ~12-bit at roughly 20-something kHz), small jitter; lower bits = noisier, lower rate = crunchy ringing. Or noise-modulation (erosion-like: sine, noise, wide-noise modes; width sets the noise band) at very low amounts; wide-noise adds stereo width.
- After heavy distortion on bass, re-add/restore sub (sub switch or low shelf) because distortion thins lows.
- Transition trick: cabinet/small-speaker sim on the master (small speaker, far/dynamic mic, mono) during an intro or bridge, then bypass when the full track drops.

### Soft tape/analog saturation on pads before space FX
Source: [How to mix Pads & Strings - The complete process - Part 1 - Saturation - Mini Series](https://www.youtube.com/watch?v=o71KYxEqPdU) · was `soft-tape-saturation-pads-before-space`
- Identify sterile/digital pad or synth-string sustains that need density. Goal is subtle analog juice, not crunch.
- Option A — low-CPU tape: insert a tape-delay emulator, set delay time to zero so only tape saturation remains (no echoes).
- Option B — gentle console/tape emulation: raise input until meters approach ~0 (not deep into red) for natural saturation; back off if obvious distortion appears.
- A/B dry vs sat: expect slightly fuller low-mid presence and mild soft compression—rewind/listen carefully; changes are subtle by design.
- Then continue the pad chain (EQ/chorus/delay/reverb). Keep this sat stage before big space so reverb blooms on the denser tone.

### Saturate drums without losing punch: an envelope follower reads the clean signal on a muted parallel chain, and its output drives a gain stage placed after the saturator so the saturated signal's peaks are pushed back up and its dynamic range is restored
Source: [Saturation Is Killing Your Mix](https://www.youtube.com/watch?v=GomiGC__HC0) · was `dynamics-restoring-saturation`
- Saturate the drums and watch the waveform: peaks get shaved and the drums stop hitting in the mix.
- Build two parallel chains: chain A holds only an envelope follower/peak controller and is muted (it just measures); chain B holds the saturator followed by a gain/utility device.
- Map the follower's output to the gain device in chain B.
- Set the follower base around 30-40% and the amount around 60-70%, then adjust until saturated hits match the original punch.
- Compare in the mix; for melodic loops combine with sidechain ducking to the drum loop for pump.
