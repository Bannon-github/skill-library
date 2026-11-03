"""Modulation sources on a filtered saw: sine LFO slow (0.2 Hz sweep) vs tempo-synced 1/8 (wobble @ 140 BPM);
sample & hold (random stepped cutoff); smoothed random (drift); envelope follower (cutoff follows a drum loop's level);
nested LFO (LFO2 modulates LFO1 depth)."""
from core import *
sec=3; tt=t(sec); x=saw(midi(38),sec,nh=80); r=np.random.default_rng(8)
def flt(c): return svf(x,c,4)
slow=flt(400*(10**(1+np.sin(2*np.pi*.2*tt))*.5+.1))
wob=flt(200+3000*(0.5+0.5*np.sin(2*np.pi*(140/60*2)*tt)))
steps=np.repeat(r.uniform(300,5000,int(sec*8)+1),SR//8)[:len(tt)]; sh=flt(steps)
drift=flt(lp(np.repeat(r.uniform(300,5000,int(sec*8)+1),SR//8)[:len(tt)],2)+200)
drum=np.zeros(len(tt))
for b in range(int(sec*2)): place(drum, np.exp(-t(.5)/.08), b*.5)
envf=flt(200+5000*lp(drum,30))
nested=flt(800+700*(1+np.sin(2*np.pi*.33*tt))*np.sin(2*np.pi*4*tt)+700)
write("modulation_lfo", np.concatenate([slow,wob,sh,drift,envf,nested]), "slow/synced/S&H/drift/env-follower/nested")
