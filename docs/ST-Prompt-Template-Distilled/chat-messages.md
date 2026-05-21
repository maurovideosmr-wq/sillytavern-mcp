# Chat / Messages

## Get Messages

```typescript
function getChatMessage(idx, role?): string
// Gets a single message by index. role filters by 'user' | 'assistant' | 'system'.

function getChatMessages(count): string[]
function getChatMessages(start, end, role?): string[]
// Gets a range of messages. Single arg = last N messages.
// Two args = [start, end) range. role filters by speaker.

function matchChatMessages(pattern, options?): string[]
// Searches message content. pattern is regex string or RegExp object.
// options: { matchAll?: boolean, flags?: string, role?: string, esc?: boolean }
```

## Find Variables

```typescript
function findVariables(key?, mes_id): VariableMap
// Finds variables in previous messages' variables.
// key — optional filter by variable name
// mes_id — message ID to search from
```

## Examples

```ejs
<% let lastMsg = getChatMessage(-1) %>
最后一条消息：<%- lastMsg %>

<% let recentMsgs = getChatMessages(5) %>
最近5条消息：
<% recentMsgs.forEach(msg => { %>
  <%- msg %>
<% }) %>

<% let matches = matchChatMessages(/战斗/) %>
