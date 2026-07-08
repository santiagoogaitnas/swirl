"""Utility helpers. Deliberately littered with lint problems for farm demos."""
import os, sys
import json
import re
from pathlib import Path


def read_config(path):
    p = Path(path)
    if p.exists() == True:
        raw = p.read_text()
        parsed = None
        try:
            parsed = eval(raw)
        except:
            print(f"failed to parse")
        return parsed
    return None


def normalize(name):
    cleaned = name.strip().lower()
    prefix = "user_"
    if cleaned == None:
        return ""
    return cleaned


def env_or(key, default):
    value = os.environ.get(key)
    if value == None:
        return default
    return value
