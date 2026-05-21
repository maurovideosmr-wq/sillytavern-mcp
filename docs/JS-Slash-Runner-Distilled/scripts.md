# Scripts

## Types

```typescript
type ScriptButton = {
  name: string;
  visible: boolean;
};

type ScriptTreesOptions = {
  type: 'global' | 'preset' | 'character';
};
```

## Public API

```typescript
function getAllEnabledScriptButtons(): { [script_id: string]: { button_id: string; button_name: string }[] }
// Returns all registered script buttons across all scopes.

function getScriptTrees(option: ScriptTreesOptions): ScriptTree[]
// Returns the script tree structure for the given scope.

function replaceScriptTrees(script_trees: PartialDeep<ScriptTree>[], option: ScriptTreesOptions): void
// Replaces script trees. Validates via ScriptTree.parse.

function updateScriptTreesWith(
  updater: (script_trees: ScriptTree[]) => PartialDeep<ScriptTree>[] | Promise<PartialDeep<ScriptTree>[]>,
  option: ScriptTreesOptions
): ScriptTree[] | Promise<ScriptTree[]>
// Gets trees, applies updater, saves, returns updated trees.
```

## Iframe-Internal (_bind) API

```typescript
function _getButtonEvent(this: Window, button_name: string): string
// Returns the event type string for a script button click.

function _getScriptButtons(this: Window): ScriptButton[]
// Returns buttons for the current script.

function _replaceScriptButtons(this: Window, buttons: ScriptButton[]): void
function _replaceScriptButtons(this: Window, script_id: string, buttons: ScriptButton[]): void
// Replaces buttons for the current script (or specified script_id).

function _updateScriptButtonsWith(
  this: Window,
  updater: (buttons: ScriptButton[]) => ScriptButton[] | Promise<ScriptButton[]>
): ScriptButton[] | Promise<ScriptButton[]>

function _appendInexistentScriptButtons(this: Window, buttons: ScriptButton[]): ScriptButton[]
function _appendInexistentScriptButtons(this: Window, script_id: string, buttons: ScriptButton[]): ScriptButton[]
// Adds buttons whose name doesn't already exist.

function _getScriptName(this: Window): string
// Returns the current script's name.

function _getScriptInfo(this: Window): string
// Returns the current script's info text.

function _replaceScriptInfo(this: Window, info: string): void
// Sets the current script's info text.
```

## Examples

```typescript
// Get script trees for current character
const trees = TavernHelper.getScriptTrees({ type: 'character' });

// Inside an iframe, add a button
const buttons = TavernHelper._bind._getScriptButtons.call(window);
TavernHelper._bind._replaceScriptButtons.call(window, [
  ...buttons,
  { name: 'My Action', visible: true },
]);
```
