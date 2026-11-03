"""Mixing: subtractive EQ first and kick/bass separation. Four mixes of kick + bass + pad, low-mid energy printed:
A) raw (pad and bass mud 150-400 Hz, kick and bass both at 50 Hz), B) high-pass pad at 200 Hz + cut 300 Hz mud,
C) + bass ducked under kick and bass high-passed 35 Hz (kick owns 50 Hz transient), D) + gain staged to -6 dBFS peak bus."""
from core import *
bpm=120; beat=60/bpm; n=int(8*beat*SR)
def kick(): tt=t(.4); return np.tanh(1.8*sine(48+100*np.exp(-tt/.03),.4)*np.exp(-tt/.3))
K=np.zeros(n); [place(K,kick(),b*beat) for b in range(8)]
bass=lp(saw(midi(31),n/SR,nh=30),250)*.7
pad=sum(saw(midi(m),n/SR,nh=60) for m in (48,55,60,64))*.15
def band(x,lo,hi): return rms_db(bp(x,lo,hi))
A=K+bass+pad
padc=hp(pad,200); padc=padc-0.5*bp(padc,250,400)
B=K+bass+padc
g=np.ones(n); sh=1-.8*np.exp(-t(beat)/.12)
for b in range(8): i=int(b*beat*SR); g[i:i+len(sh)]=sh[:n-i]
C=K+hp(bass,35)*g+padc
D=C/np.max(np.abs(C))*10**(-6/20)
for k,v in zip("ABCD",(A,B,C,D)): print(f"  {k}: 150-400Hz={band(v,150,400):.1f} dB  peak={20*np.log10(np.max(np.abs(v))):.1f} dBFS")
write("eq_mix_balance", np.concatenate([A/np.max(np.abs(A)),B/np.max(np.abs(B)),C/np.max(np.abs(C)),D]), "raw / subtractive EQ / +sidechain+HPF / gain staged")
