"""Granular synthesis: a 1 s source (plucked chord) is cut into 40-120 ms Hann-windowed grains.
Density (grains/s), position (where in the source), pitch spray and stereo spray turn a short sound into a
sustained evolving pad. Freeze = position held constant."""
from core import *
src=sum(np.sin(2*np.pi*midi(m)*t(1))*np.exp(-t(1)*3) for m in (57,64,69,72))
r=np.random.default_rng(7); sec=6; out=np.zeros((int(sec*SR),2))
for dens,start,end,freeze in ((20,0,2,False),(60,2,4,False),(60,4,6,True)):
    for g in range(int(dens*(end-start))):
        at=start+r.uniform(0,end-start); L=int(r.uniform(.04,.12)*SR)
        pos=.15 if freeze else r.uniform(0,.8); s=int(pos*SR)
        grain=src[s:s+L]; grain=grain*np.hanning(len(grain))
        if r.random()<.3: grain=np.interp(np.arange(0,len(grain),2.0),np.arange(len(grain)),grain)
        pan=r.uniform(-.8,.8); i=int(at*SR); j=min(i+len(grain),len(out))
        out[i:j]+=stereo(grain[:j-i],pan)
write("granular_cloud", np.concatenate([np.stack([src,src],1),out]), "source, sparse 20/s, dense 60/s, frozen")
