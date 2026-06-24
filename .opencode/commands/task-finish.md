---
description: Mark the active focus task as done and log it
---

Find the task currently marked with `[/]` inside tasks.md.
If no task has `[/]`, print "No active task to finish" and stop.

1. Change its symbol from `[/]` to `[x]`.
2. Check if jj is accessible: `jj log -r @ -n 1 --template 'change_id.short()' 2>/dev/null`
3. Extract the short change ID (or use "no-jj" if inaccessible).
4. Append the following context details as sub-bullets below the completed task line:
   - **Date completed**: [2026-06-24]
   - **Resolution**: <Provide a 1-2 sentence summary based on this session's chat history>
   - **Jujutsu Tracking**: Completed on Change `<change_id>`
