# Extensions API (/api/extensions)
All gated by extensions.enabled config flag.

**install** POST /api/extensions/install
  Req: {"url":"git repo","global":false,"branch":"optional"}
  Note: clones git repo, validates manifest.json

**update** POST /api/extensions/update
  Req: {"extensionName","global":false}
  Note: git pull, returns commit hash

**branches** POST /api/extensions/branches
  Req: {"extensionName","global":false}
  Res: [{current,commit,name,label}]

**switch** POST /api/extensions/switch
  Req: {"extensionName","branch","global":false}
  Note: git checkout branch

**move** POST /api/extensions/move
  Req: {"extensionName","source":"local|global","destination":"local|global"}
  Note: admin only, moves between user/global dirs

**version** POST /api/extensions/version
  Req: {"extensionName","global":false}
  Res: {currentBranchName,currentCommitHash,isUpToDate,remoteUrl}

**delete** POST /api/extensions/delete
  Req: {"extensionName","global":false}
  Note: removes entire extension directory

**discover** GET /api/extensions/discover
  Res: [{type:"system"|"local"|"global", name}]
  Note: lists all installed extensions

# Assets API (/api/assets)

**get** POST /api/assets/get
**download** POST /api/assets/download
**delete** POST /api/assets/delete
**character** POST /api/assets/character

# Avatars API (/api/avatars)

**get** POST /api/avatars/get
  Res: avatar list
**delete** POST /api/avatars/delete
  Req: {"avatar"}
**upload** POST /api/avatars/upload
  Req: multipart file

# Backgrounds API (/api/backgrounds)

**all** POST /api/backgrounds/all
**folders** POST /api/backgrounds/folders
**delete** POST /api/backgrounds/delete
  Req: {"bg"}
**rename** POST /api/backgrounds/rename
**upload** POST /api/backgrounds/upload
  Req: multipart file

# Images API (/api/images)

**upload** POST /api/images/upload
**list/:folder?** POST /api/images/list/:folder?
**folders** POST /api/images/folders
**delete** POST /api/images/delete

# Sprites API (/api/sprites)

**get** GET /api/sprites/get?file=...&type=...
**delete** POST /api/sprites/delete
**upload-zip** POST /api/sprites/upload-zip
**upload** POST /api/sprites/upload

# Files API (/api/files)

**sanitize-filename** POST /api/files/sanitize-filename
  Req: {"name"}
  Res: safe filename
**upload** POST /api/files/upload
**delete** POST /api/files/delete
**verify** POST /api/files/verify
