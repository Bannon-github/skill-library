---
name: nature-realism-inspection
description: >-
  Use this whenever inspecting any generated item in a simulation or game
  (animal, tree, rock, water, sound, behaviour) to check whether it resembles
  the real natural thing to 95% and to improve it if not.
---
# Nature realism inspection

Run this on every item you inspect. Be honest: a finding of "looks fine" needs evidence.

## A. Look
1. **What do I see here?** List every distinct element of the item (parts, materials, motion, sounds, behaviours). Capture evidence: screenshot, frame sequence, numbers, logs.
2. **Does each element have a reason for being there?** For each, name the cause in the system (the rule, value or transaction that produced it). Anything with no reason is a defect or leftover; flag it.
3. **Does it resemble nature?** Compare each element to a real reference: measured data, field guides, papers, or real video. State the reference, not an impression.
4. **How do I know?** Write the evidence trail: source and citation, what was compared, how (frame by frame for motion, measured ranges for sizes, speeds, timings, frequencies).
5. **Score it.** Give each element a match from 0 to 100% against the reference, then the overall score. The target is at least 95%. Unverified elements count as failing until checked.

## B. Make the method itself
If no method exists yet for this kind of item:
6. **How can I make sure it resembles the natural thing to 95%?** Define the references, the measurable checks and the pass thresholds for this item type.
7. **Write a plan** for running those checks.
8. **Does the plan solve the problem?** Test it against a known-good and a known-bad example. If yes, save it as a reusable skill or checklist for that item type. If no, revise the plan and repeat.

## C. Decide
9. **Does what I am looking at resemble nature?** Use the saved skill or checklist to answer. 
   - **Yes** (≥ 95% with evidence): record the evidence and stop.
   - **No**: continue below.

## D. Improve
10. **How can I improve the item?** List the specific gaps found in step 5.
11. **Is there an existing solution?** Search the codebase, open PRs, other branches, shared libraries, published research and open-source projects. Never reinvent anything that already exists.
12. **If yes, write a plan to implement it:** reuse or extend the existing solution, with the smallest change.
13. **Implement and test it.** Run the project's tests and re-run the checks from step 5.
14. **Loop** back to step 3 until the score is at least 95% or the remaining gap is documented with a reason.

## Report
For each inspection, report: items seen, reason for each, reference and evidence used, score, existing solutions found and reused, what changed, test results, and any open gaps.
