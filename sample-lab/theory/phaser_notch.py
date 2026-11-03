"""Phaser vs flanger/comb: a saw chord through a 6-stage all-pass phaser (notches at irregular spacing, swept by
a 0.25 Hz LFO, feedback 0.5) vs. a flanger (short 1-5 ms modulated delay -> harmonically spaced comb notches)."""
from core import *
sec=4; x=sum(saw(midi(m),sec,nh=60) for m in (57,64,69))/3
ph=np.zeros_like(x); st=np.zeros(6); prev=np.zeros(6); fb=0.0
lfo=0.5+0.5*np.sin(2*np.pi*.25*t(sec))
fc=300*(4000/300)**lfo; a=(np.tan(np.pi*fc/SR)-1)/(np.tan(np.pi*fc/SR)+1)
for i in range(len(x)):
    v=x[i]+.5*fb
    for s in range(6):
        y=a[i]*v+st[s]; st[s]=v-a[i]*y; v=y
    fb=v; ph[i]=.5*(x[i]+v)
dl=(1+2*(1+np.sin(2*np.pi*.25*t(sec))))*SR/1000; idx=np.arange(len(x))-dl
fl=.5*(x+np.interp(idx,np.arange(len(x)),x,left=0))
write("phaser_notch", np.concatenate([x,ph,fl]), "dry / 6-stage phaser / flanger")
