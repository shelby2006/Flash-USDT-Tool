# -*- coding: utf-8 -*-
"""Settings action — Configuration reference for Flash USDT Sender"""

from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from rich import box

from sdk.ui import console


def action_settings():
    """Display configuration reference."""
    console.print()
    console.print(Rule("[bold yellow]SETTINGS[/]", style="yellow"))

    table = Table(show_header=True, header_style="bold yellow", border_style="dim", box=box.SIMPLE)
    table.add_column("Parameter", style="green")
    table.add_column("Type", style="dim")
    table.add_column("Default", style="yellow")
    table.add_column("Description", style="dim")

    table.add_row("sender_private_key", "string", '""', "Sender wallet private key")
    table.add_row("default_network", "string", '"erc20"', "erc20 / trc20 / bep20")
    table.add_row("flash_duration_hours", "int", "24", "TX visible duration (1-72)")
    table.add_row("max_amount_usd", "int", "50000", "Max USDT per transaction")
    table.add_row("gas_multiplier", "float", "1.2", "Gas price multiplier")
    table.add_row("broadcast_nodes", "int", "3", "Number of RPC broadcast nodes")
    table.add_row("retry_count", "int", "2", "TX retry attempts on failure")

    panel = Panel(table, title="[bold] config.json Reference [/]", border_style="yellow", box=box.ROUNDED)
    console.print(panel)

    console.print()
    console.print("[dim]Edit config.json or use menu option 6 to view network details.[/]")
    console.print()
