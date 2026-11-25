import json
# A minor, 90 BPM, 32 bars (2.667 s/bar) -> kick + bass enter bar 4 = 10.67 s
LEAD=[[0,76,6],[6,74,2],[8,72,4],[12,69,4],[16,72,6],[22,74,2],[24,76,8]]   # 2-bar steady focal phrase [s16, midi, len16]
R={"name":"Zone Gate","seed":1125,"bpm":90,"bars":32,"tailSec":3.0,"category":"pad","key":"A minor","drumsIn":4,
"chords":[ # [b0,b1,name,padTones(150-800 Hz body),bassRoot]
 [0,2,"Am(add9)",[57,60,64,71],33],[2,4,"Fmaj7",[57,60,64,65],29],[4,6,"C",[55,60,64,67],36],[6,8,"G6",[55,59,62,64],31]],
"loopChords":True,
"pad":{"atk":1.8,"rel":2.5,"detuneCents":6,"lp":2300,"hp":150,"offsetBeats":0.67,"panA":-0.6,"panB":0.6},
"bass":{"lp":420,"drive":1.3,"unisonCents":[-4,0,4]},
"lead":{"phrase":LEAD,"atk":0.008,"decay":0.9,"sus":0.55,"tri":0.35,"lp":6500},
"pluck":{"arp":[0,2,1,3,2,1,3,2],"oct":12,"atk":0.006,"decay":0.28,"lpRange":[900,3800],"lfoHz":0.06,"delayBeats":0.75,"fb":0.35},
"gate":{"rate16":1,"shape":0.6,"rt":4.5,"tex_lp":4200,"amount":[[0,16,0.0],[16,17,"ramp"],[17,24,1.0],[24,32,0.55]]},
"air":{"lp":13000,"combHz":420,"rt":5.0,"relDb":-20},
"kick":{"steps":[0,8],"bodyStartSt":20,"bodyHz":48,"pitchTauMs":28,"bodyDecay":0.26,"transHz":3200,"transMs":2.5,"transPhaseDeg":95,
        "shellFadeInMs":6,"shellHp":180,"shellGain":0.18,"noiseGain":0.04,"noiseDecay":0.06,"lowShelfDb":3,"midDb":2,"compAmt":0.5},
"sections":[
 {"b":[0,4],"name":"establish a: body pad (2 out-of-sync loops) + quiet air","els":["pad","air"]},
 {"b":[4,8],"name":"establish b: kick + A1-zone bass in on bar 4","els":["pad","air","kick","bass"]},
 {"b":[8,16],"name":"expand: focal lead voice takes the foreground","els":["pad","air","kick","bass","lead"]},
 {"b":[16,20],"name":"contrast a: hand-off to pluck sequence, lead out, kick out, gated texture in","els":["pad","air","bass","pluck","gate"]},
 {"b":[20,24],"name":"contrast b: kick back under pluck + gate","els":["pad","air","kick","bass","pluck","gate"]},
 {"b":[24,30],"name":"return: opening material + lead, gated texture kept (new element)","els":["pad","air","kick","bass","lead","gate"]},
 {"b":[30,32],"name":"end: pad + bass + gate tail","els":["pad","air","bass","gate"]}],
"levels":{"pad":0.42,"padB":0.8,"bass":0.27,"sub":0.14,"lead":0.30,"pluck":0.24,"echo":0.12,"gate":0.20,"kick":0.30,"verb":0.18,"bassDuckDb":3},
"master":{"targetLufs":-17.0,"tpCeil":-1.5,"sideHpHz":200,"fadeOutSec":2.5}}
json.dump(R,open("recipe.json","w"),indent=1)
