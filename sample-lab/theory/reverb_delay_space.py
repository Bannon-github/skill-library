"""Space: dry pluck melody; + tempo-synced ping-pong delay (dotted 1/8 @ 100 BPM = 0.45 s, feedback 0.45);
+ short room (0.8 s); + long hall (4 s) with 30 ms pre-delay and low-cut 300 Hz on the return (keeps lows clean);
+ shimmer (octave-up copy fed into the long tail). Wet/dry ratio = perceived distance."""
from core import *
bpm=100; e=60/bpm/2; sec=4.5; dry=np.zeros(int(sec*SR))
for i,m in enumerate([69,72,76,74,72,69,67,69]): place(dry, lp(saw(midi(m),.4,nh=30),3000)*adsr(.4,.003,.15,0,.05), i*e)
def pingpong(x, d, fb):
    n=int(d*SR); L=np.zeros(len(x)); R=np.zeros(len(x))
    for k in range(1,8):
        g=fb**(k-1)*.6; s=np.concatenate([np.zeros(k*n),x])[:len(x)]
        (L if k%2 else R)[:]+=s*g
    return np.stack([x+L,x+R],1)
pp=pingpong(dry,.45*60/bpm*2/1.0*.5*1.5/.75*0.5,.45)
room=np.stack([reverb(dry,.8,.25,1),reverb(dry,.8,.25,2)],1)
pre=np.concatenate([np.zeros(int(.03*SR)),dry])[:len(dry)]
hall=np.stack([dry+hp(reverb(pre,4,1,3),300)*.6, dry+hp(reverb(pre,4,1,4),300)*.6],1)
up=np.interp(np.arange(0,len(dry),2.0),np.arange(len(dry)),dry); up=np.tile(up,2)[:len(dry)]
shim=hall+np.stack([hp(reverb(up,4,1,5),600),hp(reverb(up,4,1,6),600)],1)*.3
D=np.stack([dry,dry],1)
write("reverb_delay_space", np.concatenate([D,pp,room,hall,shim]), "dry/pingpong/room/hall+predelay+lowcut/shimmer")
