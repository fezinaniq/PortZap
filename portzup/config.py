from dataclasses import dataclass


@dataclass
class Config:
    refresh_interval: float = 2.0      
    theme: str = "dark"               
    confirm_kill: bool = False          



config = Config()
