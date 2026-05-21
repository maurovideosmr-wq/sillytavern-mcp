# MVU Schema System

## Purpose

Schema auto-generates from [InitVar] data structure. It controls which parts of the variable tree LLM can modify via `_.assign`/`_.remove`, preventing accidental structural corruption.

## $meta Configuration

Place `$meta` on any object in [InitVar] JSON:

```json5
{
    "$meta": {
        "extensible": false,             // allow new keys (default false)
        "required": ["Alice", "Bob"],    // keys that cannot be _remove'd
        "recursiveExtensible": true,     // propagate extensible to all children
        "template": { ... },             // default values for new keys
        "strictSet": false,              // disable VWD compat on _set
        "strictTemplate": false,         // forbid implicit string->[string] cast
        "concatTemplateArray": true      // true=concat, false=merge arrays
    }
}
```

## $__META_EXTENSIBLE__$ Marker

Place inside arrays to mark them extensible:

```json5
{
    "weapons": [["$__META_EXTENSIBLE__$", "sword", "shield"], "weapon inv"]
}
```

Both $meta and marker are cleaned from runtime data after schema generation.

## Schema Generation

```typescript
function generateSchema(data: any, oldSchemaNode?: SchemaNode,
    parentRecursiveExtensible?: boolean): SchemaNode
```

- Recursively walks stat_data
- Reads $meta for extensible/required/template
- Detects $__META_EXTENSIBLE__$ in arrays
- Merges with existing schema for incremental updates
- Produces ObjectSchemaNode | ArraySchemaNode | PrimitiveSchemaNode

## Schema Enforcement

### On _.assign

- Non-extensible object: block key insertion
- Non-extensible array: block element addition
- Missing parent path: block unless extensible parent

### On _.remove

- Array: block if not extensible
- Object: block if key is `required: true`

### On _.set

- VWD strict mode (`strictSet: true`): set entire value, no VWD wrapping
- Default (`strictSet: false`): preserve `[value, desc]` pair, update only value

## Array Template via $arrayMeta

```json5
{
    "memories": [
        { "$meta": { "template": ["important memory"] }, "$arrayMeta": true }
    ]
}
```

`_.assign('memories', ["became a cat"])` -> `[["became a cat", "important memory"]]`

## reconcileAndApplySchema

Called after every variable update. Deep-clones current stat_data, regenerates schema via generateSchema (preserving old metadata), then replaces variables.schema.

## cleanUpMetadata

Recursively removes $meta, $arrayMeta, $__META_EXTENSIBLE__$ from data. Called during init and each applyTemplate.
