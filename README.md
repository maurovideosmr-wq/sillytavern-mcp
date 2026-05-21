# sillytavern-mcp

[English](#english) | [中文](#chinese)

---

## English

An MCP server that bridges AI coding agents with [SillyTavern](https://github.com/SillyTavern/SillyTavern). It lets AI assistants **create character cards**, **run server diagnostics**, and **read console logs** — directly from their chat interface.

Compatible with any MCP client: **Claude Code**, **Cursor**, **Kilo**, **VS Code** (via MCP extensions), and more.

No SillyTavern modifications needed. No plugins required for basic operation. Just configure and go.

Built with [fastmcp](https://github.com/jlowin/fastmcp) + [uv](https://docs.astral.sh/uv/).

### Tools

| Tool | What it does |
|------|-------------|
| `write_character_card` | Create a character card from text attributes (name, personality, first message...). Writes a V2/V3 PNG card to the characters directory. |
| `import_character_card` | Import an existing character card PNG file. Copies as-is without modifying metadata. |
| `get_st_diagnostics` | Comprehensive health check on a running SillyTavern instance — API connectivity, character card integrity, chat files, config, plugins. Zero configuration needed. |
| `get_st_console` | Read the SillyTavern console log captured by the st-console-logger plugin. Supports incremental reading. |
| `setup_st_logging` | One-click install of the console logger plugin into SillyTavern's `plugins/` directory and enable server plugins in `config.yaml`. |
| `list_doc` | List all available JS-Slash-Runner (Tavern Helper) documentation topics. Returns a numbered list of doc names. |
| `read_doc` | Read the full content of a JS-Slash-Runner documentation page by topic name. |

### Bundled Resources

This server bundles 21 distilled documentation pages for **JS-Slash-Runner (Tavern Helper)**, covering scripting, macros, events, character management, worldbooks, variables, regex, audio, presets, chat messages, injection, extensions, and more. The AI can reference these docs to help write or debug TH scripts without leaving the chat.

Available via the `list_doc` and `read_doc` tools:

`about`, `audio`, `builtins`, `changelog`, `characters`, `chat-messages`, `events`, `extensions`, `generate`, `import-export`, `index`, `inject`, `interop`, `macros`, `presets`, `scripts`, `sharing`, `tavern-regex`, `utilities`, `variables`, `worldbook`

### Architecture

```
MCP Client (Claude Code / Cursor / Kilo / ...)
    │
    ▼
sillytavern-mcp (this project) ←── reads/writes ──→ ST data directory (character cards, logs)
    │
    └── talks to ──→ SillyTavern HTTP API (status, character list, CSRF)
```

### Setup

**Prerequisites:** Python 3.11+ and [uv](https://docs.astral.sh/uv/#installation).

```bash
git clone <repo-url> sillytavern-mcp
cd sillytavern-mcp
uv sync
```

### MCP Client Configuration

Add the server to your MCP client's configuration.

#### Option 1: VS Code

In `.vscode/mcp.json` or your VS Code MCP settings:

```json
{
  "servers": {
    "sillytavern-mcp": {
      "type": "local",
      "command": ["uv", "run", "--directory", "/path/to/sillytavern-mcp", "python", "-m", "sillytavern_mcp"],
      "env": {
        "SILLYTAVERN_DATA_DIR": "/path/to/SillyTavern/data",
        "SILLYTAVERN_USER": "default-user",
        "SILLYTAVERN_URL": "http://localhost:8000"
      }
    }
  }
}
```

#### Option 2: Claude Code

In `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "sillytavern-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/sillytavern-mcp", "python", "-m", "sillytavern_mcp"],
      "env": {
        "SILLYTAVERN_DATA_DIR": "/path/to/SillyTavern/data",
        "SILLYTAVERN_USER": "default-user",
        "SILLYTAVERN_URL": "http://localhost:8000"
      }
    }
  }
}
```

#### Option 3: Cursor

In Cursor settings → MCP Servers → Add new:

```json
{
  "name": "sillytavern-mcp",
  "type": "command",
  "command": "uv",
  "args": ["run", "--directory", "/path/to/sillytavern-mcp", "python", "-m", "sillytavern_mcp"],
  "env": {
    "SILLYTAVERN_DATA_DIR": "/path/to/SillyTavern/data",
    "SILLYTAVERN_USER": "default-user",
    "SILLYTAVERN_URL": "http://localhost:8000"
  }
}
```

#### Option 4: Kilo

In `~/.config/kilo/kilo.json`:

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

### Quick Test

After configuration, verify the server connects correctly:

```bash
uv run python -m sillytavern_mcp
```

It will start in stdio mode and wait for MCP protocol messages from your client. No output means it's working.

Ask your AI assistant: *"Can you check the status of my SillyTavern?"*

### Enable Console Logging (Optional)

To let your AI assistant read SillyTavern's console output (errors, model loading, etc.):

Ask your assistant to run `setup_st_logging`. It will automatically:
1. Copy the logger plugin to ST's `plugins/` directory
2. Enable server plugins in `config.yaml` (`enableServerPlugins: true`)

Then **restart SillyTavern**. After restart, console output is captured to `data/st_console.log` — readable via the `get_st_console` tool.

No terminal commands needed — your assistant handles everything.

### Configuration Reference

| Environment Variable | Default | Description |
|----------|---------|-------------|
| `SILLYTAVERN_DATA_DIR` | Auto-detect | Path to SillyTavern `data/` directory |
| `SILLYTAVERN_USER` | `default-user` | SillyTavern user handle |
| `SILLYTAVERN_URL` | `http://localhost:8000` | SillyTavern HTTP API base URL |

### Project Structure

```
sillytavern-mcp/
├── sillytavern_mcp/
│   ├── __init__.py              # FastMCP instance
│   ├── __main__.py              # Entry point (python -m)
│   ├── server.py                # Tool & resource registration
│   ├── png_util.py              # PNG chunk read/write (character card format)
│   ├── character_schema.py      # V2/V3 character card JSON builder
│   ├── default_avatar.py        # Fallback avatar generator
│   ├── st_client.py             # SillyTavern HTTP API client
│   ├── utils.py                 # Shared helpers, path resolution
│   ├── st_console_plugin/       # Node.js server plugin for log capture
│   │   ├── index.js
│   │   └── package.json
│   ├── resources/
│   │   ├── __init__.py
│   │   └── docs_distilled.py    # 21 TH doc resources (docs://TH/*)
│   └── tools/
│       ├── write_character.py
│       ├── import_character.py
│       ├── st_diagnostics.py
│       ├── st_console.py
│       ├── setup_logging.py
│       └── th_doc_reader.py     # list_doc / read_doc tools
├── docs/
│   └── JS-Slash-Runner-Distilled/  # 21 distilled TH doc files
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## 中文

适用于 [SillyTavern](https://github.com/SillyTavern/SillyTavern) 的 MCP 服务器。让 AI 助手能直接在聊天界面中 **创建角色卡**、**运行服务器诊断**、**读取控制台日志**。

兼容任何 MCP 客户端：**Claude Code**、**Cursor**、**Kilo**、**VS Code**（通过 MCP 扩展）等。

不需要修改 SillyTavern 代码，不需要安装插件即可使用基础功能。配置好就能用。

基于 [fastmcp](https://github.com/jlowin/fastmcp) + [uv](https://docs.astral.sh/uv/) 构建。

### 工具列表

| 工具 | 功能 |
|------|------|
| `write_character_card` | 从文本属性（名称、人格、首条消息等）创建角色卡，生成 V2/V3 PNG 写入 characters 目录 |
| `import_character_card` | 导入已有的角色卡 PNG 文件，原样复制不改元数据 |
| `get_st_diagnostics` | 对运行中的 SillyTavern 做全面体检——API 连通性、角色卡完整性、聊天文件、配置、插件。零配置开箱即用 |
| `get_st_console` | 读取 st-console-logger 插件捕获的 SillyTavern 控制台输出。支持增量读取 |
| `setup_st_logging` | 一键安装控制台日志插件到 ST 的 `plugins/` 目录，自动修改 `config.yaml` 启用服务器插件 |
| `list_doc` | 列出所有可用的 JS-Slash-Runner（酒馆助手）文档主题 |
| `read_doc` | 按主题名称读取 JS-Slash-Runner 文档的完整内容 |

### 内置文档

本服务内置 21 篇 **JS-Slash-Runner（酒馆助手）** 蒸馏文档，涵盖脚本、宏、事件、角色管理、世界书、变量、正则、音频、预设、聊天消息、注入、扩展等。AI 可直接参考这些文档来编写或调试 TH 脚本。

通过 `list_doc` 和 `read_doc` 工具访问：

`about`、`audio`、`builtins`、`changelog`、`characters`、`chat-messages`、`events`、`extensions`、`generate`、`import-export`、`index`、`inject`、`interop`、`macros`、`presets`、`scripts`、`sharing`、`tavern-regex`、`utilities`、`variables`、`worldbook`

### 架构

```
MCP 客户端 (Claude Code / Cursor / Kilo / ...)
    │
    ▼
sillytavern-mcp (本项目) ←── 读写 ──→ ST 数据目录 (角色卡、日志文件)
    │
    └── 调用 ──→ SillyTavern HTTP API (状态查询、角色列表、CSRF)
```

### 安装

**前置依赖：** Python 3.11+ 和 [uv](https://docs.astral.sh/uv/#installation)

```bash
git clone <仓库地址> sillytavern-mcp
cd sillytavern-mcp
uv sync
```

### MCP 客户端配置

根据你使用的 MCP 客户端，选择对应的配置方式。

#### 方式 1：VS Code

在 `.vscode/mcp.json` 或 VS Code 的 MCP 设置中添加：

```json
{
  "servers": {
    "sillytavern-mcp": {
      "type": "local",
      "command": ["uv", "run", "--directory", "D:\\path\\to\\sillytavern-mcp", "python", "-m", "sillytavern_mcp"],
      "env": {
        "SILLYTAVERN_DATA_DIR": "D:\\path\\to\\SillyTavern\\data",
        "SILLYTAVERN_USER": "default-user",
        "SILLYTAVERN_URL": "http://localhost:8000"
      }
    }
  }
}
```

#### 方式 2：Claude Code

在 `~/.claude/settings.json` 中添加：

```json
{
  "mcpServers": {
    "sillytavern-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/sillytavern-mcp", "python", "-m", "sillytavern_mcp"],
      "env": {
        "SILLYTAVERN_DATA_DIR": "/path/to/SillyTavern/data",
        "SILLYTAVERN_USER": "default-user",
        "SILLYTAVERN_URL": "http://localhost:8000"
      }
    }
  }
}
```

#### 方式 3：Cursor

在 Cursor 设置 → MCP Servers → 添加新服务：

```json
{
  "name": "sillytavern-mcp",
  "type": "command",
  "command": "uv",
  "args": ["run", "--directory", "/path/to/sillytavern-mcp", "python", "-m", "sillytavern_mcp"],
  "env": {
    "SILLYTAVERN_DATA_DIR": "/path/to/SillyTavern/data",
    "SILLYTAVERN_USER": "default-user",
    "SILLYTAVERN_URL": "http://localhost:8000"
  }
}
```

#### 方式 4：Kilo

在 `~/.config/kilo/kilo.json` 中添加：

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

### 快速测试

配置完成后，验证服务器能正常连接：

```bash
uv run python -m sillytavern_mcp
```

服务器会以 stdio 模式启动，等待客户端的 MCP 协议消息。没有输出即表示启动成功。

在你的 AI 助手中输入：**"检查一下我的 SillyTavern 的状态"**

### 可选：启用控制台日志

想让你的 AI 助手能读取 SillyTavern 的控制台输出（错误信息、模型加载等）？

对 AI 助手说：**"帮我安装日志插件"**

它会自动调用 `setup_st_logging` 完成：
1. 将日志插件复制到 ST 的 `plugins/` 目录
2. 在 `config.yaml` 中启用服务器插件

然后**重启 SillyTavern**。重启后，控制台输出会自动写入 `data/st_console.log`，通过 `get_st_console` 工具即可读取。

全程不需要手动操作终端——助手会帮你做完。

### 配置说明

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `SILLYTAVERN_DATA_DIR` | 自动检测 | SillyTavern 的 `data/` 目录路径 |
| `SILLYTAVERN_USER` | `default-user` | SillyTavern 用户名 |
| `SILLYTAVERN_URL` | `http://localhost:8000` | SillyTavern HTTP API 地址 |

### 项目结构

```
sillytavern-mcp/
├── sillytavern_mcp/
│   ├── __init__.py              # FastMCP 实例
│   ├── __main__.py              # 启动入口 (python -m)
│   ├── server.py                # 工具 & 资源注册
│   ├── png_util.py              # PNG chunk 读写（角色卡格式）
│   ├── character_schema.py      # V2/V3 角色卡 JSON 构建
│   ├── default_avatar.py        # 无头像时的占位图生成
│   ├── st_client.py             # SillyTavern HTTP API 客户端
│   ├── utils.py                 # 共用函数、路径解析
│   ├── st_console_plugin/       # Node.js 服务端日志插件
│   │   ├── index.js
│   │   └── package.json
│   ├── resources/
│   │   ├── __init__.py
│   │   └── docs_distilled.py    # 21 篇 TH 文档资源 (docs://TH/*)
│   └── tools/
│       ├── write_character.py
│       ├── import_character.py
│       ├── st_diagnostics.py
│       ├── st_console.py
│       ├── setup_logging.py
│       └── th_doc_reader.py     # list_doc / read_doc 工具
├── docs/
│   └── JS-Slash-Runner-Distilled/  # 21 篇蒸馏 TH 文档
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## License / 许可证

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0), the same license as SillyTavern.

See the [LICENSE](LICENSE) file for details.
