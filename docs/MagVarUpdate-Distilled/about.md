# MagVarUpdate (MVU) - About

## Summary

MagVarUpdate (MVU) is a SillyTavern Tavern-Helper script for variable-based state management. It lets the LLM output only differential data (variable change records) instead of full state every turn, reducing token consumption and improving reliability.

## Version

- Branch: beta
- License: MIT
- Author: MagicalAstrogy
- Min TH version: 3.4.17

## Links

- GitHub: https://github.com/MagicalAstrogy/MagVarUpdate
- Sample card: https://discord.com/channels/1291925535324110879/1367723727827111998
- Beta sample card: https://gitgud.io/KazePsi/file-storage/-/tree/master/mobius/example

## Install

1. Add local script to character card:
```javascript
import 'https://gcore.jsdelivr.net/gh/MagicalAstrogy/MagVarUpdate@master/artifact/bundle.js'
```

2. Add regex "RemoveVariableUpdate":
- Pattern: `/<UpdateVariable>[\s\S]*?<\/UpdateVariable>/gm`
- Scope: AI output
- Options: format-only-display + format-only-prompt

3. Add regex "HideStatusPlaceholderFromAI":
- Pattern: `<StatusPlaceHolderImpl/>`
- Scope: AI output
- Options: format-only-prompt

4. Add lorebook entry (blue D1) outputting variable list via `get_message_variable::stat_data` with update rules description.

## Build

```bash
corepack enable && corepack prepare yarn@3.4.1 --activate
yarn install
yarn build        # production build -> artifact/bundle.js
yarn build:dev    # dev build
yarn watch        # dev watch mode
yarn test         # run tests (jest)
```

## Architecture

```
main.ts -> init all modules:
  initPanel()       - Vue config panel
  initButtons()     - Script buttons
  initGlobals()     - window.parent.Mvu API
  initInitvar()     - Variable init on GENERATION_STARTED/MESSAGE_SENT
  initRequest()     - Entry/prompt filtering, function calling registration
  initResponse()    - Variable processing on MESSAGE_SENT/MESSAGE_RECEIVED
  initCleanup()     - Auto-cleanup old variables
  initExportedEvents() - External event interface
```
