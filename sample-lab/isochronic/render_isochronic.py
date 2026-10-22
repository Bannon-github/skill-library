#!/usr/bin/env python3
"""Isochronic + optional binaural over the drone-wavetable-artifact-drone bed. Original sound."""
import json,sys,numpy as np,soundfile as sf,pyloudnorm as pyln
R=json.load(open(sys.argv[1])); SR=48000; T=R["lengthSec"]; N=int(T*SR); t=np.arange(N)/SR
rng=np.random.default_rng(R["seed"])
# rate ramp: piecewise-linear in time between (time,rate) points
pts=np.array(R["iso"]["rampPoints"]); rate=np.interp(t,pts[:,0],pts[:,1])
phase=np.cumsum(rate)/SR; frac=phase%1.0; duty=R["iso"]["duty"]; edge=R["iso"]["edgeFrac"]
# raised-cosine gate: on for `duty` of each cycle, cosine ramps of `edge` (fraction of cycle) on each side
g=np.zeros(N); on=frac<duty
g[on]=1.0
up=frac<edge; g[up]=0.5-0.5*np.cos(np.pi*frac[up]/edge)
dn=(frac>=duty-edge)&on; g[dn]=0.5-0.5*np.cos(np.pi*(duty-frac[dn])/edge)
fc=R["iso"]["carrierHz"]; car=np.sin(2*np.pi*fc*t)+0.25*np.sin(2*np.pi*2*fc*t)
iso=car*g
L=iso.copy(); Rr=iso.copy()
if R["binaural"]["enabled"]:
    b=R["binaural"]; bf=b["carrierHz"]; off=np.interp(t,pts[:,0],pts[:,1])  # beat follows same ramp
    ph=np.cumsum(off)/SR
    L+=b["level"]*np.sin(2*np.pi*bf*t); Rr+=b["level"]*np.sin(2*np.pi*(bf*t+ph))
# bed: crossfade-loop drone renders
beds=[sf.read(p)[0] for p in R["bed"]["files"]]; xf=int(2*SR); bed=np.zeros((N,2)); pos=0;i=0
while pos<N:
    s=beds[i%len(beds)]; n=len(s); seg=s.copy()
    w=np.ones(n); w[:xf]=np.linspace(0,1,xf); w[-xf:]=np.linspace(1,0,xf); seg*=w[:,None]
    e=min(N,pos+n); bed[pos:e]+=seg[:e-pos]; pos+=n-xf; i+=1
noise=rng.standard_normal((N,2)); 
from numpy.fft import rfft,irfft
for c in range(2):  # pinkish, lowpassed soft noise
    F=rfft(noise[:,c]); f=np.fft.rfftfreq(N,1/SR); F/=np.sqrt(np.maximum(f,20)); F*=1/(1+(f/3000)**2); noise[:,c]=irfft(F,N)
noise/=np.abs(noise).max()
def db(x):return 10**(x/20)
mix=bed*db(R["bed"]["levelDb"])+np.stack([L,Rr],1)*db(R["iso"]["levelDb"])+noise*db(R["noiseDb"])
fi,fo=int(R["fadeInSec"]*SR),int(R["fadeOutSec"]*SR); env=np.ones(N); env[:fi]=(0.5-0.5*np.cos(np.pi*np.arange(fi)/fi)); env[-fo:]=env[:fo][::-1] if fo==fi else 0.5+0.5*np.cos(np.pi*np.arange(fo)/fo)
mix*=env[:,None]
meter=pyln.Meter(SR); lu=meter.integrated_loudness(mix); mix*=db(R["targetLufs"]-lu)
# true-peak ceiling via 4x oversample estimate; simple gain-down if over
from numpy import interp
def tp(x):
    up=np.stack([np.fft.irfft(np.pad(np.fft.rfft(x[:,c]),(0,3*(N//2))) ,4*N)*4 for c in range(2)],1); return 20*np.log10(np.abs(up).max())
p=tp(mix)
if p>R["peakCeilDb"]: mix*=db(R["peakCeilDb"]-p-0.1)
sf.write(sys.argv[2],mix,SR,subtype="PCM_24")
# verify: measure pulse rate from iso envelope of the mix (band around carrier, Hilbert-free: rectify+smooth)
x=mix.mean(1); F=rfft(x); f=np.fft.rfftfreq(N,1/SR); F[(f<fc*0.8)|(f>fc*1.25)]=0; band=np.abs(irfft(F,N))
k=int(SR*0.01); sm=np.convolve(band,np.ones(k)/k,'same')
meas=[]
for a in range(0,int(T)-10,10):
    seg=sm[a*SR:(a+10)*SR]; seg=seg-seg.mean(); S=np.abs(rfft(seg*np.hanning(len(seg)))); ff=np.fft.rfftfreq(len(seg),1/SR); m=(ff>2)&(ff<45)
    meas.append((a+5,round(float(ff[m][S[m].argmax()]),2),round(float(np.interp(a+5,pts[:,0],pts[:,1])),2)))
d=np.abs(np.diff(mix,axis=0)).max(); 
out=dict(lufs=round(meter.integrated_loudness(mix),2),truePeakDb=round(tp(mix),2),samplePeakDb=round(20*np.log10(np.abs(mix).max()),2),
 maxSampleStep=round(float(d),4),gateMinEdgeMs=round(1000*edge/pts[:,1].max(),1),clipped=int((np.abs(mix)>=0.999).sum()),
 first2msPeakDb=round(20*np.log10(np.abs(mix[:96]).max()+1e-12),1),last100msRmsDb=round(10*np.log10((mix[-4800:]**2).mean()+1e-20),1),
 lowSideRatio=None,rateCheck_t_measured_target=meas)
F0=rfft(mix[:,0]-mix[:,1]);Fm=rfft(mix.sum(1));lo=f<120;out["lowSideRatio"]=round(float((np.abs(F0[lo])**2).sum()/(np.abs(Fm[lo])**2).sum()),4)
print(json.dumps(out,indent=1)); json.dump(out,open(sys.argv[2]+".stats.json","w"),indent=1)
