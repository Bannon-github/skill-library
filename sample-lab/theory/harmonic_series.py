"""Harmonic series & additive timbre: build saw/square/triangle from sine partials.
Hear: a 110 Hz sine gains partials 2..16 one per 0.4 s (the harmonic series = an A-major-ish overtone chord),
then the three classic waveforms built only from their partial recipes."""
from core import *
f=110; seg=[]
acc=np.zeros(int(.4*SR))
for n in range(1,17):
    acc=acc+sine(f*n,.4)/n; seg.append(acc*adsr(.4,.005,.05,1,.02))
recipes={"saw (all n, 1/n)":lambda n:1/n,"square (odd n, 1/n)":lambda n:(n%2)/n,"triangle (odd n, 1/n^2 alt)":lambda n:(n%2)*((-1)**((n-1)//2))/n**2}
for name,amp in recipes.items():
    seg.append(sum(amp(n)*sine(f*n,1.2) for n in range(1,40))*adsr(1.2,.01,.1,.8,.1))
write("harmonic_series", np.concatenate(seg), "partials 1-16 then saw/square/triangle")
