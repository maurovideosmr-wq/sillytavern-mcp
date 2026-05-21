# Characters

## Get Character Data

```typescript
function getchar(name?, template?, data?): string
// Gets character card definition, processed through EJS template.
// name — character name (default: current character)
// template — EJS template string (default: '<%= description %>')
// data — additional context variables for the template

function getChara(name?, template?, data?): string
function getChr(name?, template?, data?): string
// Aliases for getchar
```

## Get Raw Data

```typescript
function getCharData(name?): object
// Returns raw character data object (description, personality, scenario, etc.)
```

## List Characters

```typescript
function getCharacters(include?, exclude?): string[]
// Returns array of character names.
// include — optional filter
// exclude — optional filter string or regex
```

## Example

```ejs
<%- getchar() %>
<!-- Renders current character's description -->

<%- getchar('助手', '<%= personality %> 性格: <%= tags %>') %>
<!-- Custom template for a specific character -->

<% getCharacters().forEach(name => { %>
  角色：<%- name %>
<% }) %>
```
