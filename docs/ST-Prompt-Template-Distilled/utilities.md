# Utilities

## Template Processing

```typescript
function evalTemplate(content, data?, options?): string
// Processes a string through the EJS template engine.
// content — template string with <% %> tags
// data — additional context variables
// options — processing options (sandbox, etc.)

function compileTemplate(code, options?): Function
// Compiles template source into a reusable function.
// Uses Web Worker if compile_workers setting is enabled.

function getSyntaxErrorInfo(code, max_lines?): object
// Parses template code and returns syntax error details.
// Returns { line, col, message, snippet } or null if valid.
```

## Define Globals

```typescript
function define(name, value, merge?): void
// Registers a global variable or function accessible in all templates.
// merge — boolean, uses _.merge for objects
```

## Execute ST Commands

```typescript
function execute(cmd): void
// Executes a SillyTavern slash command. Example:
// execute('/setvar key=好感度 100')
```

## Output

```typescript
function print(...args): void
// Outputs values to the template. Cannot be used inside <%- or <%= tags.
```

## JSON

```typescript
function parseJSON(text): any
// Fault-tolerant JSON parsing. Uses jsonrepair internally.
// Handles common JSON errors (trailing commas, single quotes, etc.)

function jsonPatch(dest, change): any
// Applies JSON Patch (RFC 6902) to a destination object.
// change — array of patch operations [{ op, path, value }]

function patchVariables(key, change, options?): void
// Applies JSON Patch to a variable.
```

## Faker.js

```typescript
// faker object is globally available
// Examples:
<%- faker.person.fullName() %>
<%- faker.number.int({ min: 1, max: 100 }) %>
<%- faker.lorem.sentence() %>
// Full Faker.js API: https://fakerjs.dev/
```

## Zod Validation

```typescript
function setVariableSchema(schema): void
// Sets a Zod schema for variable validation.
// All variable writes are validated against this schema.

function applyVarYamlAnnotate(key?, schema?): string
// Dumps variables as annotated YAML using schema type info.
```
