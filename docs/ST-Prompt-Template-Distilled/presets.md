# Presets

```typescript
function getpreset(name, data?): string
// Gets preset prompt content by name, processed through EJS.
// name — preset name
// data — additional context variables

function getPresetPrompt(name, data?): string
function getprp(name, data?): string
// Aliases for getpreset
```

## Example

```ejs
<%- getpreset('角色卡格式') %>
<!-- Loads a preset prompt -->
```
