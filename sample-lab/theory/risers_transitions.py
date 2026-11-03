"""Transition FX: white-noise riser (band-pass swept 300->9000 Hz, volume up, 4 bars @128), Shepard tone
(octave-spaced sines rising forever under a fixed bell-shaped spectral window), downlifter (reverse of riser),
impact + sub drop (sine 80->20 Hz with exponential glide)."""
from core import *
bar=4*60/128; sec=4*bar; n=int(sec*SR); r=np.random.default_rng(5)
noise=r.standard_normal(n); fc=np.geomspace(300,9000,n)
riser=svf(noise,fc,3,"bp")*np.linspace(0,1,n)**2
tt=t(8); sh=np.zeros(len(tt)); base=27.5
for k in range(8):
    p=((tt/8)+k/8)%1; f=base*2**(p*8); w=np.exp(-0.5*((np.log2(f/440))/1.5)**2)
    sh+=w*np.sin(2*np.pi*np.cumsum(f)/SR)
down=riser[::-1][:int(2*bar*SR)]
tt=t(2); imp=np.tanh(2*sine(20+60*np.exp(-tt/.5),2))*np.exp(-tt/.8)+ r.standard_normal(len(tt))*np.exp(-tt/.05)*.5
write("risers_transitions", np.concatenate([riser,imp,sh/4,down]), "noise riser / impact+sub drop / shepard / downlifter")
