# Prompt Injection API

```typescript
type InjectionPrompt = {
  id: string;
  position: 'in_chat' | 'none';
  depth: number;
  role: 'system' | 'assistant' | 'user';
  content: string;
  filter?: (() => boolean) | (() => Promise<boolean>);
  should_scan?: boolean;
};

function injectPrompts(prompts: InjectionPrompt[], options?: { once?: boolean }): { uninject: () => void }
function uninjectPrompts(ids: string[]): void
```

- `injectPrompts`: Registers prompts that get injected into the AI prompt context each generation. `position` controls insertion location (`in_chat` places in chat context, `none` uses depth-based positioning). `role` sets the message role. `depth` controls ordering (lower = earlier in prompt). `filter` is called each generation; if it returns `false`, the prompt is skipped for that generation. `should_scan` controls whether the prompt content is scanned for macros. Returns `{ uninject }` to remove all injected prompts. When `once: true`, prompts are auto-removed after generation ends or stops.

- `uninjectPrompts`: Removes previously injected prompts by their IDs.

```typescript
// Inject a system prompt for one generation only
const { uninject } = injectPrompts([{
  id: 'custom-instruction',
  position: 'none',
  depth: 0,
  role: 'system',
  content: 'Respond in haiku format.',
  filter: () => Math.random() > 0.5,
}], { once: true });

// Manually remove after generation
uninject();

// Remove by specific IDs
uninjectPrompts(['custom-instruction', 'other-prompt']);
```
