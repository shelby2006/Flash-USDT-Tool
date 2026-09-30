# -*- coding: utf-8 -*-
"""About action — Features, supported networks, contact"""

from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from rich import box

from sdk.ui import console


def action_about():
    """Display project info."""
    console.print()
    console.print(Rule("[bold yellow]ABOUT[/]", style="yellow"))

    features_table = Table(show_header=True, header_style="bold yellow", border_style="dim", box=box.SIMPLE)
    features_table.add_column("Feature", style="green")
    features_table.add_column("Status", justify="center")

    for feat in [
        "Flash USDT (ERC-20)",
        "Flash USDT (TRC-20)",
        "Flash USDT (BEP-20)",
        "Flash BTC / ETH",
        "Configurable duration (1-72h)",
        "Block explorer visibility",
        "Multi-wallet sender",
        "Batch transactions",
        "Custom gas/energy settings",
        "Transaction status tracker",
        "Amount range: $1 - $50,000",
    ]:
        features_table.add_row(feat, "[green]✓[/]")

    networks_table = Table(show_header=True, header_style="bold yellow", border_style="dim", box=box.SIMPLE)
    networks_table.add_column("Network", style="green")
    networks_table.add_column("Token", style="cyan")
    networks_table.add_column("Gas", style="dim")
    networks_table.add_row("Ethereum", "USDT (ERC-20)", "ETH")
    networks_table.add_row("TRON", "USDT (TRC-20)", "TRX")
    networks_table.add_row("BSC", "USDT (BEP-20)", "BNB")
    networks_table.add_row("Polygon", "USDT (ERC-20)", "MATIC")
    networks_table.add_row("Arbitrum", "USDT (ERC-20)", "ETH")

    contact_table = Table(show_header=True, header_style="bold yellow", border_style="dim", box=box.SIMPLE)
    contact_table.add_column("Channel", style="green")
    contact_table.add_column("Value", style="yellow")
    contact_table.add_row("Telegram", "JOIN OUR TELEGRAM CHAT")
    contact_table.add_row("ETH Address", "0x1c7D4E8a93B62f05dA3e91C2F78b40d5A26cE917")
    contact_table.add_row("Support", "GitHub Issues or Telegram")

    console.print(Panel(features_table, title="[bold] Features [/]", border_style="yellow", box=box.ROUNDED))
    console.print()
    console.print(Panel(networks_table, title="[bold] Supported Networks [/]", border_style="yellow", box=box.ROUNDED))
    console.print()
    console.print(Panel(contact_table, title="[bold] Contact [/]", border_style="yellow", box=box.ROUNDED))
    console.print()
