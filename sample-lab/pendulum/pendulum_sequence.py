#!/usr/bin/env python3
"""Pendulum-wave arpeggio generator (pattern idea from Virtual Riot 'Pendulum Sequence 2'; original synthesis).
usage: pendulum_sequence.py recipe.json out.wav [--iso] -> out.wav, out.mid, out.wav.stats.json"""
import json,sys,struct,numpy as np,soundfile as sf,pyloudnorm as pyln
from numpy.fft import rfft,irfft,rfftfreq
R=json.load(open(sys.argv[1]));OUT=sys.argv[2];ISO="--iso" in sys.argv or R["isochronic"]["enabled"]
SR=44100;T=R["lengthSec"];N=int(T*SR);rng=np.random.default_rng(R["seed"]);db=lambda x:10**(x/20)
NM={"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}
midi=lambda s:12*(int(s[-1])+1)+NM[s[:-1]]
pitches=[midi(x) for x in R["lanes"]]   # top lane first (as in the piano roll)
L=len(pitches);spb=60/R["bpm"];f0=1/(R["topPeriodBeats"]*spb);Nc=R["cyclesPerRealign"];TR=Nc/f0
periods=np.array([1/(f0*(Nc-i)/Nc) for i in range(L)]);T0=R["patternStartSec"]
def lane_on(i,tm):
    for s in R["sections"]:
        if s["start"]<=tm<s["end"]: return i%s["laneEvery"]==0, s["gainDb"]
    return False,0
events=[]  # (time, lane, pitch, gainDb)
for i,p in enumerate(pitches):
    k0=np.ceil(T0/periods[i]);
    for tm in np.arange(k0*periods[i]-T0+i*R["staircaseOffsetSec"],T,periods[i]):
        on,g=lane_on(i,tm)
        if on: events.append((float(tm),i,p,g))
# ---- voice: precompute one note per (pitch, layer), saw stack (bandlimited by FFT lowpass)
V=R["voice"];ly=R["layers"];nl=int(R["noteLenFrac"]*periods.mean()*SR);tn=np.arange(nl)/SR;fN=rfftfreq(nl,1/SR)
envn=np.minimum(1,tn/(V["attackMs"]/1000))*np.exp(-tn*V["decay"]);envn[-200:]*=np.linspace(1,0,200)
lpm=1/np.sqrt(1+(fN/V["lowpassHz"])**4)
def note(m,cents):
    f=440*2**((m-69)/12)*2**(cents/1200);x=0
    for k in range(V["saws"]):
        d=(k-(V["saws"]-1)/2)*V["sawDetuneCents"]/max(1,V["saws"]-1)*2;fk=f*2**(d/1200)
        x=x+2*((tn*fk+rng.random())%1)-1
    x=irfft(rfft(x)*lpm*(fN<SR/2-2000),nl);return x*envn/V["saws"]
mix=np.zeros((N+nl,2))
offs=rng.uniform(-1,1,ly["count"])*ly["offsetMs"]/1000;dets=np.linspace(-1,1,ly["count"])*ly["detuneCents"]
pans=0.5+np.linspace(-1,1,ly["count"])*ly["panSpread"]/2;rng.shuffle(pans)
vel=lambda i:db(V["velocityTopDb"]+(V["velocityBottomDb"]-V["velocityTopDb"])*i/max(1,L-1))
for j in range(ly["count"]):
    cache={p:note(p,dets[j]) for p in pitches};gl,gr=np.cos(np.pi/2*pans[j]),np.sin(np.pi/2*pans[j])
    for tm,i,p,g in events:
        a=int(max(0,tm+offs[j])*SR);s=cache[p]*vel(i)*db(g);mix[a:a+nl,0]+=s*gl;mix[a:a+nl,1]+=s*gr
mix=mix[:N]/ly["count"]
# ---- space: short multitap cross-delay (vectorised)
sp=R["space"];wet=np.zeros_like(mix)
for k,dm in enumerate(sp["delayMs"]):
    d=int(dm*SR/1000);src=mix[:,::-1] if k%2 else mix;wet[d:]+=src[:-d]*sp["feedback"]**k
wet=np.stack([irfft(rfft(wet[:,c])/np.sqrt(1+(rfftfreq(N,1/SR)/1800)**4),N) for c in range(2)],1)
mix=mix+wet*sp["wet"]
if ISO:
    I=R["isochronic"];t=np.arange(N)/SR;fr=(t*I["rateHz"])%1;d,e=I["duty"],I["edgeFrac"];g=(fr<d).astype(float)
    u=fr<e;g[u]=0.5-0.5*np.cos(np.pi*fr[u]/e);dn=(fr>=d-e)&(fr<d);g[dn]=0.5-0.5*np.cos(np.pi*(d-fr[dn])/e)
    pl=np.sin(2*np.pi*I["carrierHz"]*t)*g*np.minimum(1,np.minimum(t/8,(T-t)/8));rms=np.sqrt((mix**2).mean())
    mix+=(pl*rms/np.sqrt((pl**2).mean())*db(I["relDb"]))[:,None]
t=np.arange(N)/SR;mix*=np.minimum(1,np.minimum(t/2,(T-t)/6))[:,None];mix-=mix.mean(0)
meter=pyln.Meter(SR);mix*=db(R["targetLufs"]-meter.integrated_loudness(mix))
def tp(x):
    F=rfft(x,axis=0);return 20*np.log10(np.abs(irfft(np.concatenate([F,np.zeros((3*len(F),2))]),4*len(x),axis=0)*4).max())
p=tp(mix)
if p>R["peakCeilDb"]:
    c=db(R["peakCeilDb"]-0.2)/db(p)*1.0;k=db(R["peakCeilDb"]-0.3)
    mix=np.where(np.abs(mix)>0.6*k,np.sign(mix)*(0.6*k+0.4*k*np.tanh((np.abs(mix)-0.6*k)/(0.4*k))),mix)
    p=tp(mix)
    if p>R["peakCeilDb"]: mix*=db(R["peakCeilDb"]-p-0.05)
sf.write(OUT,mix.astype(np.float32),SR,subtype="PCM_24")
# ---- MIDI (SMF type 0, by hand): layer 0 timing, 480 tpq at bpm
tpq=480;ev=[]
for tm,i,p,g in events:
    v=int(np.clip(100*vel(i)*db(g),1,127));ev+=[(round(tm/spb*tpq),1,p,v),(round((tm+R["noteLenFrac"]*periods[0])/spb*tpq),0,p,0)]
ev.sort(key=lambda e:(e[0],e[1]))
def vlq(n):
    b=[n&127];n>>=7
    while n:b.insert(0,(n&127)|128);n>>=7
    return bytes(b)
us=int(spb*1e6);trk=b"\x00\xff\x51\x03"+us.to_bytes(3,"big");last=0
for tk,on,p,v in ev: trk+=vlq(tk-last)+bytes([0x90 if on else 0x80,p,v]);last=tk
trk+=b"\x00\xff\x2f\x00"
open(OUT.rsplit(".",1)[0]+".mid","wb").write(b"MThd"+struct.pack(">IHHH",6,0,1,tpq)+b"MTrk"+struct.pack(">I",len(trk))+trk)
S=lambda x:float(np.sqrt((x**2).mean()))
F=np.abs(rfft(mix.mean(1)))**2;ff=rfftfreq(N,1/SR)
st=dict(lengthSec=T,lanes=L,pitchRange=[pitches[0],pitches[-1]],events=len(events),notesPerSecFull=round(sum(1/periods),1),
 lufs=round(meter.integrated_loudness(mix),2),truePeakDb=round(tp(mix),2),clipped=int((np.abs(mix)>=0.999).sum()),
 sideVsMidDb=round(20*np.log10(S(mix[:,0]-mix[:,1])/S(mix[:,0]+mix[:,1])),1),energyAbove6kPct=round(100*F[ff>6000].sum()/F.sum(),3),
 iso=ISO,realignSec=TR,realignInDemoSec=[float(TR*k-T0) for k in range(1,3) if 0<TR*k-T0<T])
json.dump(st,open(OUT+".stats.json","w"),indent=1,default=float);print(json.dumps(st,default=float))
