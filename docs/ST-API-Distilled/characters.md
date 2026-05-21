# Characters API (/api/characters)

## create
POST /api/characters/create
  Req: multipart (avatar file optional) + fields: ch_name, description, personality, scenario, first_mes, mes_example, creator_notes, system_prompt, post_history_instructions, tags, talkativeness, fav, world, json_data, file_name
  Res: "avatar_name.png"
  Note: Creates PNG card + chat dir. json_data preserves extension/regex fields. world auto-links character book.

## rename
POST /api/characters/rename
  Req: {"avatar_url","new_name"}
  Res: {"avatar":"new_name.png"}
  Note: Renames file + chat dir. Updates name in card JSON.

## edit
POST /api/characters/edit
  Req: multipart (avatar file optional) + same fields as create + avatar_url
  Res: 200
  Note: Full card replace. Preserves chat/create_date from body.

## edit-avatar
POST /api/characters/edit-avatar
  Req: multipart with avatar file + {"avatar_url"}
  Res: 200
  Note: Only replaces the avatar image on existing card.

## edit-attribute
POST /api/characters/edit-attribute
  Req: {"avatar_url","ch_name","field":"topLevelKey","value":"..."}
  Res: 200
  Note: Sets a single top-level field. Cannot edit json_data.

## merge-attributes
POST /api/characters/merge-attributes
  Req: {"avatar":"name.png", ...fieldsToMerge}  OR  {"avatars":["a.png","b.png"], "data":{...}, "filter":{"path":"data.extensions.x"}}
  Res: 200  OR  {"updated":["a.png"],"skipped":["b.png"],"failed":[]}
  Note: Deep merge with __@@UNSET@@__ sentinel for deletion. Bulk mode supports filter.path to skip chars. Uses TavernCardValidator. This is the endpoint for writing extension fields (regex_scripts, etc).

## delete
POST /api/characters/delete
  Req: {"avatar_url","delete_chats":true|false}
  Res: 200

## all
POST /api/characters/all
  Req: {} (empty)
  Res: [{name, avatar_url, description, personality, ...}]  (shallow or full list)
  Note: Lists all characters. Use to refresh ST cache after filesystem writes.

## get
POST /api/characters/get
  Req: {"avatar_url":"name.png"}
  Res: Full V2 card JSON

## chats
POST /api/characters/chats
  Req: {"avatar_url":"name.png", "simple":true|false, "metadata":true|false}
  Res: [{file_name, file_id, ...}] or simple list of file names

## import
POST /api/characters/import
  Req: multipart (file) + {"file_type":"png|json|yaml|yml|charx|byaf", "preserved_name":"optional"}
  Res: {"file_name":"name.png"}

## duplicate
POST /api/characters/duplicate
  Req: {"avatar_url":"name.png"}
  Res: {"path":"name_1.png"}

## export
POST /api/characters/export
  Req: {"avatar_url":"name.png", "format":"png|json"}
  Res: File download (png: mutated buffer; json: application/json)
