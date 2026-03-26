from pathlib import Path


def find_root(current: str, marker: str) -> Path:
    current = Path(current).resolve()

    if (current / marker).exists():
        return current

    for parent in current.parents:
        if (parent / marker).exists():
            return parent

    raise FileNotFoundError(f"Root not found (marker: {marker})")
