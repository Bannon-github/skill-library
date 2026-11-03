# Turn a filtered command pipeline into a one-word bash alias

Goal: Get a specific value (e.g. the local IP address) with a single custom command.

Source: [Write Your Own Bash Scripts for Automation [Tutorial]](https://www.youtube.com/watch?v=PPQ8m8xQAs8) (Null Byte)

1. Start with a noisy command (e.g. `ifconfig`).
2. Pipe it to grep with a unique pattern on the line you want: `ifconfig | grep broadcast`.
3. Pick the field with awk: `ifconfig | grep broadcast | awk '{print $2}'`.
4. Create the alias, keeping double quotes outside and single quotes inside, and wrap the pipeline in echo with command substitution so it runs before printing: `alias whatismyip="echo $(ifconfig | grep broadcast | awk '{print $2}')"`.
5. Run the alias name to check the output.
6. To keep it across sessions, add the alias line to ~/.bashrc (standard bash practice; not shown in the video). Note that with double quotes the $( ) expands when the alias is defined; use single quotes around the alias body if the value should be recomputed each run.

Batch: `2026-10-05-batch-01` · transcript: YouTube-provided (auto-generated)
