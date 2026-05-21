# Built-in Macros and registerMacroLike

## Built-in Prompt Macros

Available in character descriptions, system prompts, and any prompt context:

```
{{get_global_variable::key}}          - Output global variable value as string/JSON
{{format_global_variable::key}}       - Format global variable as YAML block
{{get_preset_variable::key}}          - Get current preset variable
{{format_preset_variable::key}}       - Format preset variable as YAML block
{{get_character_variable::key}}       - Get current character variable
{{format_character_variable::key}}    - Format character variable as YAML block
{{get_chat_variable::key}}            - Get current chat variable
{{format_chat_variable::key}}         - Format chat variable as YAML block
{{get_message_variable::key}}         - Get current message variable
{{format_message_variable::key}}      - Format message variable as YAML block
```

`get_` variants return string values directly, or JSON.stringify for objects. `format_` variants return YAML-formatted blocks with literal block scalars.

## registerMacroLike

```typescript
type MacroLikeContext = {
  message_id?: number;
  role?: 'user' | 'assistant' | 'system';
};

function registerMacroLike(
  regex: RegExp,
  replace: (context: MacroLikeContext, substring: string, ...args: any[]) => string,
): { unregister: () => void }

function unregisterMacroLike(regex: RegExp): void
```

- `registerMacroLike`: Registers a custom macro that expands in prompt contexts. The `regex` should match the full `{{...}}` pattern (capture groups become `args`). The `replace` function receives `MacroLikeContext`, the full matched substring, and capture group values. Returns `{ unregister }` to remove the macro. Duplicate regex sources are silently ignored (only first registration applies).
- `unregisterMacroLike`: Removes a registered macro by its RegExp.

```typescript
// Register a custom macro: {{time}}
const { unregister } = registerMacroLike(
  /\{\{time\}\}/g,
  () => new Date().toLocaleTimeString(),
);

// Register with capture: {{repeat::text::count}}
const { unregister } = registerMacroLike(
  /\{\{repeat::(.*?)::(\d+)\}\}/g,
  (_ctx, _sub, text, count) => text.repeat(parseInt(count)),
);

// Remove when done
unregister();
unregisterMacroLike(/\{\{time\}\}/g);
```
