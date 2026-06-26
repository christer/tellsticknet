# Project Tasks

## How to use this file

- `- [ ]` = Unstarted Task (Upcoming backlog item)
- `- [/]` = **Active Focus Task** (The single item currently being coded)
- `- [-]` = **Paused Task** (Shelved midway through; paired with context notes)
- `- [x]` = **Completed Task** (Kept in place to act as a rolling context bridge)

## Completed

- [x] **Replace docopt with argparse**: Rewrote CLI parsing using argparse with subparsers. Same interface, no dependency.
  - **Jujutsu Tracking**: Completed on Change `znnyuwuv`
- [x] **Remove dead deps**: Dropped docopt, requests, websockets, libnacl (7→3 runtime deps).
  - **Jujutsu Tracking**: Completed on Change `znnyuwuv`
- [x] **Fix scripts/Makefile for out-of-box use**: All scripts now use `uv run` / `uv run --with`, no pre-activated venv needed.
  - **Jujutsu Tracking**: Completed on Change `mrwzvztx`
- [x] **Pin Python 3.14**: Created `.python-version` pinned to 3.14, consistent with production.
  - **Jujutsu Tracking**: Completed on Change `mrwzvztx`
- [x] **Relax uv_build constraint**: Changed from `>=0.11.24,<0.12` to `>=0.11` for wider pip compatibility.
  - **Jujutsu Tracking**: Completed on Change `mrwzvztx`

