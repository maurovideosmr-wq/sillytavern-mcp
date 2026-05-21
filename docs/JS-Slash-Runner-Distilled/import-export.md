# Raw Data Import Functions

```typescript
function importRawCharacter(name: string, content: Blob): Promise<Response>
function importRawChat(name: string, content: string): Promise<Response>
function importRawPreset(name: string, content: string): Promise<boolean>
function importRawWorldbook(name: string, content: string): Promise<boolean>
function importRawTavernRegex(name: string, content: string): boolean
```

- `importRawCharacter`: Imports a character card from a PNG Blob (avatar). The Blob should be the raw PNG file data. Strips `.png`/`.json` suffix from name. Updates the character's worldbook if one existed. Returns the ST API Response.
- `importRawChat`: Imports a chat file (JSONL string) for the currently selected character. Requires a character to be selected (`this_chid` defined). Returns the ST API Response.
- `importRawPreset`: Imports a preset from a JSON string. Parses the JSON and saves via `preset_manager.savePreset`. Returns `true` on success, `false` on error.
- `importRawWorldbook`: Imports a worldbook from a JSON string. Parses JSON (expects `entries` field) and saves via `saveWorldInfo`. Reloads the worldbook editor. Returns `true` on success, `false` on error.
- `importRawTavernRegex`: Imports a regex script from a JSON string. Content must have a `findRegex` field. Assigns a UUID and script name, then appends to `extension_settings.regex`. Synchronous, returns `false` if JSON lacks `findRegex`.

```typescript
// Import a character from a URL
const response = await fetch('https://example.com/character.png');
const blob = await response.blob();
await importRawCharacter('my-character', blob);

// Import a preset from JSON string
const json = JSON.stringify({ ...presetData });
const ok = await importRawPreset('my-preset', json);

// Import a worldbook
const wb = JSON.stringify({ entries: [...] });
await importRawWorldbook('my-world', wb);
```
