---
description: Archive old completed tasks to tasks-archive.md
---

Scan tasks.md for all completed tasks marked with `[x]`.

If fewer than 2 completed tasks are found, print "Not enough completed tasks to archive. Leaving them as context bridges." and stop.

1. Sort the completed tasks by chronological order or document position.
2. Keep the absolute latest/most recently completed `[x]` task (including its sub-bullets) inside tasks.md to preserve the active context bridge.
3. Move/Cut all older `[x]` tasks and their nested sub-bullet metadata structures from tasks.md.
4. Append them smoothly to the bottom of tasks-archive.md under the main header.
5. Print a summary: "Archived <count> task(s) to tasks-archive.md. Kept the latest task as a context bridge."
