# Users API

## Public (/api/users) - no auth required

**list** POST /api/users/list
  Res: [{handle, name, avatar}]

**login** POST /api/users/login
  Req: {"handle","password"}
  Res: user profile + session cookie

**recover-step1** POST /api/users/recover-step1
  Req: {"handle"}

**recover-step2** POST /api/users/recover-step2
  Req: token + new password

## Private (/api/users) - auth required

**logout** POST /api/users/logout
**me** GET /api/users/me
  Res: current user profile

**change-avatar** POST /api/users/change-avatar
  Req: multipart file upload

**change-password** POST /api/users/change-password
  Req: {"current_password","new_password"}

**backup** POST /api/users/backup
  Res: backup file download

**reset-settings** POST /api/users/reset-settings
  Note: resets user settings to default

**change-name** POST /api/users/change-name
  Req: {"handle"}

**reset-step1** POST /api/users/reset-step1
**reset-step2** POST /api/users/reset-step2

## Admin (/api/users) - requires admin role

**get** POST /api/users/get
  Res: all users with metadata

**disable** POST /api/users/disable
  Req: {"handle"}

**enable** POST /api/users/enable
  Req: {"handle"}

**promote** POST /api/users/promote
  Req: {"handle"}

**demote** POST /api/users/demote
  Req: {"handle"}

**create** POST /api/users/create
  Req: {"handle","password","name"}

**delete** POST /api/users/delete
  Req: {"handle"}

**slugify** POST /api/users/slugify
  Req: {"text"}
  Res: URL-safe slug
