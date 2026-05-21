# Worldbook (Lorebook)

The API has two layers: **lorebook** (older, manages settings and entry-level operations) and **worldbook** (newer, higher-level abstraction with structured entries). Both operate on the same underlying data.

## Lorebook API (Settings & Bindings)

```typescript
type LorebookSettings = {
  selected_global_lorebooks: string[];
  scan_depth: number;
  context_percentage: number;
  budget_cap: number;          // 0 = disabled
  min_activations: number;
  max_depth: number;            // 0 = unlimited
  max_recursion_steps: number;
  insertion_strategy: 'evenly' | 'character_first' | 'global_first';
  include_names: boolean;
  recursive: boolean;
  case_sensitive: boolean;
  match_whole_words: boolean;
  use_group_scoring: boolean;
  overflow_alert: boolean;
};

type CharLorebooks = {
  primary: string | null;
  additional: string[];
};

function getLorebookSettings(): LorebookSettings
function setLorebookSettings(settings: Partial<LorebookSettings>): void

function getLorebooks(): string[]
function deleteLorebook(lorebook: string): Promise<boolean>
function createLorebook(lorebook: string): Promise<boolean>

function getCharLorebooks(options?: { name?: string; type?: 'all' | 'primary' | 'additional' }): CharLorebooks
function setCurrentCharLorebooks(lorebooks: Partial<CharLorebooks>): Promise<void>
function getCurrentCharPrimaryLorebook(): string | null

function getChatLorebook(): string | null
function setChatLorebook(lorebook: string | null): Promise<void>
function getOrCreateChatLorebook(lorebook?: string): Promise<string>
```

## Lorebook Entry API

```typescript
type LorebookEntry = {
  uid: number;
  display_index: number;
  comment: string;
  enabled: boolean;
  type: 'constant' | 'selective' | 'vectorized';
  position:
    | 'before_character_definition'
    | 'after_character_definition'
    | 'before_example_messages'
    | 'after_example_messages'
    | 'before_author_note'
    | 'after_author_note'
    | 'at_depth_as_system'
    | 'at_depth_as_user'
    | 'at_depth_as_assistant';
  depth: number | null;
  order: number;
  probability: number;
  key: string[];          // deprecated, use keys
  keys: string[];
  logic: 'and_any' | 'and_all' | 'not_all' | 'not_any';
  filter: string[];       // deprecated, use filters
  filters: string[];
  scan_depth: 'same_as_global' | number;
  case_sensitive: 'same_as_global' | boolean;
  match_whole_words: 'same_as_global' | boolean;
  use_group_scoring: 'same_as_global' | boolean;
  automation_id: string | null;
  exclude_recursion: boolean;
  prevent_recursion: boolean;
  delay_until_recursion: boolean | number;
  content: string;
  group: string;
  group_prioritized: boolean;
  group_weight: number;
  sticky: number | null;
  cooldown: number | null;
  delay: number | null;
};

function getLorebookEntries(lorebook: string, options?: { filter?: 'none' | Partial<LorebookEntry> }): Promise<LorebookEntry[]>
function replaceLorebookEntries(lorebook: string, entries: Partial<LorebookEntry>[]): Promise<void>
function updateLorebookEntriesWith(lorebook: string, updater: (entries: LorebookEntry[]) => Partial<LorebookEntry>[] | Promise<Partial<LorebookEntry>[]>): Promise<LorebookEntry[]>
function setLorebookEntries(lorebook: string, entries: Array<Pick<LorebookEntry, 'uid'> & Partial<LorebookEntry>>): Promise<LorebookEntry[]>
function createLorebookEntries(lorebook: string, entries: Partial<LorebookEntry>[]): Promise<{ entries: LorebookEntry[]; new_uids: number[] }>
function deleteLorebookEntries(lorebook: string, uids: number[]): Promise<{ entries: LorebookEntry[]; delete_occurred: boolean }>

// Deprecated
function createLorebookEntry(lorebook: string, field_values: Partial<LorebookEntry>): Promise<number>
function deleteLorebookEntry(lorebook: string, uid: number): Promise<boolean>
```

## Worldbook API (Higher-Level)

```typescript
type WorldbookEntry = {
  uid: number;
  name: string;
  enabled: boolean;
  strategy: {
    type: 'constant' | 'selective' | 'vectorized';
    keys: (string | RegExp)[];
    keys_secondary: { logic: 'and_any' | 'and_all' | 'not_all' | 'not_any'; keys: (string | RegExp)[] };
    scan_depth: 'same_as_global' | number;
  };
  position: {
    type:
      | 'before_character_definition'
      | 'after_character_definition'
      | 'before_example_messages'
      | 'after_example_messages'
      | 'before_author_note'
      | 'after_author_note'
      | 'at_depth'
      | 'outlet';
    role: 'system' | 'assistant' | 'user';
    depth: number;
    order: number;
  };
  content: string;
  probability: number;
  recursion: {
    prevent_incoming: boolean;
    prevent_outgoing: boolean;
    delay_until: null | number;
  };
  effect: {
    sticky: null | number;
    cooldown: null | number;
    delay: null | number;
  };
  extra?: Record<string, any>;
};

type CharWorldbooks = { primary: string | null; additional: string[] };

type ReplaceWorldbookOptions = { render?: 'debounced' | 'immediate' };

function getWorldbookNames(): string[]
function getGlobalWorldbookNames(): string[]
function rebindGlobalWorldbooks(worldbook_names: string[]): Promise<void>

function getCharWorldbookNames(character_name: LiteralUnion<'current', string>): CharWorldbooks
function rebindCharWorldbooks(character_name: 'current', char_worldbooks: CharWorldbooks): Promise<void>

function getChatWorldbookName(chat_name: 'current'): string | null
function rebindChatWorldbook(chat_name: 'current', worldbook_name: string): Promise<void>
function getOrCreateChatWorldbook(chat_name: 'current', worldbook_name?: string): Promise<string>

function getWorldbook(worldbook_name: string): Promise<WorldbookEntry[]>
function createWorldbook(worldbook_name: string, worldbook?: WorldbookEntry[]): Promise<boolean>
function createOrReplaceWorldbook(worldbook_name: string, worldbook?: PartialDeep<WorldbookEntry>[], options?: ReplaceWorldbookOptions): Promise<boolean>
function deleteWorldbook(worldbook_name: string): Promise<boolean>
function replaceWorldbook(worldbook_name: string, worldbook: PartialDeep<WorldbookEntry>[], options?: ReplaceWorldbookOptions): Promise<void>
function updateWorldbookWith(worldbook_name: string, updater: WorldbookUpdater, options?: ReplaceWorldbookOptions): Promise<WorldbookEntry[]>
function createWorldbookEntries(worldbook_name: string, new_entries: PartialDeep<WorldbookEntry>[], options?: ReplaceWorldbookOptions): Promise<{ worldbook: WorldbookEntry[]; new_entries: WorldbookEntry[] }>
function deleteWorldbookEntries(worldbook_name: string, predicate: (entry: WorldbookEntry) => boolean, options?: ReplaceWorldbookOptions): Promise<{ worldbook: WorldbookEntry[]; deleted_entries: WorldbookEntry[] }>
```

## Import

```typescript
function importRawWorldbook(name: string, content: string): Promise<boolean>
// Imports a worldbook from a JSON string. content must have an 'entries' key.
```

## Examples

```typescript
// Get all entries from a worldbook
const entries = await TavernHelper.getWorldbook('my_lore');

// Add a new entry
await TavernHelper.createWorldbookEntries('my_lore', [{
  name: 'New Entry',
  strategy: { type: 'constant' },
  content: 'Some lore text',
  probability: 100,
}]);

// Bind worldbook to current character
await TavernHelper.rebindCharWorldbooks('current', { primary: 'my_lore', additional: [] });
```
