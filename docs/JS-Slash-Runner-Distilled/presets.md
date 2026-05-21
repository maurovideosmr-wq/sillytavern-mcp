# Presets

## Types

```typescript
type Preset = {
  settings: {
    max_context: number;
    max_completion_tokens: number;
    reply_count: number;
    should_stream: boolean;
    temperature: number;
    frequency_penalty: number;
    presence_penalty: number;
    repetition_penalty: number;
    top_p: number;
    min_p: number;
    top_k: number;
    top_a: number;
    seed: number;
    squash_system_messages: boolean;
    reasoning_effort: 'auto' | 'min' | 'low' | 'medium' | 'high' | 'max';
    request_thoughts: boolean;
    request_images: boolean;
    enable_function_calling: boolean;
    enable_web_search: boolean;
    allow_sending_images: 'disabled' | 'auto' | 'low' | 'high';
    allow_sending_videos: boolean;
    character_name_prefix: 'none' | 'default' | 'content' | 'completion';
    wrap_user_messages_in_quotes: boolean;
  };
  prompts: PresetPrompt[];
  prompts_unused: PresetPrompt[];
  extensions: {
    regex_scripts?: TavernRegex[];
    tavern_helper: { scripts: Record<string, any>[]; variables: Record<string, any> };
    [other: string]: any;
  };
};

type PresetPrompt = {
  id: LiteralUnion<
    | 'main' | 'nsfw' | 'jailbreak' | 'enhanceDefinitions'
    | 'worldInfoBefore' | 'personaDescription' | 'charDescription'
    | 'charPersonality' | 'scenario' | 'worldInfoAfter'
    | 'dialogueExamples' | 'chatHistory',
    string
  >;
  name: string;
  enabled: boolean;
  position:
    | { type: 'relative'; depth?: never; order?: never }
    | { type: 'in_chat'; depth: number; order: number };
  role: 'system' | 'user' | 'assistant';
  content?: string;
  extra?: Record<string, any>;
};
```

## Prompt Categorization Helpers

```typescript
function isPresetNormalPrompt(prompt: PresetPrompt): prompt is PresetNormalPrompt
// True for custom prompts (not system, not placeholder).

function isPresetSystemPrompt(prompt: PresetPrompt): prompt is PresetSystemPrompt
// True for 'main', 'nsfw', 'jailbreak', 'enhanceDefinitions'.

function isPresetPlaceholderPrompt(prompt: PresetPrompt): prompt is PresetPlaceholderPrompt
// True for worldInfoBefore, personaDescription, charDescription, etc.

const default_preset: Preset
// Default Preset with sensible defaults for all settings.
```

## API

```typescript
function getPresetNames(): string[]
// Includes 'in_use' as first entry, then all saved preset names.

function getLoadedPresetName(): string
// Returns the currently active preset name.

function loadPreset(preset_name: Exclude<string, 'in_use'>): boolean
// Loads a saved preset. Returns false if not found.

function getPreset(preset_name: LiteralUnion<'in_use', string>): Preset
// Returns preset data. 'in_use' returns the active settings from oai_settings.

function createPreset(preset_name: Exclude<string, 'in_use'>, preset?: Preset): Promise<boolean>
// Creates a new preset. Returns false if name already exists.

function createOrReplacePreset(
  preset_name: LiteralUnion<'in_use', string>,
  preset?: Preset,
  options?: { render?: 'debounced' | 'immediate' | 'none' }
): Promise<boolean>

function deletePreset(preset_name: Exclude<string, 'in_use'>): Promise<boolean>

function renamePreset(preset_name: Exclude<string, 'in_use'>, new_name: string): Promise<boolean>

function replacePreset(
  preset_name: LiteralUnion<'in_use', string>,
  preset: Preset,
  options?: { render?: 'debounced' | 'immediate' | 'none' }
): Promise<void>

function updatePresetWith(
  preset_name: LiteralUnion<'in_use', string>,
  updater: (preset: Preset) => Preset | Promise<Preset>,
  options?: { render?: 'debounced' | 'immediate' | 'none' }
): Promise<Preset>

function setPreset(
  preset_name: LiteralUnion<'in_use', string>,
  preset: PartialDeep<Preset>,
  options?: { render?: 'debounced' | 'immediate' | 'none' }
): Promise<Preset>
// Shallow merges preset fields into existing. Uses defaultsDeep for settings/extensions.
```

## Import

```typescript
function importRawPreset(name: string, content: string): Promise<boolean>
// Imports a preset from a JSON string.
```

## Examples

```typescript
// Get current preset
const preset = TavernHelper.getPreset('in_use');

// Change temperature
await TavernHelper.setPreset('in_use', { settings: { temperature: 0.8 } });

// Add a custom prompt
await TavernHelper.updatePresetWith('in_use', p => {
  p.prompts.push({
    id: 'my_prompt',
    name: 'Custom Instruction',
    enabled: true,
    position: { type: 'relative' },
    role: 'system',
    content: 'Be helpful.',
  });
  return p;
});
```
