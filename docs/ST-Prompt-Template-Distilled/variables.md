# Variables

## Scopes

| Scope | Storage | Persistence |
|-------|---------|-------------|
| `cache` | Runtime variable map | Lost after current generate/render |
| `message` | `chat[msg_id].variables[swipe_id]` | Saved with chat |
| `local` | `chat_metadata.variables` | Saved with chat |
| `global` | `extension_settings.variables.global` | Global across all chats |
| `initial` | `[InitialVariables]` WI entry | Persisted with worldbook data |

Merge priority (read order): `message` > `local` > `global`

## Set Functions

```typescript
function setvar(key, value, options?: SetVarOption)
function setLocalVar(key, value, options?: SetVarOption)
function setGlobalVar(key, value, options?: SetVarOption)
function setMessageVar(key, value, options?: SetVarOption)
```

**SetVarOption:**
- `index` — array/object variable index
- `scope` — `'global' | 'local' | 'message' | 'cache' | 'initial'` (default: `'message'`)
- `flags` — `'nx'` (set if not exists) | `'xx'` (set if exists) | `'n'` (force) | `'nxs'` (set if not exists in scope) | `'xxs'` (set if exists in scope)
- `results` — `'old' | 'new' | 'fullcache'`
- `merge` — boolean, uses lodash `_.merge`
- `dryRun` — boolean, allows setting during preparation phase
- `noCache` — boolean, refreshes cache immediately
- `withMsg` — `MessageFilter`, select target message

## Get Functions

```typescript
function getvar(key, options?: GetVarOption)
function getLocalVar(key, options?: GetVarOption)
function getGlobalVar(key, options?: GetVarOption)
function getMessageVar(key, options?: GetVarOption)
```

**GetVarOption:**
- `scope` — (same as above) default: `'cache'`
- `defaults` — fallback value if not found
- `clone` — boolean, returns deep copy
- `noCache` — bypass cache
- `withMsg` — MessageFilter

## Increment/Decrement

```typescript
function incvar(key, value?, options?)    // increment by value (default 1)
function incLocalVar/incGlobalVar/incMessageVar(key, value?, options?)
function decvar(key, value?, options?)    // decrement by value (default 1)
function decLocalVar/decGlobalVar/decMessageVar(key, value?, options?)
```

## Delete

```typescript
function delvar(key, index?, options?)
function delLocalVar/delGlobalVar/delMessageVar(key, index?, options?)
```

## Insert

```typescript
function insvar(key, value, index?, options?)
function insertLocalVar/insertGlobalVar/insertMessageVar(key, value, index?, options?)
```

## Special Variables (set automatically)

| Variable | Description |
|----------|-------------|
| `LAST_SEND_TOKENS` | Input token count of last generation |
| `LAST_SEND_CHARS` | Input character count of last generation |
| `LAST_RECEIVE_TOKENS` | Output token count of last generation |
| `LAST_RECEIVE_CHARS` | Output character count of last generation |

## Examples

```ejs
<% setvar('好感度', 100) %>
好感度：<%- getvar('好感度') %>

<% incvar('好感度', 10) %>
<% delvar('好感度') %>

<% setLocalVar('stats', { hp: 100, mp: 50 }) %>
HP: <%- getvar('stats.hp') %>
```
