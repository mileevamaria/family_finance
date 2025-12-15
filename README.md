# Family Finance

Accounting of family's expenses.

## Tasks

### TODO

- [x] Move stuff from todo.md here
- [ ] /export
  - [ ] all
  - [ ] YYYY-MM-DD - YYYY-MM-DD
- [ ] /delete (+ confirmation)
- [ ] /category_add
  - [ ] empty -> ask
  - [ ] <name> -> add category + notify
- [ ] /category_list - lists them
- [ ] /report (image, matplotlib, pie/bar chart or whatever)
  - [ ] all
  - [ ] YYYY-MM-DD - YYYY-MM-DD
  - [ ] YTD
  - [ ] MTD
- [x] Add expense:
  - [x] Notify when added
  - [x] <number> <category>
  - [x] <category> <number> 
  - [x] <category> -> We're adding to category X, gimme the number
  - [x] <number> -> We're adding X amount, gimme the category
- Category matching:
  - [x] Strict case insensitive match
  - [x] Strict contains match
  - [ ] 2+ matches -> Give user a choice (check how many buttons are possible, if more matches than this number, tell user about that and ask for clarification)
  - [ ] None found -> Create new category request
- [x] Figure out GitHub profile and Git committer mismatch
- [x] Remove unused dependencies
- [x] Avoid non-strict dependency versions
- [ ] Migrate from requests to aiohttp
- [ ] Learn about `async with`, async context managers, and how to use them properly
- [ ] `main` function, reusable TG API client, reuse SQLite connection, pass all dependencies explicitly.
- [ ] Read about SQLite pragmas
- [ ] Make sure all aiosqlite cursors are closed properly
- [ ] Make sure all aiosqlite rollbacks/commits are done properly
- [ ] Learn more stuff about asyncio, asyncio.Lock, asyncio.gather (avoid asyncio.Task for now)
- [ ] Learn about FastAPI graceful shutdown (signals, SIGERM, SIGKILL, etc)

### Backlog

- [ ] Research WhatsApp bots, avoid rigid Telegram dependencies
- [ ] Figure out currencies + conversion rates
- [ ] Category aliases
- [ ] Levenshtein distance for category matching
- [ ] Rename category 
- [ ] Collaboration
- [ ] Logs
- [ ] Taskfile
- [ ] README.md
- [ ] Dockerfile
  - [ ] Figure out rootless container
  - [ ] Bind to :8080 instead of :80
  - [ ] Reduce image size (multi-stage build? alpine?)
