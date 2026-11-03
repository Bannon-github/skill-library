"""Rhythm: straight vs swung 16ths (swing delays every 2nd 16th; 50%=straight, 66%=triplet swing),
polyrhythms 3:2 and 4:3 (two pulse streams sharing a bar), Euclidean E(3,8) tresillo, E(5,8) cinquillo, E(7,16)."""
from core import *
def click(f,dec=.03): tt=t(.08); return np.sin(2*np.pi*f*tt)*np.exp(-tt/dec)
def euclid(k,n): return [1 if (i*k)%n<k else 0 for i in range(n)]
bpm=100; beat=60/bpm; out=[]
for sw in (.5,.58,.66):
    b=np.zeros(int(4*beat*SR)+SR//4)
    for i in range(16):
        pos=(i//2)*beat/2 + (sw*beat/2 if i%2 else 0)
        place(b, click(6000,.01)*(1 if i%2==0 else .6), pos)
    for i in range(4): place(b, click(60,.15), i*beat)
    out.append(b)
for a,c in ((3,2),(4,3)):
    bar=2.0; b=np.zeros(int(2*bar*SR)+SR//4)
    for rep in range(2):
        for i in range(a): place(b, click(880), rep*bar+i*bar/a)
        for i in range(c): place(b, click(330), rep*bar+i*bar/c)
    out.append(b)
for k,n in ((3,8),(5,8),(7,16)):
    pat=euclid(k,n); step=beat*4/n; b=np.zeros(int(2*4*beat*SR)+SR//4)
    for rep in range(2):
        for i,h in enumerate(pat):
            place(b, click(1200 if h else 4000, .03 if h else .005)*(1 if h else .2), rep*4*beat+i*step)
    out.append(b)
write("rhythm_polyrhythm", np.concatenate(out), "swing 50/58/66%, 3:2, 4:3, E(3,8) E(5,8) E(7,16)")
