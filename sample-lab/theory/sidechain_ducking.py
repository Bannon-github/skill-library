"""Sidechain ducking per element at 124 BPM four-on-the-floor:
A) no sidechain (bass masks kick), B) bass ducked for the whole kick (deep, ~200 ms recovery),
C) pad ducked only on the punch (~6 dB, ~60 ms fast recovery), D) both = the 'pump' heard in house/EDM.
Duck gain is a per-beat envelope: g = 1 - depth*exp(-t/rel) with a 2 ms attack."""
from core import *
bpm=124; beat=60/bpm; bars=2; n=int(bars*4*beat*SR)
def kick(): tt=t(.4); return np.tanh(1.8*sine(45+105*np.exp(-tt/.03),.4)*np.exp(-tt/.25))
def duck(depth,rel):
    g=np.ones(n); tt=t(beat)
    shape=1-depth*np.minimum(tt/.002,1)*np.exp(-tt/rel)
    for b in range(bars*4): i=int(b*beat*SR); g[i:i+len(shape)]=shape[:n-i]
    return g
K=np.zeros(n); [place(K,kick(),b*beat) for b in range(bars*4)]
bass=lp(saw(midi(33),n/SR,nh=40),300)*.5
pad=sum(lp(saw(midi(m),n/SR,nh=40),2500) for m in (57,60,64,67))*.12
segs=[]
for bd,pd in (((0,.1),(0,.1)),((.95,.18),(0,.1)),((0,.1),(.5,.06)),((.95,.18),(.5,.06))):
    segs.append(K+bass*duck(*bd)+pad*duck(*pd))
write("sidechain_ducking", np.concatenate(segs), "none / bass-full / pad-punch / both")
