# QBittorrent MCP

## 概述

本项目提供了一个通过MCP协议与QBittorrent WebUI进行交互的Python客户端，可以方便地管理QBittorrent中的种子。

## 安装

1. 确保Python版本 >= 3.7
2. 克隆本仓库
3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

在`qbittorrent-mcp.py`中配置QBittorrent WebUI连接信息：
- 主机地址
- 端口号
- 用户名
- 密码

## 功能

- 连接QBittorrent WebUI
- 获取种子列表
- 暂停/恢复种子
- 删除种子
- 添加磁力链接

## 使用

```python
# 连接QBittorrent
await connect(host, port, username, password)

# 获取种子列表
torrents = await list_torrents()

# 暂停种子
await pause_torrent(torrent_hash)

# 恢复种子
await resume_torrent(torrent_hash)

# 删除种子
await delete_torrent(torrent_hash)

# 添加磁力链接
await add_magnet(magnet_url)
```

## 依赖

- httpx
- mcp

## 许可证

MIT License