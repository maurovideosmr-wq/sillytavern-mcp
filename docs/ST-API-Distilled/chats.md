# Chats API (/api/chats)

## save
POST /api/chats/save
  Req: {"avatar_url","chat","mes"}

## get
POST /api/chats/get
  Req: {"avatar_url","chat_file"}

## rename
POST /api/chats/rename
  Req: {"avatar_url","chat_file","new_chat_file"}

## delete
POST /api/chats/delete
  Req: {"avatar_url","chat_file"}

## export
POST /api/chats/export
  Req: {"avatar_url","chat_file"}

## group/import
POST /api/chats/group/import
  Req: multipart file

## import
POST /api/chats/import
  Req: multipart file + {"avatar_url"}

## group/get
POST /api/chats/group/get
  Req: {"id":"groupId","chat_file"}

## group/info
POST /api/chats/group/info
  Req: {"id":"groupId"}

## group/delete
POST /api/chats/group/delete
  Req: {"id":"groupId","chat_file"}

## group/save
POST /api/chats/group/save
  Req: {"id":"groupId","chat_file","chat"}

## search
POST /api/chats/search
  Req: {"avatar_url","text"}

## recent
POST /api/chats/recent
  Req: {"avatar_url","limit"}

# World Info API (/api/worldinfo)

## list
POST /api/worldinfo/list
  Req: {}
  Res: [{file_id, name, extensions}]

## get
POST /api/worldinfo/get
  Req: {"name"}
  Res: {"entries":{...}, "name":"..."}

## delete
POST /api/worldinfo/delete
  Req: {"name"}

## import
POST /api/worldinfo/import
  Req: multipart (file) + {"convertedData":"optionalJsonString"}
  Res: {"name"}

## edit
POST /api/worldinfo/edit
  Req: {"name","data":{"entries":{...}}}
  Res: {"ok":true}

# Groups API (/api/groups)

## all
POST /api/groups/all
  Req: {}
  Res: [group objects]

## create
POST /api/groups/create
  Req: {group fields}

## edit
POST /api/groups/edit
  Req: {"id","...fields"}

## delete
POST /api/groups/delete
  Req: {"id"}
