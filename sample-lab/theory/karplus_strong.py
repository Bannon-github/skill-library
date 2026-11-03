"""Physical modelling: Karplus-Strong pluck. A noise burst excites a delay line of length SR/f; a 2-tap average
low-pass in the loop makes high harmonics decay faster (like a real string). Brightness of the excitation
(filtered vs raw noise) = pick position/hardness; loop gain = damping/sustain."""
from core import *
def ks(f,sec,bright=1.0,damp=.996,seed=0):
    N=int(SR/f); r=np.random.default_rng(seed); exc=r.uniform(-1,1,N)
    if bright<1: exc=lp(exc,max(200,bright*SR/2*0.9))
    y=np.zeros(int(sec*SR)); y[:N]=exc
    for i in range(N,len(y)): y[i]=damp*.5*(y[i-N]+y[i-N-1 if i-N-1>=0 else 0])
    return y
out=[]
for m in (45,52,57,60,64,69): out.append(ks(midi(m),1.0))
for b,d in ((.1,.99),(.5,.996),(1,.999)): out.append(ks(midi(52),2,b,d))
write("karplus_strong", np.concatenate(out), "A-minor arpeggio then dark/med/bright plucks")
