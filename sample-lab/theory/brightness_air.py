"""Brightness / air at the source for pads. Same chord 4 ways (spectral centroid printed):
1) dark: saw through 800 Hz LP (typical 'muddy' pad), 2) open the filter + key-track (more upper harmonics),
3) add an exciter: high-passed (>3 kHz) copy driven through tanh (generates new upper harmonics) blended ~-12 dB,
4) add an 'air' layer: octave-up sine/triangle partials + high-passed noise (>8 kHz) at -24 dB + gentle 10 kHz shelf.
Lesson: brightness comes from harmonic content created upstream, not a big treble boost at the end."""
from core import *
sec=3; ch=[57,60,64,67]
def pad(cut): return sum(svf(saw(midi(m),sec,nh=80),cut*(midi(m)/midi(57)),.8) for m in ch)/4*adsr(sec,.4,.3,.9,.6)
dark=pad(800); opened=pad(3500)
exc=np.tanh(4*hp(opened,3000)); excited=opened+.25*exc
air=sum(sine(midi(m+12)*2,sec)*.04 for m in ch)*adsr(sec,.4,.3,.9,.6)+hp(np.random.default_rng(4).standard_normal(int(sec*SR)),8000,4)*.004*adsr(sec,.6,.3,.9,.6)
shelf=excited+air; shelf=shelf+.12*hp(shelf,10000)
for k,v in (("dark",dark),("open+keytrack",opened),("+exciter",excited),("+air layer+shelf",shelf)):
    print(f"  {k}: centroid={centroid(v):.0f} Hz")
write("brightness_air", np.concatenate([dark,opened,excited,shelf]), "dark/open/exciter/air")
