from pathlib import Path

def find_root(marker: str = "pyproject.toml") -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(f"Project root not found (marker: {marker})")

PROJECT_ROOT = find_root()
