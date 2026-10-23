#!/usr/bin/env python3
"""Flow State v2: sectioned arrangement (intro/build/mainA/breakdown/mainB/outro) over isochronic+binaural. Original sound.
Arrangement logic follows library skills: hybrid-score role-first layering (staggered entry), one-bar transition riser,
reverse-reverb swell, sub-drop sine glide, plus today's isochronic/binaural skills (rate automation, fades, ratio-locked octaves, carrier notch)."""
import json,sys,os,numpy as np,soundfile as sf,pyloudnorm as pyln
from numpy.fft import rfft,irfft,rfftfreq
R=json.load(open(sys.argv[1])); OUT=sys.argv[2]; SR=48000; T=R["lengthSec"]; N=int(T*SR); t=np.arange(N)/SR
rng=np.random.default_rng(R["seed"]); db=lambda x:10**(x/20); f32=np.float32
def ease(points,tt,db_mode=False):
    p=np.array([(a,(-200 if v is None else v)) for a,v in points],float); xs,ys=p[:,0],p[:,1]
    if db_mode: ys=np.where(ys<=-120,0.0,10**(ys/20))
    i=np.clip(np.searchsorted(xs,tt,side='right')-1,0,len(xs)-2); u=np.clip((tt-xs[i])/(xs[i+1]-xs[i]),0,1); e=0.5-0.5*np.cos(np.pi*u)
    return ys[i]+(ys[i+1]-ys[i])*e
# ---- rate arc (cosine-eased, then 10 ms smoothing per isochronic skill)
rate=ease(R["rate"],t); k=int(0.01*SR); rate=np.convolve(rate,np.ones(k)/k,'same')
phase=np.cumsum(rate)/SR; frac=phase%1.0; iso=R["iso"]; duty,edge=iso["duty"],iso["edgeFrac"]
g=(frac<duty).astype(float); up=frac<edge; g[up]=0.5-0.5*np.cos(np.pi*frac[up]/edge)
dn=(frac>=duty-edge)&(frac<duty); g[dn]=0.5-0.5*np.cos(np.pi*(duty-frac[dn])/edge); del frac,up,dn
fc=iso["carrierHz"]; ph_c=2*np.pi*fc*t
def pulse_layer(f0,gain): return (np.sin(2*np.pi*f0*t)+0.1*np.sin(4*np.pi*f0*t))*g*gain
P=pulse_layer(fc,1.0)
for ratio,lvl in iso.get("octaves",[]): P=P+pulse_layer(fc*ratio,db(lvl))*ease(iso["octaveGateDb"],t,True)   # 1:1 ratio-locked octave pulses
pulse_env=ease(iso["levelAutomationDb"],t,True)
b=R["binaural"]; B_L=np.sin(ph_c); B_R=np.sin(ph_c+2*np.pi*phase)   # left = carrier, right = carrier+beat (skill form)
bin_env=ease(b["levelAutomationDb"],t,True)
# ---- bed layers
def lowpass(x,hz,order=2):
    F=rfft(x,axis=0); f=rfftfreq(len(x),1/SR); F*=(1/np.sqrt(1+(f/hz)**(2*order)))[:,None].astype(f32); return irfft(F,len(x),axis=0).astype(f32)
def loop_segment(files,trim,xf_s,n,octave=False):
    segs=[]
    for p in files:
        s,_=sf.read(p,dtype='float32'); s=s[int(trim[0]*SR):int(trim[1]*SR)]
        if octave: s=np.stack([np.interp(np.arange(0,len(s)-1,2),np.arange(len(s)),s[:,c]) for c in range(2)],1).astype(f32)
        segs.append(s)
    xf=int(xf_s*SR); ramp=np.sin(0.5*np.pi*np.arange(xf)/xf).astype(f32); out=np.zeros((n,2),f32); pos=0;i=0;seams=[]
    while pos<n:
        s=segs[i%len(segs)].copy(); m=len(s); w=np.ones(m,f32)
        if i>0:w[:xf]=ramp
        w[-xf:]=ramp[::-1]; s*=w[:,None]; e=min(n,pos+m); out[pos:e]+=s[:e-pos]
        if i>0: seams.append(pos)
        pos+=m-xf; i+=1
    return out,seams
seam_log=[]  # (time s, kind, layer)
def build_layer(L):
    out=np.zeros((N,2),f32); ov=L.get("overlapSec",6)
    for sg in L["segments"]:
        a=max(0,int((sg["start"]-ov/2)*SR)); e=min(N,int((sg["end"]+ov/2)*SR)); n=e-a
        x,sm=loop_segment([os.path.expandvars(p) for p in sg["files"]],sg["trim"],sg["xfadeSec"],n,L.get("octave",False))
        w=np.ones(n,f32); m=int(ov*SR)
        if sg["start"]>0: w[:m]=np.sin(0.5*np.pi*np.arange(m)/m)
        if sg["end"]<T: w[-m:]=np.cos(0.5*np.pi*np.arange(m)/m)
        out[a:e]+=x*w[:,None]
        seam_log.extend([((a+s)/SR+sg["xfadeSec"]/2,"loop-crossfade",L["name"]) for s in sm])
        if sg["start"]>0: seam_log.append((sg["start"],"segment-change",L["name"]))
    if L.get("lpHz"): out=lowpass(out,L["lpHz"])
    return out*f32(db(L["levelDb"]))*ease(L["gainAutomationDb"],t,True).astype(f32)[:,None]
bed=np.zeros((N,2),f32); stems={}
for L in R["layers"]:
    x=build_layer(L); stems[L["name"]]=float(np.sqrt((x**2).mean())); bed+=x; del x
# soft pink noise bed with slow auto-pan (skill: noise atmosphere, panned)
nz=np.zeros((N,2),f32); f=rfftfreq(N,1/SR)
for c in range(2):
    F=rfft(rng.standard_normal(N)); F/=np.sqrt(np.maximum(f,20)); F/=1+(f/R["noise"]["lpHz"])**2; nz[:,c]=irfft(F,N)
nz/=np.abs(nz).max(); pan=0.5+0.4*np.sin(2*np.pi*t/R["noise"]["panPeriodSec"]); nz[:,0]*=np.cos(0.5*np.pi*pan); nz[:,1]*=np.sin(0.5*np.pi*pan)
# notch on bed at carrier (binaural-meditation skill: narrow cut so bed does not mask carrier)
def notch(x,f0,bw=10.0,depth_db=-28):
    F=rfft(x,axis=0); ff=rfftfreq(len(x),1/SR); m=1-(1-db(depth_db))*np.exp(-0.5*((ff-f0)/bw)**2); F*=m[:,None].astype(f32); return irfft(F,len(x),axis=0).astype(f32)
for f0 in (fc,) + tuple(fc*r for r,_ in iso.get("octaves",[])): bed=notch(bed,f0)
bedr=float(np.sqrt((bed**2).mean()))
nz_env=ease(R["noise"]["gainAutomationDb"],t,True).astype(f32)
bed+=nz*f32(bedr*db(R["noise"]["relDb"]))*nz_env[:,None]; del nz
# ---- pulse mix: level relative to the bed RMS *in the mid sections* then automated
mono_ref=np.sqrt((P**2).mean()); Pst=np.stack([P*pulse_env,P*pulse_env],1)
pl=Pst*(bedr/mono_ref*db(iso["relDbUnderBed"])); del Pst
pulse_stereo=pl.astype(f32); del pl
bs=np.stack([B_L,B_R],1)*bin_env[:,None]*(bedr/mono_ref*db(iso["relDbUnderBed"])*b["level"]); pulse_stereo+=bs.astype(f32); del bs,B_L,B_R,P
mix=bed+pulse_stereo; del bed
# ---- transitions: riser (one-bar skill), reverse-reverb swell, sub drop
def conv(x,ir):
    n=len(x)+len(ir)-1; M=1<<(n-1).bit_length(); return irfft(rfft(x,M)*rfft(ir,M),M)[:n]
def make_ir(sec,lp=3500):
    n=int(sec*SR); tt=np.arange(n)/SR; ir=rng.standard_normal(n)*np.exp(-tt*6.9/sec); F=rfft(ir); ff=rfftfreq(n,1/SR); F/=1+(ff/lp)**2; ir=irfft(F,n); return ir/np.abs(ir).sum()*8
def place(sig,start,gain_db):
    a=int(start*SR); e=min(N,a+len(sig)); mix[a:e]+=(sig[:e-a]*db(gain_db)).astype(f32)
rr=R["riser"]; Lr=int(rr["lengthSec"]*SR); tr=np.arange(Lr)/SR; u=tr/rr["lengthSec"]; curve=u**2.2
nzr=rng.standard_normal(Lr); pk=np.zeros(Lr); s1=s2=0.0  # SVF sweep (resonant band-pass), cutoff opens with the timeline
fcs=2*np.sin(np.pi*(rr["fHz"][0]+(rr["fHz"][1]-rr["fHz"][0])*curve)/SR); q=1/ rr["q"]
for i in range(Lr):
    hp=nzr[i]-s1*q-s2; s1+=fcs[i]*hp; s2+=fcs[i]*s1; pk[i]=s1
pk/=np.abs(pk).max(); pk*=curve; 
saw=sum(((2*((tr*rr["sawHz"]*(2**(c/1200)))%1)-1)) for c in (-9,0,9))/3; saw=np.convolve(saw,np.ones(60)/60,'same')*curve*0.35
mono=pk+saw; pan=u; ris=np.stack([mono*np.cos(0.5*np.pi*pan),mono*np.sin(0.5*np.pi*pan)],1)
ris*= np.minimum(1,(Lr-np.arange(Lr))/int(0.01*SR))[:,None]       # safety drop at the end of the timeline
tail=np.stack([conv(ris[:,c],make_ir(rr["tailSec"])) for c in range(2)],1); tail=tail[Lr:]; tail=tail*np.minimum(1,np.arange(len(tail))/(0.6*SR))[:,None]  # ducked: blooms only after riser cuts
start=rr["endAt"]-rr["lengthSec"]; place(ris,start,rr["gainDb"]+20*np.log10(bedr)); place(tail,rr["endAt"],rr["gainDb"]-4+20*np.log10(bedr))
sw=R["revSwell"]; src=None
src,_=sf.read(os.path.expandvars(sw["sourceFile"]),dtype='float32'); src=src[int(sw["sourceTrim"][0]*SR):int(sw["sourceTrim"][1]*SR)]; src=lowpass(src,sw["lpHz"])
ir=make_ir(sw["irSec"],3000); swell=np.stack([conv(src[::-1,c],ir)[::-1] for c in range(2)],1)[:len(ir)]   # reverse -> 100% wet print -> re-reverse; keep the lead-in before the onset
swell*=np.sin(0.5*np.pi*np.minimum(1,np.arange(len(swell))/(0.8*sw["irSec"]*SR)))[:,None]**2; swell[-int(0.02*SR):]*=np.linspace(1,0,int(0.02*SR))[:,None]
swell*=1.0/np.abs(swell).max()*bedr*db(sw["gainDbRelBed"])*3
place(swell,sw["endAt"]-len(swell)/SR,0)
sd=R["subDrop"]; Ls=int(sd["lengthSec"]*SR); ts=np.arange(Ls)/SR; fq=sd["hz"][0]*(sd["hz"][1]/sd["hz"][0])**(ts/sd["lengthSec"]); sine=np.sin(2*np.pi*np.cumsum(fq)/SR)
sine*=np.minimum(1,ts/0.4)*np.minimum(1,(sd["lengthSec"]-ts)/1.5); place(np.stack([sine,sine],1)*bedr*db(sd["gainDbRelBed"])*1.4,sd["startAt"],0)
# ---- mono lows (<120 Hz side removed, smooth), DC, master fades
mid=(mix[:,0]+mix[:,1])/2; side=(mix[:,0]-mix[:,1])/2; del mix
F=rfft(side); F*=(1/(1+(120/np.maximum(f,1e-3))**4)).astype(f32); side=irfft(F,N).astype(f32); del F
mix=np.stack([mid+side,mid-side],1).astype(f32); del mid,side
mix-=mix.mean(0)
mix*=ease(R["masterFadeDb"],t,True).astype(f32)[:,None]
meter=pyln.Meter(SR); lu=meter.integrated_loudness(mix.astype(np.float64)); mix*=f32(db(R["targetLufs"]-lu))
def tp(x,ch=480000):
    m=0.0
    for a in range(0,len(x),ch):
        seg=x[max(0,a-2400):a+ch+2400].astype(np.float64)
        for c in range(2):
            F=rfft(seg[:,c]); m=max(m,np.abs(irfft(np.concatenate([F,np.zeros(3*len(F),complex)]),4*len(seg))*4).max())
    return 20*np.log10(m)
p=tp(mix); lim=R["peakCeilDb"]; capped=False
if p>lim: mix*=f32(db(lim-p-0.05)); capped=True
sf.write(OUT,mix,SR,subtype="PCM_24")
# ---------- verification
x=mix.astype(np.float64).mean(1); bandF=rfft(x); ff=rfftfreq(N,1/SR)
band=np.abs(irfft(np.where(((ff>fc*0.9)&(ff<fc*1.1)),bandF,0),N)); k=int(SR*0.01); sm=np.convolve(band,np.ones(k)/k,'same'); del bandF
W=R.get("checkWinSec",10); meas=[]
for a in range(0,int(T)-W+1,W):
    s=sm[a*SR:(a+W)*SR]; s=s-s.mean(); S=np.abs(rfft(s*np.hanning(len(s)),8*len(s))); fq_=rfftfreq(8*len(s),1/SR); m=(fq_>3)&(fq_<25)
    pe=float(fq_[m][S[m].argmax()]); tgt=float(rate[a*SR:(a+W)*SR].mean()); pg=float(20*np.log10(pulse_env[a*SR:(a+W)*SR].mean()+1e-9))
    meas.append(dict(t0=a,t1=a+W,measuredHz=round(pe,2),targetHz=round(tgt,2),errHz=round(abs(pe-tgt),2),pulseGainDb=round(pg,1)))
active=[m for m in meas if m["pulseGainDb"]>-12]
hop=int(0.1*SR); bm=mix[:,0].astype(np.float64)+mix[:,1]
fr=np.array([np.log10(np.abs(rfft(bm[i:i+hop]*np.hanning(hop)))+1e-9) for i in range(0,N-hop,hop)])
flux=np.r_[0,np.sqrt(((np.diff(fr,axis=0))**2).mean(1))]; med=float(np.median(flux)); loc=lambda s:flux[max(0,int(s/0.1)-8):int(s/0.1)+8].max()/med
loops=[loc(s) for s,k_,_ in seam_log if k_=="loop-crossfade" and s<T-2]; segs=[(round(s,1),n,round(float(loc(s)),2)) for s,k_,n in seam_log if k_=="segment-change"]
bounds=[round(float(loc(s)),2) for s in (R["sectionBoundaries"])]
cent=lambda a:float((np.abs(rfft(x[a*SR:a*SR+SR*10]))*rfftfreq(SR*10,1/SR)).sum()/np.abs(rfft(x[a*SR:a*SR+SR*10])).sum())
lowF=rfft(mix[:,0].astype(np.float64)-mix[:,1]); lowM=rfft(mix[:,0].astype(np.float64)+mix[:,1]); lo=ff<120
sections=[]
for s in R["sections"]:
    a,e=int(s["start"]*SR),int(s["end"]*SR); seg=mix[a:e].astype(np.float64)
    sections.append(dict(section=s["name"],time=f'{int(s["start"]//60)}:{int(s["start"]%60):02d}-{int(e/SR//60)}:{int(e/SR%60):02d}',layers=s["layers"],rateHz=s["rateText"],
        lufsShortTerm=round(meter.integrated_loudness(seg),1) if e-a>SR*5 else None,skills=s["skills"]))
mp=lambda a,b:20*np.log10(np.abs(mix[int(a*SR):int(b*SR)]).max()+1e-12)
out=dict(lengthSec=T,targetLufs=R["targetLufs"],lufs=round(meter.integrated_loudness(mix.astype(np.float64)),2),truePeakDb=round(tp(mix),2),peakCapped=capped,
 clipped=int((np.abs(mix)>=0.999).sum()),maxSampleStep=round(float(np.abs(np.diff(mix,axis=0)).max()),4),first2msPeakDb=round(mp(0,0.002),1),last100msRmsDb=round(10*np.log10((mix[-4800:].astype(np.float64)**2).mean()+1e-20),1),
 gateEdgeMsAtMaxRate=round(1000*edge/rate.max(),1),pulseRelDbUnderBed=iso["relDbUnderBed"],centroidHz={"2:00":round(cent(120)),"5:00":round(cent(300)),"6:30":round(cent(390)),"8:00":round(cent(480))},
 lowSideEnergyRatioBelow120Hz=round(float((np.abs(lowF[lo])**2).sum()/(np.abs(lowM[lo])**2).sum()),5),
 rate=dict(windowSec=W,activeWindows=len(active),maxAbsErrHzActive=max(m["errHz"] for m in active),meanAbsErrHzActive=round(float(np.mean([m["errHz"] for m in active])),3),windows=meas),
 seams=dict(loopCrossfades=len(loops),loopFluxMaxVsMedian=round(float(max(loops)),2),globalFlux99VsMedian=round(float(np.percentile(flux,99)/med),2),segmentChanges=segs,sectionBoundaryFluxVsMedian=dict(zip([str(s) for s in R["sectionBoundaries"]],bounds)),
   note="loop crossfades = repeated-loop joins inside a section (should be ~1x median); segment changes and section boundaries are intentional layer/chord changes"),
 sectionMap=sections,layerRmsDb={k:round(20*np.log10(v+1e-12),1) for k,v in stems.items()})
json.dump(out,open(OUT+".stats.json","w"),indent=1,default=float)
print(json.dumps({k:v for k,v in out.items() if k not in("rate","sectionMap")},indent=1,default=float)); print({k:v for k,v in out["rate"].items() if k!="windows"})
for m in meas: print(m)
