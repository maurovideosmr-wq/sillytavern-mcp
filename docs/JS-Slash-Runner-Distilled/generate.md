# Generate

## Types

```typescript
type GenerateConfig = {
  generation_id?: string;
  user_input?: string;
  image?: File | string | (File | string)[];
  should_stream?: boolean;
  should_silence?: boolean;
  overrides?: Overrides;
  injects?: Omit<InjectionPrompt, 'id'>[];
  max_chat_history?: 'all' | number;
  custom_api?: CustomApiConfig;
  tools?: ToolDefinition[];
  tool_choice?: ToolChoice;
  json_schema?: JsonSchema;
};

type GenerateRawConfig = {
  // Same as GenerateConfig plus:
  ordered_prompts?: (BuiltinPrompt | RolePrompt)[];
};

type Overrides = {
  world_info_before?: string;
  persona_description?: string;
  char_description?: string;
  char_personality?: string;
  scenario?: string;
  world_info_after?: string;
  dialogue_examples?: string;
  chat_history?: {
    with_depth_entries?: boolean;
    author_note?: string;
    prompts?: RolePrompt[];
  };
};

type InjectionPrompt = {
  id: string;
  position: 'in_chat' | 'none';
  depth: number;
  role: 'system' | 'assistant' | 'user';
  content: string;
  filter?: (() => boolean) | (() => Promise<boolean>);
  should_scan?: boolean;
};

type CustomApiConfig = {
  proxy_preset?: string;
  apiurl?: string;
  key?: string;
  model?: string;
  source?: string;
  max_tokens?: 'same_as_preset' | 'unset' | number;
  temperature?: 'same_as_preset' | 'unset' | number;
  frequency_penalty?: 'same_as_preset' | 'unset' | number;
  presence_penalty?: 'same_as_preset' | 'unset' | number;
  top_p?: 'same_as_preset' | 'unset' | number;
  top_k?: 'same_as_preset' | 'unset' | number;
};

type RolePrompt = {
  role: 'system' | 'assistant' | 'user';
  content: string;
  image?: File | string | (File | string)[];
};

type BuiltinPrompt =
  | 'world_info_before'
  | 'persona_description'
  | 'char_description'
  | 'char_personality'
  | 'scenario'
  | 'world_info_after'
  | 'dialogue_examples'
  | 'chat_history'
  | 'user_input';

const builtin_prompt_default_order: BuiltinPrompt[];

type ToolDefinition = {
  type: 'function';
  function: { name: string; description?: string; parameters?: Record<string, any> };
};

type ToolChoice = 'auto' | 'required' | 'none' | 'any' | { type: 'function'; function: { name: string } };

type JsonSchema = {
  name: string;
  description?: string;
  value: Record<string, any>;
  strict?: boolean;
};

type GenerateToolCallResult = {
  content: string;
  tool_calls: {
    id: string;
    type: 'function';
    function: { name: string; arguments: string };
    thought_signature?: string;
  }[];
  reasoning_signature?: string;
};
```

## API

```typescript
function generate(config: GenerateConfig): Promise<string | GenerateToolCallResult>
// Generate using the current preset. user_input is processed through regex/macros.
// When tools are provided, may return GenerateToolCallResult.

function generateRaw(config: GenerateRawConfig): Promise<string | GenerateToolCallResult>
// Generate without using a preset. ordered_prompts controls prompt ordering explicitly.

function getModelList(custom_api: { apiurl: string; key?: string }): Promise<string[]>
// Fetches available models from a custom API endpoint.

function getProxyPresetNames(): string[]
// Returns names of configured proxy presets.

function stopGenerationById(id: string): boolean
// Aborts a specific generation by its generation_id.

function stopAllGeneration(): boolean
// Aborts all active TH-generate tasks.

// Prompt injection:
function injectPrompts(
  prompts: InjectionPrompt[],
  options?: { once?: boolean }
): { uninject: () => void }
// Injects prompts into the next generation. Returns a cleanup function.

function uninjectPrompts(ids: string[]): void
// Removes injected prompts by id.
```

## Examples

```typescript
// Basic generation
const response = await TavernHelper.generate({
  user_input: 'Hello!',
});

// Streaming generation
await TavernHelper.generate({
  user_input: 'Tell me a story',
  should_stream: true,
});

// Using a custom API
const result = await TavernHelper.generate({
  user_input: 'What is the meaning of life?',
  custom_api: { apiurl: 'https://api.example.com/v1', key: 'sk-...' },
});

// With tool calling
const result = await TavernHelper.generate({
  user_input: 'What is 2+2?',
  tools: [{ type: 'function', function: { name: 'calculate', parameters: { type: 'object', properties: { expr: { type: 'string' } } } } }],
  tool_choice: 'auto',
});
```
