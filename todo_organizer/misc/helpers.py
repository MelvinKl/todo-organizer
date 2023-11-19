from functools import lru_cache
from pathlib import Path


@lru_cache
def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.resolve()
