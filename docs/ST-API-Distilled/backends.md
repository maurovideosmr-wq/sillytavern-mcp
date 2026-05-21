# AI Backends API

## Chat Completions (/api/backends/chat-completions)

**status**
POST /api/backends/chat-completions/status
  Req: API connection params
  Res: {result:"...", api_key_valid, api_url, etc}

**bias**
POST /api/backends/chat-completions/bias
  Req: {"logit_bias", token config}

**generate**
POST /api/backends/chat-completions/generate
  Req: messages, model params
  Res: streaming or full response text

**process**
POST /api/backends/chat-completions/process
  Req: Shared API request fields

## Kobold (/api/backends/kobold)

**generate**
POST /api/backends/kobold/generate
  Req: prompt, model params

**status**
POST /api/backends/kobold/status
  Req: {}
  Res: model info, version, capabilities

**transcribe-audio**
POST /api/backends/kobold/transcribe-audio
  Req: audio file/URL
  Res: transcribed text

**embed**
POST /api/backends/kobold/embed
  Req: {"text"}
  Res: embedding vector

## Text Completions (/api/backends/text-completions)

**status**
POST /api/backends/text-completions/status
  Req: API config
  Res: {result, api_key_valid, etc}

**props**
POST /api/backends/text-completions/props
  Req: {}
  Res: model properties/config

**generate**
POST /api/backends/text-completions/generate
  Req: prompt, model params
  Res: generated text
