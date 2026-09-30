# -*- coding: utf-8 -*-
"""Flash USDT Sender — Rich terminal UI"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich import box

console = Console(force_terminal=True, color_system="auto")

LOGO = r"""███████╗██╗      █████╗ ███████╗██╗  ██╗
██╔════╝██║     ██╔══██╗██╔════╝██║  ██║
█████╗  ██║     ███████║███████╗███████║
██╔══╝  ██║     ██╔══██║╚════██║██╔══██║
██║     ███████╗██║  ██║███████║██║  ██║
╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
██╗   ██╗███████╗██████╗ ████████╗
██║   ██║██╔════╝██╔══██╗╚══██╔══╝
██║   ██║███████╗██║  ██║   ██║
██║   ██║╚════██║██║  ██║   ██║
╚██████╔╝███████║██████╔╝   ██║
 ╚═════╝ ╚══════╝╚═════╝    ╚═╝"""


def print_banner():
    """Print main banner."""
    panel = Panel(
        Text.from_markup(
            f"[bold yellow]{LOGO}[/]\n\n"
            "[bold white]M U L T I - N E T W O R K   F L A S H   T O O L[/]\n"
            "[dim]ERC-20  |  TRC-20  |  BEP-20  |  BTC  |  ETH  |  Block Explorer Visible[/]"
        ),
        box=box.ROUNDED,
        border_style="yellow",
        padding=(0, 2),
        title="[bold white on yellow] FLASH USDT SENDER [/]",
        title_align="center",
    )
    console.print(panel)


def show_menu_table(menu_items: list) -> str:
    """Display menu."""
    console.print()
    console.print(Rule("[bold yellow]MENU[/]", style="yellow"))
    table = Table(
        show_header=True,
        header_style="bold yellow",
        border_style="dim",
        box=box.SIMPLE,
        expand=True,
    )
    table.add_column("[#]", style="bold", justify="center", width=4)
    table.add_column("Action", style="green")
    table.add_column("Description", style="dim")

    for key, action, desc in menu_items:
        table.add_row(key, action, desc)

    console.print(table)
    return console.input("\n[bold yellow]Select action [#]: [/]").strip()


def show_load_status_table(config: dict):
    """Display load status."""
    console.print()
    console.print(Rule("[bold yellow]STATUS[/]", style="yellow"))
    table = Table(
        show_header=True,
        header_style="bold yellow",
        border_style="dim",
        box=box.SIMPLE,
    )
    table.add_column("Parameter", style="green")
    table.add_column("Value", justify="center")
    table.add_column("Status", justify="center", style="bold")

    has_key = bool(config.get("sender_private_key", ""))
    network = config.get("default_network", "erc20")
    duration = config.get("flash_duration_hours", 24)

    table.add_row("Sender Wallet", "Configured" if has_key else "Not set", "[green]OK[/]" if has_key else "[red]MISSING[/]")
    table.add_row("Default Network", network.upper(), "[green]OK[/]")
    table.add_row("Flash Duration", f"{duration}h", "[green]OK[/]")
    table.add_row("Max Amount", f"${config.get('max_amount_usd', 50000):,}", "[green]OK[/]")

    console.print(table)
    console.print()


def show_tx_status_table(rows: list):
    """Display transaction status."""
    console.print()
    console.print(Rule("[bold yellow]TRANSACTION STATUS[/]", style="yellow"))
    table = Table(show_header=True, header_style="bold yellow", border_style="dim", box=box.SIMPLE)
    table.add_column("TX Hash", style="cyan")
    table.add_column("Network", style="green")
    table.add_column("Amount", style="yellow", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Expires", style="dim")

    for row in rows:
        table.add_row(*row)

    console.print(table)
    console.print()


def show_network_table(networks: dict):
    """Display network configuration."""
    console.print()
    console.print(Rule("[bold yellow]NETWORKS[/]", style="yellow"))
    table = Table(show_header=True, header_style="bold yellow", border_style="dim", box=box.SIMPLE)
    table.add_column("Network", style="green")
    table.add_column("RPC/API", style="cyan")
    table.add_column("Contract", style="dim")
    table.add_column("Status", justify="center")

    for name, cfg in networks.items():
        rpc = cfg.get("rpc_url", cfg.get("api_url", "N/A"))
        contract = cfg.get("usdt_contract", "N/A")
        table.add_row(name.upper(), rpc[:35] + "..." if len(rpc) > 35 else rpc, contract[:12] + "...", "[green]Ready[/]")

    console.print(table)
    console.print()


def print_success(msg: str):
    console.print(f"[green]✓[/] {msg}")


def print_error(msg: str):
    console.print(f"[red]✗[/] {msg}")


def print_info(msg: str):
    console.print(f"[cyan]i[/] {msg}")


def print_warning(msg: str):
    console.print(f"[yellow]![/] {msg}")


def separator(char: str = "─", length: int = 58):
    console.print(Rule(style="dim"))


def progress_bar(current: int, total: int, width: int = 30, prefix: str = ""):
    filled = int(width * current / total) if total > 0 else 0
    pct = (current / total * 100) if total > 0 else 0
    bar = "█" * filled + "░" * (width - filled)
    console.print(f"\r{prefix}[yellow]{bar}[/] [dim]{pct:.0f}%[/]", end="")
