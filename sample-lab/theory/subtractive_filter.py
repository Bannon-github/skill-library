"""Subtractive synthesis: oscillator -> filter -> envelope. A 55 Hz saw swept by a low-pass 150 Hz->8 kHz,
first at Q 0.7 (no resonance), then Q 6 (resonant peak whistles at the cutoff), then a filter-envelope pluck
(cutoff = base + env*amount) at three envelope amounts."""
from core import *
d=3; x=saw(55,d); sweep=np.geomspace(150,8000,len(x))
a=svf(x,sweep,0.7); b=svf(x,sweep,6.0)
pl=[]
for amt in (300,2000,6000):
    for k in range(4):
        e=adsr(.5,.002,.25,0,.05); s=saw(midi(45+[0,3,7,10][k]),.5)
        pl.append(svf(s,200+amt*e,2.0)*adsr(.5,.002,.3,.3,.1))
write("subtractive_filter", np.concatenate([a,b]+pl), "LP sweep Q0.7, Q6, then env amounts 300/2000/6000 Hz")
