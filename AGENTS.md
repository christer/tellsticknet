# AGENTS.md

## Project
Single-package Python CLI/library (`tellsticknet`) for Tellstick Net devices. Async I/O via `asyncio`, CLI built with `argparse`.

Use `uv run --with <tool>` or `uvx` to invoke dev tools without pre-activating the venv. Python version pinned to 3.14 via `.python-version`.

## Commands

| command | what it does |
|---|---|
| `make check` | `lint && test` (via Makefile targets) |
| `make lint` | `uv run --with tox tox -e lint` |
| `make test` | `uv run --with tox tox` |
| `make format` | `uv run --with ruff ruff format tellsticknet pyproject.toml` |
| `tox -e lint` | `ruff check ... && ruff format --check ...` |
| `tox` | runs `py.test tellsticknet` with `--doctest-modules` (doctests in source are tested) |

## Testing quirks
- Tests live in `tellsticknet/test_protocols.py` (pytest) **and** as doctests in `tellsticknet/protocol.py` — both run under `tox`.
- `tox.ini` only defines env `py314`; CI runs on Python 3.14 (via `.python-version`).

## Package structure
- `tellsticknet/__main__.py` — CLI entrypoint. Commands: `discover`, `listen`, `send`, `mqtt`, `mock`, `parse`, `devices`, `sensors`.
- `tellsticknet/protocols/` — per-protocol modules loaded dynamically via `importlib.import_module`. Each must implement `decode()` and `encode()`.
- Entry point: `tellsticknet=tellsticknet.__main__:app_main` (set in `pyproject.toml` `[project.scripts]`).

## Gotchas
- Config is YAML (`tellsticknet.conf` / `.tellsticknet.conf`) looked up in CWD, `$HOME`, `$XDG_CONFIG_HOME` (see `tellsticknet-sample.conf`).
- Docker entrypoint is `python3 -m tellsticknet mqtt`; exposes UDP ports 30303 and 42314.
- Uses `uv` for dependency management (`uv.lock`). Dependencies declared in `pyproject.toml` `[project]`.
- Protocol implementations adapted from [telldus-core](https://github.com/telldus/telldus/tree/master/telldus-core/service). See `tellsticknet/test_protocols.py` for exact test vectors.
- Python version pinned via `.python-version` (3.14). Run `uv run` or `uv run --with <tool>` to auto-use the correct Python.
- Runtime deps: `pyyaml`, `gmqtt`, `coloredlogs` only. All others (`ruff`, `tox`) are ephemeral via `uv run --with`.

## Task Management Rules

You must read and update `./tasks.md` using the single-line symbol system. Do not restructure headers and avoid moving text blocks; only alter the checkbox state on the task line to change status.

- `[ ]` = Unstarted / Todo
- `[/]` = Active Focus (Only ONE task can be active at a time)
- `[-]` = Paused / Shelved
- `[x]` = Completed / Done

1. **Starting a Task**: Change the target task's symbol to `[/]`. Check `jj log` or `jj status` to extract the short Change ID, and append a sub-bullet metadata block if tracking is active. Turn any previous `[/]` task into `[-]` or `[x]`.
2. **Pausing a Task**: Shifting a task from `[/]` to `[-]`. Append a single sub-bullet note detailing the stopping point and current Jujutsu Change ID.
3. **Finishing a Task**: Turn `[/]` into `[x]`. Append completion details, resolution summary, and Jujutsu Change ID as sub-bullets. Never delete a completed task during daily operations.
4. **Task Sequencing**: Complete or pause the current task before starting another. If you discover related work while on a task, note it in the backlog — don't switch mid-stream. Only proceed to the next task after the current one is finished or paused and the user has OK'd the switch.
5. **Archiving**: Move finished tasks from `tasks.md` to `tasks-archive.md` using the `/task-archive` command when they start to become too many, always leaving the last completed task as a context bridge.

- **Reference Blueprints**: If the structure of any markdown file becomes corrupted or needs resetting, look at the clean layouts described in README-TASKS.md.

## jj Workflow

This repo uses [Jujutsu (jj)](https://github.com/jj-vcs/jj) instead of git. Every working copy
is also a commit — there is no staging area.

### Basic workflow

```sh
jj status            # see uncommitted changes
jj log --no-graph    # commit history (short Change IDs)
jj describe -m "msg" # describe/set the commit message
jj new               # create a new empty commit on top (move working copy)
jj squash            # merge working copy into parent
jj squash --from <change> --into <parent>  # move changes between commits
jj split <files...>  # split the current commit: selected files go to first commit
jj edit <change>     # make an existing change the working copy
jj restore <paths>   # discard uncommitted changes to specific files
```

### Commit messages

- Use `jj describe -m "..."` with a short summary line.
- Add a blank line then bullet points for details.
- Add `Co-authored-by: Name <email>` as the last line if the AI/opencode was involved.

### Conventions

- The working copy (@) is always the current commit — amend it with `jj describe`.
- To commit work and start fresh: `jj new` then `jj describe -m "..."`.
- To combine commits: `jj squash --from <child> --into <parent>`.
- To split a commit by file: `jj split <file1> <file2> ...` (selected files → first commit, rest → second commit).
- When `EDITOR=nano` fails (not installed), use `EDITOR='cp /tmp/desc' jj describe` with the message in `/tmp/desc`.

### Current commit stack

```
mrwzvztx  Relax uv_build constraint, pin Python 3.14, fix scripts
znnyuwuv  Replace docopt with argparse, remove dead deps
uqqoouqp  Remove await from gmqtt publish/subscribe calls
ytqxovsq  Fix gmqtt callback registration: use assignment
pyluqsns  Strip stale files, switch to uv_build
mnwnumzw  Modernize toolchain: uv, ruff, gmqtt
pzxxqvul  Update Python version to 3.14
uyplzokw  Add Pipfile, pyproject.toml, and shell scripts
pwwowoym  Add AGENTS.md, docs/README-TASKS.md, .gitignore
uutlntnn  Bootstrap task tracking system
lqmyzmvk  master: changed a couple of hbmqtt to amqtt
...
```
