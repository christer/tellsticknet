---
description: Start working on a task
arguments:
  task_name: The exact name of the task to start
---

If no task_name is given, print "Usage: /task-start <task name>" and stop.

Find the line matching "<task_name>" inside tasks.md:

1. Ensure any other task previously marked as `[/]` is reverted to `[-]`, ask user if there is uncommitted work.
2. Change its checkbox symbol from `[ ]` or `[-]` to `[/]`.
3. Check if jj is accessible by running: `jj log -r @ -n 1 --template 'change_id.short()' 2>/dev/null`
4. If it works, append the following sub-bullet metadata block directly below the active task line:
   - **Jujutsu Tracking**: Active on Change `<change_id>`
