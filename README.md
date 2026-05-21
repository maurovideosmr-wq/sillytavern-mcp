# sillytavern-mcp

[English](#english) | [中文](#chinese)

---

## English

MCP (Model Context Protocol) server for [SillyTavern](https://github.com/SillyTavern/SillyTavern). Enables AI coding agents (such as Kilo) to interact with a running SillyTavern instance — create character cards, run health checks, and read console logs.

Built with [fastmcp](https://github.com/jlowin/fastmcp) + [uv](https://docs.astral.sh/uv/).

### Tools

| Tool | What it does |
|------|-------------|
| `write_character_card` | Create a character from name, personality, first message, etc. Writes a V2/V3 PNG card. |
| `import_character_card` | Import an existing character card PNG file. Copies as-is without modifying metadata. |
| `get_st_diagnostics` | Health check on your running ST — API status, character card integrity, chat files, config, plugins. |
| `get_st_console` | Read the ST console log (requires the st-console-logger plugin). |
| `setup_st_logging` | One-click install of the console logger plugin into ST's plugins directory. |

### How It Works

```
Kilo (AI Agent) ←→ sillytavern-mcp (this project) ←→ SillyTavern (your ST)
                          │
                          ├── writes character card PNGs to data/.../characters/
                          ├── reads ST status via HTTP API
                          └── reads console output via st_console.log (plugin)
```

### Setup

**Step 1: Install Python 3.11+**

https://www.python.org/downloads/

> During installation on Windows, check **"Add Python to PATH"**.

**Step 2: Install uv (Python package manager)**

Open a terminal (cmd.exe or PowerShell) and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal after this step.

**Step 3: Get the project**

```bash
git clone <repo-url> sillytavern-mcp
cd sillytavern-mcp
```

Or download and extract the ZIP from GitHub.

**Step 4: Install dependencies**

```bash
uv sync
```

This creates a virtual environment and installs all required packages.

**Step 5: Configure for Kilo**

Add this to your `kilo.json` (global at `C:\Users\<you>\.config\kilo\kilo.json` or project-level):

```json
{
  "sillytavern-mcp": {
    "type": "local",
    "command": ["uv", "run", "--directory", "C:\\path\\to\\sillytavern-mcp", "python", "-m", "sillytavern_mcp"],
    "environment": {
      "SILLYTAVERN_DATA_DIR": "C:\\path\\to\\SillyTavern\\data",
      "SILLYTAVERN_USER": "default-user",
      "SILLYTAVERN_URL": "http://localhost:8000"
    },
    "enabled": true
  }
}
```

Replace the paths with your actual SillyTavern installation locations.

**Step 6: Verify it works**

Ask your Kilo agent: *"检查 ST 的状态"* (or *"check ST status"*).

The agent will call `get_st_diagnostics` and report back.

### Optional: Enable Console Logging

To let the AI agent read ST's console output (errors, model loading, etc.):

1. Ask your agent: **"帮我安装日志插件"** (or *"install the console logger plugin"*)
2. The agent runs `setup_st_logging`, which:
   - Copies the plugin to ST's `plugins/` directory
   - Enables server plugins in `config.yaml`
3. **Restart SillyTavern** (close and reopen it)
4. After restart, ask: **"看看 ST 的控制台输出"** (or *"show me ST's console"*)

No terminal commands needed — your agent handles everything.

### Configuration Reference

| Environment Variable | Default | Description |
|----------|---------|-------------|
| `SILLYTAVERN_DATA_DIR` | Auto-detect | Path to ST `data/` directory |
| `SILLYTAVERN_USER` | `default-user` | ST user handle |
| `SILLYTAVERN_URL` | `http://localhost:8000` | ST HTTP API base URL |

---

## 中文

[SillyTavern](https://github.com/SillyTavern/SillyTavern) 的 MCP 服务器。让 AI 编程助手（如 Kilo）能与运行中的 SillyTavern 交互——创建角色卡、运行体检、读取控制台日志。

基于 [fastmcp](https://github.com/jlowin/fastmcp) + [uv](https://docs.astral.sh/uv/) 构建。

### 工具列表

| 工具 | 功能 |
|------|------|
| `write_character_card` | 从名称、人格、首条消息等文本属性创建角色卡，生成 V2/V3 PNG 文件 |
| `import_character_card` | 导入已有的角色卡 PNG 文件，原样复制不改元数据 |
| `get_st_diagnostics` | 对运行中的 ST 做全面体检——API 状态、角色卡完整性、聊天文件、配置、插件 |
| `get_st_console` | 读取 ST 的控制台日志（需要 st-console-logger 插件） |
| `setup_st_logging` | 一键将控制台日志插件安装到 ST 的 plugins 目录 |

### 工作原理

```
Kilo (AI助手) ←→ sillytavern-mcp (本项目) ←→ SillyTavern (你的ST)
                        │
                        ├── 写入角色卡 PNG 到 data/.../characters/
                        ├── 通过 HTTP API 读取 ST 状态
                        └── 通过 st_console.log 读取控制台输出（插件）
```

### 安装教程

**第一步：安装 Python 3.11+**

https://www.python.org/downloads/

> Windows 安装时请勾选 **"Add Python to PATH"**（添加到环境变量）。

**第二步：安装 uv（Python 包管理器）**

打开终端（cmd.exe 或 PowerShell），运行：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安装完成后**重启终端**。

**第三步：获取项目**

```bash
git clone <仓库地址> sillytavern-mcp
cd sillytavern-mcp
```

或者从 GitHub 下载 ZIP 解压。

**第四步：安装依赖**

```bash
uv sync
```

这会自动创建虚拟环境并安装所有依赖包。

**第五步：配置到 Kilo**

将以下内容添加到你的 `kilo.json`（全局路径 `C:\Users\<用户名>\.config\kilo\kilo.json`，或项目目录下的）：

```json
{
  "sillytavern-mcp": {
    "type": "local",
    "command": ["uv", "run", "--directory", "C:\\path\\to\\sillytavern-mcp", "python", "-m", "sillytavern_mcp"],
    "environment": {
      "SILLYTAVERN_DATA_DIR": "C:\\path\\to\\SillyTavern\\data",
      "SILLYTAVERN_USER": "default-user",
      "SILLYTAVERN_URL": "http://localhost:8000"
    },
    "enabled": true
  }
}
```

把路径换成你实际的 SillyTavern 安装位置。

**第六步：验证是否成功**

在 Kilo 中对 AI 助手说：**"检查 ST 的状态"**

助手会调用 `get_st_diagnostics` 工具并返回体检结果。

### 可选：启用控制台日志

如果你想让 AI 助手能读取 ST 的控制台输出（错误信息、模型加载等），只需：

1. 对 AI 助手说：**"帮我安装日志插件"**
2. 助手会调用 `setup_st_logging`，自动完成：
   - 将插件复制到 ST 的 `plugins/` 目录
   - 在 `config.yaml` 中启用服务器插件
3. **重启 SillyTavern**（关闭再打开）
4. 重启后对助手说：**"看看 ST 的控制台输出"**

全程不需要手动操作终端——助手会帮你做完。

### 配置说明

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `SILLYTAVERN_DATA_DIR` | 自动检测 | ST 的 `data/` 目录路径 |
| `SILLYTAVERN_USER` | `default-user` | ST 用户名 |
| `SILLYTAVERN_URL` | `http://localhost:8000` | ST 的 HTTP API 地址 |

---

## License

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0), the same license as SillyTavern.

See the [LICENSE](LICENSE) file for details.
