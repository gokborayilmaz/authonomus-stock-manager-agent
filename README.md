# Autonomous Stock Agent (Build in Public Twitter Series Day -5-)

An autonomous stock portfolio agent built with [Upsonic](https://github.com/Upsonic/Upsonic). It tracks your stocks, runs analysis, and manages a live dashboard, all through Telegram conversations on your phone.

https://github.com/user-attachments/assets/55f04c5d-a0a4-4538-a42d-9e64495a0bbc

## What This Is

A fully autonomous agent that:

- **Manages your portfolio** through natural conversation on Telegram
- **Runs stock/ETF analysis** using real-time Yahoo Finance data
- **Updates a Streamlit dashboard** automatically based on your conversations
- **Remembers context** between sessions using workspace memory
- **Tracks a watchlist** of stocks you're interested in but haven't bought yet

The agent's behavior is defined entirely in markdown files (skills, personality, instructions). No hardcoded logic for what it does or how it responds.

## Stack

| Component | Tool |
|-----------|------|
| Agent Framework | [Upsonic](https://github.com/Upsonic/Upsonic) AutonomousAgent |
| LLM | Claude Sonnet 4.6 |
| Financial Data | Yahoo Finance (via Upsonic YFinanceTools) |
| Chat Interface | Telegram Bot API |
| Dashboard | Streamlit + Plotly |
| Observability | PromptLayer (optional) |

## How It Works

```
You (Telegram) --> Agent reads skills & memory --> Calls YFinance tools --> Writes to workspace/data/ --> Dashboard reads & displays
```

The agent lives in a sandboxed `workspace/` directory. Everything it knows and does is driven by markdown files:

```
workspace/
├── AGENTS.md                          # What to do on startup, available skills
├── SOUL.md                            # Agent personality and boundaries
├── skills/
│   ├── stock_analysis/SKILL.md        # How to analyze stocks vs ETFs
│   └── portfolio_management/SKILL.md  # How to manage portfolio and watchlist
├── data/                              # Agent-managed, dashboard reads from here
│   ├── portfolio.json
│   ├── watchlist.json
│   └── analysis/*.json
└── memory/                            # Session logs, long-term memory
```

When you say "I bought 5 shares of AAPL at $200" on Telegram, the agent:
1. Reads the `portfolio_management` skill
2. Fetches live price from Yahoo Finance
3. Writes updated data to `portfolio.json`
4. Confirms the action back to you

The dashboard picks it up on the next page load.

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Anthropic API key
- Telegram bot token (create one via [@BotFather](https://t.me/BotFather))

### Install

```bash
git clone https://github.com/IremOztimur/autonomous-stock-agent.git
cd autonomous-stock-agent
make setup
source .venv/bin/activate
```

### Configure

Fill in your `.env` (created by `make setup`):

```
ANTHROPIC_API_KEY=sk-ant-...
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook
```

For local development, you can use [ngrok](https://ngrok.com/) to expose a webhook URL:

```bash
ngrok http 8000
```

Then set `TELEGRAM_WEBHOOK_URL` to the ngrok HTTPS URL.

### Run

```bash
make all        # starts both agent and dashboard
```

Or run them separately:

```bash
make run        # start the telegram bot
make dashboard  # start the streamlit dashboard
```

### Available Commands

| Command | Description |
|---------|-------------|
| `make setup` | Create venv, install dependencies, copy .env |
| `make run` | Start the Telegram bot |
| `make dashboard` | Start the Streamlit dashboard |
| `make all` | Run both in parallel |
| `make clean` | Remove venv, cache, and agent data |

## Dashboard

The dashboard is read-only. You don't manage it directly. The agent writes data files during your Telegram conversations, and the dashboard renders them.

Features:
- Portfolio overview with gain/loss per position
- Allocation pie chart and gain/loss bar chart
- Watchlist tab for tracked stocks
- Analysis reports tab with full markdown reports
- Dark/light mode toggle
- Commission and purchase date tracking

## Customization

Everything the agent does is controlled by markdown files in `workspace/`. You can:

- Edit `SOUL.md` to change the agent's personality
- Edit `skills/*/SKILL.md` to change how it analyzes or manages data
- Add new skills by creating a new folder under `skills/` with a `SKILL.md`
- Edit `AGENTS.md` to register new skills or change startup behavior

No code changes needed.

## Example Telegram Commands

These are natural language, not slash commands. Just talk to it:

- "I bought 10 shares of AAPL at $195, commission was $1.50"
- "Track TSLA for me, I'm waiting for a rise"
- "Analyze my portfolio"
- "Run a full analysis on COPX"
- "Remove AMZN from my watchlist"
- "Update all prices"
- `/reset` to clear conversation history
