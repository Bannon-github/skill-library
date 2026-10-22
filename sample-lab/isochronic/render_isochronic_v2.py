#!/usr/bin/env python3
"""v2: multi-layer looped beds (trim + equal-power crossfade + lowpass), isochronic + binaural, seam check. Original sound."""
import json,sys,numpy as np,soundfile as sf,pyloudnorm as pyln
from numpy.fft import rfft,irfft,rfftfreq
R=json.load(open(sys.argv[1])); OUT=sys.argv[2]; SR=48000; T=R["lengthSec"]; N=int(T*SR); t=np.arange(N)/SR
rng=np.random.default_rng(R["seed"]); db=lambda x:10**(x/20)
pts=np.array(R["iso"]["rampPoints"],float); rate=np.interp(t,pts[:,0],pts[:,1])
frac=(np.cumsum(rate)/SR)%1.0; duty=R["iso"]["duty"]; edge=R["iso"]["edgeFrac"]
g=(frac<duty).astype(float); up=frac<edge; g[up]=0.5-0.5*np.cos(np.pi*frac[up]/edge)
dn=(frac>=duty-edge)&(frac<duty); g[dn]=0.5-0.5*np.cos(np.pi*(duty-frac[dn])/edge)
g=g*(1-R["iso"].get("depthFloor",0))+R["iso"].get("depthFloor",0)
fc=R["iso"]["carrierHz"]; iso=(np.sin(2*np.pi*fc*t)+R["iso"].get("h2",0.15)*np.sin(4*np.pi*fc*t))*g
L=iso.copy(); Rr=iso.copy()
b=R["binaural"]
if b["enabled"]:
    ph=np.cumsum(rate)/SR; bf=b["carrierHz"]
    L+=b["level"]*np.sin(2*np.pi*(bf*t-ph/2)); Rr+=b["level"]*np.sin(2*np.pi*(bf*t+ph/2))
del g,frac,up,dn,iso
def lp(x,hz,order=2):
    F=rfft(x,axis=0); f=rfftfreq(len(x),1/SR); F*=(1/np.sqrt(1+(f/hz)**(2*order)))[:,None]; return irfft(F,len(x),axis=0)
seams=[]
def loop(layer):
    segs=[]
    for p in layer["files"]:
        s,_=sf.read(p); a,e=layer["trim"]; segs.append(s[int(a*SR):int(e*SR)])
    xf=int(layer["xfadeSec"]*SR); out=np.zeros((N,2)); pos=0;i=0
    ramp=np.sin(0.5*np.pi*np.arange(xf)/xf)  # equal power
    while pos<N:
        s=segs[i%len(segs)].copy(); n=len(s); w=np.ones(n)
        if i>0: w[:xf]=ramp
        w[-xf:]=ramp[::-1]; s*=w[:,None]; e=min(N,pos+n); out[pos:e]+=s[:e-pos]
        if i>0: seams.append(pos/SR+layer["xfadeSec"]/2)
        pos+=n-xf; i+=1
    if layer.get("lpHz"): out=lp(out,layer["lpHz"])
    return out*db(layer["levelDb"])
bed=sum(loop(l) for l in R["beds"])
nz=rng.standard_normal((N,2)); f=rfftfreq(N,1/SR)
for c in range(2):
    F=rfft(nz[:,c]); F/=np.sqrt(np.maximum(f,20)); F/=1+(f/R.get("noiseLpHz",2500))**2; nz[:,c]=irfft(F,N)
nz/=np.abs(nz).max()
# set pulse level relative to bed RMS
bedr=np.sqrt((bed**2).mean()); pulse=np.stack([L,Rr],1); pulse*=bedr/np.sqrt((pulse**2).mean())*db(R["iso"]["relDbUnderBed"])
del L,Rr
mix=bed+pulse+nz*bedr*db(R["noiseRelDb"])
fi,fo=int(R["fadeInSec"]*SR),int(R["fadeOutSec"]*SR); env=np.ones(N)
env[:fi]=0.5-0.5*np.cos(np.pi*np.arange(fi)/fi); env[N-fo:]=0.5+0.5*np.cos(np.pi*np.arange(fo)/fo); mix*=env[:,None]
mix-=mix.mean(0)
meter=pyln.Meter(SR); mix*=db(R["targetLufs"]-meter.integrated_loudness(mix))
def tp(x,ch=480000):
    m=0
    for a in range(0,len(x),ch):
        seg=x[max(0,a-4800):a+ch+4800]
        for c in range(2):
            F=rfft(seg[:,c]); u=irfft(np.concatenate([F,np.zeros(3*len(F))]),4*len(seg))*4; m=max(m,np.abs(u).max())
    return 20*np.log10(m)
p=tp(mix)
if p>R["peakCeilDb"]: mix*=db(R["peakCeilDb"]-p-0.1)
sf.write(OUT,mix,SR,subtype="PCM_24")
# rate check
x=mix.mean(1); F=rfft(x); F[(f<fc*0.85)|(f>fc*1.15)]=0; band=np.abs(irfft(F,N)); k=int(SR*0.01); sm=np.convolve(band,np.ones(k)/k,'same')
meas=[];W=R.get("checkWinSec",20)
for a in range(0,int(T)-W+1,W):
    s=sm[a*SR:(a+W)*SR]; s=s-s.mean(); S=np.abs(rfft(s*np.hanning(len(s)),8*len(s))); ff=rfftfreq(8*len(s),1/SR); m=(ff>3)&(ff<30)
    meas.append([a+W/2,round(float(ff[m][S[m].argmax()]),2),round(float(np.interp(a+W/2,pts[:,0],pts[:,1])),2)])
err=max(abs(a-b) for _,a,b in meas if 1)  # includes ramp windows (window-avg vs midpoint)
# seam check on bed only: spectral flux of 100ms frames, 2s around each seam vs global median
hop=int(0.1*SR); bm=bed.mean(1); fr=np.array([np.log10(np.abs(rfft(bm[i:i+hop]*np.hanning(hop)))+1e-9) for i in range(0,N-hop,hop)])
flux=np.r_[0,np.sqrt(((np.diff(fr,axis=0))**2).mean(1))]; med=np.median(flux)
sr=[round(float(flux[max(0,int(s/0.1)-10):int(s/0.1)+10].max()/med),2) for s in seams if s<T-1]
glob95=round(float(np.percentile(flux,99)/med),2)
cent=lambda seg:float((np.abs(rfft(seg))*rfftfreq(len(seg),1/SR)).sum()/np.abs(rfft(seg)).sum())
out=dict(lengthSec=T,lufs=round(meter.integrated_loudness(mix),2),truePeakDb=round(tp(mix),2),clipped=int((np.abs(mix)>=0.999).sum()),
 maxSampleStep=round(float(np.abs(np.diff(mix,axis=0)).max()),4),first2msPeakDb=round(20*np.log10(np.abs(mix[:96]).max()+1e-12),1),
 last100msRmsDb=round(10*np.log10((mix[-4800:]**2).mean()+1e-20),1),gateEdgeMsAtMaxRate=round(1000*edge/pts[:,1].max(),1),
 pulseRelDbUnderBed=R["iso"]["relDbUnderBed"],spectralCentroidHz=round(cent(x[N//2:N//2+SR*10]),0),
 seams=len(sr),seamFluxMaxVsMedian=max(sr) if sr else None,globalFlux99thVsMedian=glob95,
 rateMaxAbsErrHz=round(err,2),rateCheck_t_measured_target=meas)
print(json.dumps({k:v for k,v in out.items() if k!="rateCheck_t_measured_target"},indent=1)); print(meas)
json.dump(out,open(OUT+".stats.json","w"),indent=1)
