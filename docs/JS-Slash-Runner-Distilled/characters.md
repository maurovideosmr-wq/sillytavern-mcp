# Characters

## Types

```typescript
type Character = {
  avatar: `${string}.png` | Blob;
  version: string;
  creator: string;
  creator_notes: string;
  worldbook: string | null;
  description: string;
  first_messages: string[];
  extensions: {
    regex_scripts: TavernRegex[];
    tavern_helper: {
      scripts: Record<string, any>[];
      variables: Record<string, any>;
    };
    [other: string]: any;
  };
};

type ReplaceCharacterOptions = {
  render?: 'debounced' | 'immediate' | 'none';
};
// debounced: waits 1s then triggers re-render (default)
// immediate: re-renders avatar, hotswap, first message, selects character
// none: no re-render
```

## Public API

```typescript
function getCharacterNames(): string[]
// Returns names of all loaded characters.

function getCurrentCharacterName(): string | null
// Returns current character name, or null if none selected.

function getCharacter(name: LiteralUnion<'current', string>): Promise<Character>
// Fetches full character data. 'current' resolves to the active character.

function createCharacter(
  character_name: Exclude<string, 'current'>,
  character?: PartialDeep<Character>
): Promise<boolean>
// Creates a new character via POST /api/characters/create.
// Returns false if name already exists.

function createOrReplaceCharacter(
  character_name: Exclude<string, 'current'>,
  character?: PartialDeep<Character>,
  options?: ReplaceCharacterOptions
): Promise<boolean>
// Creates or replaces. Returns true if created, false if replaced.

function deleteCharacter(
  character_name: LiteralUnion<'current', string>,
  option?: { delete_chats?: boolean }
): Promise<boolean>
// Deletes via internal API. delete_chats defaults to true.

function replaceCharacter(
  character_name: Exclude<string, 'current'>,
  character: PartialDeep<Character>,
  options?: ReplaceCharacterOptions
): Promise<void>
// Updates an existing character via POST /api/characters/edit.

function updateCharacterWith(
  character_name: LiteralUnion<'current', string>,
  updater: (c: Character) => Character | Promise<Character>
): Promise<Character>
// Gets character, applies updater, saves result, returns updated character.
```

## RawCharacter & Helpers

```typescript
class RawCharacter {
  static find({ name }: { name: LiteralUnion<'current', string> }): v1CharData | null;
  static findIndex(name: LiteralUnion<'current', string>): number;
}

function getCharData(name: LiteralUnion<'current', string>): v1CharData | null;
function getCharAvatarPath(name: LiteralUnion<'current', string>): string | null;
function getChatHistoryBrief(name: LiteralUnion<'current', string>): Promise<any[] | null>;
function getChatHistoryDetail(data: any[], isGroupChat?: boolean): Promise<Record<string, any> | null>;
```

## Import

```typescript
function importRawCharacter(name: string, content: Blob): Promise<Response>
// Imports a character card from a PNG/JSON blob via POST /api/characters/import.
// name is the character name (without extension). content is the raw PNG/JSON file blob.
```

## Examples

```typescript
// Get current character name
const name = TavernHelper.getCurrentCharacterName();

// Update character description
await TavernHelper.updateCharacterWith('current', char => {
  char.description = 'Updated description';
  return char;
});

// Create a new character
await TavernHelper.createCharacter('NewChar', {
  description: 'A brand new character',
  first_messages: ['Hello there!'],
});
```
