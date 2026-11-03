"""Arrangement energy curve in 8-bar blocks at 124 BPM (compressed to 1 bar per 'section' for audition):
intro (pad+hats, kick high-passed) -> build (add kick, bass, rising noise, snare roll doubling 4->8->16) ->
1 beat of silence (pre-drop gap) -> drop (everything, full low end) -> breakdown (pad+lead only) -> outro (mirror intro).
Each section changes something: the 'add or subtract one element per 8 bars' rule."""
from core import *
bpm=124; beat=60/bpm; bar=4*beat; r=np.random.default_rng(9)
def kick(): tt=t(.35); return np.tanh(1.8*sine(45+100*np.exp(-tt/.03),.35)*np.exp(-tt/.25))
def hat(): tt=t(.06); return hp(r.standard_normal(len(tt)),8000)*np.exp(-tt/.02)*.3
def snare(): tt=t(.2); return bp(r.standard_normal(len(tt)),1500,8000)*np.exp(-tt/.06)*.6
pad=lambda sec: sum(lp(saw(midi(m),sec,nh=40),2500) for m in (57,60,64))*.1
plan=[("intro",dict(pad=1,hat=1,kick="hp")),("intro",dict(pad=1,hat=1,kick="hp")),
      ("build",dict(pad=1,hat=1,kick=1,bass=1,roll=4,riser=1)),("build",dict(pad=1,hat=1,kick=1,bass=1,roll=8,riser=1)),
      ("build",dict(pad=1,hat=1,roll=16,riser=1,gap=1)),("drop",dict(pad=1,hat=1,kick=1,bass=1,snare=1)),("drop",dict(pad=1,hat=1,kick=1,bass=1,snare=1)),
      ("break",dict(pad=1)),("outro",dict(pad=1,hat=1,kick="hp"))]
out=np.zeros(int(len(plan)*bar*SR)+SR)
for si,(name,p) in enumerate(plan):
    o=si*bar
    if p.get("pad"): place(out,pad(bar),o)
    for b in range(4):
        if p.get("kick")==1: place(out,kick(),o+b*beat)
        if p.get("kick")=="hp": place(out,hp(kick(),250),o+b*beat)
        if p.get("hat"): place(out,hat(),o+b*beat+beat/2)
        if p.get("snare") and b%2: place(out,snare(),o+b*beat)
    if p.get("bass"): place(out,lp(saw(midi(33),bar,nh=30),300)*.4,o)
    if p.get("roll"):
        k=p["roll"]
        for i in range(k): place(out,snare()*(.3+.7*i/k),o+i*bar/k)
    if p.get("riser"):
        n=int(bar*SR); place(out,svf(r.standard_normal(n),np.geomspace(500,8000,n),2,"bp")*np.linspace(0,.6,n),o)
    if p.get("gap"): i=int((o+3*beat)*SR); out[i:i+int(beat*SR)]=0
write("arrangement_energy", out, " -> ".join(n for n,_ in plan))
