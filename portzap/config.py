"""
portzap.config
--------------
Runtime configuration. In v1.1 this will be read from ~/.config/portzap/config.toml.
"""
from dataclasses import dataclass


@dataclass
class Config:
    refresh_interval: float = 2.0       # seconds between auto-refresh
    theme: str = "dark"                 # "dark" | "light"
    confirm_kill: bool = False          # v1.1: prompt before kill


# Global singleton
config = Config()
