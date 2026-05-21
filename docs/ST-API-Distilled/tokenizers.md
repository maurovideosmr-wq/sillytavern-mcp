# Tokenizers API (/api/tokenizers)

## Encode (text -> token count/ids)
POST /api/tokenizers/{model}/encode
  Req: {"text"}
  Res: token count or token IDs

Models: llama, nerdstash, nerdstash_v2, mistral, yi, gemma, jamba
(Use SentencePiece / rust tokenizers backend)

Models: gpt2, claude, llama3, qwen2, command-r, command-a, nemo, deepseek
(Use WebTokenizer / tiktoken backend)

## Decode (token IDs -> text)
POST /api/tokenizers/{model}/decode
  Req: {"tokens":[id,...]}
  Res: text

Same model list as encode.

## OpenAI
**encode** POST /api/tokenizers/openai/encode
  Req: {"text","model"}
  Res: token count

**decode** POST /api/tokenizers/openai/decode
  Req: {"tokens","model"}
  Res: text

**count** POST /api/tokenizers/openai/count
  Req: {"text","model"}
  Res: {"count":N} (uses OpenAI tiktoken)

## Remote backends
**remote/kobold/count** POST /api/tokenizers/remote/kobold/count
  Req: {"text"}
  Res: token count via Kobold API

**remote/textgenerationwebui/encode** POST /api/tokenizers/remote/textgenerationwebui/encode
  Req: {"text"}
  Res: token count via oobabooga API

# Vectors API (/api/vector)

**query** POST /api/vector/query
  Req: search params
  Res: ranked results

**query-multi** POST /api/vector/query-multi
  Req: multiple queries
  Res: multi-ranked results

**insert** POST /api/vector/insert
  Req: data to index

**list** POST /api/vector/list
  Req: {}
  Res: indexed items

**delete** POST /api/vector/delete
  Req: ID or filter

**purge-all** POST /api/vector/purge-all
  Note: clear entire vector DB

**purge** POST /api/vector/purge
  Req: selective filter
