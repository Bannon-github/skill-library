"""FM: carrier fc, modulator fm = ratio*fc, index I = peak deviation/fm. Sidebands at fc +/- k*fm.
Integer ratios (1:1, 2:1, 3:1) give harmonic spectra; irrational 1:1.414 and 1:3.5 give inharmonic bells.
Last: a decaying index (bright attack -> mellow tail) = the classic FM electric piano/bell."""
from core import *
fc=220; out=[]
for r in (1,2,3,1.414,3.5):
    tt=t(1.2); I=3
    out.append(np.sin(2*np.pi*fc*tt+I*np.sin(2*np.pi*fc*r*tt))*adsr(1.2,.01,.2,.7,.2))
tt=t(2.5); I=6*np.exp(-tt*3)
out.append(np.sin(2*np.pi*fc*tt+I*np.sin(2*np.pi*fc*3.5*tt))*np.exp(-tt*1.5))
write("fm_ratios", np.concatenate(out), "ratios 1,2,3,1.414,3.5 then index decay bell")
