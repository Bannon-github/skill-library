"""Formants: a buzzy saw (rich source) through parallel band-passes at vowel formants F1/F2/F3
(a: 730/1090/2440, e: 530/1840/2480, i: 270/2290/3010, o: 570/840/2410, u: 300/870/2240) -> 'talking' synth,
the principle behind vocoders and formant filters. Then a smooth a->i->u morph."""
from core import *
V={"a":(730,1090,2440),"e":(530,1840,2480),"i":(270,2290,3010),"o":(570,840,2410),"u":(300,870,2240)}
src=lambda sec: saw(midi(45),sec,nh=150)
out=[]
for f in V.values():
    s=src(.8); out.append(sum(svf(s,fc,8,"bp")*g for fc,g in zip(f,(1,.6,.3)))*adsr(.8,.03,.1,.9,.1))
sec=3; s=src(sec); path=np.array([V["a"],V["i"],V["u"]],float); x=np.linspace(0,2,len(s))
F=np.stack([np.interp(x,[0,1,2],path[:,k]) for k in range(3)],1)
out.append(sum(svf(s,F[:,k],8,"bp")*g for k,g in enumerate((1,.6,.3))))
write("formant_vowels", np.concatenate(out), "a e i o u then a->i->u morph")
