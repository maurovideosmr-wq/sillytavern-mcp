# Introduction

JS-Slash-Runner (aka 酒馆助手 / Tavern-Helper) is a SillyTavern extension that runs JavaScript in isolated iframes. It provides a comprehensive API for managing characters, variables, worldbooks, presets, AI generation, events, and more.

## Version

- Current: 4.8.4
- Minimum ST version: 1.12.13
- License: Aladdin Free Public License (AFPL) - restrictive
- Author: KAKAA (N0VI028)

## Links

- GitHub: https://github.com/N0VI028/JS-Slash-Runner
- Documentation: https://n0vi028.github.io/JS-Slash-Runner-Doc/

## Installation

Add to SillyTavern extensions from:
```
https://github.com/n0vi028/JS-Slash-Runner
```

Or install via the ST extension manager using the same URL.

## Build

Build system: pnpm + Vite + TypeScript + Vue 3

```bash
pnpm install
pnpm build    # production build
pnpm watch    # dev mode with hot rebuild
```

Source location: `C:\Users\user\Projects\JS-Slash-Runner`

## Contributing

- Project uses `dist/` in-tree with CI auto-build
- Set git merge driver: `git config --global merge.ours.driver true`
- PRs welcome via GitHub
- Minimum Node 22+ required for development
