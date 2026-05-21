# Tavern Regex

## Types

```typescript
type TavernRegex = {
  id: string;
  script_name: string;
  enabled: boolean;
  find_regex: string;
  trim_strings: string[];
  replace_string: string;
  source: {
    user_input: boolean;
    ai_output: boolean;
    slash_command: boolean;
    world_info: boolean;
  };
  destination: {
    display: boolean;
    prompt: boolean;
  };
  run_on_edit: boolean;
  min_depth: number | null;
  max_depth: number | null;
};

type TavernRegexOption =
  | { type: 'global' }
  | { type: 'character'; name?: string | 'current' }
  | { type: 'preset'; name?: string | 'in_use' };

type FormatAsTavernRegexedStringOption = {
  depth?: number;
  character_name?: string;
};

type ReplaceTavernRegexesOption = TavernRegexOption & {
  /** @deprecated */ scope?: 'all' | 'global' | 'character';
};
```

## API

```typescript
function getTavernRegexes(option?: GetTavernRegexesOption): TavernRegex[]
// Without option.type, uses legacy scope/enable_state filtering (all, global, character).
// With option.type, returns regexes from the specified scope.

function isCharacterTavernRegexesEnabled(): boolean
// Returns whether character-specific regex scripts are enabled for current character.

function formatAsTavernRegexedString(
  text: string,
  source: 'user_input' | 'ai_output' | 'slash_command' | 'world_info' | 'reasoning',
  destination: 'display' | 'prompt',
  options?: FormatAsTavernRegexedStringOption
): string
// Applies tavern regex engine to text for the given source/destination.
// Also substitutes macros.

function replaceTavernRegexes(regexes: TavernRegex[], option?: ReplaceTavernRegexesOption): Promise<void>
// Replaces regexes in the specified scope. Triggers debounced re-render.

function updateTavernRegexesWith(
  updater: (regexes: TavernRegex[]) => TavernRegex[] | Promise<TavernRegex[]>,
  option?: ReplaceTavernRegexesOption
): Promise<TavernRegex[]>
// Gets regexes, applies updater, saves, returns updated regexes.
```

## Import

```typescript
function importRawTavernRegex(name: string, content: string): boolean
// Imports a single regex from JSON string. Must have a 'findRegex' key.
// Adds to global regex list and triggers debounced re-render.
```

## Examples

```typescript
// Get all global regexes
const regexes = TavernHelper.getTavernRegexes({ type: 'global' });

// Add a new global regex
await TavernHelper.updateTavernRegexesWith(
  r => [...r, {
    id: crypto.randomUUID(),
    script_name: 'My Regex',
    enabled: true,
    find_regex: 'hello (\\w+)',
    replace_string: 'hi $1',
    source: { user_input: true, ai_output: false, slash_command: false, world_info: false },
    destination: { display: true, prompt: false },
    run_on_edit: false,
    min_depth: null,
    max_depth: null,
    trim_strings: [],
  }],
  { type: 'global' }
);
```
