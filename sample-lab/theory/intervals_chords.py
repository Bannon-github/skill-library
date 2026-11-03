"""Intervals, chord qualities, voicings and voice leading.
1) Intervals from unison to octave (just-ish ratios hear consonance->dissonance: P5 3:2, M3 5:4, m2 16:15).
2) Triad/7th qualities on C: maj, min, dim, aug, sus2, sus4, maj7, min7, dom7.
3) i-VI-III-VII in A minor, block root-position (jumpy) vs voice-led (common tones held, others move by step)."""
from core import *
def tone(m,sec): return lp(saw(midi(m),sec,nh=30),3000)*adsr(sec,.02,.2,.6,.3)
def chord(ms,sec): return sum(tone(m,sec) for m in ms)/len(ms)
out=[]
for iv in range(13): out.append(chord([60,60+iv],.6))
Q={"maj":[0,4,7],"min":[0,3,7],"dim":[0,3,6],"aug":[0,4,8],"sus2":[0,2,7],"sus4":[0,5,7],"maj7":[0,4,7,11],"min7":[0,3,7,10],"dom7":[0,4,7,10]}
for q in Q.values(): out.append(chord([60+i for i in q],.9))
root=[[57,60,64],[53,57,60],[60,64,67],[55,59,62]]
led=[[57,60,64],[57,60,65],[55,60,64],[55,59,62]]
for prog in (root,led):
    for c in prog: out.append(chord(c+[c[0]-12],1.0))
write("intervals_chords", np.concatenate(out), "13 intervals, 9 qualities, root-pos vs voice-led i-VI-III-VII")
