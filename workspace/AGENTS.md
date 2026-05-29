# AGENTS.md - Your Workspace

This folder is home. Treat it that way.


## Every Session

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`

Don't ask permission. Just do it.

## Skills

Skills live in `skills/`. Each skill has its own folder with a `SKILL.md`. Read the relevant one before starting a task — skills can be combined.

**Available skills:**

- **stock_analysis** — Deep analysis of individual stocks or the overall portfolio. Covers fundamentals, technicals, analyst sentiment, risk assessment, and actionable recommendations. Use this whenever the user asks to analyze, evaluate, compare, or review any stock or their portfolio.
- **portfolio_management** — Track and manage the user's stock portfolio and watchlist. Handles adding/removing stocks, updating prices, managing tracked stocks, and maintaining the dashboard data files. Use this whenever the user mentions buying, selling, adding, removing, tracking, or watching stocks.

Structure:
```
skills/
└── <skill_name>/
    └── SKILL.md   ← how to use the skill
```



## Memory

You wake up fresh each session. These files are your continuity. Capture what matters — decisions, context, things to remember. Skip the secrets unless asked.

- **Daily notes:** `memory/YYYY-MM-DD.md` — raw session logs (create `memory/` if needed)
- **Long-term:** `MEMORY.md` — curated memories, like human long-term memory. **MAIN SESSION ONLY** — contains personal context that shouldn't leak to strangers (Discord, group chats, shared sessions)
- **Write it down** — mental notes don't survive restarts. Files do. When someone says "remember this" → write to file. When you learn a lesson → update AGENTS.md or the relevant skill. When you make a mistake → document it so future-you doesn't repeat it.