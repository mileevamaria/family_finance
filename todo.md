Basic commands:
- Research WhatsApp bots, avoid rigid Telegram dependencies
- /export
  + all
  + YYYY-MM-DD - YYYY-MM-DD
- /delete (+ confirmation)
- /category_add
  + empty -> ask
  + <name> -> add category + notify
- /category_list - lists them
- /report (image, matplotlib, pie/bar chart or whatever)
  + all
  + YYYY-MM-DD - YYYY-MM-DD
  + YTD
  + MTD

Add expense:
- Notify when added DONE
- <number> <category> DONE
- <category> <number> DONE
- Matching:
  + Strict case insensitive match DONE
  + Strict contains match DONE
  + 2+ matches -> Give user a choice (check how many buttons are possible, if more matches than this number, tell user about that and ask for clarification)
  + None found -> Create new category request
- <category> -> We're adding to category X, gimme the number DONE
- <number> -> We're adding X amount, gimme the category DONE

Backlog:
- Figure out currencies + conversion rates
- Category aliases
- Levenshtein distance for category matching
- Rename category
- Collaboration
- Logs
- Taskfile
- README.md