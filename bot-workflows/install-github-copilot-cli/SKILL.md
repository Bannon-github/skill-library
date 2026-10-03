---
name: Install GitHub Copilot CLI
description: >-
  Use when the user wants GitHub Copilot CLI installed and runnable on Linux
  (the `copilot` command).
---
# Install GitHub Copilot CLI

Install the official GitHub Copilot CLI so `copilot` runs from a shell. Assumes a GitHub account with an active Copilot plan. Do not sign the user up for a paid plan, and do not enter or store passwords, passkeys, or tokens.

## Inputs

- None required. Optional: which shell profile to persist PATH in (default: the user’s current shell, usually bash).

## Steps

1. Open the official install page and follow that, not a search result: https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli
2. Check Node.js. Copilot CLI needs Node.js 22 or later (`node -v`). If it is missing or older, install the current Node via nvm from https://nodejs.org/en/download (the Linux/macOS nvm script on that page). Source nvm in the same shell (`\. "$HOME/.nvm/nvm.sh"`) before continuing. Do not use WinGet on Linux.
3. Before any global npm install, clear a conflicting prefix if it is set: `unset NPM_CONFIG_PREFIX`. If npm warns that `NPM_CONFIG_PREFIX` is set (often `/home/box/.local`), this is why `copilot` installs but is not found.
4. Install: `npm install -g @github/copilot`
5. Put the global npm bin on PATH for this shell and in the shell profile so it survives a new terminal:
   - `export PATH="$(npm prefix -g)/bin:$PATH"`
   - Persist that line in `~/.bashrc` (or the user’s actual profile) if it is not already there.
6. Confirm the binary, not just “added N packages”:
   - `hash -r`
   - `command -v copilot`
   - `copilot --version` (or `copilot` if `--version` is not supported)
7. If the shell says `copilot: command not found`, do not reinstall blindly. Check `npm prefix -g`, `npm bin -g`, and whether that `bin` directory is on PATH. Fix PATH, then retry.
8. First launch asks for GitHub authentication. Assume the browser or CLI is signed into the GitHub account that has Copilot. Confirm with the user before starting login if it will open a browser or request a device code. Do not type passwords, one-time codes, or passkeys.

## Notes

- A successful `npm install -g` is not enough. The demo failed because the binary was not on PATH after install.
- Ignore Windows-only commands (`winget install GitHub.Copilot.Prerelease`).
- Signing into Gmail or creating a new browser profile is not part of this install.
