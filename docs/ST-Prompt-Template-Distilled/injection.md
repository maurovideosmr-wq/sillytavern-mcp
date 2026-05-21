# Injection

## @INJECT System

Inject full message objects (`{role, content}`) into the prompt from disabled worldbook entries.

### Syntax (in worldbook content)

```
@INJECT pos=N,role=system
@INJECT target=user,index=1,at=before,role=system
@INJECT regex=pattern,at=before,role=system
```

### Parameters

- `pos` — message position number
- `target` — `'user' | 'char' | character name`
- `index` — occurrence index
- `at` — `'before' | 'after'` (placement relative to match)
- `role` — `'system' | 'user' | 'assistant'`
- `order` — sort order when multiple injections
- `probability` — trigger probability (0-1)

### Requirements

- Entry must be **disabled** (inverted logic: disabled = active for @INJECT)

## injectPrompt API

```typescript
function injectPrompt(key, prompt, order?, sticky?, uid?): void
```
Adds a prompt string to a keyed injection group.
- `key` — group identifier
- `prompt` — string content
- `order` — sort order (default: 0)
- `sticky` — boolean, persists after injection
- `uid` — unique identifier for deduplication

```typescript
function getPromptsInjected(key, postprocess?): string
```
Retrieves all prompts in a group, concatenated with newlines.
- `key` — group identifier
- `postprocess` — optional `{ search, replace }` for search/replace

```typescript
function hasPromptsInjected(key): boolean
```
Checks if a key exists in the injected prompts.

## Example

```ejs
<% injectPrompt("CoT", `## Chain of Thought\nQ: What should I do?`) %>
<%- getPromptsInjected("CoT") %>
```
