"""Wavetable morph: 8 single-cycle frames from sine -> triangle -> square -> saw -> formant-ish pulse; the
position is swept by an LFO so the harmonic spectrum moves over time (spectral motion without a filter)."""
from core import *
N=2048; ph=np.arange(N)/N
def addf(amps): return sum(a*np.sin(2*np.pi*(k+1)*ph) for k,a in enumerate(amps))
frames=[addf([1]),addf([(k%2==0)*((-1)**(k//2))/(k+1)**2 for k in range(40)]),addf([(k%2==0)/(k+1) for k in range(40)]),
        addf([1/(k+1) for k in range(60)]),addf([np.exp(-((k+1-8)/3)**2) for k in range(40)])]
frames=np.array([f/np.max(np.abs(f)) for f in frames])
sec=6; f0=midi(45); tt=t(sec); pos=(0.5-0.5*np.cos(2*np.pi*tt/sec))*(len(frames)-1)
phase=(np.cumsum(np.full(len(tt),f0))/SR)%1*N
i0=np.floor(pos).astype(int); fr=pos-i0; i1=np.minimum(i0+1,len(frames)-1)
pi=phase.astype(int)
y=(1-fr)*frames[i0,pi]+fr*frames[i1,pi]
write("wavetable_morph", y*adsr(sec,.05,.1,.9,.3), "position sweep sine->tri->square->saw->formant and back")
