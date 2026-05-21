# Third-party LLM APIs

## Anthropic (/api/anthropic)
**caption-image** POST /api/anthropic/caption-image

## Google (/api/google)
**caption-image** POST /api/google/caption-image
**list-voices** POST /api/google/list-voices
**generate-voice** POST /api/google/generate-voice
**list-native-voices** POST /api/google/list-native-voices
**generate-native-tts** POST /api/google/generate-native-tts
**generate-image** POST /api/google/generate-image
**generate-video** POST /api/google/generate-video

## OpenRouter (/api/openrouter)
**models/providers** POST /api/openrouter/models/providers
**models/multimodal** POST /api/openrouter/models/multimodal
**models/embedding** POST /api/openrouter/models/embedding
**models/image** POST /api/openrouter/models/image
**credits** POST /api/openrouter/credits
**image/generate** POST /api/openrouter/image/generate

## NovelAI (/api/novelai)
**status** POST /api/novelai/status
**generate** POST /api/novelai/generate
**generate-image** POST /api/novelai/generate-image
**generate-voice** POST /api/novelai/generate-voice

## Horde (/api/horde)
**text-workers** POST /api/horde/text-workers
**text-models** POST /api/horde/text-models
**status** POST /api/horde/status
**cancel-task** POST /api/horde/cancel-task
**task-status** POST /api/horde/task-status
**generate-text** POST /api/horde/generate-text
**sd-samplers** POST /api/horde/sd-samplers
**sd-models** POST /api/horde/sd-models
**caption-image** POST /api/horde/caption-image
**user-info** POST /api/horde/user-info
**generate-image** POST /api/horde/generate-image

## NanoGPT (/api/nanogpt)
**credits** POST /api/nanogpt/credits
**models/providers** POST /api/nanogpt/models/providers

## Minimax (/api/minimax)
**generate-voice** POST /api/minimax/generate-voice

## Azure (/api/azure)
**list** POST /api/azure/list -> available voices
**generate** POST /api/azure/generate -> TTS

## Volcengine (/api/volcengine)
**generate-voice** POST /api/volcengine/generate-voice
