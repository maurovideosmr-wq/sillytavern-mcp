# MVU Variable Initialization

## InitVar Lorebook Entries

Create lorebook entries with comment containing `[InitVar]` (case-insensitive). Content is JSON5 format:

```json5
{
    "date": ["03-15", "date format MM-DD"],
    "time": ["09:00", "hh:mm, update per action"],
    "user": {
        "identity": ["new priest", "changes with story"],
        "location": ["church", "user location"]
    },
    "li": {
        "affinity": [15, "range[-100,100]"],
        "mood": {
            "pleasure": [0.1, "range[-1,1], emotion change"]
        }
    }
}
```

- Each var is a `[value, description]` pair
- Support arbitrary nesting
- Entries can be disabled (turned off); MVU still reads them
- Multiple [InitVar] entries per lorebook are merged via correctlyMerge

## InitVar with <initvar> XML Block

Alternatively embed <initvar> in worldbook content directly:

```xml
<initvar>
```json5
{ "user": { "identity": ["traveler", "desc"] } }
```
</initvar>
```

## Alternate Greeting Overrides

In alternate greetings (extra first messages), add `<UpdateVariable>` block:

```

<UpdateVariable>
_.set('user.identity', 'unknown', 'new priest');//greeting init
_.set('li.affinity', 0, 15);//greeting init
</UpdateVariable>
```

Old value is ignored (accepts anything). These override [InitVar] base values.

## Init Check Logic

```typescript
async function initCheck():
    if welcome page -> skip
    if no messages -> skip
    variables = getLastValidVariable(latest+1) ?? createEmptyGameData()
    for each lorebook:
        if not already initialized (checked via initialized_lorebooks record):
            load [InitVar] entries
            correctlyMerge into stat_data
    generate schema from stat_data
    cleanUpMetadata (remove $meta, $__META_EXTENSIBLE__$)
    if message_id == 0:
        process each swipe: apply <initvar> blocks, run updateVariables
    else:
        replaceVariables at latest

triggered on: GENERATION_STARTED, MESSAGE_SENT
```

## Initialized Lorebooks Tracking

- Format: `Record<string, any[]>` (was string[] in old versions, auto-migrated)
- Key = lorebook name, value = []
- Prevents re-initializing the same lorebook

## Empty GameData

```typescript
function createEmptyGameData(): MvuData {
    return {
        display_data: {},
        initialized_lorebooks: {},
        stat_data: {},
        delta_data: {},
        schema: { type: 'object', properties: {} },
    };
}
```
