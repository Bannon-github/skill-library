import json,sys,numpy as np,soundfile as sf
from numpy.fft import rfft,irfft,rfftfreq
R=json.load(open(sys.argv[1])); wav=sys.argv[2]; SR=48000
x,_=sf.read(wav,dtype='float32'); x=x.mean(1).astype(np.float64); fc=R["iso"]["carrierHz"]
pts=np.array(R["rate"],float)
def tr(tt):
    i=np.clip(np.searchsorted(pts[:,0],tt,side='right')-1,0,len(pts)-2); u=np.clip((tt-pts[i,0])/(pts[i+1,0]-pts[i,0]),0,1); return pts[i,1]+(pts[i+1,1]-pts[i,1])*(0.5-0.5*np.cos(np.pi*u))
res=[]
for lo,hi in [(240,290),(370,395),(520,600)]:
    seg=x[(lo-1)*SR:(hi+1)*SR]; F=rfft(seg); ff=rfftfreq(len(seg),1/SR)
    band=np.abs(irfft(np.where((ff>fc*0.9)&(ff<fc*1.1),F,0),len(seg))); k=int(SR*0.01); sm=np.convolve(band,np.ones(k)/k,'same')
    for a in np.arange(lo,hi-3,4):
        s=sm[int((a-lo+1)*SR):int((a-lo+5)*SR)]; s=s-s.mean(); S=np.abs(rfft(s*np.hanning(len(s)),16*len(s))); q=rfftfreq(16*len(s),1/SR); m=(q>3)&(q<25)
        pe=q[m][S[m].argmax()]; mt=(abs(q-tr(np.arange(a,a+4,0.01)).mean())<0.6); pt=q[mt][S[mt].argmax()]; prom=20*np.log10(S[mt].max()/np.median(S[m])); tg=tr(np.arange(a,a+4,0.01)).mean(); res.append((float(a),round(float(pt),2),round(float(prom),1),round(float(tg),2),round(abs(pt-tg),2)))
for r in res: print(r)
print("max err",max(r[4] for r in res))
