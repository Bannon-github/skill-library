"""Drum synthesis from first principles: kick = sine with fast pitch envelope (150->45 Hz, ~35 ms) + amp decay;
snare = two sines (~180/330 Hz) + band-passed noise; clap = 3 noise bursts ~10 ms apart then a tail (1-6 kHz);
closed/open hat = high-passed noise (>7 kHz) with short/long decay; 808 = long sine at the song root with slight drive."""
from core import *
def kick(f0=150,f1=45,pt=.035,dec=.35):
    tt=t(.6); f=f1+(f0-f1)*np.exp(-tt/pt); return np.tanh(1.5*sine(f,.6)*np.exp(-tt/dec))
def snare():
    tt=t(.3); body=(sine(180,.3)+.6*sine(330,.3))*np.exp(-tt/.06); n=bp(np.random.default_rng(1).standard_normal(len(tt)),1500,9000)*np.exp(-tt/.09)
    return body*.6+n
def clap():
    n=bp(np.random.default_rng(2).standard_normal(int(.35*SR)),1000,6000); e=np.zeros(len(n)); tt=t(.35)
    for k in range(3): i=int(k*.011*SR); e[i:i+int(.008*SR)]=1
    return n*np.maximum(e, np.exp(-np.maximum(tt-.033,0)/.08)*(tt>.033))
def hat(dec): tt=t(.4); return hp(np.random.default_rng(3).standard_normal(len(tt)),7000,4)*np.exp(-tt/dec)*.2
def b808(f=midi(33),sec=1.2): tt=t(sec); return np.tanh(2*sine(f*(1+.5*np.exp(-tt/.02)),sec)*np.exp(-tt/.6))*.8
solo=[kick(),snare(),clap(),hat(.03),hat(.25),b808()]
gap=np.zeros(int(.2*SR)); x=np.concatenate(sum([[s,gap] for s in solo],[]))
bpm=120; s16=60/bpm/4; loop=np.zeros(int(16*s16*2*SR)+SR)
for bar in range(2):
    o=bar*16*s16
    for i in (0,6,10): place(loop,kick(),o+i*s16)
    for i in (4,12): place(loop,clap()*.7,o+i*s16); place(loop,snare()*.5,o+i*s16)
    for i in range(16): place(loop,hat(.03)*(.5 if i%2 else .3),o+i*s16)
    place(loop,b808(sec=.7)*.6,o)
write("drums_synthesis", np.concatenate([x,loop]), "kick snare clap chh ohh 808 then 2-bar 120 BPM loop")
