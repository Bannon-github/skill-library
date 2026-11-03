# Design an agent-run media production pipeline: map team roles to tools, encode style as a skill, improve it from feedback

Source: [I Fully Automated My Video Editing Using Claude Code (Full Walkthrough)](https://www.youtube.com/watch?v=HzXD4GVqXwM), YouTube-provided transcript.

**Goal:** Design an automated media workflow (shown for video editing; same pattern for automated song generation) by listing every human job in the production team, assigning each to a tool with one coordinating agent, writing the creative style into a skill file the agent reads first, and growing that skill from time-stamped human feedback after each run.

## Steps
1. List every job a human team would do to make the product (video: editor, transcriber, animator, researcher, screen editor, sound designer, finisher). _Expect: Ordered list of roles_
2. Assign each job to a tool; make the agent the coordinator/project manager that calls the others, and add a converter for any media the agent cannot perceive. _Expect: Role-to-tool map with one coordinator_
3. Set up the agent locally with a working folder and connect each tool/connector, then have the agent save the setup as a skill. _Expect: Connectors active; skill file saved_
4. Open a new session and test the skill on a small piece of input, with any extra instructions. _Expect: V1 output plus a summary of what the agent did_
5. Review the output and give specific, time-stamped feedback (look, sound, pacing, cuts); try several alternatives for one element until one fits. _Expect: Revised output_
6. Tell the agent to save what it learned into the skill, then run the next job in a fresh session with the updated skill. _Expect: Skill gains rules (video grew to 36 rules); repeated mistakes stop_
7. Once tuned, give the full raw input, let it run unattended, then review and give final notes. _Expect: Near-final product needing only a few notes_

## Constraints
- The human keeps director jobs: providing the input and giving feedback (human in the loop).
- One agent coordinates; it cannot perceive some media directly (it could not hear audio), so add a tool that converts it to readable data (timestamped transcription).
- Tools do not know the desired look/sound; that lives in the skill file.
- Start with small pieces (a hook) before whole products; feed the full input only once the skill is tuned.
- Track cost per run (video measured token use per video).
- Mapping to song generation (e.g. composer, sound designer, mixer roles) is an analogy and must be checked against real tools.

## Verification
- Every production role has exactly one assigned tool or is marked human
- Skill file changes after each feedback round
- A fresh session using the updated skill does not repeat an earlier corrected mistake
