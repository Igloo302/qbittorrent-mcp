from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import httpx
from mcp.server.fastmcp import FastMCP
import os
import sys

# Initialize FastMCP server
mcp = FastMCP("qbittorrent")

@dataclass
class QBittorrentConfig:
    """QBittorrent WebUI connection configuration."""
    host: str
    port: int
    username: str
    password: str

class QBittorrentClient:
    """QBittorrent WebUI API client."""
    def __init__(self, config: QBittorrentConfig):
        self.base_url = f"http://{config.host}:{config.port}"
        self.auth = (config.username, config.password)
        self.session = httpx.AsyncClient()
        self._cookies = None

    async def _login(self) -> bool:
        """Login to QBittorrent WebUI."""
        try:
            response = await self.session.post(
                f"{self.base_url}/api/v2/auth/login",
                data={"username": self.auth[0], "password": self.auth[1]}
            )
            response.raise_for_status()
            self._cookies = response.cookies
            return True
        except Exception:
            return False

    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Any]:
        """Make an authenticated request to QBittorrent WebUI API."""
        if not self._cookies:
            if not await self._login():
                return None

        try:
            response = await self.session.request(
                method,
                f"{self.base_url}/api/v2/{endpoint}",
                cookies=self._cookies,
                **kwargs
            )
            response.raise_for_status()
            return response.json() if response.content else None
        except Exception:
            return None

    async def get_torrents(self) -> List[Dict[str, Any]]:
        """Get list of torrents."""
        result = await self._request("GET", "torrents/info")
        return result or []

    async def pause_torrents(self, hashes: List[str]) -> bool:
        """Pause torrents by their hashes."""
        result = await self._request(
            "POST", 
            "torrents/pause",
            data={"hashes": "|".join(hashes)}
        )
        return result is not None

    async def resume_torrents(self, hashes: List[str]) -> bool:
        """Resume torrents by their hashes."""
        result = await self._request(
            "POST", 
            "torrents/resume",
            data={"hashes": "|".join(hashes)}
        )
        return result is not None

    async def delete_torrents(self, hashes: List[str], delete_files: bool = False) -> bool:
        """Delete torrents by their hashes."""
        result = await self._request(
            "POST",
            "torrents/delete",
            data={
                "hashes": "|".join(hashes),
                "deleteFiles": str(delete_files).lower()
            }
        )
        return result is not None

    async def add_torrent(self, magnet_url: str) -> bool:
        """Add a new torrent from magnet link."""
        result = await self._request(
            "POST",
            "torrents/add",
            data={"urls": magnet_url}
        )
        return result is not None

# Utility to get parameter from env or command line

def get_param_value(param_name: str, default=None):
    # Check command line arguments
    for arg in sys.argv[1:]:
        if arg.startswith(f"--{param_name}="):
            return arg.split("=", 1)[1]
    # Check environment variables
    env_name = param_name.upper()
    return os.environ.get(env_name, default)

# Example: get QBittorrent config from params
def get_qbittorrent_config_from_params():
    host = get_param_value("host", "localhost")
    port = int(get_param_value("port", 8080))
    username = get_param_value("username", "admin")
    password = get_param_value("password", "adminadmin")
    return QBittorrentConfig(host, port, username, password)

# Global client instance
_client: Optional[QBittorrentClient] = None

@mcp.tool()
async def connect(host: str = None, port: int = None, username: str = None, password: str = None) -> str:
    """Connect to QBittorrent WebUI.

    Args:
        host: QBittorrent WebUI host
        port: QBittorrent WebUI port
        username: WebUI username
        password: WebUI password
    """
    global _client
    # Use provided params, or fallback to global params
    config = QBittorrentConfig(
        host or get_param_value("host", "localhost"),
        int(port or get_param_value("port", 8080)),
        username or get_param_value("username", "admin"),
        password or get_param_value("password", "adminadmin")
    )
    _client = QBittorrentClient(config)
    if await _client._login():
        return "Successfully connected to QBittorrent WebUI"
    return "Failed to connect to QBittorrent WebUI"

@mcp.tool()
async def list_torrents() -> str:
    """Get list of all torrents and their download information."""
    if not _client:
        return "Not connected to QBittorrent. Use connect() first."

    torrents = await _client.get_torrents()
    if not torrents:
        return "No torrents found or failed to fetch torrents."

    result = []
    for t in torrents:
        status = f"""
名称: {t.get('name', 'Unknown')}
哈希值: {t.get('hash', 'Unknown')}
状态: {t.get('state', 'Unknown')}
进度: {t.get('progress', 0) * 100:.1f}%
大小: {t.get('size', 0) / (1024*1024*1024):.2f} GB
下载速度: {t.get('dlspeed', 0) / (1024*1024):.1f} MB/s
上传速度: {t.get('upspeed', 0) / (1024*1024):.1f} MB/s"""
        result.append(status)

    return "\n---\n".join(result)

@mcp.tool()
async def pause_torrent(torrent_hash: str) -> str:
    """Pause a torrent by its hash.

    Args:
        torrent_hash: Hash of the torrent to pause
    """
    if not _client:
        return "Not connected to QBittorrent. Use connect() first."

    if await _client.pause_torrents([torrent_hash]):
        return "Successfully paused torrent"
    return "Failed to pause torrent"

@mcp.tool()
async def resume_torrent(torrent_hash: str) -> str:
    """Resume a paused torrent by its hash.

    Args:
        torrent_hash: Hash of the torrent to resume
    """
    if not _client:
        return "Not connected to QBittorrent. Use connect() first."

    if await _client.resume_torrents([torrent_hash]):
        return "Successfully resumed torrent"
    return "Failed to resume torrent"

@mcp.tool()
async def delete_torrent(torrent_hash: str, delete_files: bool = False) -> str:
    """Delete a torrent by its hash.

    Args:
        torrent_hash: Hash of the torrent to delete
        delete_files: Whether to delete downloaded files
    """
    if not _client:
        return "Not connected to QBittorrent. Use connect() first."

    if await _client.delete_torrents([torrent_hash], delete_files):
        return "Successfully deleted torrent"
    return "Failed to delete torrent"

@mcp.tool()
async def add_magnet(magnet_url: str) -> str:
    """Add a new torrent from magnet link.

    Args:
        magnet_url: Magnet URL of the torrent
    """
    if not _client:
        return "Not connected to QBittorrent. Use connect() first."

    if await _client.add_torrent(magnet_url):
        return "Successfully added torrent"
    return "Failed to add torrent"

if __name__ == "__main__":
    mode = get_param_value("mode", "stdio")
    if mode == "rest":
        try:
            from mcp.server.restmcp import RestMCP
        except ImportError:
            print("RestMCP transport is not available. Please ensure mcp.server.restmcp is installed.")
            sys.exit(1)
        mcp_rest = RestMCP("qbittorrent", port=int(get_param_value("rest_port", 8081)), endpoint=get_param_value("endpoint", "/"))
        mcp_rest.run()
    else:
        mcp.run(transport='stdio')