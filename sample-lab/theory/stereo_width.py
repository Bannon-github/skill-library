"""Stereo & phase: mono; hard-panned identical copies (still mono-centred); Haas 15 ms delay on one side
(wide but collapses with comb filtering in mono); detuned L/R (+/-7 cents, decorrelated, mono-safe-ish);
mid/side widening of the highs only (lows stay mono). Correlation printed for each (1=mono, 0=wide, <0=phase risk)."""
from core import *
sec=2; x=lp(saw(midi(57),sec,nh=60),4000)*adsr(sec,.05,.1,.8,.3)
def corr(s): return float(np.corrcoef(s[:,0],s[:,1])[0,1])
d=int(.015*SR); haas=np.stack([x,np.concatenate([np.zeros(d),x[:-d]])],1)
det=np.stack([lp(saw(midi(57)*2**(-7/1200),sec,nh=60),4000),lp(saw(midi(57)*2**(7/1200),sec,nh=60),4000)],1)*adsr(sec,.05,.1,.8,.3)[:,None]
M=(det[:,0]+det[:,1])/2; S=(det[:,0]-det[:,1])/2; S=hp(S,300)*1.8; ms=np.stack([M+S,M-S],1)
segs={"mono":np.stack([x,x],1),"haas15ms":haas,"detuneLR":det,"ms_highs_wide":ms}
for k,v in segs.items(): print(f"  {k}: corr={corr(v):+.2f}  mono-sum rms={rms_db(v.mean(1)):.1f} dB")
write("stereo_width", np.concatenate(list(segs.values())), " / ".join(segs))
