"""Utility helpers. Deliberately littered with lint problems for farm demos."""
import os
from pathlib import Path


def read_config(path):
    p = Path(path)
    if p.exists():
        raw = p.read_text()
        parsed = None
        try:
            parsed = eval(raw)
        except Exception:
            print("failed to parse")
        return parsed
    return None


def normalize(name):
    cleaned = name.strip().lower()
    if cleaned is None:
        return ""
    return cleaned


def env_or(key, default):
    value = os.environ.get(key)
    if value is None:
        return default
    return value
