---
description: Query and search your task lists
arguments:
  query: The search term or filter
---

If no query is given, print: "Usage: /tasks <todo|paused|done|all|<search-term>>" and stop.

- `todo` — show all lines marked with `[ ]` in tasks.md
- `paused` — show all lines marked with `[-]` in tasks.md
- `all` — show all lines marked with `[ ]`, `[-]`, or `[/]` in tasks.md
- `done` — show all done tasks in tasks.md
- `archived` — show last 10 tasks in tasks-archive.md
- Anything else — grep across tasks.md and tasks-archive.md for the term, and show matching lines with the filename.
