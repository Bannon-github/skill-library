"""Scales & modes: the seven diatonic modes all starting on C (parallel modes) over a C drone, brightest
to darkest: Lydian(#4) Ionian Mixolydian(b7) Dorian(b3,b7) Aeolian(b6) Phrygian(b2) Locrian(b5).
Also major & minor pentatonic. Characteristic note is what gives each mode its colour."""
from core import *
M={"lydian":[0,2,4,6,7,9,11],"ionian":[0,2,4,5,7,9,11],"mixolydian":[0,2,4,5,7,9,10],"dorian":[0,2,3,5,7,9,10],
   "aeolian":[0,2,3,5,7,8,10],"phrygian":[0,1,3,5,7,8,10],"locrian":[0,1,3,5,6,8,10],"maj_penta":[0,2,4,7,9],"min_penta":[0,3,5,7,10]}
out=[]
for steps in M.values():
    notes=[60+s for s in steps]+[72]; sec=.22*len(notes)+.4
    mel=np.zeros(int(sec*SR))
    for i,m in enumerate(notes): place(mel, sine(midi(m),.3)*adsr(.3,.005,.1,.5,.1)+.3*sine(midi(m)*2,.3)*adsr(.3,.005,.05,0,.05), i*.22)
    drone=lp(saw(midi(36),sec,nh=40),400)*.25
    out.append(mel+drone)
write("scales_modes", np.concatenate(out), " ".join(M))
