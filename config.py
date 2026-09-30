# -*- coding: utf-8 -*-
"""Configuration loader for Flash USDT Sender — config.json"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

_DEFAULTS = {
    "sender_private_key": "",
    "default_network": "erc20",
    "networks": {
        "erc20": {
            "rpc_url": "https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY",
            "chain_id": 1,
            "usdt_contract": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        },
        "trc20": {
            "api_url": "https://api.trongrid.io",
            "usdt_contract": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
        },
        "bep20": {
            "rpc_url": "https://bsc-dataseed1.binance.org",
            "chain_id": 56,
            "usdt_contract": "0x55d398326f99059fF775485246999027B3197955",
        },
    },
    "flash_duration_hours": 24,
    "max_amount_usd": 50000,
    "gas_multiplier": 1.2,
    "broadcast_nodes": 3,
    "retry_count": 2,
}


def load_config() -> dict:
    """Load configuration from config.json."""
    config_path = BASE_DIR / "config.json"
    if not config_path.exists():
        save_config(_DEFAULTS)
        return dict(_DEFAULTS)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        merged = dict(_DEFAULTS)
        merged.update(data)
        return merged
    except (json.JSONDecodeError, IOError):
        return dict(_DEFAULTS)


def save_config(config: dict):
    """Save configuration to config.json."""
    config_path = BASE_DIR / "config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def get_networks(config: dict) -> dict:
    """Return networks dict."""
    return config.get("networks", {})
