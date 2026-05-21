# MVU Commands

## Core Update Commands

LLM outputs these inside `<UpdateVariable>` block:

### _.set - Set Value

```
_.set('path', newValue);//reason
_.set('path', oldValue, newValue);//reason (oldValue is informational)
_.set('path[0]', newValue);//reason (precise VWD targeting)
```

### _.add - Numeric Delta

```
_.add('path', delta);//reason
_.add('gold', 10);         // +10
_.add('health', -5);       // -5
_.add('currentTime', 600000); // ms delta for dates
```

### _.assign - Insert into Collection

```
// Append to array (2 args)
_.assign('inventory', 'new item');//reason

// Insert at index (3 args)
_.assign('inventory', 0, 'scroll');//reason

// Set object key (3 args)
_.assign('achievements', 'FIRST', 'met Alice');//reason
```

### _.remove - Delete

```
_.remove('path');                           // delete whole variable
_.remove('inventory', 'potion');            // remove by value from array
_.remove('inventory', 2);                   // remove by index from array
_.remove('achievements', 'FIRST');          // remove by key from object
_.remove('achievements', 1);                // remove by index from object
```

## JSON Patch (RFC 6902) Dialect

### Standard Operations

```json
[
    { "op": "replace", "path": "/affinity", "value": 60 },
    { "op": "add", "path": "/inventory/-", "value": "sword" },
    { "op": "remove", "path": "/inventory/0" },
    { "op": "move", "from": "/active/0", "path": "/completed/-" }
]
```

### Extended Operations

| op | Description | Value |
|----|-------------|-------|
| `delta` | Numeric add/subtract | number |
| `insert` | Alias for add on array | any |

Enclosed in `<JSONPatch>...</JSONPatch>` inside `<UpdateVariable>`.

## Command Extraction

State machine parser with bracket matching, string-aware. Handles nested structures:

```javascript
_.set('path', ["complex].value"], [[]]);  // correctly parsed
```

## CommandInfo Types

```typescript
type CommandInfo =
    | SetCommandInfo    // type: 'set'
    | InsertCommandInfo // type: 'insert' / 'assign'
    | DeleteCommandInfo // type: 'delete' / 'remove' / 'unset'
    | AddCommandInfo    // type: 'add'
    | MoveCommandInfo;  // type: 'move'

type SetCommandInfo = {
    type: 'set';
    full_match: string;
    args: [path: string] | [path: string, old: string, new: string];
    reason: string;
};
```

## Math Expressions

All command values support mathjs evaluation:

```
_.set('affinity', 10, 10 + 2);        // -> 12
_.set('affinity', 10, math.pow(2,3)); // -> 8
_.add('affinity', math.sin(Math.PI)); // -> 0
```

Quoted strings are NOT evaluated:
```
_.set('date', '2000-01-01');        // safe, stored as string
```

## Path Resolution

- `pathFix()` normalizes paths with bracket notations `[0]`, quoted keys `["key with space"]`, and dot vs bracket hybrid.
- `parseCommandValue()` converts string args to typed values (JSON, number, boolean, null, math expression).
