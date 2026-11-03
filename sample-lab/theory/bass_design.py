"""Bass design: Reese (3 saws detuned +/-15 cents, one an octave down, low-passed 900 Hz, soft-clipped) with a
separate clean sine sub below 100 Hz (mono) so distortion never muddies the fundamental; then punchy 808
(sine, pitch envelope +12 st -> 0 in 35 ms) and a sub drop (80->20 Hz)."""
from core import *
sec=3; f=midi(33)
reese=sum(saw(f*2**(c/1200)*m,sec,nh=60) for c,m in ((-15,1),(15,1),(0,.5)))
top=hp(np.tanh(2.5*lp(reese,900)),100)*.5; sub=lp(sine(f,sec),100)*.8
tt=t(1.2); b808=np.tanh(1.6*sine(f*(1+np.exp(-tt/.035)),1.2)*np.exp(-tt/.7))
tt=t(2); drop=sine(20+60*np.exp(-tt/.6),2)*np.exp(-tt/1.2)
write("bass_design", np.concatenate([top,sub,top+sub,b808,b808,drop]), "reese top / sine sub / combined / 808 x2 / sub drop")
