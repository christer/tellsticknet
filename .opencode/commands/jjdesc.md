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
