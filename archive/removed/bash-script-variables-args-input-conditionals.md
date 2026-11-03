# Write a basic bash automation script

Goal: Create a bash script that uses variables, arguments, command output, user input and a conditional.

Source: [Write Your Own Bash Scripts for Automation [Tutorial]](https://www.youtube.com/watch?v=PPQ8m8xQAs8) (Null Byte)

1. Run `which bash` to get the interpreter path (e.g. /bin/bash).
2. Create a file ending in .sh (e.g. `nano myscript.sh`) and make the first line the shebang `#!/bin/bash`.
3. Variables: `string="value"` then `echo "text $string"`.
4. Positional arguments: reference `$1`, `$2`, `$3` in the script and pass words after the script name when running it.
5. Command substitution: `echo "$(whoami)"` prints a command's output rather than the literal text.
6. Interactive input: `echo "What is your name?"`, `read name`, then use `$name`.
7. Conditional: `if [ "$name" ]; then echo "$name sounds alright"; else echo "Doesn't sound like anything"; fi`. A missing `fi` causes "unexpected end of file".
8. Save (nano: Ctrl+X, Y, Enter) and run with `bash myscript.sh arg1 arg2 arg3`.

Batch: `2026-10-05-batch-01` · transcript: YouTube-provided (auto-generated)
