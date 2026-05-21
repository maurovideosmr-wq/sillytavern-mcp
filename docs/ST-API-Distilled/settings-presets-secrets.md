# Settings API (/api/settings)

**save** POST /api/settings/save
  Req: {"settings_key": value, ...}  (merged into extension_settings)
  Res: 200

**get** POST /api/settings/get
  Req: {}
  Res: current settings object

**get-snapshots** POST /api/settings/get-snapshots
  Req: {}
  Res: available snapshot list

**load-snapshot** POST /api/settings/load-snapshot
  Req: {"name"}
  Res: snapshot data

**make-snapshot** POST /api/settings/make-snapshot
  Req: {"name"}

**restore-snapshot** POST /api/settings/restore-snapshot
  Req: {"name"}

# Presets API (/api/presets)

**save** POST /api/presets/save
  Req: preset config object
  Note: saves inference preset

**delete** POST /api/presets/delete
  Req: preset identifier

**restore** POST /api/presets/restore
  Req: {"name"}

# Secrets API (/api/secrets)

**write** POST /api/secrets/write
  Req: {"key","value","type"}
  Note: encrypts and stores secret

**read** POST /api/secrets/read
  Req: {"key"}
  Res: decrypted secret value

**view** POST /api/secrets/view
  Req: {"key"}
  Res: metadata (not value)

**find** POST /api/secrets/find
  Req: {"key"}
  Res: whether key exists + type

**delete** POST /api/secrets/delete
  Req: {"key"}

**rotate** POST /api/secrets/rotate
  Req: {"key"}
  Note: re-encrypts with new key

**rename** POST /api/secrets/rename
  Req: {"old_key","new_key"}

**settings** POST /api/secrets/settings
  Req: {}
  Res: secrets config (enabled, etc)
