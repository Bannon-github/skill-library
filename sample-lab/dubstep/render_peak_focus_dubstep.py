#!/usr/bin/env python3
"""Minimal half-time dubstep bed + beta isochronic pulse. Original synthesis. Gating reused from render_flow_state_v2 (raised-cosine)."""
import json,sys,numpy as np,soundfile as sf,pyloudnorm as pyln
from numpy.fft import rfft,irfft,rfftfreq
R=json.load(open(sys.argv[1]));OUT=sys.argv[2];SR=44100;bar=4*60/R["bpm"];beat=bar/4
secs=[];a=0
for n,b in R["sections"]: secs.append((n,a*bar,(a+b)*bar));a+=b
T=a*bar;N=int(T*SR);t=np.arange(N)/SR;rng=np.random.default_rng(R["seed"]);db=lambda x:10**(x/20)
def env(name,fade=2*bar):  # 0..1 presence of layer with crossfades at boundaries
    e=np.zeros(N)
    for n,s,en in secs:
        if name in R["layers"][n]: e[int(s*SR):int(en*SR)]=1
    k=int(fade*SR);return np.convolve(e,np.hanning(k)/np.hanning(k).sum(),'same')
def lp(x,hz,o=2):
    F=rfft(x);f=rfftfreq(len(x),1/SR);return irfft(F/np.sqrt(1+(f/hz)**(2*o)),len(x))
def hit(sig,times,g=1.0):
    out=np.zeros(N)
    for tm in times:
        i=int(tm*SR);e=min(N,i+len(sig));out[i:e]+=sig[:e-i]*g
    return out
# drums (half-time: kick beat1, snare beat3)
tk=np.arange(int(.45*SR))/SR;kick=np.sin(2*np.pi*np.cumsum(45+120*np.exp(-tk*30))/SR)*np.exp(-tk*7)
ts=np.arange(int(.35*SR))/SR;snare=(0.6*rng.standard_normal(len(ts))*np.exp(-ts*14)+0.5*np.sin(2*np.pi*190*ts)*np.exp(-ts*25));snare=snare-lp(snare,300)
th=np.arange(int(.05*SR))/SR;hat=rng.standard_normal(len(th))*np.exp(-th*90);hat=hat-lp(hat,7000)
bars=np.arange(0,T,bar)
K=hit(kick,list(bars)+[b+2.5*beat for b in bars[1::2]])*env("kick",bar/2)
S=hit(snare,bars+2*beat)*env("snare",bar/2)
H=hit(hat,np.arange(0,T,beat/2)+beat/4,0.25)*env("hat")
P=hit(hat,[b+3.75*beat for b in bars],0.5)*env("perc")
# sub + soft wobble (F1 / Db1 / Eb1 / C1 progression, 2 bars each)
roots=[43.65,34.65,38.89,32.70];fr=np.array(roots)[(t//(2*bar)).astype(int)%4];fr=np.convolve(fr,np.ones(800)/800,'same')
ph=2*np.pi*np.cumsum(fr)/SR;sub=np.sin(ph)
wob_rate=np.where((t//(4*bar))%2==0,R["bpm"]/60/2,R["bpm"]/60)  # 1/2-note then 1/4-note wobble
lfo=0.5-0.5*np.cos(2*np.pi*np.cumsum(wob_rate)/SR)
saw=sum(((ph*2*(1+d)/(2*np.pi))%1*2-1) for d in(-.004,0,.004))/3
cuts=[150,290,430,570,710,850];bank=[lp(saw,c,3) for c in cuts];pos=lfo*(len(cuts)-1)  # smooth LFO sweep: per-sample interpolation across a filter bank
i0=np.minimum(pos.astype(int),len(cuts)-2);w=pos-i0;bank=np.array(bank);wob=bank[i0,np.arange(N)]*(1-w)+bank[i0+1,np.arange(N)]*w;del bank
wob=np.tanh(2*wob)*(0.4+0.6*lfo)
B=sub*0.9*env("sub")+wob*0.25*env("wobble")
# pad: Fm chords, detuned, lowpassed, stereo
chords=[[174.6,207.7,261.6],[138.6,174.6,207.7],[155.6,196.0,233.1],[130.8,164.8,196.0]]
padL=np.zeros(N);padR=np.zeros(N)
for ci,c in enumerate(chords):
    m=((t//(2*bar))%4==ci).astype(float);m=np.convolve(m,np.hanning(int(.6*SR))/np.hanning(int(.6*SR)).sum(),'same')
    for f in c:
        padL+=m*np.sin(2*np.pi*f*.997*t+rng.uniform(0,6));padR+=m*np.sin(2*np.pi*f*1.003*t+rng.uniform(0,6))
padL=lp(padL,1500);padR=lp(padR,1500);pe=env("pad",4*bar)*(0.7+0.3*np.sin(2*np.pi*t/(8*bar)))
# riser before main + sub drop / reverse swell into peak2
def riser(end,L=8*bar):
    n=int(L*SR);u=np.arange(n)/n;x=rng.standard_normal(n);y=np.zeros(n);ch=SR//4
    for i in range(0,n,ch): y[i:i+ch]=lp(x[i:i+ch],300+6000*u[i]**2)
    return hit(y*u**2*0.3,[end-L])
m_s=[s for n,s,e in secs if n=="main"][0];p_s=[s for n,s,e in secs if n=="peak2"][0];b_s=[s for n,s,e in secs if n=="breakdown"][0]
FX=riser(m_s)+riser(p_s,4*bar)
td=np.arange(int(3*SR))/SR;drop=np.sin(2*np.pi*np.cumsum(80*(30/80)**(td/3))/SR)*np.minimum(1,(3-td)/1)*0.6;FX+=hit(drop,[b_s])
# bed mix + carrier notch
mono_bed=K*0.9+S*0.5+H+P*0.4+B*0.7
L_=mono_bed+padL*0.06*pe+FX;R_=mono_bed+padR*0.06*pe+FX
fc=R["iso"]["carrierHz"]
def notch(x):
    F=rfft(x);f=rfftfreq(len(x),1/SR);return irfft(F*(1-(1-db(-24))*np.exp(-0.5*((f-fc)/8)**2)),len(x))
L_=notch(L_);R_=notch(R_)
# isochronic pulse (raised-cosine gate, smoothed rate ramp)
rp=np.array(R["rate"],float);rate=np.interp(t,rp[:,0],rp[:,1]);k=int(.01*SR);rate=np.convolve(rate,np.ones(k)/k,'same')
frac=(np.cumsum(rate)/SR)%1;d,e=R["iso"]["duty"],R["iso"]["edgeFrac"];g=(frac<d).astype(float)
up=frac<e;g[up]=0.5-0.5*np.cos(np.pi*frac[up]/e);dn=(frac>=d-e)&(frac<d);g[dn]=0.5-0.5*np.cos(np.pi*(d-frac[dn])/e)
pulse=(np.sin(2*np.pi*fc*t)+0.1*np.sin(4*np.pi*fc*t))*g
bedr=np.sqrt(((L_+R_)**2/4).mean());pulse*=bedr/np.sqrt((pulse**2).mean())*db(R["iso"]["relDbUnderBed"])
fade=np.minimum(1,np.minimum(t/8,(T-t)/10));pulse*=np.clip(0.3+t/30,0,1)
mix=np.stack([L_+pulse,R_+pulse],1)*fade[:,None];mix-=mix.mean(0)
meter=pyln.Meter(SR);mix*=db(R["targetLufs"]-meter.integrated_loudness(mix))
pk=20*np.log10(np.abs(mix).max())
if pk>R["peakCeilDb"]: # soft limit
    c=db(R["peakCeilDb"]);mix=np.where(np.abs(mix)>c*0.7,np.sign(mix)*(c*0.7+c*0.3*np.tanh((np.abs(mix)-c*0.7)/(c*0.3))),mix)
sf.write(OUT,mix.astype(np.float32),SR,subtype="PCM_24")
# verify pulse rate per 20 s window
x=mix.mean(1);F=rfft(x);f=rfftfreq(N,1/SR);band=np.abs(irfft(np.where((f>fc-100)&(f<fc+100),F,0),N));sm=np.convolve(band,np.ones(44)/44,'same')
W=20;errs=[]
for a in range(10,int(T)-W-10,W):
    s=sm[a*SR:(a+W)*SR];s=s-s.mean();Sp=np.abs(rfft(s*np.hanning(len(s)),4*len(s)));fq=rfftfreq(4*len(s),1/SR);m=(fq>R['verify'][0])&(fq<R['verify'][1])
    errs.append((a,round(float(fq[m][Sp[m].argmax()]),2),round(float(rate[a*SR:(a+W)*SR].mean()),2)))
st=dict(lengthSec=round(T,1),lufs=round(meter.integrated_loudness(mix),2),samplePeakDb=round(20*np.log10(np.abs(mix).max()),2),clipped=int((np.abs(mix)>=0.999).sum()),
 sections=[(n,round(s,1),round(e,1)) for n,s,e in secs],rateWindows=errs,maxRateErrHz=max(abs(a-b) for _,a,b in errs))
json.dump(st,open(OUT+".stats.json","w"),indent=1);print(json.dumps(st))
