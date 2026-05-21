# ST-Prompt-Template

A SillyTavern extension that enables full JavaScript execution in prompts, character cards, and worldbooks via the [EJS](https://ejs.co/) template engine. Supports dynamic prompt generation, conditional logic, loops, and advanced variable management.

## Version

- Current: 1.16.1.4
- Minimum ST version: not specified
- License: AGPL-3.0
- Author: zonde306
- Repository: https://github.com/zonde306/ST-Prompt-Template

## Installation

Add to SillyTavern extensions from:
```
https://github.com/zonde306/ST-Prompt-Template
```

Or install via the ST extension manager using the same URL.

## Architecture

```
Prompt Text (with <% %> tags)
    │
    ▼
EJS Template Engine (embedded, modified for nested tags)
    │
    ├── Optional: Web Worker (compile_workers setting)
    ├── Optional: iframe sandbox (sandbox setting)
    │
    ▼
    Processed text → sent to LLM or rendered in chat
```

Two processing phases:
- **Generate** — before sending to LLM (`runType: 'generate'`)
- **Render** — when displaying response in chat (`runType: 'render'`)

## Links

- GitHub: https://github.com/zonde306/ST-Prompt-Template
- Docs in repo: `docs/features.md`, `docs/reference.md`
