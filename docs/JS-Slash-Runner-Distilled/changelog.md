# Changelog (API Changes Only)

## 4.8.4
- Fix `generate` / `generateRaw` custom API default source and key/url not working with `custom` source

## 4.8.3
- Add `getProxyPresetNames`
- `generate` / `generateRaw` now support tool calling

## 4.8.1
- `generate` supports ST proxy preset via `custom_api.proxy_preset` field
- `custom_api` now optional (omit `apiurl` to use current ST source)

## 4.8.0
- Rewrite `getTavernRegexes`, `replaceTavernRegexes`, `updateTavernRegexesWith`
- Add `getScriptTrees`, `replaceScriptTrees`, `updateScriptTreesWith`

## 4.7.11
- Add `updateScriptButtonsWith`
- Add `getScriptName`

## 4.7.7
- Add `getCurrentCharacterName`

## 4.7.3
- `errorCatched` now shows source script/frontend name in error toast

## 4.6.2
- `createOrReplacePreset`, `replacePreset`, `createOrReplaceWorldbook`, `replaceWorldbook` add `render: 'none'` option
- Import functions no longer require page refresh

## 4.6.0
- Add `getCharacter`, `replaceCharacter`, `createOrReplaceCharacter`, `deleteCharacter` and related character functions
- `generate` / `generateRaw` add `should_silence` and `generation_id` parameters
- Minimum ST version raised to 1.12.13

## 4.5.5
- Add `getModelList`

## 4.5.0
- `eventOn` / event listener functions now return `{ stop }` for unsubscription
- `formatAsDisplayedMessage` now returns HTML with syntax highlighting

## 4.4.4
- Fix `formatAsDisplayedMessage` error in some contexts

## 4.4.0
- `createChatMessages`, `deleteChatMessages`, `rotateChatMessages` add `refresh: 'affected'` default
- Add `refreshOneMessage`
- Add `builtin.copyText`

## 4.3.18
- `importRawCharacter` now updates character worldbook on re-import

## 4.3.11
- `registerMacroLike` macros auto-unregister on script close

## 4.3.9
- `{{get_message_variable}}` and `{{format_message_variable}}` ignore `$`-prefixed keys
- `generate` / `generateRaw` `custom_api` supports `'same_as_preset'` and `'unset'` values

## 4.3.7
- Add `registerVariableSchema` for zod variable validation

## 4.2.0
- `eventOn` returns `{ stop }` for listener unsubscription (BREAKING: return type changed)
- `injectPrompts` returns `{ uninject }`

## 4.1.4
- Add `{{format_xxx_variable}}` macros (YAML block output)
- Export `builtin.parseRegexFromString`

## 4.1.1
- `registerMacroLike` deduplicates by regex source
- Add `unregisterMacroLike`

## 4.0.14
- `generate` / `generateRaw` `custom_api` adds `temperature` etc.
- Export `builtin.duringGenerating`, `builtin.renderMarkdown`, `builtin.uuidv4`
- Add `reloadIframe`

## 4.0.13
- Export `builtin.getImageTokenCost`, `builtin.getVideoTokenCost`

## 4.0.12
- `initializeGlobal` and `waitGlobalInitialized` exposed on `TavernHelper` interface

## 4.0.0
- Vue + Pinia + TailwindCSS rewrite
- `getVariables` / `replaceVariables` now support `'preset'` and `'extension'` types
- `replaceVariables` no longer requires `await` (BREAKING: sync now)
- Add `getAllEnabledScriptButtons`
- Add `installExtension`, `uninstallExtension`, `reinstallExtension`, `updateExtension`
- Add `getTavernHelperExtensionId`, `getTavernVersion`
- Audio: new function interfaces (`playAudio`, `pauseAudio`, `setAudioSettings` etc.), `/audioselect` etc. deprecated
- Presets can now bind scripts
- Add `{{get_character_variable}}`, `{{get_preset_variable}}` macros

## 3.6.13
- Add `iframe_events.GENERATION_BEFORE_END` for `generate` / `generateRaw`

## 3.6.2
- Add `pixi.js` as built-in library
- Add `initializeGlobal`, `waitGlobalInitialized`

## 3.6.1
- (BREAKING) `Character` renamed to `RawCharacter`

## 3.5.1
- `getAllVariables` fix: inserting arrays now overwrites instead of merging

## 3.5.0
- Add `importRawChat`
- `setChatMessages` supports depth parameter

## 3.4.21
- `stopGenerationById` / `stopAllGeneration` now emit `GENERATION_STOPPED` with generation ID

## 3.4.20
- Add `generation_id` parameter to `generate` / `generateRaw`
- Add `stopGenerationById`, `stopAllGeneration`

## 3.4.17
- Add `Vue` and `VueRouter` globals to iframes

## 3.4.16
- Add `importRawCharacter`, `importRawPreset`, `importRawWorldbook`, `importRawTavernRegex`

## 3.4.15
- Add `injectPrompts`, `uninjectPrompts`

## 3.4.14
- Add `getScriptInfo`, `replaceScriptInfo`
- Add `SillyTavern.registerFunctionTool` type definitions

## 3.4.13
- `getScriptButtons` / `replaceScriptButtons` etc. no longer require `script_id` param

## 3.4.11
- `prompt.position` now includes `injection_order` field
- Preset placeholder prompt IDs changed from `snake_case` to `camelCase` (BREAKING)

## 3.4.8
- `generate` / `generateRaw` support `custom_api`

## 3.4.3
- Add `builtin.renderPromptManager`, `builtin.renderPromptManagerDebounced`

## 3.4.1
- Add `createWorldbookEntries`, `deleteWorldbookEntries`

## 3.4.0
- Rewrite worldbook API: `Worldbook` replaces `Lorebook` (BREAKING: old Lorebook functions deprecated)
- Add `Mvu` interface (MagVarUpdate framework)
- Add `appendInexistentScriptButtons`

## 3.3.2
- Add `zod` (z) as built-in library

## 3.3.1
- `{{get_xxx_variable}}` string values no longer quoted

## 3.3.0
- New preset API: `getPreset`, `replacePreset`, `setPreset`, `updatePresetWith`, `createPreset`, `deletePreset`

## 3.2.11
- Add `getAllVariables()`

## 3.2.6
- Default log level reduced (enable debug mode for verbose)

## 3.2.5
- Add `getScriptButtons`, `replaceScriptButtons`
- Add `eventEmitAndWait`

## 3.2.3
- Script folders, batch operations, script data storage, `getVariables({type: 'script'})`

## 3.2.0
- `{{get_message_variable}}` macros work in displayed messages
- Add `registerMacros` (renamed to `registerMacroLike` later)

## 3.1.4
- Export `builtin.addOneMessage`

## 3.1.2
- Add `createChatMessages`, `deleteChatMessages`, `rotateChatMessages`
- Add `getChatLorebook`, `setChatLorebook`

## 3.1.1
- Add `setChatMessages` (replaces `setChatMessage`)
- `getChatMessages` now returns typed results based on `include_swipes` option

## 3.0.7
- Export `toastr` library

## 3.0.5
- Add `replaceLorebookEntries`, `updateLorebookEntriesWith`
- Add `createLorebookEntries`, `deleteLorebookEntries`

## 3.0.2
- Add `getScriptId`
- `getVariables` supports `'character'` type and negative `message_id`
- `getChatMessage` / `setChatMessage` support negative indices

## 3.0.0
- Script library with import/export
- Character-bound variables
- Real-time code editing
- Core functions registered to global scope
