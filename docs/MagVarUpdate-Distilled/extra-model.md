# MVU Extra Model Analysis

## Overview

Instead of having the main LLM output variable updates inline, MVU can dispatch a separate generate request for variable analysis. This is useful when:
- Main model's response should not be affected by variable formatting
- A cheaper/faster model can handle variable updates
- Function calling is needed for structured updates

## Configuration

Settings in MVU panel:

| Setting | Values | Default |
|---------|--------|---------|
| updateMode | 'inline-with-ai-output' / 'extra-model-analysis' | 'inline' |
| jailbreak | 'builtin' / 'current-preset' / 'other-preset' | 'builtin' |
| responseFormat | 'chat-message' / 'tool-call' / 'formatted-output' | 'chat-message' |
| autoTrigger | boolean | true |
| requestStrategy | 'sequential' / 'concurrent' / 'hybrid' | 'sequential' |
| requestCount | number | 3 |
| fakeStreamCompat | boolean | false |

## Request Strategies

```typescript
'sequential': // try one at a time, retry on failure (up to N times)
    for i in 0..N:
        result = await safeInvoke()
        if result -> return
    return null

'concurrent': // fire N requests simultaneously, take first success
    return await Promise.any(requests)

'hybrid': // try one, if fail then concurrent
    result = await safeInvoke()
    if result -> return
    return concurrentInvoke(N-1)
```

## Response Formats

### Chat Message

Extra model outputs raw text with `<UpdateVariable>` block. MVU extracts the last such block.

### Tool Call (Function Calling)

Registers function tool `mvu_VariableUpdate_{scriptId}` with schema:

```json
{
    "name": "mvu_VariableUpdate_xxx",
    "parameters": {
        "type": "object",
        "properties": {
            "analysis": { "type": "string" },
            "delta": { "type": "string", "description": "variable update block" }
        },
        "required": ["delta"]
    }
}
```

Tool choice forced to `required` when other tools exist. Supports JSON Patch dialect via `mvu_json_patch` response schema.

### Formatted Output (JSON Schema)

Uses `json_schema` to constrains output to `{"analysis": "...", "json_patch": [...]}`.

## Flow

```typescript
onMessageReceived(message_id):
    if updateMode != 'extra-model':
        handleVariablesInMessage(message_id)
        return

    if not autoTrigger -> return
    result = await invokeExtraModelWithStrategy()
    if result:
        append result + '\n\n' to message content
    else:
        toastr error
    handleVariablesInMessage(message_id) // process the result
```

## Built-in Jailbreak Prompts

Four encoded prompt files in `src/prompts/`:
- claude_head.txt / claude_tail.txt
- gemini_head.txt / gemini_tail.txt
- extra_model_task.txt

Decoded via base64 at runtime.

## Entry Filtering

Worldbook entries tagged with `[mvu_update]` / `[mvu_plot]` in their comment are filtered:

| Phase | [mvu_update] entries | [mvu_plot] entries |
|-------|---------------------|-------------------|
| Extra analysis | excluded | included |
| Main response | included | excluded |

This prevents sending variable update rules during plot analysis and vice versa.

## Prompt Filtering

During extra analysis, `<UpdateVariable>` blocks from previous turns and `<StatusPlaceHolderImpl/>` are stripped from the prompt to avoid confusing the model.
