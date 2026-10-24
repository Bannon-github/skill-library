#!/usr/bin/env python3
"""Tracks 2/3 of the latest-distills set. usage: render_combo.py recipe.json out.wav"""
import json,sys,numpy as np,soundfile as sf,pyloudnorm as pyln
from numpy.fft import rfft,irfft,rfftfreq
from scipy.signal import stft,istft
from scipy.ndimage import uniform_filter
R=json.load(open(sys.argv[1]));OUT=sys.argv[2];SR=44100;bar=240/R["bpm"];beat=bar/4;rng=np.random.default_rng(R["seed"]);db=lambda x:10**(x/20)
secs=[];a=0
for n,b in R["sections"]: secs.append((n,a*bar,(a+b)*bar));a+=b
T=a*bar;N=int(T*SR);t=np.arange(N)/SR
def lp(x,hz,o=2):F=rfft(x,axis=0);f=rfftfreq(len(x),1/SR);g=1/np.sqrt(1+(f/hz)**(2*o));return irfft(F*(g if x.ndim==1 else g[:,None]),len(x),axis=0)
def hp(x,hz,o=2):return x-lp(x,hz,o)
def env(names,fade=bar):
    e=np.zeros(N)
    for n,s,en in secs:
        if n in names:e[int(s*SR):int(en*SR)]=1
    k=int(fade*SR);return np.convolve(e,np.hanning(k)/np.hanning(k).sum(),'same')
def place(sig,times):
    o=np.zeros(N)
    for tm in times:
        i=int(tm*SR);e=min(N,i+len(sig));o[i:e]+=sig[:e-i]
    return o
def saws(freq,det=(-.004,0,.004)):return sum(2*((np.cumsum(freq*(1+d))/SR+rng.random())%1)-1 for d in det)/len(det)
def kickhits(kt,mask):
    k=np.searchsorted(kt,t,side='right')-1;since=np.where(k>=0,t-kt[np.maximum(k,0)],9);return since*1.0,mask
def duck(since,on,length,depth):
    g=np.where(since<length,0.5-0.5*np.cos(np.pi*since/length),1.0);return 1-depth*(1-g)*on
tk=np.arange(int(.32*SR))/SR;kick=np.sin(2*np.pi*np.cumsum(46+150*np.exp(-tk*32))/SR)*np.exp(-tk*9)
cl=rng.standard_normal(500)*np.exp(-np.arange(500)/90);kick[:500]+=0.4*hp(cl,1500)
ts=np.arange(int(.3*SR))/SR;snare=hp(0.6*rng.standard_normal(len(ts))*np.exp(-ts*15)+0.5*np.sin(2*np.pi*185*ts)*np.exp(-ts*22),250)
th=np.arange(int(.04*SR))/SR;hat=hp(rng.standard_normal(len(th))*np.exp(-th*100),7000)
m=pyln.Meter(SR)
def riser(end,L):
    n=int(L*SR);u=np.arange(n)/n;x=rng.standard_normal(n);fr=rfftfreq(4096,1/SR);y=np.zeros(n)
    for i in range(0,n,4096):
        c=300+7000*u[i]**2;seg=x[i:i+4096];y[i:i+len(seg)]=irfft(rfft(seg,4096)/np.sqrt(1+(fr/c)**4),4096)[:len(seg)]
    return place(y*u**2*0.25,[end-L])
if R["track"]==2:
    bars=np.arange(0,T,bar);drums=["build","drop A","drop B"];full=["drop A","drop B"]
    kt=np.array(sorted(list(bars)+[b+2.5*beat for b in bars[1::2]]));kon=np.interp(kt,t,env(drums,bar/4))
    K=place(kick,[]);K=sum(place(kick*g,[x]) for x,g in zip(kt,kon) if g>0.01)
    S=place(snare,bars+2*beat)*env(full,bar/4);H=place(hat,np.arange(0,T,beat/2)+beat/4)*0.25*env(drums+["outro"])
    since,_=kickhits(kt[kon>0.01],None);on=1.0;sc=R["sidechain"]
    roots=np.array([43.65,34.65,38.89,32.70]);f=roots[(t//(2*bar)).astype(int)%4];f=np.convolve(f,np.ones(600)/600,'same')
    sub=np.sin(2*np.pi*np.cumsum(f)/SR)*env(full+["build"])*0.9
    lfo=0.5-0.5*np.cos(2*np.pi*np.cumsum(np.where((t//(4*bar))%2==0,R["bpm"]/120,R["bpm"]/60))/SR)
    rz=saws(f*2,(-.006,0,.006));cuts=[160,320,520,760,1000];bank=np.array([lp(rz,c,3) for c in cuts]);pos=lfo*(len(cuts)-1);i0=np.minimum(pos.astype(int),len(cuts)-2);w=pos-i0;idx=np.arange(N)
    wob=np.tanh(2.2*(bank[i0,idx]*(1-w)+bank[i0+1,idx]*w))*(0.4+0.6*lfo)*env(full)*0.5;del bank
    wl=lp(wob,sc["wobbleLow"]["splitHz"],4);wh=wob-wl   # multiband sidechain on the reese
    wob=wl*duck(since,on,sc["wobbleLow"]["len"],sc["wobbleLow"]["depth"])+wh*duck(since,on,sc["wobbleHigh"]["len"],sc["wobbleHigh"]["depth"])
    sub*=duck(since,on,sc["sub"]["len"],sc["sub"]["depth"])
    chords=[[174.6,207.7,261.6],[138.6,174.6,207.7],[155.6,196.0,233.1],[130.8,164.8,196.0]]
    padL=np.zeros(N);padR=np.zeros(N)
    for ci,c in enumerate(chords):
        mk=np.convolve(((t//(2*bar))%4==ci).astype(float),np.hanning(20000)/np.hanning(20000).sum(),'same')
        for fq in c:padL+=mk*np.sin(2*np.pi*fq*.997*t+rng.random()*6);padR+=mk*np.sin(2*np.pi*fq*1.003*t+rng.random()*6)
    pe=env([n for n,_,_ in secs],2*bar)*0.1;dp=duck(since,on,sc["pad"]["len"],sc["pad"]["depth"]);padL*=pe*dp;padR*=pe*dp
    lead_notes=np.array([698.5,622.3,523.3,466.2,523.3,415.3,466.2,523.3]);lf=lead_notes[(t//beat).astype(int)%8]
    lg=np.where((t%beat)<beat*0.6,1,0.0);lg=np.convolve(lg,np.ones(300)/300,'same')
    lead=lp(saws(lf),2600)*lg*0.13*env(["drop B"])*duck(since,on,sc["lead"]["len"],sc["lead"]["depth"])
    I=R["iso"];fr_=(t*I["rateHz"])%1;g=np.clip(np.minimum(fr_,0.5-fr_)/0.075,0,1)*(fr_<0.5);g=0.5-0.5*np.cos(np.pi*g)
    iso=np.sin(2*np.pi*I["carrierHz"]*t)*g*env(I["sections"],2*bar)*db(I["relDb"])*0.5
    fx=riser(secs[2][1],8*bar)+riser(secs[4][1],4*bar)
    mono=K*0.9+S*0.5+H+sub*0.7+wob+lead+iso+fx
    L=mono+padL;Rr=mono+padR
else:
    pst,_=sf.read(R["pendulumStem"]);pst=pst[:N];pst=np.pad(pst,((0,N-len(pst)),(0,0)))
    roots=np.array([41.2,32.7,49.0,36.7]);f=roots[(t//(2*bar)).astype(int)%4];f=np.convolve(f,np.ones(600)/600,'same')
    beats=np.arange(0,T,beat);kt=np.array([b for b in beats if int(round(b/beat))%4 in (0,2) or int(round(b/beat))%8==7])
    dr=["verse","chorus","chorus 2"];kon=np.interp(kt,t,env(dr,bar/4));kt=kt[kon>0.3]
    K=sum(place(kick,[x]) for x in kt);S=place(snare,np.arange(beat,T,2*beat))*env(["chorus","chorus 2"],bar/4)*0.8
    H=place(hat,np.arange(0,T,beat/2)+beat/4)*0.2*env(dr)
    since,_=kickhits(kt,None);sc=R["sidechain"]
    bass=lp(saws(f*2),300)*0.6*env(dr)*duck(since,1,sc["bass"]["len"],sc["bass"]["depth"])
    # focus lead: formant (vocal-like) synth, phrases with pauses
    mel=np.array([329.6,392,440,493.9,440,392,370,329.6,293.7,329.6,392,329.6]);lf=mel[(t//(beat*2)).astype(int)%12]
    lf=np.convolve(lf,np.ones(1500)/1500,'same');ph=2*np.pi*np.cumsum(lf*(1+0.005*np.sin(2*np.pi*5*t)))/SR
    src=sum(np.sin(k*ph)/k for k in range(1,24))
    fq,_,Z=stft(src,SR,nperseg=2048);fm=np.exp(-0.5*((fq-650)/220)**2)+0.7*np.exp(-0.5*((fq-1150)/280)**2)+0.35*np.exp(-0.5*((fq-2500)/380)**2)
    voc=istft(Z*fm[:,None],SR,nperseg=2048)[1][:N];voc=np.pad(voc,(0,N-len(voc)))
    phr=((t%(4*bar))<3.25*bar).astype(float);phr=np.convolve(phr,np.hanning(4000)/np.hanning(4000).sum(),'same')
    voc*=phr*env(["verse","chorus","chorus 2","break"],bar)*np.where(env(["break"],bar)>0.5,0.6,1)
    voc=voc/np.sqrt((voc**2).mean()+1e-12)*0.12
    chords=[[164.8,196,246.9],[130.8,164.8,196],[196,246.9,293.7],[146.8,185,220]]
    padL=np.zeros(N);padR=np.zeros(N)
    for ci,c in enumerate(chords):
        mk=np.convolve(((t//(2*bar))%4==ci).astype(float),np.hanning(20000)/np.hanning(20000).sum(),'same')
        for fqq in c:padL+=mk*lp(saws(np.full(N,fqq),(-.005,.002)),1800)*0.5;padR+=mk*lp(saws(np.full(N,fqq),(.005,-.002)),1800)*0.5
    pe=env([n for n,_,_ in secs],2*bar)*0.09;padL*=pe;padR*=pe
    arp=pst*db(6)*env(["intro","verse","chorus","break","chorus 2"],bar)[:,None]*duck(since,1,sc["arp"]["len"],sc["arp"]["depth"])[:,None]
    # --- the new technique: dynamic EQ on arp + pad keyed by the focus lead, mid only
    _,_,VZ=stft(voc,SR,nperseg=2048);ke=uniform_filter(np.abs(VZ),(9,3));ke=ke/(np.percentile(ke,99.5)+1e-12)
    G=db(-R["dynEq"]["maxCutDb"]*np.clip(ke*3,0,1))
    def dyn(x):_,_,X=stft(x,SR,nperseg=2048);y=istft(X*G,SR,nperseg=2048)[1][:N];return np.pad(y,(0,N-len(y)))
    sL=arp[:,0]+padL;sR=arp[:,1]+padR;Mi=dyn((sL+sR)/2);Si=(sL-sR)/2
    fx=riser(secs[2][1],4*bar)+riser(secs[4][1],4*bar)
    mono=K*0.85+S*0.45+H+bass+voc+fx
    L=mono+Mi+Si;Rr=mono+Mi-Si
mix=np.stack([L,Rr],1);mid=mix.mean(1);side=(mix[:,0]-mix[:,1])/2;side=hp(side,120,4);mix=np.stack([mid+side,mid-side],1)  # mono lows
mix*=np.minimum(1,np.minimum(t/0.5,(T-t)/4))[:,None];mix-=mix.mean(0)
mix*=db(R["targetLufs"]-m.integrated_loudness(mix))
def tp(x):F=rfft(x,axis=0);return 20*np.log10(np.abs(irfft(np.concatenate([F,np.zeros((3*len(F),2))]),4*len(x),axis=0)*4).max())
c=db(R["peakCeilDb"]-0.3);k=0.6*c;a_=np.abs(mix);mix=np.where(a_>k,np.sign(mix)*(k+(c-k)*np.tanh((a_-k)/(c-k))),mix)  # soft-knee clipper
mix*=db(R["targetLufs"]-m.integrated_loudness(mix));p=tp(mix)
if p>R["peakCeilDb"]:mix*=db(R["peakCeilDb"]-p-0.05)
sf.write(OUT,mix.astype(np.float32),SR,subtype="PCM_24")
Fm=np.abs(rfft(mix.mean(1)))**2;ff=rfftfreq(N,1/SR)
print(json.dumps(dict(name=R["name"],lengthSec=round(T,1),lufs=round(m.integrated_loudness(mix),2),truePeakDb=round(tp(mix),2),clipped=int((np.abs(mix)>=0.999).sum()),
 below120Pct=round(100*Fm[ff<120].sum()/Fm.sum(),1),mid120_500Pct=round(100*Fm[(ff>=120)&(ff<500)].sum()/Fm.sum(),1),above6kPct=round(100*Fm[ff>6000].sum()/Fm.sum(),2),sections=[(n,round(s,1)) for n,s,_ in secs])))
