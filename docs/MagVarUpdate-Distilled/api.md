# MVU API

## Global Mvu Object

Exposed on `window.parent.Mvu` after MVU loads. Accessible from other ST extensions.

```typescript
const Mvu = {
    events: variable_events,

    getMvuData(options: VariableOption): MvuData,
    replaceMvuData(data: MvuData, options: VariableOption): Promise<void>,

    parseMessage(
        message: string,
        oldData: MvuData
    ): Promise<MvuData | undefined>,

    isDuringExtraAnalysis(): boolean,

    // deprecated:
    getCurrentMvuData(): MvuData,
    replaceCurrentMvuData(data: MvuData): Promise<void>,
    reloadInitVar(data: MvuData): Promise<boolean>,
    setMvuVariable(data: MvuData, path: string, newValue: any, opts?): Promise<boolean>,
    getMvuVariable(data: MvuData, path: string, opts?): any,
    getRecordFromMvuData(data: MvuData, category: string): Record<string, any>,
};
```

### VariableOption

```typescript
type VariableOption = {
    type: 'message' | 'chat' | 'character' | 'global';
    message_id?: number | 'latest';
    script_id?: string;
};
```

## Exported Events

```typescript
// Trigger MVU processing externally:
eventOn('mag_invoke_mvu', async (message_content, in_out_variable_info) => {
    in_out_variable_info.new_variables = klona(in_out_variable_info.old_variables);
    await updateVariables(message_content, in_out_variable_info.new_variables);
    return in_out_variable_info.new_variables;
});

// Direct variable update:
eventOn('mag_update_variable', updateVariable);
```

## Script Buttons

Registered via `initButtons()`:

| Button | Description |
|--------|-------------|
| reprocess-variables | Clear current msg variables, reprocess from message content |
| reload-initvar (legacy) | Reload [InitVar] entries, merge with current variables |
| snapshot-message (legacy) | Mark a message as snapshot (prevent cleanup) |
| replay-messages (legacy) | Replay variable updates from a past message forward |
| retry-extra-analysis | Retry last extra model analysis |
| clear-old-variables (legacy) | Manually clean old message variable data |

## TavernHelper Integration

MVU registers as a unique script (via `registerAsUniqueScript('MVU')`). When multiple MVU instances exist, only the preferred one runs logic.

## waitGlobalInitialized

Other extensions should wait:

```typescript
await waitGlobalInitialized('Mvu');
// now Mvu.getMvuData() etc. are available
```
