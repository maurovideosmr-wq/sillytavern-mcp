# sillytavern-mcp

MCP (Model Context Protocol) server for SillyTavern. Enables AI agents to interact with a running SillyTavern instance — manage character cards, run diagnostics, and read console logs.

Built with [fastmcp](https://github.com/jlowin/fastmcp) + [uv](https://docs.astral.sh/uv/).

## Tools

| Tool | Description |
|------|-------------|
| `write_character_card` | Create a SillyTavern character card from text attributes. Writes a V2/V3 PNG card to the characters directory. |
| `import_character_card` | Import an existing character card PNG (with embedded V2/V3 metadata). Copies as-is. |
| `get_st_diagnostics` | Comprehensive health check on a running ST instance — API, CSRF, character cards, chat files, config, plugins, process. |
| `get_st_console` | Read ST console log captured by the st-console-logger plugin. Supports incremental reads. |
| `setup_st_logging` | Install the st-console-logger plugin into ST's `plugins/` directory and enable server plugins. |

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/#installation)
- A running [SillyTavern](https://github.com/SillyTavern/SillyTavern) instance

### Setup

```bash
# Clone the repository
git clone <repo-url> sillytavern-mcp
cd sillytavern-mcp

# Install dependencies (auto-creates .venv)
uv sync
```

### Configure Kilo

Add to your `kilo.json` (global at `~/.config/kilo/kilo.json` or project-level):

```json
{
  "sillytavern-mcp": {
    "type": "local",
    "command": ["uv", "run", "--directory", "/path/to/sillytavern-mcp", "python", "-m", "sillytavern_mcp"],
    "environment": {
      "SILLYTAVERN_DATA_DIR": "/path/to/SillyTavern/data",
      "SILLYTAVERN_USER": "default-user",
      "SILLYTAVERN_URL": "http://localhost:8000"
    },
    "enabled": true
  }
}
```

### Verify

```bash
uv run python -m sillytavern_mcp
```

The server starts in stdio mode. Kilo will automatically discover the 5 tools.

## Console Logging (Optional)

The `get_st_console` tool requires the st-console-logger plugin:

```bash
# One-time: deploy the plugin
uv run python -c "import asyncio; from sillytavern_mcp import mcp; asyncio.run(mcp.call_tool('setup_st_logging', {}))"
```

Then **restart SillyTavern**. Console output will be captured to `data/st_console.log`.

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SILLYTAVERN_DATA_DIR` | auto-detect | Path to ST `data/` directory |
| `SILLYTAVERN_USER` | `default-user` | ST user handle |
| `SILLYTAVERN_URL` | `http://localhost:8000` | ST HTTP API base URL |

## Project Structure

```
sillytavern-mcp/
├── sillytavern_mcp/
│   ├── __init__.py              # FastMCP instance
│   ├── __main__.py              # python -m entry point
│   ├── server.py                # Tool registration
│   ├── png_util.py              # PNG chunk read/write (character cards)
│   ├── character_schema.py      # V2/V3 card JSON builder
│   ├── default_avatar.py        # Fallback avatar generator
│   ├── st_client.py             # ST HTTP API client (cookie-aware CSRF)
│   ├── utils.py                 # Path resolution, shared helpers
│   ├── st_console_plugin/       # Node.js plugin for console capture
│   │   ├── index.js
│   │   └── package.json
│   └── tools/
│       ├── write_character.py
│       ├── import_character.py
│       ├── st_diagnostics.py
│       ├── st_console.py
│       └── setup_logging.py
├── pyproject.toml
└── README.md
```

## License

MIT
