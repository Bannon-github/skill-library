import json
# G minor, 88 BPM, 30 bars (2.727 s/bar) + 3 s tail -> kick + bass enter bar 4 = 10.91 s
V={"Gm9":[[55,58,62,69],43],"Ebmaj7":[[51,55,58,62],39],"Bbmaj7":[[53,57,58,62],46],"Cm9":[[51,55,60,62],36]}
prog=["Gm9","Ebmaj7","Bbmaj7","Cm9"]
CH=[]
for k in range(15):
    n=prog[k%4] if k<14 else "Gm9"; CH.append([2*k,2*k+2,n,V[n][0],V[n][1]])
CH[-2]=[26,28,"Ebmaj7"]+V["Ebmaj7"]  # outro Eb -> Gm
lead=[]  # B section, steady triangle half/whole notes, fixed pitch
for b,ns in [(20,[(0,70,8),(8,69,8)]),(21,[(0,67,16)]),(22,[(0,67,8),(8,70,8)]),(23,[(0,74,16)]),
             (24,[(0,69,8),(8,65,8)]),(25,[(0,62,16)])]:
    lead+=[[b,s,m+12,l] for s,m,l in ns]
R={"name":"Root Pulse","seed":1127,"bpm":88,"bars":30,"tailSec":3.0,"category":"pad","key":"G minor","drumsIn":4,
 "chords":CH,"lead":lead,
 "sections":[{"n":"intro","b":[0,4],"els":["pad"]},
             {"n":"groove","b":[4,8],"els":["pad","kick","bass"]},
             {"n":"A","b":[8,16],"els":["pad","kick","kick4","bass","iso"]},
             {"n":"break","b":[16,20],"els":["pad","iso"]},
             {"n":"B","b":[20,26],"els":["pad","kick","kick4","bass","iso","lead"]},
             {"n":"outro","b":[26,30],"els":["pad","iso","kickout"]}],
 # JhZU6JGvoHw punchy tuned kick
 "kick":{"rootMidi":31,"holdS":0.10,"decayS":0.10,"pitchSt":30,"pitchTauS":0.016,"curve":1.6,"lpBase":160,"lpEnvHz":5200,
         "drive":2.2,"noiseDb":-20,"noiseMs":5,"noiseBp":[2500,5000],"mudHz":360,"mudDb":-4,"lowShelfDb":2.0,"highShelfDb":1.5,
         "sat":1.15,"comp":{"thrDb":-14,"ratio":4,"attS":0.030,"relS":0.20,"makeupDb":3}},
 # 0qOs9e5UwAU four-role pad
 "pad":{"atk":1.6,"rel":1.8,"low":{"lp":900,"lfoBars":1,"uni":3,"g":1.0},"high":{"hp":2600,"lp":9000,"lfoHz":0.23,"uni":3,"g":0.42},
        "tri":{"uni":2,"g":0.35},"noise":{"fb":0.82,"hp":3000,"lp":8000,"g":0.3},
        "chorus":{"rate":0.3,"depth":2.0,"base":12,"mix":0.4},"phaser":{"rate":0.08,"mix":0.15},"flanger":{"rate":0.12,"base":2.0,"fb":0.15,"mix":0.12},
        "delay":{"mix":0.2,"fb":0.3},"verb":{"rt":6.0,"size":2.2,"mix":0.45},"eqHp":140,"eqLp":11000,
        "detuneMacro":[[0,4,0.4],[4,8,0.5],[8,16,0.6],[16,20,0.9],[20,26,0.75],[26,30,0.5]],"detuneCents":[4,14]},
 # in-house isochronic staged gate-rate ramp
 "iso":{"carrierMidi":74,"stagesBars":[[8,12,10,10],[12,20,10,6],[20,30,6,6]],"edgeS":0.004,"duty":0.5},
 "levels":{"pad":1.0,"kick":0.55,"bass":0.26,"sub":0.22,"iso":0.07,"lead":0.10,"bassDuckDb":6,"verb":0.18},
 "master":{"targetLufs":-17.0,"tpCeil":-1.2,"sideHpHz":120,"fadeOutSec":4.0}}
json.dump(R,open("recipe.json","w"),indent=1)
