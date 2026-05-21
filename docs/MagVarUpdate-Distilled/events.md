# MVU Events

## Internal Events

```typescript
const variable_events = {
    VARIABLE_INITIALIZED:       'mag_variable_initialized',
    VARIABLE_UPDATE_STARTED:    'mag_variable_update_started',
    COMMAND_PARSED:             'mag_command_parsed',
    VARIABLE_UPDATE_ENDED:      'mag_variable_update_ended',
    BEFORE_MESSAGE_UPDATE:      'mag_before_message_update',
    // deprecated:
    SINGLE_VARIABLE_UPDATED:    'mag_variable_updated',
} as const;
```

## Listener Signatures

```typescript
type ListenerType = {
    [variable_events.VARIABLE_INITIALIZED]:
        (variables: MvuData, swipe_id: number) => void;

    [variable_events.VARIABLE_UPDATE_STARTED]:
        (variables: MvuData, out_is_updated: boolean) => void;

    [variable_events.COMMAND_PARSED]:
        (variables: MvuData, commands: CommandInfo[], message_content: string) => void;

    [variable_events.VARIABLE_UPDATE_ENDED]:
        (variables: MvuData, variables_before_update: MvuData) => void;

    [variable_events.BEFORE_MESSAGE_UPDATE]:
        (context: UpdateContext) => void;

    [variable_events.SINGLE_VARIABLE_UPDATED]:
        (stat_data: Record<string, any>, path: string, oldValue: any, newValue: any) => void;
};
```

## Exported Events (External Interface)

```typescript
const exported_events = {
    INVOKE_MVU_PROCESS: 'mag_invoke_mvu',
    UPDATE_VARIABLE:    'mag_update_variable',
} as const;
```

## Usage Examples

```typescript
// Fix command paths (e.g. gemini adds hyphens)
eventOn(Mvu.events.COMMAND_PARSED, commands => {
    commands.forEach(cmd => {
        cmd.args[0] = cmd.args[0].replace(/-/g, '');
    });
});

// Clamp values after update
eventOn(Mvu.events.VARIABLE_UPDATE_ENDED, (variables, before) => {
    const val = _.get(variables, 'stat_data.affinity');
    if (val < 0) _.set(variables, 'stat_data.affinity', 0);
});

// Add custom commands
eventOn(Mvu.events.COMMAND_PARSED, (variables, commands) => {
    commands.push({
        type: 'set',
        full_match: "_.set('affinity', 5)",
        args: ['affinity', '5'],
        reason: 'script override',
    });
});
```

## Event Flow

```
MESSAGE_SENT/MESSAGE_RECEIVED
    -> VARIABLE_UPDATE_STARTED
    -> extractCommands from message
    -> COMMAND_PARSED (allow modification)
    -> COMMAND_PARSED_for_zod
    -> pathFixPass
    -> execute each command
        -> SINGLE_VARIABLE_UPDATED per command
    -> VARIABLE_UPDATE_ENDED
    -> reconcileAndApplySchema
    -> BEFORE_MESSAGE_UPDATE
    -> save to variables
```
