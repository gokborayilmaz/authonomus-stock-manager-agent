"""
Stock Agent — Autonomous Portfolio Manager

An autonomous agent that tracks stocks, analyzes portfolios, and provides
investment insights via Telegram. Dashboard is agent-managed through conversation.
"""

import os
from dotenv import load_dotenv
from upsonic import AutonomousAgent, Task
from upsonic.tools.common_tools.financial_tools import YFinanceTools
from upsonic.interfaces import InterfaceManager, TelegramInterface, InterfaceMode
# from upsonic.integrations.promptlayer import PromptLayer

load_dotenv()

finance_tools = YFinanceTools()
finance_tools._enable_all_tools()

# pl = PromptLayer()

agent = AutonomousAgent(
    model="anthropic/claude-sonnet-4-6",
    workspace=os.path.join(os.path.dirname(__file__), "workspace"),
    tools=finance_tools.functions(),
    # promptlayer=pl,
    print=True
)

telegram = TelegramInterface(
    agent=agent,
    bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
    webhook_url=os.getenv("TELEGRAM_WEBHOOK_URL"),
    mode=InterfaceMode.CHAT,
    reset_command="/reset",
    parse_mode="Markdown",
)

manager = InterfaceManager(interfaces=[telegram])

if __name__ == "__main__":
    manager.serve(host="0.0.0.0", port=8000)
    # pl.shutdown()