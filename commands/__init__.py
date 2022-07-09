"""
定数など
"""

from pathlib import Path

THIS_MODULE = Path(__file__).parent
CONFIG_FILE = THIS_MODULE.parent / "config.json"
LOGIN_URL = "https://atcoder.jp/login?continue="
