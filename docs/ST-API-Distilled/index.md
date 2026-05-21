# SillyTavern REST API

## Base URL
http://localhost:8001 (default)

## Auth
- Basic auth mode: use Authorization header (Base64 user:pass)
- Whitelist mode: 403 if IP not whitelisted
- Multi-user mode: login via POST /api/users/login first, session cookie
- CSRF: GET /csrf-token -> {"token":"..."}; send as x-csrf-token header on POST/PUT/DELETE

## Common patterns
- All non-app routes under /api/* require login unless /api/users (public)
- Most accept POST with JSON body
- File uploads: multipart/form-data, field name 'avatar'
- Responses: JSON or sendStatus
- Deprecated endpoints auto-redirect (52 redirects: /getcharacters -> /api/characters/all)

## App-level endpoints
GET / -> index.html
GET /csrf-token -> {"token":"..."}
GET /callback/:source? -> OAuth PKCE redirect (307)
GET /login -> login page
POST /api/ping -> 204 (optional ?extend to touch session)
GET /version -> {"pkgVersion","gitBranch","commitDate","commitHash","isLatest"}

## Static file serving
/ -> backgrounds/*, characters/*, User%20Avatars/*, assets/*, user/images/*, user/files/*
/scripts/extensions/third-party/* -> third-party extension files
/thumbnail?file=&type=bg|avatar|persona -> thumbnail images
