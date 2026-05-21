# Audio

## Types

```typescript
type Audio = {
  title: string;
  url: string;
};

type AudioWithOptionalTitle = {
  title?: string;
  url: string;
};

type AudioSettings = {
  enabled: boolean;
  mode: AudioMode;       // enum from ST settings
  muted: boolean;
  volume: number;        // 0-100
};
```

## API

```typescript
function playAudio(type: 'bgm' | 'ambient', audio: AudioWithOptionalTitle): void
// Plays an audio URL. Adds to playlist if not already present.
// If title is omitted, extracts from URL filename.

function pauseAudio(type: 'bgm' | 'ambient'): void
// Pauses the current audio.

function getAudioList(type: 'bgm' | 'ambient'): Audio[]
// Returns deep-cloned playlist.

function replaceAudioList(type: 'bgm' | 'ambient', audio_list: AudioWithOptionalTitle[]): void
// Replaces entire playlist.

function appendAudioList(type: 'bgm' | 'ambient', audio_list: AudioWithOptionalTitle[]): void
// Appends to existing playlist.

function getAudioSettings(type: 'bgm' | 'ambient'): AudioSettings
// Returns { enabled, mode, muted, volume }.

function setAudioSettings(type: 'bgm' | 'ambient', settings: Partial<AudioSettings>): void
// Updates settings. Volume is clamped 0-100.
```

## Deprecated Slash Command Helpers

```typescript
// These are legacy wrappers for slash-command-style audio control:
function audioEnable(type: 'bgm' | 'ambient', enabled: boolean): void
function audioPlay(type: 'bgm' | 'ambient', audio?: AudioWithOptionalTitle): void
function audioMode(type: 'bgm' | 'ambient', mode: AudioMode): void
function audioImport(type: 'bgm' | 'ambient', urls: string[]): void
function audioSelect(type: 'bgm' | 'ambient', title: string): void
// Prefer the non-deprecated playAudio/getAudioList/etc functions.
```

## Examples

```typescript
// Play background music
TavernHelper.playAudio('bgm', { url: 'https://example.com/music.mp3', title: 'Ambient Theme' });

// Get current playlist
const playlist = TavernHelper.getAudioList('ambient');

// Adjust volume
TavernHelper.setAudioSettings('bgm', { volume: 50 });
```
