"""Detune & beating: two sines 440 and 443 Hz beat at |f1-f2| = 3 Hz. Then a 7-voice unison saw at
detune spreads 0, 10, 25, 50 cents (supersaw). Voices panned across stereo -> width from decorrelation."""
from core import *
b=(sine(440,3)+sine(443,3))*.5
segs=[np.stack([b,b],1)]
for cents in (0,10,25,50):
    L=np.zeros(int(2*SR)); R=np.zeros_like(L)
    for i,o in enumerate(np.linspace(-1,1,7)):
        v=saw(midi(57)*2**(o*cents/1200),2,nh=60)*adsr(2,.05,.1,.9,.3)
        pan=o*.8; L+=v*np.cos((pan+1)*np.pi/4); R+=v*np.sin((pan+1)*np.pi/4)
    segs.append(np.stack([L,R],1)/7)
write("detune_unison", np.concatenate(segs), "3 Hz beating then 7-voice unison 0/10/25/50 cents")
