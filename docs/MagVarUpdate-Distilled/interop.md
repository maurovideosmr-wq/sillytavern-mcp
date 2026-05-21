# MVU Interop

## From Other Extensions

```typescript
// 1. Wait for MVU to be ready
await waitGlobalInitialized('Mvu');

// 2. Get current variables
const vars = Mvu.getMvuData({ type: 'message', message_id: 'latest' });

// 3. Modify
_.set(vars.stat_data, 'affinity', 50);

// 4. Save back
await Mvu.replaceMvuData(vars, { type: 'message', message_id: 'latest' });

// Or use parseMessage to process LLM commands
const newVars = await Mvu.parseMessage(
    "_.set('affinity', 50);//script update",
    Mvu.getMvuData({ type: 'chat' })
);
await Mvu.replaceMvuData(newVars, { type: 'chat' });
```

## Via Events

```typescript
// Listen for updates
eventOn('mag_variable_update_ended', (variables, before) => {
    console.log('Updated:', variables.stat_data);
});

// Trigger MVU processing
const result = await eventEmit('mag_invoke_mvu', {
    old_variables: currentMvuData
});

// Direct variable update
await eventEmit('mag_update_variable', statData, path, newValue, reason);
```

## Via TavernHelper

MVU is accessible via TavernHelper's variable system:

```typescript
// Get raw MvuData from message variables
const data = TavernHelper.getVariables({
    type: 'message',
    message_id: message_id
});

// Check if it's MvuData
if (data.stat_data && data.schema) {
    const val = _.get(data.stat_data, 'affinity');
}
```

## With ST-Prompt-Template

In EJS worldbook entries:

```ejs
<% if (getvar("stat_data").affinity[0] >= 50) { %>
// high affinity behavior
<% } %>
```

Note: `getvar("stat_data")` returns the whole object. Access paths with `[0]` for VWD values.

## Script Button API

MVU registers buttons via `appendInexistentScriptButtons()` and `getButtonEvent()`. Other scripts can trigger MVU actions:

```typescript
// Trigger MVU re-process
await triggerSlash('/button reprocess-variables');
```
