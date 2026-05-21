# Dynamic Regex

Temporary regex replacements that apply during prompt processing or message rendering.

## activateRegex

```typescript
function activateRegex(pattern, replacement, opts?): boolean
```

**pattern** — regex string or RegExp object
**replacement** — string (with `$1` backrefs) or function `(match, ...groups) => string`
**opts** — options object:

| Option | Type | Description |
|--------|------|-------------|
| `generate` | boolean | Apply during generation (supports function replacement) |
| `render` | boolean | Apply during message rendering |
| `basic` | boolean | Use ST's basic regex system (string-only replacement) |
| `raw` | boolean | Use raw message content instead of HTML |
| `globalMatch` | boolean | Replace all occurrences vs first match |
| `once` | boolean | Run only once then auto-remove |
| `uid` | string | Unique ID for deduplication |

### Modes

- **basic** — uses ST's built-in regex system, string replacement only
- **generate** — applies during generation, supports function replacement
- **message** — applies during message rendering, supports HTML or raw content

## deactivateRegex

```typescript
function deactivateRegex(selector?, count?): number
```
Removes temporary regex entries.
- `selector` — filter string or regex
- `count` — number of entries to remove
- Returns count of removed entries

## Examples

```ejs
<%
    activateRegex(/\{\{getvars::([a-zA-Z0-9_]+?)\}\}/gi, function(match, varName) {
        return this.getvar(varName);
    }, { generate: true });
%>

<% activateRegex(/\[b\]/g, '<strong>', { render: true }) %>
```
