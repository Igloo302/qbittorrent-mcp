# qbittorrent-mcp

MCP Compatible

一个基于 Model Context Protocol (MCP) 的 QBittorrent 远程管理工具，专为自动化脚本、AI 助手、机器人集成或自定义管理工具开发而设计。通过 MCP 协议与 QBittorrent WebUI API 对接，实现种子任务的远程管理与自动化操作。

## 设计理念

qbittorrent-mcp 旨在让 AI 或自动化系统能够以极简、标准化的方式远程控制 QBittorrent，实现批量种子管理、自动化下载、智能监控等场景。通过抽象出高层 API，屏蔽底层 WebUI 细节，让开发者专注于业务逻辑。

核心优势：
- **MCP 标准协议**：与主流 AI/自动化平台无缝集成
- **极简接口**：一行代码即可完成连接与操作
- **异步支持**：高并发、低延迟，适合大规模自动化
- **安全隔离**：无需暴露 QBittorrent 账号密码给第三方

## 功能特点

- 连接 QBittorrent WebUI（支持鉴权）
- 获取全部种子列表及详细信息
- 暂停/恢复指定种子
- 删除种子（可选是否删除文件）
- 添加磁力链接任务
- 适用于自动化脚本、AI 助手、机器人等多种场景

## 安装方法

### 方法一：PyPI 安装

```bash
pip install qbittorrent-mcp
```

### 方法二：uv 安装

```bash
uv pip install qbittorrent-mcp
```

### 方法三：配置 Claude Desktop

在 Claude Desktop 配置文件中添加服务器配置：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

添加如下配置：
```json
{
  "mcpServers": {
    "qbittorrent": {
      "command": "uvx",
      "args": [
        "qbittorrent-mcp"
      ]
    }
  }
}
```

### 方法四：从源码安装并配置 Cursor 本地开发环境

在 Cursor IDE 中，可以通过本地配置文件来设置 MCP 服务器：
- Windows: `C:\Users\用户名\.cursor\mcp.json`
- macOS: `~/.cursor/mcp.json`

添加如下配置：
```json
{
  "mcpServers": {
    "qbittorrent": {
      "command": "uv",
      "args": [
        "--directory",
        "/你的本地项目路径/qbittorrent-mcp/",
        "run",
        "qbittorrent-mcp.py"
      ]
    }
  }
}
```

这种配置方式适合本地开发和测试使用，可以直接指向本地代码目录。

### 方法二：源码安装

```bash
git clone https://github.com/yourname/qbittorrent-mcp.git
cd qbittorrent-mcp
pip install .
```

## 快速上手

```python
from qbittorrent_mcp import connect, list_torrents, pause_torrent, resume_torrent, delete_torrent, add_magnet

# 连接 QBittorrent WebUI
await connect(host="127.0.0.1", port=8080, username="admin", password="adminadmin")

# 获取种子列表
print(await list_torrents())

# 暂停种子
torrent_hash = "your_torrent_hash"
await pause_torrent(torrent_hash)

# 恢复种子
await resume_torrent(torrent_hash)

# 删除种子
await delete_torrent(torrent_hash, delete_files=False)

# 添加磁力链接
await add_magnet("magnet:?xt=urn:btih:...")
```

## 典型场景

- **AI 助手自动管理下载任务**：结合大模型，实现智能下载、自动暂停/恢复、异常监控等
- **机器人批量任务处理**：批量添加、暂停、删除种子，适合 Telegram/QQ/微信机器人集成
- **自定义 Web/CLI 工具**：快速开发自己的种子管理前端或命令行工具

## API 说明

### 1. 连接 QBittorrent WebUI
```python
await connect(host: str, port: int, username: str, password: str) -> str
```
连接 QBittorrent WebUI，成功返回提示信息。

### 2. 获取种子列表
```python
await list_torrents() -> str
```
返回所有种子的详细信息（名称、哈希、状态、进度、速度等）。

### 3. 暂停种子
```python
await pause_torrent(torrent_hash: str) -> str
```
暂停指定哈希的种子。

### 4. 恢复种子
```python
await resume_torrent(torrent_hash: str) -> str
```
恢复指定哈希的种子。

### 5. 删除种子
```python
await delete_torrent(torrent_hash: str, delete_files: bool = False) -> str
```
删除指定哈希的种子，可选是否同时删除已下载文件。

### 6. 添加磁力链接
```python
await add_magnet(magnet_url: str) -> str
```
添加新的磁力链接任务。

## 最佳实践

- **连接前请确保 QBittorrent WebUI 已开启并允许 API 访问**
- **所有操作均为异步，建议在 async 环境下调用**
- **建议将账号密码配置在安全环境变量中，避免泄露**

## 常见问题解答

**Q: 连接失败怎么办？**
A: 请检查 QBittorrent WebUI 是否开启、端口/用户名/密码是否正确，或是否有防火墙阻挡。

**Q: 如何获取种子的哈希值？**
A: 调用 `list_torrents()`，返回信息中包含每个种子的哈希值。

**Q: 支持批量操作吗？**
A: 当前接口为单种子操作，如需批量可自行循环调用。

## 依赖说明

- Python >= 3.7
- httpx
- mcp

## 许可证

MIT License
