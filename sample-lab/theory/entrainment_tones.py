"""Binaural & isochronic tone construction (audio-craft only; no health claims).
Binaural: left 200 Hz, right 210 Hz -> 10 Hz interaural difference, only perceived on headphones.
Isochronic: a 400 Hz carrier gated on/off at 10 Hz with raised-cosine edges (~3.75 ms) -> audible on speakers.
Also 40 Hz gating on a C5 (523.25 Hz) carrier as in the Peak-Focus recipe."""
from core import *
sec=6; tt=t(sec)
bin_=np.stack([sine(200,sec),sine(210,sec)],1)*.5
def iso(fc,rate,edge=.00375):
    ph=(tt*rate)%1; on=.5; g=np.clip(np.minimum(ph/ (edge*rate), (on-ph)/(edge*rate)),0,1)*(ph<on)
    g=.5-.5*np.cos(np.pi*g); return sine(fc,sec)*g
i10=iso(400,10); i40=iso(523.25,40)
write("entrainment_tones", np.concatenate([bin_,np.stack([i10,i10],1)*.5,np.stack([i40,i40],1)*.5]), "binaural 10Hz / iso 10Hz / iso 40Hz")

# --- In-house (2026-11-27): isochronic GATE-RATE RAMP, staged hold -> ramp -> hold. ---
# The gate phase is the running integral of the rate (cumsum(rate)/SR), so the rate glides with no
# phase jumps; each pulse keeps raised-cosine edges (no clicks). Carrier pitch stays fixed (steady).
def iso_ramp(fc, stages, edge=.004, duty=.5):
    """stages: list of (seconds, start_rate, end_rate); linear rate glide inside each stage."""
    r=np.concatenate([np.linspace(a,b,int(s*SR),endpoint=False) for s,a,b in stages])
    ph=np.cumsum(r)/SR%1; e=np.minimum(edge*r, duty/2)          # edge (in cycles) never > half the on-time
    g=np.clip(np.minimum(ph/e,(duty-ph)/e),0,1)*(ph<duty); g=.5-.5*np.cos(np.pi*g)
    return sine(fc,len(r)/SR)*g, r
ramp,rate=iso_ramp(400,[(4,12,12),(12,12,6),(4,6,6)])          # hold 12 Hz, glide to 6 Hz over 12 s, hold
write("entrainment_gate_rate_ramp", np.stack([ramp,ramp],1)*.5, "iso 400 Hz carrier: 12 Hz hold 4 s -> 6 Hz glide 12 s -> hold 4 s")
