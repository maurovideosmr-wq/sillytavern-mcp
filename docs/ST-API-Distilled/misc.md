# Translate API (/api/translate)
**libre** POST /api/translate/libre
**google** POST /api/translate/google
**yandex** POST /api/translate/yandex
**lingva** POST /api/translate/lingva
**deepl** POST /api/translate/deepl
**onering** POST /api/translate/onering
**deeplx** POST /api/translate/deeplx
**bing** POST /api/translate/bing

# Speech API (/api/speech)
**recognize** POST /api/speech/recognize  (STT)
**synthesize** POST /api/speech/synthesize  (TTS)

# Search API (/api/search)
**serpapi** POST /api/search/serpapi
**transcript** POST /api/search/transcript
**searxng** POST /api/search/searxng
**tavily** POST /api/search/tavily
**koboldcpp** POST /api/search/koboldcpp
**serper** POST /api/search/serper
**zai** POST /api/search/zai
**visit** POST /api/search/visit

# Classify API (/api/extra/classify)
**labels** POST /api/extra/classify/labels
  Req: {"text"}
  Res: {label, confidence}
**/** POST /api/extra/classify/

# Caption API (/api/extra/caption)
**/** POST /api/extra/caption/
  Req: image

# Stable Diffusion API (/api/sd)
**ping** POST /api/sd/ping
**upscalers** POST /api/sd/upscalers
**vaes** POST /api/sd/vaes
**samplers** POST /api/sd/samplers
**schedulers** POST /api/sd/schedulers
**models** POST /api/sd/models
**get-model** POST /api/sd/get-model
**set-model** POST /api/sd/set-model
**generate** POST /api/sd/generate
**sd-next/upscalers** POST /api/sd/sd-next/upscalers

# Stats API (/api/stats)
**get** POST /api/stats/get
**recreate** POST /api/stats/recreate
**update** POST /api/stats/update

# Themes API (/api/themes)
**save** POST /api/themes/save
**delete** POST /api/themes/delete

# Quick Replies API (/api/quick-replies)
**save** POST /api/quick-replies/save
**delete** POST /api/quick-replies/delete

# Moving UI API (/api/moving-ui)
**save** POST /api/moving-ui/save

# Content Manager API (/api/content)
**importURL** POST /api/content/importURL
**importUUID** POST /api/content/importUUID

# Data Maid API (/api/data-maid)
**report** POST /api/data-maid/report
  Req: data cleanup params
**finalize** POST /api/data-maid/finalize
**view** GET /api/data-maid/view
  Res: current cleanup state
**delete** POST /api/data-maid/delete

# Backups API (/api/backups)
**chat/get** POST /api/backups/chat/get
**chat/delete** POST /api/backups/chat/delete
**chat/download** POST /api/backups/chat/download

# Image Metadata API (/api/image-metadata)
**folders/get** POST /api/image-metadata/folders/get
**folders/create** POST /api/image-metadata/folders/create
**folders/set-thumbnails** POST /api/image-metadata/folders/set-thumbnails
**folders/update** POST /api/image-metadata/folders/update
**folders/delete** POST /api/image-metadata/folders/delete
**folders/assign** POST /api/image-metadata/folders/assign
**folders/unassign** POST /api/image-metadata/folders/unassign
**/** POST /api/image-metadata/
**all** POST /api/image-metadata/all
**cleanup** POST /api/image-metadata/cleanup

# Thumbnails
**thumbnail** GET /thumbnail?file=...&type=bg|avatar|persona&animated=true|false
  Note: serves resized image; auto-generates if missing; falls back to original
