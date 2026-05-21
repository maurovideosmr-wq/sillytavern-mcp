# Features

## Core: EJS Template Processing

Processes `<% %>`, `<%= %>`, `<%- %>` tags in prompts, character descriptions, and worldbook entries.

| Tag | Purpose |
|-----|---------|
| `<% code %>` | Execute code (no output) |
| `<%= expr %>` | Output escaped value |
| `<%- expr %>` | Output raw/unencoded value |
| `<%_ ... _%>` | Strip whitespace before/after |
| `<%# comment %>` | Comment (no output) |
| `<%%` / `%%>` | Literal `<%` / `%>` |

### Scope Escaping

Wrap content in `<#escape-ejs>...<#/escape-ejs>` to auto-convert `<%` → `<%%` and `%>` → `%%>`, preventing EJS processing.

## Content Injection (World Book Title Tags)

Prefix world book entry titles to control placement:

| Title Prefix | Effect |
|-------------|--------|
| `[GENERATE:BEFORE]` | Inject to start of LLM prompt (blue only) |
| `[GENERATE:AFTER]` | Inject to end of LLM prompt (blue + green) |
| `[RENDER:BEFORE]` | Inject before rendered message (blue only) |
| `[RENDER:AFTER]` | Inject after rendered message (blue + green) |
| `[GENERATE:N:BEFORE]` | Inject before the N-th message |
| `[GENERATE:N:AFTER]` | Inject after the N-th message |
| `[GENERATE:REGEX:pattern]` | Inject when message matches regex |
| `[InitialVariables]` | JSON used as initial variable tree |
| `[Preprocessing]` | Preprocess entry before ST handling |

## Decorators (`@@` prefix in worldbook content)

Place at the top of worldbook entry content:

| Decorator | Effect |
|-----------|--------|
| `@@activate` | Treat as blue entry |
| `@@dont_activate` | Prevent activation entirely |
| `@@generate_before` | Alias for `[GENERATE:BEFORE]` |
| `@@generate_after` | Alias for `[GENERATE:AFTER]` |
| `@@render_before` | Alias for `[RENDER:BEFORE]` |
| `@@render_after` | Alias for `[RENDER:AFTER]` |
| `@@dont_preload` | Skip during preload |
| `@@initial_variables` | Alias for `[InitialVariables]` |
| `@@always_enabled` | Force-enable special entries |
| `@@only_preload` | Enable only during preload |
| `@@private` | Wrap content to avoid variable conflicts |
| `@@if condition` | Conditional include/exclude |
| `@@iframe [title]` | Wrap content in an iframe |
| `@@preprocessing` | Pre-process entry |
| `@@message_formatting` | Apply message formatting to output |

## @INJECT Prompt Injection

Inject full messages (`{role, content}`) anywhere in the prompt.

```
@INJECT pos=N,role=system
@INJECT target=user,index=1,at=before,role=system
@INJECT regex=pattern,at=before,role=system
```

Entry must be **disabled** to take effect. Supports trigger probability and ordering.

## Variable System

Five scopes: `cache`, `message`, `local`, `global`, `initial`.

Merge priority: `message` > `local` > `global`

## Dynamic Regex

`activateRegex(pattern, replacement, opts)` creates temporary regex replacements during prompt processing. Three modes: `basic`, `generate`, `message`.

## Prompt Injection

`injectPrompt(key, prompt, order, sticky?, uid?)` and `getPromptsInjected(key, postprocess?)` for code-driven prompt injection.

## Settings Options

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | true | Master toggle |
| `generate_enabled` | true | Process during generation |
| `render_enabled` | true | Process during message rendering |
| `debug_enabled` | false | Verbose console logging |
| `sandbox` | false | iframe sandbox execution isolation |
| `compile_workers` | false | Use Web Workers for background compilation |
| `cache_enabled` | 0 | 0=disabled, 1=all, 2=worldbook only |
| `cache_size` | 64 | Max cache entries |
| `depth_limit` | -1 | Max message depth for rendering (-1=unlimited) |
