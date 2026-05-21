# Quick Reply

```typescript
function getqr(name, label, data?): string
// Gets quick reply button content.
// name — quick reply set name
// label — button label
// data — additional context variables

function getQuickReply(name, label, data?): string
// Alias for getqr

function getQuickReplyData(name): object
// Gets raw quick reply set data
```

## Example

```ejs
<%- getqr('战斗宏', '攻击') %>
```
