"""Run every theory generator and report pass/fail. Usage: /home/box/audio-tools/bin/python run_all.py"""
import subprocess, sys, time
from pathlib import Path
here=Path(__file__).parent; ok=[]; bad=[]
for p in sorted(here.glob("*.py")):
    if p.name in ("core.py","run_all.py"): continue
    t0=time.time(); r=subprocess.run([sys.executable,p.name],cwd=here,capture_output=True,text=True)
    (ok if r.returncode==0 else bad).append(p.stem)
    print(f"{'PASS' if r.returncode==0 else 'FAIL'} {p.stem} ({time.time()-t0:.1f}s)\n{r.stdout.strip()}\n{r.stderr.strip()[-800:] if r.returncode else ''}")
print(f"\n{len(ok)} passed, {len(bad)} failed: {bad}"); sys.exit(1 if bad else 0)
