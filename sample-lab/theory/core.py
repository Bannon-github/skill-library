"""Shared DSP helpers for the music-theory sample generators (numpy/scipy only)."""
import numpy as np, soundfile as sf, sys
from pathlib import Path
from scipy.signal import lfilter, butter, sosfilt
SR = 44100
OUT = Path(__file__).parent / "out"

def t(sec): return np.arange(int(sec*SR))/SR
def midi(n): return 440.0*2**((n-69)/12)
def sine(f, sec, ph=0): 
    f=np.broadcast_to(np.asarray(f,float),(int(sec*SR),)); return np.sin(2*np.pi*np.cumsum(f)/SR+ph)
def saw(f, sec, nh=None):
    """Band-limited additive saw: sum 1/n * sin(n w t)."""
    f0=float(np.max(f)); nh=nh or int((SR/2)/f0)
    ph=2*np.pi*np.cumsum(np.broadcast_to(np.asarray(f,float),(int(sec*SR),)))/SR
    return (2/np.pi)*sum(((-1)**(n+1))*np.sin(n*ph)/n for n in range(1,nh+1))
def adsr(sec, a=.01, d=.1, s=.7, r=.2):
    n=int(sec*SR); e=np.zeros(n); A,D,R=int(a*SR),int(d*SR),int(r*SR); S=max(n-A-D-R,0)
    seg=np.concatenate([np.linspace(0,1,A,endpoint=False),np.linspace(1,s,D,endpoint=False),np.full(S,s),np.linspace(s,0,R)])
    e[:min(n,len(seg))]=seg[:n]; return e
def svf(x, fc, q=0.707, mode="lp"):
    """Chamberlin/TPT state-variable filter with per-sample cutoff (array or float)."""
    fc=np.broadcast_to(np.asarray(fc,float),x.shape); g=np.tan(np.pi*np.clip(fc,10,SR*0.45)/SR); k=1/q
    ic1=ic2=0.0; y=np.empty_like(x)
    for i in range(len(x)):
        gi=g[i]; a1=1/(1+gi*(gi+k)); v3=x[i]-ic2; v1=a1*ic1+gi*a1*v3; v2=ic2+gi*v1
        ic1=2*v1-ic1; ic2=2*v2-ic2
        y[i]= v2 if mode=="lp" else (v1 if mode=="bp" else x[i]-k*v1-v2)
    return y
def hp(x, fc, order=2): return sosfilt(butter(order, fc, 'hp', fs=SR, output='sos'), x)
def lp(x, fc, order=2): return sosfilt(butter(order, fc, 'lp', fs=SR, output='sos'), x)
def bp(x, lo, hi, order=2): return sosfilt(butter(order, [lo,hi], 'bp', fs=SR, output='sos'), x)
def delay(x, sec, fb=0.4, mix=0.3):
    d=int(sec*SR); y=np.copy(x); buf=np.zeros(len(x)+d)
    out=np.zeros(len(x))
    for i in range(len(x)):
        w=buf[i]; out[i]=w; buf[i+d]+= x[i]+w*fb
    return x*(1-mix)+out*mix
def reverb(x, sec=2.5, mix=0.3, seed=1):
    """Exponentially decaying noise IR convolution (simple algorithmic room)."""
    r=np.random.default_rng(seed); n=int(sec*SR); ir=r.standard_normal(n)*np.exp(-6.9*np.arange(n)/n)
    ir=lp(ir,8000); ir/=np.sqrt(np.sum(ir**2))
    w=np.convolve(x, ir)[:len(x)] if x.ndim==1 else np.stack([np.convolve(x[:,c], np.roll(ir,c*37))[:len(x)] for c in range(x.shape[1])],1)
    return x*(1-mix)+w*mix
def place(buf, x, at):
    i=int(at*SR); j=min(len(buf), i+len(x)); buf[i:j]+=x[:j-i]; return buf
def stereo(x, pan=0.0):
    return np.stack([x*np.cos((pan+1)*np.pi/4), x*np.sin((pan+1)*np.pi/4)],1)
def centroid(x):
    m=x.mean(1) if x.ndim>1 else x; S=np.abs(np.fft.rfft(m)); f=np.fft.rfftfreq(len(m),1/SR); return float((S*f).sum()/max(S.sum(),1e-9))
def rms_db(x): return 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def write(name, x, notes=""):
    OUT.mkdir(exist_ok=True); x=np.asarray(x,float); peak=np.max(np.abs(x)) or 1
    x=x/peak*0.89; p=OUT/f"{name}.wav"; sf.write(p, x, SR, subtype="PCM_16")
    print(f"[ok] {p.name} {len(x)/SR:.1f}s centroid={centroid(x):.0f}Hz {notes}"); return p
