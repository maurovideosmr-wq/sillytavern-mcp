# Interacting with SillyTavern and Other Extensions

## TavernHelper (globalThis.TavernHelper)

All functions documented in these distilled files are accessible via the `TavernHelper` global object (exposed to other extensions as well). You can call any function directly without the `TavernHelper.` prefix from within scripts/frontends.

```typescript
// From another ST extension:
const version = globalThis.TavernHelper.getTavernHelperVersion();
await globalThis.TavernHelper.triggerSlash('/echo hello');
```

### TavernHelper._th_impl

Internal implementation object with low-level access:

```typescript
// Write character extension data
await TavernHelper._th_impl.writeExtensionField(chid, field, value): Promise<void>
```

This is used by `SillyTavern.getContext().writeExtensionField` in the iframe proxy. `chid` is character ID, `field` is the field name (e.g. `'data'`), `value` is the data to write.

## SillyTavern (window.SillyTavern)

SillyTavern's own stable API is available via `window.SillyTavern` (dynamic getter that always returns the latest context):

```typescript
SillyTavern.chat           - Current chat messages array
SillyTavern.characters     - All characters array
SillyTavern.name1          - User name
SillyTavern.name2          - Character name
SillyTavern.this_chid      - Current character ID
SillyTavern.getContext()   - Returns full context with writeExtensionField
```

This is a live proxy - it always reflects the current ST state, not a snapshot from initialization time.

## EjsTemplate

SillyTavern's EJS-based prompt template engine. Available globally:

```typescript
EjsTemplate.evalTemplate(template: string, context?: object): Promise<string>
EjsTemplate.prepareContext(data: object): Promise<object>
EjsTemplate.getFeatures(): EjsTemplate.Features
EjsTemplate.setFeatures(features: Partial<EjsTemplate.Features>): void
```

## Mvu

MagVarUpdate framework for variable management. Available after `await waitGlobalInitialized('Mvu')`:

```typescript
Mvu.getMvuData(options): object
Mvu.parseMessage(content: string, oldData: object): Promise<object>
// + event: 'mag_variable_update_ended' fires when MVU finishes updating variables
```
