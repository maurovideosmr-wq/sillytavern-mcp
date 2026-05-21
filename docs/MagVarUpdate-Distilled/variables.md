# MVU Variables

## Data Layers

Three layers stored in chat message `variables`:

| Layer | Key | Description |
|-------|-----|-------------|
| State | `stat_data` | Current variable values, read by LLM |
| Display | `display_data` | Visual diff `"old->new (reason)"`, for UI |
| Delta | `delta_data` | Only changed vars this turn, same format |

## MvuData Structure

```typescript
type MvuData = {
    stat_data: StatData & RootAdditionalMetaProps;
    schema: ObjectSchemaNode & Partial<RootAdditionalProps>;
    display_data?: Record<string, any>;
    delta_data?: Record<string, any>;
    initialized_lorebooks: Record<string, any[]>;
    [key: string]: any;
};
```

## ValueWithDescription (VWD)

A pair `[value, description]`:

```json5
{ "affinity": [50, "range[-100,100], updates with interaction, delta[-5,8]"] }
```

- Index 0 = actual value
- Index 1 = description / change condition

Path convention: use `[0]` to target the value:
```
_.set('li.affinity[0]', 55);    // recommended
_.set('li.affinity', 55);       // backward-compat by VWD detection
```

VWD detection: `Array.isArray(v) && v.length === 2 && typeof v[1] === 'string'`

## InternalData

```typescript
type InternalData = {
    display_data: Record<string, any>;
    delta_data: Record<string, any>;
};
```

Attached at `stat_data.$internal` during update processing, removed after.

## Schema

```typescript
type ObjectSchemaNode = {
    type: 'object';
    properties: { [key: string]: SchemaNode & { required?: boolean } };
    extensible?: boolean;
    recursiveExtensible?: boolean;
    template?: TemplateType;
};

type ArraySchemaNode = {
    type: 'array';
    elementType: SchemaNode;
    extensible?: boolean;
    template?: TemplateType;
};

type PrimitiveSchemaNode = {
    type: 'string' | 'number' | 'boolean' | 'any';
};
```

## RootAdditionalProps

```typescript
type RootAdditionalProps = {
    strictTemplate?: boolean;    // default false
    concatTemplateArray?: boolean; // default true
    strictSet?: boolean;         // default false
};
```
