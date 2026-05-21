# Events

## Constants

```typescript
const iframe_events = {
  MESSAGE_IFRAME_RENDER_STARTED: 'message_iframe_render_started',
  MESSAGE_IFRAME_RENDER_ENDED: 'message_iframe_render_ended',
  GENERATION_STARTED: 'js_generation_started',
  STREAM_TOKEN_RECEIVED_FULLY: 'js_stream_token_received_fully',
  STREAM_TOKEN_RECEIVED_INCREMENTALLY: 'js_stream_token_received_incrementally',
  GENERATION_ENDED: 'js_generation_ended',
} as const;

const tavern_events = {
  APP_READY: 'app_ready',
  EXTRAS_CONNECTED: 'extras_connected',
  MESSAGE_SWIPED: 'message_swiped',
  MESSAGE_SENT: 'message_sent',
  MESSAGE_RECEIVED: 'message_received',
  MESSAGE_EDITED: 'message_edited',
  MESSAGE_DELETED: 'message_deleted',
  MESSAGE_UPDATED: 'message_updated',
  MESSAGE_FILE_EMBEDDED: 'message_file_embedded',
  MESSAGE_REASONING_EDITED: 'message_reasoning_edited',
  MESSAGE_REASONING_DELETED: 'message_reasoning_deleted',
  MESSAGE_SWIPE_DELETED: 'message_swipe_deleted',
  MORE_MESSAGES_LOADED: 'more_messages_loaded',
  IMPERSONATE_READY: 'impersonate_ready',
  CHAT_CHANGED: 'chat_id_changed',
  GENERATION_AFTER_COMMANDS: 'GENERATION_AFTER_COMMANDS',
  GENERATION_STARTED: 'generation_started',
  GENERATION_STOPPED: 'generation_stopped',
  GENERATION_ENDED: 'generation_ended',
  SD_PROMPT_PROCESSING: 'sd_prompt_processing',
  EXTENSIONS_FIRST_LOAD: 'extensions_first_load',
  EXTENSION_SETTINGS_LOADED: 'extension_settings_loaded',
  SETTINGS_LOADED: 'settings_loaded',
  SETTINGS_UPDATED: 'settings_updated',
  MOVABLE_PANELS_RESET: 'movable_panels_reset',
  SETTINGS_LOADED_BEFORE: 'settings_loaded_before',
  SETTINGS_LOADED_AFTER: 'settings_loaded_after',
  CHATCOMPLETION_SOURCE_CHANGED: 'chatcompletion_source_changed',
  CHATCOMPLETION_MODEL_CHANGED: 'chatcompletion_model_changed',
  OAI_PRESET_CHANGED_BEFORE: 'oai_preset_changed_before',
  OAI_PRESET_CHANGED_AFTER: 'oai_preset_changed_after',
  OAI_PRESET_EXPORT_READY: 'oai_preset_export_ready',
  OAI_PRESET_IMPORT_READY: 'oai_preset_import_ready',
  WORLDINFO_SETTINGS_UPDATED: 'worldinfo_settings_updated',
  WORLDINFO_UPDATED: 'worldinfo_updated',
  CHARACTER_EDITOR_OPENED: 'character_editor_opened',
  CHARACTER_EDITED: 'character_edited',
  CHARACTER_PAGE_LOADED: 'character_page_loaded',
  USER_MESSAGE_RENDERED: 'user_message_rendered',
  CHARACTER_MESSAGE_RENDERED: 'character_message_rendered',
  FORCE_SET_BACKGROUND: 'force_set_background',
  CHAT_DELETED: 'chat_deleted',
  CHAT_CREATED: 'chat_created',
  GENERATE_BEFORE_COMBINE_PROMPTS: 'generate_before_combine_prompts',
  GENERATE_AFTER_COMBINE_PROMPTS: 'generate_after_combine_prompts',
  GENERATE_AFTER_DATA: 'generate_after_data',
  WORLD_INFO_ACTIVATED: 'world_info_activated',
  TEXT_COMPLETION_SETTINGS_READY: 'text_completion_settings_ready',
  CHAT_COMPLETION_SETTINGS_READY: 'chat_completion_settings_ready',
  CHAT_COMPLETION_PROMPT_READY: 'chat_completion_prompt_ready',
  CHARACTER_FIRST_MESSAGE_SELECTED: 'character_first_message_selected',
  CHARACTER_DELETED: 'characterDeleted',
  CHARACTER_DUPLICATED: 'character_duplicated',
  CHARACTER_RENAMED: 'character_renamed',
  CHARACTER_RENAMED_IN_PAST_CHAT: 'character_renamed_in_past_chat',
  SMOOTH_STREAM_TOKEN_RECEIVED: 'stream_token_received',
  STREAM_TOKEN_RECEIVED: 'stream_token_received',
  STREAM_REASONING_DONE: 'stream_reasoning_done',
  FILE_ATTACHMENT_DELETED: 'file_attachment_deleted',
  WORLDINFO_FORCE_ACTIVATE: 'worldinfo_force_activate',
  OPEN_CHARACTER_LIBRARY: 'open_character_library',
  ONLINE_STATUS_CHANGED: 'online_status_changed',
  IMAGE_SWIPED: 'image_swiped',
  CONNECTION_PROFILE_LOADED: 'connection_profile_loaded',
  CONNECTION_PROFILE_CREATED: 'connection_profile_created',
  CONNECTION_PROFILE_DELETED: 'connection_profile_deleted',
  CONNECTION_PROFILE_UPDATED: 'connection_profile_updated',
  TOOL_CALLS_PERFORMED: 'tool_calls_performed',
  TOOL_CALLS_RENDERED: 'tool_calls_rendered',
  CHARACTER_MANAGEMENT_DROPDOWN: 'charManagementDropdown',
  SECRET_WRITTEN: 'secret_written',
  SECRET_DELETED: 'secret_deleted',
  SECRET_ROTATED: 'secret_rotated',
  SECRET_EDITED: 'secret_edited',
  PRESET_CHANGED: 'preset_changed',
  PRESET_DELETED: 'preset_deleted',
  PRESET_RENAMED: 'preset_renamed',
  PRESET_RENAMED_BEFORE: 'preset_renamed_before',
  MAIN_API_CHANGED: 'main_api_changed',
  WORLDINFO_ENTRIES_LOADED: 'worldinfo_entries_loaded',
  WORLDINFO_SCAN_DONE: 'worldinfo_scan_done',
  MEDIA_ATTACHMENT_DELETED: 'media_attachment_deleted',
} as const;
```

## Event Listener Signatures

```typescript
type ListenerType = {
  [iframe_events.MESSAGE_IFRAME_RENDER_STARTED]: (iframe_name: string) => void;
  [iframe_events.MESSAGE_IFRAME_RENDER_ENDED]: (iframe_name: string) => void;
  [iframe_events.GENERATION_STARTED]: (generation_id: string) => void;
  [iframe_events.STREAM_TOKEN_RECEIVED_FULLY]: (full_text: string, generation_id: string) => void;
  [iframe_events.STREAM_TOKEN_RECEIVED_INCREMENTALLY]: (incremental_text: string, generation_id: string) => void;
  [iframe_events.GENERATION_ENDED]: (text: string, generation_id: string) => void;

  [tavern_events.APP_READY]: () => void;
  [tavern_events.CHAT_CHANGED]: (chat_file_name: string) => void;
  [tavern_events.MESSAGE_SWIPED]: (message_id: number) => void;
  [tavern_events.MESSAGE_SENT]: (message_id: number) => void;
  [tavern_events.MESSAGE_RECEIVED]: (message_id: number, type: string) => void;
  [tavern_events.MESSAGE_EDITED]: (message_id: number) => void;
  [tavern_events.MESSAGE_DELETED]: (message_id: number) => void;
  [tavern_events.IMPERSONATE_READY]: (message: string) => void;
  [tavern_events.CHARACTER_SELECTED]: () => void;
  [tavern_events.CHARACTER_EDITED]: (result: { detail: { id: string; character: object } }) => void;
  [tavern_events.GROUP_UPDATED]: () => void;
  [tavern_events.PRESET_CHANGED]: (data: { apiId: string; name: string }) => void;
  [tavern_events.WORLDINFO_SCAN_DONE]: (event_data: object) => void;
  [tavern_events.SETTINGS_LOADED]: () => void;
  [tavern_events.GENERATION_STARTED]: (type: string, option: object, dry_run: boolean) => void;
  [tavern_events.GENERATION_ENDED]: (message_id: number) => void;
  [tavern_events.GENERATION_STOPPED]: () => void;
  // See full ListenerType in source for complete signatures
  [custom_event: string]: (...args: any) => any;
};
```

## _bind API (Iframe-Internal Only)

```typescript
type EventOnReturn = { stop: () => void };

function _eventOn(this: Window, event_type: EventType, listener: Function): EventOnReturn
// Registers a listener. Returns { stop } to remove.

function _eventMakeLast(this: Window, event_type: EventType, listener: Function): EventOnReturn
// Registers listener to run last.

function _eventMakeFirst(this: Window, event_type: EventType, listener: Function): EventOnReturn
// Registers listener to run first.

function _eventOnce(this: Window, event_type: EventType, listener: Function): EventOnReturn
// Registers listener that fires once then auto-removes.

function _eventEmit(this: Window, event_type: EventType, ...data: any[]): Promise<void>
// Emits an event asynchronously.

function _eventEmitAndWait(this: Window, event_type: EventType, ...data: any[]): void
// Emits an event and waits for all listeners to complete.

function _eventRemoveListener(this: Window, event_type: EventType, listener: Function): void
// Removes a specific listener.

function _eventClearEvent(this: Window, event_type: EventType): void
// Removes all listeners for a specific event.

function _eventClearListener(this: Window, listener: Function): void
// Removes a specific listener from all events.

function _eventClearAll(this: Window): void
// Removes all registered listeners for the iframe.
```

## Notes

- `_eventOn`, `_eventMakeLast`, etc. are only available via `TavernHelper._bind.*` and require `this: Window` (call with `.call(window)` or from within iframe context).
- Message-id arguments in events (`MESSAGE_SWIPED`, `MESSAGE_SENT`, etc.) are automatically parsed to integers.
- The `stop()` return from event registration functions removes the listener.
- All TavernHelper event listener references are tracked per-iframe and cleaned up on iframe reload.

## Examples

```typescript
// Inside iframe context:
const listener = TavernHelper._bind._eventOn.call(window, TavernHelper.tavern_events.MESSAGE_SENT, (message_id) => {
  console.log('New message:', message_id);
});

// Later: remove it
listener.stop();

// Emit a custom event
await TavernHelper._bind._eventEmit.call(window, 'my_custom_event', 'some_data');
```
