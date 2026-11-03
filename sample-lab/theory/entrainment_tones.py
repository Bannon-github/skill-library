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
