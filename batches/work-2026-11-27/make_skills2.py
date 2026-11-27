import sys; sys.path.insert(0,'/workspace/skill-library/batches/work-2026-11-27')
from lib_s import S
S("mxUQyUs1eGo","How to add PUNCH to your KICKS using Compression (3 SIMPLE STEPS)",
 "kick-punch-compression-threshold-on-top-section-3-to-1-slow-40ms-attack-keeps-transient-200ms-release-makeup-gain",
 "Kick punch by compression: threshold catches only the upper part of the kick, 3:1 ratio, slow ~40 ms attack lets the transient through, ~200 ms release returns before the tail sinks, then make-up gain so the transient stands taller than the sloped tail",
 "Add punch and depth to a dull, thuddy kick with one compressor: set the threshold so only the top section of the kick exceeds it (about -10.5 dB in the source; -2 dB does nothing), ratio 3:1 (2-3:1 moderate, 5:1 strong, 10:1+ limiting), attack ~40 ms so the initial transient passes uncompressed and the body after it is pulled down, release ~200 ms so gain recovers without dragging the tail under the threshold, then make-up gain (~+2.3 dB) and A/B at matched loudness. Result: higher relative transient and a sloped tail that cuts through the mix. Complements the synthesized punchy/felt kick variants (use after synthesis).",
 ["Any compressor, ideally one that shows the waveform/gain reduction","A kick in a basic drum loop"],
 [("kick","audio","Kick needing more punch (thud with a small transient)",True)],
 [("kick_compressed","audio","Kick with a more pronounced transient and sloped tail")],
 ["Use loudness-matched A/B; the change is subtle by design.","Slow attack (tens of ms) is the punch move; very fast attack instead trades click for fatness.","Do not let release push the tail fully under the threshold."],
 [("Solo the kick in a basic loop; note the dry waveform (small transient, flat body).","Meter/waveform view","Reference for before/after"),
  ("Lower the threshold until only the upper section of each kick crosses it (about -10.5 dB in the source).","Compressor threshold","Only the loud part triggers compression"),
  ("Set ratio about 3:1 (2-3:1 moderate, 5:1 strong, 10:1+ acts like a limiter).","Compressor ratio","Peaks pulled down moderately"),
  ("Raise attack to about 40 ms so the initial transient passes before gain reduction starts.","Compressor attack","Transient kept, body compressed after it"),
  ("Set release about 200 ms so it affects only the upper section and recovers before the next hit.","Compressor release","Tail sloped, not buried"),
  ("Add make-up gain (~+2.3 dB) and A/B against the dry kick at equal loudness; compare waveforms.","Output gain","Punchier kick with a taller relative transient")],
 ["Gain reduction begins only after the transient (~40 ms attack) and returns to 0 dB before the next kick.","Compressed kick's peak-to-body ratio (first 10 ms vs 50-150 ms RMS) is higher than the dry kick's.","Loudness-matched output; peak below 0 dBFS."],
 ["kick","compression","punch","transient","attack","release","drums","mix"])
