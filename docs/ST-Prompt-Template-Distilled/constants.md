# Built-in Constants

Available in all EJS template contexts.

## Runtime Info

```typescript
runType: string
// 'generate' | 'preparation' | 'render' | 'render_permanent'
```

## Chat/Character Info

```typescript
charName: string         // Current character name
userName: string         // Current user name
charLoreBook: string     // Character worldbook name
userLoreBook: string     // User worldbook name
chatLoreBook: string     // Chat worldbook name
chatId: string           // Chat session ID
characterId: string      // Character card ID
groupId: string | null   // Group chat ID
groups: array            // Group chat info
charAvatar: string       // Character avatar URL
userAvatar: string       // User avatar URL
```

## Message Indexes

```typescript
lastUserMessageId: number   // Last user message index
lastCharMessageId: number   // Last character message index
lastUserMessage: string     // Last user message content
lastCharMessage: string     // Last character message content
lastMessageId: number       // Last message index
```

## Generation

```typescript
model: string            // Current LLM model name
generateType: string     // '' | 'custom' | 'normal' | 'continue' | 'impersonate' | 'regenerate' | 'swipe' | 'quiet'
```

## Render-Only

Available only during `runType === 'render'`:

```typescript
message_id: number    // Floor/entry ID
swipe_id: number      // Floor swipe ID
name: string          // Message role name
is_last: boolean      // Is the last message
is_user: boolean      // Is from user
is_system: boolean    // Is from system
```

## Generate-Only

Available only during `runType === 'generate'`:

```typescript
world_info: object        // Current world info entries
generateBuffer: string    // Processed accumulated prompt
generateData: array       // Raw message data
```

## Libraries

```typescript
variables: object    // Merged variables (message > local > global)
SillyTavern: object  // SillyTavern.getContext()
_: object            // Lodash library
$: function          // jQuery
toastr: object       // Toastr notifications
z: object            // Zod validation library
faker: object        // Faker.js for random data
```
