# Variables

## Variable Types

| type | backing store | persistence |
|------|---------------|-------------|
| `global` | `extension_settings.variables.global` | saves on write |
| `preset` | preset settings `variables` key | saves on write |
| `character` | character settings `variables` key | saves on write |
| `chat` | `chat_metadata.variables` | debounced save |
| `message` | per-message per-swipe `variables[swipe_id]` | debounced save |
| `script` | iframe runtime data (ephemeral) | not persisted |
| `extension` | `extension_settings[extension_id]` | saves on write |

## Option Types

```typescript
type VariableOptionNormal = { type: 'chat' | 'character' | 'preset' | 'global' };
type VariableOptionMessage = { type: 'message'; message_id?: number | 'latest' };
type VariableOptionScript = { type: 'script'; script_id?: string };
type VariableOptionExtension = { type: 'extension'; extension_id: string };
type VariableOption =
  | VariableOptionNormal
  | VariableOptionMessage
  | VariableOptionScript
  | VariableOptionExtension;
```

## Public API

```typescript
function getVariables(option?: VariableOption): Record<string, any>
// Returns a deep-cloned copy of variables for the given scope.
// Default option: { type: 'chat' }.

function replaceVariables(variables: Record<string, any>, option?: VariableOption): void
// Replaces the entire variables object for the given scope.

function updateVariablesWith(
  updater: ((v: Record<string, any>) => Record<string, any>)
    | ((v: Record<string, any>) => Promise<Record<string, any>>),
  option?: VariableOption
): Record<string, any> | Promise<Record<string, any>>
// Gets variables, applies updater, saves result. Return type matches updater sync/async.

function insertVariables(variables: Record<string, any>, option?: VariableOption): Record<string, any>
// Merges variables INTO existing (existing keys win). Uses lodash mergeWith, arrays replaced by new.

function insertOrAssignVariables(variables: Record<string, any>, option?: VariableOption): Record<string, any>
// Merges existing INTO variables (new keys win). Uses lodash mergeWith, arrays replaced by new.

function deleteVariable(
  variable_path: string,
  option?: VariableOption
): { variables: Record<string, any>; delete_occurred: boolean }
// Unsets a nested path via lodash.unset. Returns the updated variables and whether deletion happened.

function registerVariableSchema(
  schema: z.ZodType<any>,
  options: { type: 'global' | 'preset' | 'character' | 'chat' | 'message' }
): void
// Registers a Zod schema for validation of a variable scope. Applied when variables are set via UI.
```

## Iframe-Internal (_bind) API

```typescript
function _getVariables(this: Window, option?: VariableOption): Record<string, any>
// Like getVariables but defaults type='script' to current script's id.

function _getAllVariables(this: Window): Record<string, any>
// Merges global + character + script + chat + message scope.
// Message scope is included only inside TH-message iframes.
// Earlier scopes are overwritten by later ones (assign merge order).

function _replaceVariables(this: Window, variables: Record<string, any>, option?: VariableOption): void
function _updateVariablesWith(this: Window, updater, option?): Record<string, any> | Promise<Record<string, any>>
function _insertVariables(this: Window, variables: Record<string, any>, option?): Record<string, any>
function _insertOrAssignVariables(this: Window, variables: Record<string, any>, option?): Record<string, any>
function _deleteVariable(this: Window, variable_path: string, option?): { variables; delete_occurred: boolean }
// All _ variants auto-resolve type='script' to the current iframe's script id.
```

## Prompt Macros

```
{{get_global_variable::key}}              -> outputs extension_settings.variables.global[key]
{{format_global_variable::key}}           -> JSON.stringify(value)
{{get_character_variable::key}}           -> current character settings variables[key]
{{format_character_variable::key}}        -> JSON.stringify(value)
{{get_chat_variable::key}}               -> chat_metadata.variables[key]
{{format_chat_variable::key}}            -> JSON.stringify(value)
{{get_message_variable::key}}            -> current message swipe variables[key]
{{format_message_variable::key}}         -> JSON.stringify(value)
{{get_preset_variable::key}}             -> current preset variables[key]
{{format_preset_variable::key}}          -> JSON.stringify(value)
```

## Examples

```typescript
// Read chat variables
const vars = TavernHelper.getVariables({ type: 'chat' });

// Update a nested value
TavernHelper.updateVariablesWith(old => ({ ...old, count: (old.count ?? 0) + 1 }), { type: 'chat' });

// Delete a key
const result = TavernHelper.deleteVariable('temp_data', { type: 'global' });

// Register a schema (validates UI edits)
TavernHelper.registerVariableSchema(z.object({ hp: z.number(), mp: z.number() }), { type: 'character' });
```
