# AGENTS.md

## Project
Single-package Python CLI/library (`tellsticknet`) for Tellstick Net devices. Async I/O via `asyncio`, uses `docopt` for CLI.

## Commands

| command | what it does |
|---|---|
| `make check` | `lint && test` (sequential via `script/check`) |
| `make lint` | `tox -e lint` |
| `make test` | `tox` |
| `make black` / `make format` | **runs `white`, not `black`** — the formatter is `white` |
| `make release` | `git diff-index --quiet HEAD -- && make check && bumpversion patch && git push --tags && git push && make pypi` |
| `tox -e lint` | `black --version; white --check tellsticknet setup.py; pylint -E tellsticknet setup.py; flake8 ...; yamllint ...` |
| `tox` | runs `py.test tellsticknet` with `--doctest-modules` (doctests in source are tested) |

## Testing quirks
- Tests live in `tellsticknet/test_protocols.py` (pytest) **and** as doctests in `tellsticknet/protocol.py` — both run under `tox`.
- `tox.ini` only defines env `py37`; CI runs on Python 3.7 (Xenial). Pipfile declares 3.12.

## Package structure
- `tellsticknet/__main__.py` — CLI entrypoint. Commands: `discover`, `listen`, `send`, `mqtt`, `mock`, `parse`, `devices`, `sensors`.
- `tellsticknet/protocols/` — per-protocol modules loaded dynamically via `importlib.import_module`. Each must implement `decode()` and `encode()`.
- Entry point: `tellsticknet=tellsticknet.__main__:app_main` (set in `setup.py`).

## Gotchas
- `script/tellsticknet` hardcodes `python3.7` — if you don't have 3.7, use `python3 -m tellsticknet` directly.
- Config is YAML (`tellsticknet.conf` / `.tellsticknet.conf`) looked up in CWD, `$HOME`, `$XDG_CONFIG_HOME` (see `tellsticknet-sample.conf`).
- Docker entrypoint is `python3 -m tellsticknet mqtt`; exposes UDP ports 30303 and 42314.
- Uses `pipenv` for dev; `requirements.txt` for runtime install.
- Protocol implementations adapted from [telldus-core](https://github.com/telldus/telldus/tree/master/telldus-core/service). See `tellsticknet/test_protocols.py` for exact test vectors.

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
