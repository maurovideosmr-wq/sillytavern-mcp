# Processing Flow

## Generate Phase

1. `GENERATION_AFTER_COMMANDS` triggers → process `[GENERATE:BEFORE]` entries
2. `WORLDINFO_ENTRIES_LOADED` triggers → preprocess entries (decorators, conditions, force activation)
3. `CHAT_COMPLETION_SETTINGS_READY` triggers → process all messages:
   - Apply EJS templates
   - Inject `[GENERATE:BEFORE]/[GENERATE:AFTER]` content
   - Apply @INJECT entries
   - Apply external injectPrompt injections
4. After generation: cleanup, save variables, update token stats

## Render Phase

Triggered by: `MESSAGE_UPDATED`, `MESSAGE_SWIPED`, `USER_MESSAGE_RENDERED`, `CHARACTER_MESSAGE_RENDERED`

1. Process `[RENDER:BEFORE]` entries
2. Optionally process raw message content (`raw_message_evaluation_enabled`)
3. Clean up HTML
4. Process `[RENDER:AFTER]` entries
5. Update DOM

## Caching

When enabled (`cache_enabled`), compiled templates are cached:
- LRU cache with configurable size (`cache_size`, default 64)
- Hash algorithm: xxhash (`cache_hasher`, default `'h32ToString'`)
- Modes: 0=disabled, 1=all, 2=worldbook only

## Slash Commands

```
/ejs [ctx=json]? [block=bool]? code
```
Executes EJS template code inline.
- `ctx` — JSON object passed as context
- `block` — if true, wraps code in `<%= ... %>` for output

```
/ejs-refresh
```
Reloads and reprocesses all worldbook entries.

## Exports (globalThis.EjsTemplate)

```typescript
EjsTemplate.evalTemplate(code, context?, options?)
EjsTemplate.prepareContext(context?, end?)
EjsTemplate.getSyntaxErrorInfo(code, max_lines?)
EjsTemplate.setFeatures(features)
EjsTemplate.getFeatures()
EjsTemplate.allVariables(end?)
EjsTemplate.saveVariables()
EjsTemplate.resetFeatures()
EjsTemplate.defines
EjsTemplate.initialVariables
EjsTemplate.refreshWorldInfo()
EjsTemplate.parseJSON(text)
EjsTemplate.jsonPatch(dest, change)
EjsTemplate.compileTemplate(code, options?)
EjsTemplate.finalization
```
