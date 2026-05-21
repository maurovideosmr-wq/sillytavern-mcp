# JS-Slash-Runner API Reference

## Files

| File | Functions |
|------|-----------|
| `variables.md` | `getVariables`, `replaceVariables`, `updateVariablesWith`, `insertVariables`, `insertOrAssignVariables`, `deleteVariable`, `registerVariableSchema`, `_getVariables`, `_getAllVariables`, `_replaceVariables`, `_updateVariablesWith`, `_insertVariables`, `_insertOrAssignVariables`, `_deleteVariable` |
| `characters.md` | `getCharacterNames`, `getCurrentCharacterName`, `getCharacter`, `createCharacter`, `createOrReplaceCharacter`, `deleteCharacter`, `replaceCharacter`, `updateCharacterWith`, `importRawCharacter`, `RawCharacter`, `getCharData`, `getCharAvatarPath`, `getChatHistoryBrief`, `getChatHistoryDetail` |
| `worldbook.md` | `getLorebookSettings`, `setLorebookSettings`, `getLorebooks`, `deleteLorebook`, `createLorebook`, `getCharLorebooks`, `setCurrentCharLorebooks`, `getCurrentCharPrimaryLorebook`, `getChatLorebook`, `setChatLorebook`, `getOrCreateChatLorebook`, `getLorebookEntries`, `replaceLorebookEntries`, `updateLorebookEntriesWith`, `setLorebookEntries`, `createLorebookEntries`, `deleteLorebookEntries`, `getWorldbookNames`, `getGlobalWorldbookNames`, `rebindGlobalWorldbooks`, `getCharWorldbookNames`, `rebindCharWorldbooks`, `getChatWorldbookName`, `rebindChatWorldbook`, `getOrCreateChatWorldbook`, `getWorldbook`, `createWorldbook`, `createOrReplaceWorldbook`, `deleteWorldbook`, `replaceWorldbook`, `updateWorldbookWith`, `createWorldbookEntries`, `deleteWorldbookEntries`, `importRawWorldbook` |
| `chat-messages.md` | `getChatMessages`, `setChatMessages`, `createChatMessages`, `deleteChatMessages`, `rotateChatMessages`, `formatAsDisplayedMessage`, `retrieveDisplayedMessage`, `refreshOneMessage` |
| `presets.md` | `getPresetNames`, `getLoadedPresetName`, `loadPreset`, `getPreset`, `createPreset`, `createOrReplacePreset`, `deletePreset`, `renamePreset`, `replacePreset`, `updatePresetWith`, `setPreset`, `isPresetNormalPrompt`, `isPresetSystemPrompt`, `isPresetPlaceholderPrompt`, `default_preset`, `importRawPreset` |
| `audio.md` | `playAudio`, `pauseAudio`, `getAudioList`, `replaceAudioList`, `appendAudioList`, `getAudioSettings`, `setAudioSettings`, `audioEnable`, `audioPlay`, `audioMode`, `audioImport`, `audioSelect` |
| `tavern-regex.md` | `getTavernRegexes`, `isCharacterTavernRegexesEnabled`, `formatAsTavernRegexedString`, `replaceTavernRegexes`, `updateTavernRegexesWith`, `importRawTavernRegex` |
| `scripts.md` | `getAllEnabledScriptButtons`, `getScriptTrees`, `replaceScriptTrees`, `updateScriptTreesWith`, `_getButtonEvent`, `_getScriptButtons`, `_replaceScriptButtons`, `_updateScriptButtonsWith`, `_appendInexistentScriptButtons`, `_getScriptName`, `_getScriptInfo`, `_replaceScriptInfo` |
| `generate.md` | `generate`, `generateRaw`, `getModelList`, `getProxyPresetNames`, `stopGenerationById`, `stopAllGeneration`, `builtin_prompt_default_order`, `injectPrompts`, `uninjectPrompts` |
| `events.md` | `_eventOn`, `_eventMakeLast`, `_eventMakeFirst`, `_eventOnce`, `_eventEmit`, `_eventEmitAndWait`, `_eventRemoveListener`, `_eventClearEvent`, `_eventClearListener`, `_eventClearAll`, `iframe_events`, `tavern_events` |

## Prefix Convention

- **Unprefixed**: Public API, accessible via `TavernHelper.*`
- **`_` prefixed**: Internal iframe functions, accessible via `TavernHelper._bind.*`
- **`importRaw`** prefixed: Raw import helpers for character/chat/preset/worldbook/regex blobs

All functions are synchronous unless the signature returns `Promise<T>`.
