# MVU Cleanup System

## Auto-Cleanup

Triggered every 5 messages on MESSAGE_RECEIVED. Controlled by settings:

| Setting | Default | Description |
|---------|---------|-------------|
| auto_cleanup.enabled | true | Enable auto-cleanup |
| auto_cleanup.snapshot_interval | 50 | Keep a snapshot every N messages |
| auto_cleanup.keep_recent_count | 20 | Always keep last N messages' variables |
| auto_cleanup.restore_trigger_count | 10 | Trigger restore when within N of snapshot |

### Cleanup Logic

```
on MESSAGE_RECEIVED:
    if chat.length % 5 != 0 -> skip
    old_id = message_id - keep_recent_count
    if old_id > 0:
        cleanup range [1, old_id], keeping snapshots every snapshot_interval
```

- Messages marked `snapshot: true` are preserved
- Non-snapshot messages have their stat_data/display_data/delta_data/schema removed
- initialized_lorebooks is kept on all messages

## Snapshot

Messages can be marked as snapshots:
- Auto by cleanup process at interval boundaries
- Manual via "snapshot-message" button
- Snapshots preserve their full variable data

## Restore on Delete

When a message is deleted, `restoreVariables()` is called (debounced 2s).
It re-derives variable state from the last valid message before the deletion point.

## Legacy Chat Migration

On init, `checkAndCleanupLegacyChat()` runs to:
- Detect old chat format where initialized_lorebooks was `string[]`
- Auto-migrate to `Record<string, any[]>`
- Clean up any stale variable structures

## Legacy Buttons

| Button | Description |
|--------|-------------|
| snapshot-message | Mark current message as snapshot via popup |
| clear-old-variables | Popup prompts for depth, then clears all older messages' variables |
| replay-messages | Popup asks start and end IDs, re-runs updateVariables on each message in range, saves final state to end message |

### Replay Algorithm

```typescript
for i = start+1 to end:
    await updateVariables(chat[i].message, replay_data)
// save replay_data.stat_data to end message
```
