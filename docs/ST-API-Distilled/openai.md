# OpenAI API (/api/openai)

**caption-image**
POST /api/openai/caption-image
  Req: image + optional prompt

**generate-voice**
POST /api/openai/generate-voice
  Req: {"text","voice"} (TTS)

**electronhub/generate-voice**
POST /api/openai/electronhub/generate-voice

**electronhub/models**
POST /api/openai/electronhub/models
  Res: [{id, name, ...}]

**chutes/generate-voice**
POST /api/openai/chutes/generate-voice

**chutes/models/embedding**
POST /api/openai/chutes/models/embedding

**nanogpt/models/embedding**
POST /api/openai/nanogpt/models/embedding

**siliconflow/models/embedding**
POST /api/openai/siliconflow/models/embedding

**workers-ai/models/embedding**
POST /api/openai/workers-ai/models/embedding

**generate-image**
POST /api/openai/generate-image
  Req: prompt, model params

**generate-video**
POST /api/openai/generate-video
  Req: prompt, model params

**transcribe-audio**
POST /api/openai/transcribe-audio
  Req: audio file
  Res: transcribed text

**groq/transcribe-audio**
POST /api/openai/groq/transcribe-audio

**mistral/transcribe-audio**
POST /api/openai/mistral/transcribe-audio

**zai/transcribe-audio**
POST /api/openai/zai/transcribe-audio

**chutes/transcribe-audio**
POST /api/openai/chutes/transcribe-audio
