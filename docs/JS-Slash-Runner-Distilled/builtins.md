# Built-in Third-Party Libraries

## Globally Available (in script/message iframes)

| Global | Library | Description |
|--------|---------|-------------|
| `$` | jQuery | DOM manipulation and event handling |
| `_` | Lodash | Utility functions (clone, get, set, merge, etc.) |
| `PIXI` | Pixi.JS | 2D rendering engine for animations and games |
| `Vue` | Vue 3 | Reactive UI framework (runtime global prod build) |
| `VueRouter` | Vue Router | Official Vue 3 router |
| `YAML` | js-yaml | YAML parser and stringifier |
| `z` | zod | Schema validation library |
| `toastr` | toastr | Notification toasts (`info`, `success`, `warning`, `error`) |
| `showdown` | Showdown | Markdown-to-HTML converter |
| `Popper` | Popper.js | Tooltip/popover positioning engine |
| `hljs` | highlight.js | Code syntax highlighting |
| `EjsTemplate` | ST EJS Template | SillyTavern's EJS prompt template engine |

jQuery UI (with touch-punch) and Tailwind CSS are also available in message iframes. FontAwesome icons are loaded in message iframes.

## TavernHelper.builtin Object

```typescript
const builtin = {
  addOneMessage: (message, options?) => any,
  copyText: (text: string) => void,
  duringGenerating: () => boolean,
  getImageTokenCost: (url: string) => Promise<number>,
  getVideoTokenCost: (url: string) => Promise<number>,
  parseRegexFromString: (str: string) => RegExp | null,
  promptManager: object,
  reloadAndRenderChatWithoutEvents: () => any,
  reloadChatWithoutEvents: () => any,
  reloadEditor: (world: string) => void,
  reloadEditorDebounced: (world: string) => void,
  renderMarkdown: (text: string) => string,
  renderPromptManager: () => void,
  renderPromptManagerDebounced: () => void,
  saveSettings: () => void,
  uuidv4: () => string,
};
```

- `addOneMessage`: Add a message to the chat display (not persistent).
- `copyText`: Copy text to clipboard.
- `duringGenerating`: Returns `true` if ST is currently generating.
- `getImageTokenCost` / `getVideoTokenCost`: Calculate token cost for media URLs.
- `parseRegexFromString`: Parse `"/pattern/flags"` string into RegExp, or `null` on failure.
- `promptManager`: ST's PromptManager instance for preset prompt manipulation.
- `reloadAndRenderChatWithoutEvents`: Full chat reload and re-render without firing events.
- `reloadChatWithoutEvents`: Reload chat data without firing events.
- `reloadEditor` / `reloadEditorDebounced`: Reload a worldbook editor by name.
- `renderMarkdown`: Convert markdown string to HTML.
- `renderPromptManager` / `renderPromptManagerDebounced`: Re-render preset prompts.
- `saveSettings`: Save ST settings immediately.
- `uuidv4`: Generate a v4 UUID.

```typescript
// Copy text to clipboard
builtin.copyText('Copied text');

// Check if generating
if (builtin.duringGenerating()) {
  toastr.warning('Generation in progress');
}

// Render markdown
const html = builtin.renderMarkdown('**bold** text');

// Generate UUID
const id = builtin.uuidv4();
```
