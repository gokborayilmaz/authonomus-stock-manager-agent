# Skill: Stock Analysis

Perform comprehensive analysis using YFinance data and write results to the dashboard.

---

## Task

**Goal:** Analyze individual stocks or the full portfolio, produce actionable insights, and save a structured report to `data/analysis/`.

### Steps

1. **Identify Security Type** — First call `get_company_info(symbol)` to determine if this is a **stock** or an **ETF/fund**.
   - If `quoteType` is `"ETF"` or the name contains "ETF" or "Fund" → treat as ETF.
   - If `quoteType` is `"EQUITY"` → treat as stock.

2. **Gather Data** — Call the appropriate tools based on security type:

   **For Stocks (AAPL, AMZN, TSLA, etc.):**
   - `get_current_stock_price(symbol)`
   - `get_stock_fundamentals(symbol)`
   - `get_key_financial_ratios(symbol)`
   - `get_income_statements(symbol)`
   - `get_analyst_recommendations(symbol)`
   - `get_company_news(symbol, 5)`
   - `get_technical_indicators(symbol, "6mo")`
   - `get_historical_stock_prices(symbol, "1y", "1d")`

   **For ETFs (COPX, SPY, QQQ, etc.):**
   - `get_current_stock_price(symbol)`
   - `get_company_news(symbol, 5)`
   - `get_technical_indicators(symbol, "6mo")`
   - `get_historical_stock_prices(symbol, "1y", "1d")`
   - Do **NOT** call `get_stock_fundamentals`, `get_key_financial_ratios`, or `get_income_statements` — these return 404 errors for ETFs.

3. **Analyze** — Evaluate across applicable dimensions:

   **For Stocks:**
   - Valuation: P/E, P/B, PEG ratio vs sector averages
   - Growth: Revenue and earnings growth trends
   - Profitability: Margins, ROE, ROA
   - Analyst Sentiment: Buy/hold/sell distribution and price targets
   - Technical: Moving averages, RSI, MACD signals
   - News Sentiment: Key recent developments and their likely impact
   - Risk Assessment: Volatility, beta, debt levels

   **For ETFs:**
   - ETF Profile: Assets under management, expense ratio, holdings, category
   - Performance: YTD, 1Y, 3Y, 5Y returns
   - Technical: Moving averages, RSI, support/resistance levels
   - News Sentiment: Sector/commodity trends and their likely impact
   - Risk Assessment: Volatility, beta, drawdown from highs

4. **Synthesize** — Produce a clear summary with:
   - Overall outlook (Bullish / Neutral / Bearish) with confidence level
   - Key strengths and concerns (3-5 each)
   - Actionable recommendation
   - If portfolio analysis: diversification assessment, sector exposure, risk profile

5. **Save Report** — Write the analysis to `data/analysis/YYYY-MM-DD_<topic>.json`:
   ```json
   {
     "title": "Analysis title",
     "date": "YYYY-MM-DD",
     "type": "stock_analysis | portfolio_review | sector_analysis | comparison",
     "content": "Full markdown-formatted analysis"
   }
   ```

6. **Update Portfolio** — If analysis reveals updated prices, refresh `data/portfolio.json` with current prices.

### Rules

- Always use real data from YFinance. Never fabricate numbers.
- Include specific numbers and percentages, not vague statements.
- Compare metrics to industry/sector averages when possible.
- Flag any data that couldn't be retrieved rather than guessing.
- For portfolio reviews, assess correlation and diversification.
- Date all reports and reference the data retrieval time.
- Always write reports in English unless the user explicitly asks for another language.
- If a tool call fails or returns an error, skip that data point and continue with what you have. Do not retry failed calls.