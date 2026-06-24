# Local Task Tracking

This project uses a unified, low-friction task tracking environment optimized for manual human editing, Jujutsu (`jj`) history tracking, and AI token-efficiency.

---

## 📂 File Architecture

- **README-TASKS.md**: The single master source of truth. Contains documentation, backup blueprints, and installation scripts.
- **AGENTS.md**: Holds short runtime instructions for daily AI operations. Left purposefully sparse to minimize token usage.
- **tasks.md**: The single active repository file. Holds your todo pipeline, active focus, paused tasks, and recent history.
- **tasks-archive.md**: Long-term cold storage. Used to dump rows of completed `[x]` tasks when appropriate to keep `tasks.md` lightning fast.

---

## 🛠 The No-Cut Workflow System

To maximize speed when working manually, tasks are never cut, pasted, or shuffled between headers during daily work. They stay exactly where they are written. State changes are handled exclusively by updating the single-character symbol inside the markdown checkbox:

- `- [ ]` = Unstarted Task (Upcoming backlog item)
- `- [/]` = **Active Focus Task** (The single item currently being coded)
- `- [-]` = **Paused Task** (Shelved midway through; paired with context notes)
- `- [x]` = **Completed Task** (Kept in place to act as a rolling context bridge)

### 📝 Extending Tasks with Rich Context

When a task requires detailed descriptions, acceptance criteria, or technical notes, **never append them to the main task line**. Instead, nest them directly beneath the task using indented sub-bullets (`  *` or `  -`).

This preserves the single-line parsing efficiency for tools and AI agents while keeping all relevant metadata grouped with the task:

- [ ] **Implement User Authentication**: Add JWT session handling.
  - **Requirements**:
    - Must use HTTP-only cookies for token storage.
    - Expire sessions after 15 minutes of inactivity.
  - **Resources**: See RFC 7519 for specification details.
  - **Blocked by**: Database migration task #42.

---

## 📋 Master Blueprint: `tasks.md`

When initializing a fresh tracking file, match this layout exactly:

```markdown
# Project Tasks

## How to use this file

- `- [ ]` = Unstarted Task (Upcoming backlog item)
- `- [/]` = **Active Focus Task** (The single item currently being coded)
- `- [-]` = **Paused Task** (Shelved midway through; paired with context notes)
- `- [x]` = **Completed Task** (Kept in place to act as a rolling context bridge)

## Urgent

- [ ] **Initialize setup**: Begin project configurations. (example task)

## Backlog

- [ ] **Initialize setup**: Add tasks. (example task)
```

---

## 📋 Master Blueprint: `tasks-archive.md`

When initializing a fresh cold-storage log file, match this layout exactly:

```markdown
# Completed Tasks Archive
```

---

## 🤖 Master Blueprint: `AGENTS.md` (Workflow Section Only)

If `AGENTS.md` already exists, do not overwrite it. Append the following block to the very bottom of the existing file to integrate daily issue-handling rules:

```markdown
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
```

---

## 🚀 OpenCode Slash Commands Source Code Matrix

The target AI agent must extract each block below and write it to its respective destination under `.opencode/commands/` during bootstrapping.

### File: `.opencode/commands/current.md`

```markdown
---
description: Show current task status summary
---

Print a brief status summary by inspecting tasks.md:

- Active focus task (marked with `[/]`)
- Total count of unstarted tasks (marked with `[ ]`)
- Total count of paused tasks (marked with `[-]`)
- Latest 3 entries finished tasks (marked with `[x]`)
- jj status
```

### File: `.opencode/commands/task-start.md`

```markdown
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
```

### File: `.opencode/commands/task-pause.md`

```markdown
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
```

### File: `.opencode/commands/task-finish.md`

```markdown
---
description: Mark the active focus task as done and log it
---

Find the task currently marked with `[/]` inside tasks.md.
If no task has `[/]`, print "No active task to finish" and stop.

1. Change its symbol from `[/]` to `[x]`.
2. Check if jj is accessible: `jj log -r @ -n 1 --template 'change_id.short()' 2>/dev/null`
3. Extract the short change ID (or use "no-jj" if inaccessible).
4. Append the following context details as sub-bullets below the completed task line:
   - **Date completed**: [2026-06-16]
   - **Resolution**: <Provide a 1-2 sentence summary based on this session's chat history>
   - **Jujutsu Tracking**: Completed on Change `<change_id>`
```

### File: `.opencode/commands/task-add.md`

```markdown
---
description: Add a new task to the pipeline
arguments:
  task_name: The name of the task to create
---

If no task_name is given, print "Usage: /task-add <name>" and stop.

Append a new unstarted task line to the bottom of the backlog list inside tasks.md:

- [ ] **<task_name>**
```

### File: `.opencode/commands/tasks.md`

```markdown
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
```

### File: `.opencode/commands/task-archive.md`

```markdown
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
```

### File: `.opencode/commands/jjdesc.md`

```markdown
---
description: Generate jj desc message
---

Check if jj is accessible:
`jj log -r @ -n 1 --template 'change_id.short()' 2>/dev/null`

If it works:

- Run `jj status` and `jj diff --stat` for scope
- Scope is changes not yet described (since the last commit)

If it fails:

- Use conversation context
- Scope is changes done this session

Format:
`type: short description`

Types: feat, fix, refactor, test, docs, chore, exp

Include a body with bullet points of key changes.
End with:

Co-authored-by: opencode (AI assistant)
```

---

## 🚀 AI Bootstrapping & Migration Instructions

### Task 1: Environment Initialization

When setting up this workspace for the first time, read this `README-TASKS.md` and complete these steps:

1. Check if `tasks.md` exists. If not, generate it using the `## Master Blueprint: tasks.md`.
2. Check if `tasks-archive.md` exists. If not, generate it using the `## Master Blueprint: tasks-archive.md`.
3. Check `AGENTS.md`. If it already exists, read the `## Master Blueprint: AGENTS.md (Workflow Section Only)` block and append it cleanly to the very bottom of the existing file. Do not touch or overwrite old settings at the top. If it does not exist, create a minimal file including the workflow section.
4. Extract all command blocks listed under the `## 🚀 OpenCode Slash Commands Source Code Matrix` and write them into individual files inside the `.opencode/commands/` directory.

### Task 2: Interactive Migration Routine

If old todo files exist in the project, ask the user if you should migrate them to your newly built `tasks.md` file. Ask the user for confirmation if file names are unclear.

# EOF
