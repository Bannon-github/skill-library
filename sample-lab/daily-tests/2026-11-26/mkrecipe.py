import json
# D minor, 96 BPM, 34 bars (2.5 s/bar) -> kick + boom enter bar 4 = 10.0 s
CH=[[0,2,"Dm"],[2,4,"Bb"],[4,6,"Dm"],[6,8,"Bb"],
    [8,9,"Dm"],[9,10,"Bb"],[10,11,"C"],[11,12,"Dm"],[12,13,"Dm"],[13,14,"Bb"],[14,15,"C"],[15,16,"Dm"],
    [16,17,"Dm"],[17,18,"Bb"],[18,19,"C"],[19,20,"G"],
    [20,21,"Dm/A"],[21,22,"Am7"],[22,23,"Bbmaj7/A"],[23,24,"Aaug"],[24,26,"A7"],
    [26,27,"Dm"],[27,28,"Bb"],[28,29,"C"],[29,30,"Dm"],[30,32,"Dm7"],[32,34,"Dmaj7"]]
V={"Dm":[[57,62,65,69],38],"Bb":[[58,62,65,70],34],"C":[[55,60,64,67],36],"G":[[55,59,62,67],31],
   "Dm/A":[[57,62,65,69],33],"Am7":[[55,60,64,69],33],"Bbmaj7/A":[[58,62,65,69],33],"Aaug":[[57,61,65,69],33],
   "A7":[[55,61,64,69],33],"Dm7":[[57,60,65,69],38],"Dmaj7":[[57,61,66,69],38]}
chords=[[a,b,n,V[n][0],V[n][1]] for a,b,n in CH]
cell=lambda bar,a,b,c,d:[[bar,0,a,4],[bar,4,b,2],[bar,6,c,2],[bar,8,d,8]]
A=[(69,67,65,62),(74,72,70,65),(76,74,72,67),(77,76,74,69)]
mel=[]
for i,c in enumerate(A): mel+=cell(8+i,*c)
mel+=cell(12,*A[0])+cell(13,*A[1])+cell(14,79,76,74,72)+[[15,0,77,4],[15,4,76,4],[15,8,74,8]]
vio=[]
for i,c in enumerate(A[:3]): vio+=[[b,s,m+12,l] for b,s,m,l in cell(16+i,*c)]
vio+=[[19,0,86,4],[19,4,83,2],[19,6,79,2],[19,8,83,8]]          # G major (borrowed IV, B natural)
seqB=[[20,0,77,4],[20,4,76,4],[20,8,74,8],[21,0,76,4],[21,4,74,4],[21,8,72,8],[22,0,74,4],[22,4,72,4],[22,8,70,8],
      [23,0,69,16],[24,0,67,16],[25,0,76,4],[25,4,73,12]]          # sequence down one step over common-tone A, A7 -> D
a2=[]
for i,c in enumerate(A[:3]): a2+=cell(26+i,*c)
a2+=[[29,0,77,4],[29,4,76,4],[29,8,74,8]]
horn=[[26,8,57,8],[27,8,62,8],[28,8,64,8],[29,8,65,8]]             # countermelody only in held notes
vec=[[30,0,76,4],[30,4,74,4],[30,8,72,4],[30,12,71,4],[31,0,69,8],[31,8,67,8],   # D Dorian vector 9th -> 11th
     [32,0,76,4],[32,4,74,4],[32,8,73,4],[32,12,71,4],[33,0,69,8],[33,8,68,8]]   # D Lydian after 2-note half-step slip
cello=[[4,0,57,16],[5,0,55,8],[5,8,53,8],[6,0,50,32]]               # augmented motive A G F D
R={"name":"Borrowed Light","seed":1126,"bpm":96,"bars":34,"tailSec":3.0,"category":"pad","key":"D minor","drumsIn":4,
"chords":chords,
"pad":{"atk":1.0,"rel":2.5,"macro":[[0,4,0.55],[4,8,0.55],[8,16,0.65],[16,20,0.75],[20,26,0.4],[26,30,0.95],[30,34,0.6]],
  "mids":{"lfo":[0.07,0.11],"amt":0.35,"uni":[-8,0,8],"lp":[1300,5000],"hp":220,"envAmt":0.3},
  "highs":{"lfo":[0.04,0.09],"amt":0.2,"uni":[-15,-7,0,7,15],"lp":7500,"hp":1400,"det":7},
  "lows":{"lp":420,"hp":40,"lfo":0.03},"mix":{"lows":0.42,"mids":1.0,"highs":0.6},
  "comp":{"ratio":4},"verb1":{"rt":2.5,"damp":6000},"sat":1.4,"verb2":{"rt":7.0,"mix":0.5},"limDb":2.5},
"mel":mel,"vio":vio,"seqB":seqB,"a2":a2,"horn":horn,"vec":vec,"cello":cello,"pedal":{"midi":81,"bars":[4,8]},
"ost":{"pat":[0,1,2,1,0,1,2,1],"lo":60,"hi":68,"atk":0.006,"decay":0.22,"lp":2600},
"metal":{"bars":[4,12,20,26],"base":1250,"rt":9.0},
"kick":{"steps":[0,8],"bodyStartSt":20,"bodyHz":48,"pitchTauMs":28,"bodyDecay":0.26,"transHz":3200,"transMs":2.5,"transPhaseDeg":95,
        "shellFadeInMs":6,"shellHp":180,"shellGain":0.18,"noiseGain":0.04,"noiseDecay":0.06,"lowShelfDb":3,"midDb":2,"compAmt":0.5},
"sections":[
 {"b":[0,4],"name":"intro a: 3-band wavetable pad on first two chords only","els":["pad"]},
 {"b":[4,8],"name":"intro b: boom + soft kick pulse, augmented motive, high pedal, metal verb, ostinato fade, horn swell","els":["pad","kick","boom","cello","pedal","ost","hornswell"]},
 {"b":[8,16],"name":"A1: motive on piano, ostinato, root bass","els":["pad","kick","bass","mel","ost"]},
 {"b":[16,20],"name":"A1': melody to strings +8va, low brass, borrowed major IV","els":["pad","kick","bass","vio","ost","brass"]},
 {"b":[20,26],"name":"B: no perc/ostinato, lyrical step sequence over common-tone A","els":["pad","bass","seqB"]},
 {"b":[26,30],"name":"A2: melody in octaves, fuller perc, tam-tam, horn countermelody","els":["pad","kick","boom","bass","a2","ost","horn","perc"]},
 {"b":[30,34],"name":"outro: vector melody Dorian -> Lydian slip","els":["pad","kick","bass","vec"]}],
"levels":{"pad":0.55,"bass":0.21,"sub":0.12,"mel":0.28,"vio":0.16,"seqB":0.17,"horn":0.12,"vec":0.24,"cello":0.2,"pedal":0.07,
  "ost":0.12,"brass":0.13,"metal":0.09,"kick":0.28,"boom":0.22,"perc":0.08,"verb":0.15,"bassDuckDb":3},
"master":{"targetLufs":-17.0,"tpCeil":-1.5,"sideHpHz":200,"fadeOutSec":2.5}}
json.dump(R,open("recipe.json","w"),indent=1)
