# World Book

## Get Entry Content

```typescript
function getwi(lorebook?, title, data?): string
function getWorldInfo(lorebook?, title, data?): string
```

`lorebook` — worldbook name (optional, uses all enabled if omitted)
`title` — entry name, uid, or regex pattern
`data` — optional context object for EJS in entry content

## Activate Entry

```typescript
function activewi(lorebook?, title, force?): boolean
function activateWorldInfo(lorebook?, title, force?): boolean
function activateWorldInfoByKeywords(keywords, condition?): void
```

`force` — boolean, activates even if disabled
`keywords` — string or string[]
`condition` — `'AND' | 'OR'` (default `'OR'`)

## Query Entries

```typescript
function getWorldInfoEntries(name?): WorldInfoEntry[]
// Returns all entry data for a worldbook

function getWorldInfoActivatedData(name, keyword, condition?): ActivatedEntry[]
// Returns data of activated entries matching keywords

function getEnabledWorldInfoEntries(chara?, global?, persona?, charaExtra?, onlyExisting?): WorldInfoEntry[]
// Gets entries across all scopes: character, global, persona, character extra

function getEnabledLoreBooks(chara?, global?, persona?, charaExtra?): string[]
// Gets enabled worldbook names

function selectActivatedEntries(entries, keywords, condition?): WorldInfoEntry[]
// Filters activated entries from list by keywords

function getWorldInfoData(name): WorldInfoData
// Gets raw worldbook data structure
```

## Title Tags (for injection placement)

| Prefix | Placement |
|--------|-----------|
| `[GENERATE:BEFORE]` | Start of LLM prompt |
| `[GENERATE:AFTER]` | End of LLM prompt |
| `[RENDER:BEFORE]` | Before rendered message |
| `[RENDER:AFTER]` | After rendered message |
| `[GENERATE:N:BEFORE]` | Before the N-th message |
| `[GENERATE:N:AFTER]` | After the N-th message |
| `[GENERATE:REGEX:pattern]` | When message matches regex |
| `[InitialVariables]` | Initial variable tree (JSON content) |
| `[Preprocessing]` | Pre-process before ST handling |

## Decorators (in entry content, line-start `@@`)

| Decorator | Effect |
|-----------|--------|
| `@@activate` | Force blue entry |
| `@@dont_activate` | Prevent activation |
| `@@generate_before` | Same as `[GENERATE:BEFORE]` |
| `@@generate_after` | Same as `[GENERATE:AFTER]` |
| `@@render_before` | Same as `[RENDER:BEFORE]` |
| `@@render_after` | Same as `[RENDER:AFTER]` |
| `@@dont_preload` | Skip during preload |
| `@@initial_variables` | Same as `[InitialVariables]` |
| `@@always_enabled` | Force-enable special entries |
| `@@only_preload` | Enable only during preload |
| `@@private` | Wrap to avoid variable conflicts |
| `@@if condition` | Conditional include |
| `@@iframe [title]` | Wrap in iframe |
| `@@preprocessing` | Pre-process entry |
| `@@message_formatting` | Apply message formatting |

## Example

```ejs
<% if(variables.好感度 > 80) { %>
  <%- await getwi("lily is lover") %>
<% } %>
```
