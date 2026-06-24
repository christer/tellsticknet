---
description: Pause the current active focus task
---

Find the task currently marked with `[/]` inside tasks.md.
If no task has `[/]`, print "No active task to pause" and stop.

1. Change its symbol from `[/]` to `[-]`.
2. Check if jj is accessible: `jj log -r @ -n 1 --template 'change_id.short()' 2>/dev/null`
3. Extract the short change ID (or use "no-jj" if inaccessible).
4. Prompt the user: "What note or reason should I add for pausing this task?"
5. Append their reply along with the Jujutsu metadata as sub-bullets below the task line:
   - **Paused Reason**: <User's response>
   - **Jujutsu Tracking**: Paused on Change `<change_id>`
