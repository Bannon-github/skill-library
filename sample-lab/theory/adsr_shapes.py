"""ADSR envelope shapes on one saw-through-LP tone: pluck (0 sustain), stab, pad (slow attack/release),
swell (reverse-like), and bowed string. Amplitude contour defines the instrument family as much as timbre."""
from core import *
shapes={"pluck":(.002,.3,0,.1),"stab":(.005,.12,.5,.08),"pad":(.8,.5,.8,1.2),"swell":(1.8,.01,1,.15),"bowed":(.15,.2,.85,.4)}
out=[]
for k,(a,d,s,r) in shapes.items():
    x=lp(saw(220,2.2),2500); out.append(x*adsr(2.2,a,d,s,r)); out.append(np.zeros(int(.25*SR)))
write("adsr_shapes", np.concatenate(out), " / ".join(shapes))
