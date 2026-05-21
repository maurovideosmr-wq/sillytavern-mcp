# Chat Messages

## Types

```typescript
type ChatMessage = {
  message_id: number;
  name: string;
  role: 'system' | 'assistant' | 'user';
  is_hidden: boolean;
  message: string;
  data: Record<string, any>;
  extra: Record<string, any>;
};

type ChatMessageSwiped = {
  message_id: number;
  name: string;
  role: 'system' | 'assistant' | 'user';
  is_hidden: boolean;
  swipe_id: number;
  swipes: string[];
  swipes_data: Record<string, any>[];
  swipes_info: Record<string, any>[];
};

type GetChatMessagesOption = {
  role?: 'all' | 'system' | 'assistant' | 'user';
  hide_state?: 'all' | 'hidden' | 'unhidden';
  include_swipes?: boolean;
};

type ChatMessageCreating = {
  name?: string;
  role: 'system' | 'assistant' | 'user';
  is_hidden?: boolean;
  message: string;
  data?: Record<string, any>;
  extra?: Record<string, any>;
};

type CreateChatMessagesOption = {
  insert_at?: number | 'end';
  insert_before?: number | 'end';
  refresh?: 'none' | 'affected' | 'all';
};
```

## API

```typescript
function getChatMessages(
  range: string | number,
  options?: GetChatMessagesOption
): ChatMessage[] | ChatMessageSwiped[]
// range formats: "start:end", "id", "start:end:limit" or just a number.
// Supports negative indices and macros via substituteParamsExtended.
// When include_swipes is false, returns ChatMessage[] (default).
// When include_swipes is true, returns ChatMessageSwiped[].

function setChatMessages(
  chat_messages: Array<{ message_id: number } & (Partial<ChatMessage> | Partial<ChatMessageSwiped>)>,
  options?: { refresh?: 'none' | 'affected' | 'all' }
): Promise<void>
// Merges provided fields into existing messages by message_id.
// Supports message/data (simple) and swipe_id/swipes/swipes_data/swipes_info (full swipe) modes.

function createChatMessages(
  chat_messages: ChatMessageCreating[],
  options?: CreateChatMessagesOption
): Promise<void>
// Creates new messages. insert_before defaults to 'end' (appends).
// Emits MESSAGE_SENT / MESSAGE_RECEIVED and render events.

function deleteChatMessages(
  message_ids: number[],
  options?: { refresh?: 'none' | 'affected' | 'all' }
): Promise<void>
// Removes messages by id. Pulls from internal chat array.

function rotateChatMessages(
  begin: number,
  middle: number,
  end: number,
  options?: { refresh?: 'none' | 'affected' | 'all' }
): Promise<void>
// Moves messages in [middle, end) range to before begin position.
```

## Displayed Message Helpers

```typescript
function formatAsDisplayedMessage(
  text: string,
  options?: { message_id?: 'last' | 'last_user' | 'last_char' | number }
): string
// Applies messageFormatting + syntax highlighting like in-chat display.

function retrieveDisplayedMessage(message_id: number): JQuery<HTMLDivElement>
// Returns the $('.mes_text') div for a given message from parent document.

function refreshOneMessage(message_id: number, $mes?: JQuery<HTMLElement>): Promise<void>
// Refreshes a single message's DOM element with current data.
```

## Examples

```typescript
// Get last 10 unhidden messages
const msgs = TavernHelper.getChatMessages('-10-', { hide_state: 'unhidden' });

// Create a new assistant message
await TavernHelper.createChatMessages([
  { role: 'assistant', message: 'Hello world!' }
]);

// Delete message 5
await TavernHelper.deleteChatMessages([5]);

// Format text as displayed message
const html = TavernHelper.formatAsDisplayedMessage('**bold** text', { message_id: 'last' });
```
