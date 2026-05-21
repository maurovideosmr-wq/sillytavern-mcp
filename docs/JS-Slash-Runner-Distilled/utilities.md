# Utility Functions

```typescript
// From util.ts:
function substitudeMacros(text: string): string
function getLastMessageId(): number
function errorCatched<T extends any[], U>(fn: (...args: T) => U): (...args: T) => U
function getMessageId(iframe_name: string): number

// _bind versions (iframe-scoped, auto-cleanup on pagehide):
function _reloadIframe(this: Window): void
function _errorCatched(this: Window, fn): (...args: T) => U
function _getIframeName(this: Window): string
function _getScriptId(this: Window): string
function _getCurrentMessageId(this: Window): number

// From version.ts:
function getTavernHelperVersion(): string
function updateTavernHelper(): Promise<boolean>
function getTavernVersion(): string

// From slash.ts:
function triggerSlash(command: string): Promise<string>
```

- `substitudeMacros`: Replaces ST macros (e.g. `{{user}}`, `{{char}}`, `{{lastMessageId}}`) in a string using `substituteParamsExtended`.
- `getLastMessageId`: Returns the ID of the last message in the current chat (via `{{lastMessageId}}`).
- `errorCatched`: Wraps a function so errors are caught and displayed via toastr (to the log viewer) instead of crashing. Handles both sync and async (Promise) functions.
- `getMessageId`: Extracts the message floor number from an iframe name (format `TH-message--{id}--...`). Throws if not a message iframe.
- `_reloadIframe`: Reloads the current iframe (equivalent to `location.reload()`).
- `_getIframeName`: Returns the current iframe's unique name/ID. Throws if frameElement is null.
- `_getScriptId`: Returns the script ID from the iframe name. Only works in script iframes (`TH-script--...`).
- `_getCurrentMessageId`: Returns the current message floor ID for the iframe.
- `getTavernHelperVersion` (also `getFrontendVersion`): Returns the installed version string from manifest.
- `updateTavernHelper` (also `updateFrontendVersion`): Updates the extension via the ST API. Returns `true` on success.
- `getTavernVersion`: Returns the running SillyTavern version string.
- `triggerSlash` (also `triggerSlashWithResult`): Executes any ST slash command and returns the result string. Throws on error.

```typescript
// Macro substitution
const text = substitudeMacros('Hello {{user}}, I am {{char}}');

// Safely wrap callback
const safeHandler = errorCatched(async () => {
  await riskyOperation();
});

// Run a slash command
const result = await triggerSlash('/echo Hello World');
toastr.success(result);

// Get current version
const helperVer = getTavernHelperVersion();
const stVer = getTavernVersion();

// Get current script/message context
const scriptId = _getScriptId();      // inside a script
const messageId = _getCurrentMessageId(); // inside a message iframe
```
