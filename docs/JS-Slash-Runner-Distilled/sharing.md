# Global Variable / Cross-Script Interface Sharing

```typescript
function initializeGlobal(global: LiteralUnion<'Mvu', string>, value: any): void
function waitGlobalInitialized(global: LiteralUnion<'Mvu', string>): Promise<void>

// _bind versions (iframe-scoped, auto-cleanup on pagehide):
function _initializeGlobal(this: Window, global, value): void
function _waitGlobalInitialized(this: Window, global): Promise<void>
```

- `initializeGlobal`: Sets `window[global]` to `value` and emits a `global_{name}_initialized` event. Other scripts/frames can then access the value via `window[global]` after awaiting initialization.
- `waitGlobalInitialized`: Returns a Promise that resolves once `window[global]` has been set (either already present or after `initializeGlobal` is called). The `_` variant also sets up a property getter on the frame's window and, for `'Mvu'`, waits for `stat_data` to appear in message variables.

```typescript
// Script A - shares a service
const myService = {
  getData: () => { ... },
  setData: (v) => { ... },
};
initializeGlobal('MyService', myService);

// Script B - uses the service (in another script/frame)
await waitGlobalInitialized('MyService');
const data = MyService.getData();

// Wait for the built-in MVU framework
await waitGlobalInitialized('Mvu');
// Mvu is now available: Mvu.getMvuData(), Mvu.parseMessage(), etc.
```
