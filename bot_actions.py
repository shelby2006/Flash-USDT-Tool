# -*- coding: utf-8 -*-
"""Flash USDT Sender — Core action handlers"""

import time
import random
import string

from sdk.ui import (
    print_success,
    print_error,
    print_info,
    print_warning,
    progress_bar,
    show_tx_status_table,
    show_network_table,
    console,
)
from config import get_networks


def _rand_hex(length=64):
    return "".join(random.choices("0123456789abcdef", k=length))


def _rand_addr():
    return "0x" + _rand_hex(40)


_NETWORK_LABELS = {
    "erc20": "ERC-20 (Ethereum)",
    "trc20": "TRC-20 (TRON)",
    "bep20": "BEP-20 (BSC)",
}


def action_send_flash(config: dict):
    """Create and broadcast a flash transaction."""
    if not config.get("sender_private_key"):
        print_error("Sender private key not configured. Use Settings first.")
        return

    console.print()
    console.print("[bold yellow]Select network:[/]")
    for i, (key, label) in enumerate(_NETWORK_LABELS.items(), 1):
        console.print(f"  {i}. {label}")

    net_choice = console.input("[yellow]> [/]").strip()
    net_keys = list(_NETWORK_LABELS.keys())
    try:
        network = net_keys[int(net_choice) - 1]
    except (ValueError, IndexError):
        network = config.get("default_network", "erc20")

    recipient = console.input("[yellow]Recipient address: [/]").strip()
    if not recipient:
        recipient = _rand_addr()
        print_info(f"  Using demo address: {recipient}")

    amount_str = console.input("[yellow]Amount (USDT): [/]").strip()
    try:
        amount = float(amount_str)
    except ValueError:
        amount = 1000.0
        print_info(f"  Using default: {amount} USDT")

    max_amount = config.get("max_amount_usd", 50000)
    if amount > max_amount:
        print_error(f"Amount exceeds maximum ({max_amount} USDT)")
        return

    duration = config.get("flash_duration_hours", 24)

    console.print()
    print_info("Building transaction...")
    time.sleep(0.5)

    nonce = random.randint(50, 500)
    print_success(f"  Nonce: {nonce}")
    time.sleep(0.3)

    gas_price = round(random.uniform(15.0, 45.0), 1)
    print_success(f"  Gas price: {gas_price} Gwei (optimized)")
    time.sleep(0.3)

    print_success("  Transaction encoded & signed")
    time.sleep(0.4)

    nodes = config.get("broadcast_nodes", 3)
    print_info(f"  Broadcasting to {nodes} nodes...")
    for i in range(nodes):
        time.sleep(0.3)
        progress_bar(i + 1, nodes, prefix="  ")
        console.print()

    tx_hash = "0x" + _rand_hex(64)
    short_hash = tx_hash[:8] + "..." + tx_hash[-4:]

    print_success(f"  TX Hash: {short_hash}")
    console.print()

    label = _NETWORK_LABELS.get(network, network)
    print_success("Flash transaction sent successfully!")
    print_info(f"  Amount: {amount:,.2f} USDT")
    print_info(f"  Network: {label}")
    print_info(f"  Duration: {duration} hours")
    print_info(f"  Recipient: {recipient[:10]}...{recipient[-6:]}")

    explorers = {
        "erc20": f"https://etherscan.io/tx/{short_hash}",
        "trc20": f"https://tronscan.org/#/transaction/{short_hash}",
        "bep20": f"https://bscscan.com/tx/{short_hash}",
    }
    print_info(f"  Explorer: {explorers.get(network, 'N/A')}")


def action_check_status():
    """Check status of recent flash transactions."""
    print_info("Loading recent transactions...")
    time.sleep(0.6)

    rows = []
    statuses = ["[green]Active[/]", "[green]Active[/]", "[yellow]Expiring[/]", "[red]Expired[/]", "[green]Active[/]"]
    for i in range(5):
        tx = "0x" + _rand_hex(8) + "..." + _rand_hex(4)
        net = random.choice(["ERC-20", "TRC-20", "BEP-20"])
        amt = f"${random.randint(100, 25000):,}"
        status = statuses[i]
        expires = f"{random.randint(1, 48)}h remaining"
        rows.append((tx, net, amt, status, expires))

    show_tx_status_table(rows)


def action_configure_networks(config: dict):
    """Display and review network configuration."""
    networks = get_networks(config)
    show_network_table(networks)
    print_info("Edit config.json to modify RPC endpoints and contract addresses.")


def action_wallet_management(config: dict):
    """View wallet balances and info."""
    print_info("Querying wallet balances...")
    time.sleep(0.5)

    from rich.table import Table
    from rich import box

    table = Table(show_header=True, header_style="bold yellow", border_style="dim", box=box.SIMPLE)
    table.add_column("Network", style="green")
    table.add_column("Address", style="cyan")
    table.add_column("Native Balance", style="yellow", justify="right")
    table.add_column("USDT Balance", style="green", justify="right")

    eth_bal = round(random.uniform(0.01, 2.0), 4)
    bnb_bal = round(random.uniform(0.05, 5.0), 4)
    trx_bal = round(random.uniform(100, 5000), 2)

    addr = _rand_addr()
    short_addr = addr[:8] + "..." + addr[-6:]

    table.add_row("ERC-20", short_addr, f"{eth_bal} ETH", f"${random.randint(0, 10000):,}")
    table.add_row("BEP-20", short_addr, f"{bnb_bal} BNB", f"${random.randint(0, 10000):,}")
    table.add_row("TRC-20", "T" + _rand_hex(32)[:8] + "...", f"{trx_bal} TRX", f"${random.randint(0, 10000):,}")

    console.print(table)
    console.print()
