"""
Stock Agent Dashboard — Streamlit Frontend

Reads agent-managed data from workspace/data/ and displays portfolio overview,
analysis reports, charts, and stock tracking. Updated by the agent via conversation.
"""

import json
import os
import glob

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

WORKSPACE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")
DATA_DIR = os.path.join(WORKSPACE, "data")
PORTFOLIO_FILE = os.path.join(DATA_DIR, "portfolio.json")
WATCHLIST_FILE = os.path.join(DATA_DIR, "watchlist.json")
ANALYSIS_DIR = os.path.join(DATA_DIR, "analysis")

# --- Theme ---

DARK = {
    "bg": "#0e1117",
    "card": "#1a1d23",
    "border": "#2d3139",
    "text": "#e6e6e6",
    "muted": "#8b949e",
    "green": "#00c853",
    "red": "#ff1744",
    "accent": "#58a6ff",
}

LIGHT = {
    "bg": "#ffffff",
    "card": "#f6f8fa",
    "border": "#d1d5db",
    "text": "#1f2937",
    "muted": "#6b7280",
    "green": "#16a34a",
    "red": "#dc2626",
    "accent": "#2563eb",
}


def get_theme(dark_mode):
    return DARK if dark_mode else LIGHT


def apply_theme(theme):
    st.markdown(f"""
    <style>
        .stApp, .stApp > header, [data-testid="stHeader"],
        [data-testid="stToolbar"], [data-testid="stDecoration"],
        [data-testid="stStatusWidget"], .stDeployButton,
        section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {{
            background-color: {theme["bg"]} !important;
            color: {theme["text"]};
        }}
        [data-testid="stHeader"] {{
            background: {theme["bg"]} !important;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {theme["bg"]};
        }}
        .stTabs [data-baseweb="tab"] {{
            color: {theme["muted"]};
        }}
        .stTabs [aria-selected="true"] {{
            color: {theme["text"]} !important;
        }}
        [data-testid="stExpander"] {{
            background-color: {theme["card"]};
            border-color: {theme["border"]};
            border-radius: 10px;
        }}
        .metric-card {{
            background: {theme["card"]};
            border: 1px solid {theme["border"]};
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        .metric-label {{
            font-size: 0.8rem;
            color: {theme["muted"]};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }}
        .metric-value {{
            font-size: 1.6rem;
            font-weight: 700;
            color: {theme["text"]};
        }}
        .metric-delta-pos {{
            font-size: 0.85rem;
            color: {theme["green"]};
            font-weight: 600;
        }}
        .metric-delta-neg {{
            font-size: 0.85rem;
            color: {theme["red"]};
            font-weight: 600;
        }}
        .stock-row {{
            background: {theme["card"]};
            border: 1px solid {theme["border"]};
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .stock-symbol {{
            font-size: 1.1rem;
            font-weight: 700;
            color: {theme["accent"]};
            min-width: 70px;
        }}
        .stock-name {{
            font-size: 0.85rem;
            color: {theme["muted"]};
            min-width: 140px;
        }}
        .stock-field {{
            text-align: right;
            min-width: 90px;
        }}
        .stock-field-label {{
            font-size: 0.7rem;
            color: {theme["muted"]};
            text-transform: uppercase;
        }}
        .stock-field-value {{
            font-size: 0.95rem;
            font-weight: 600;
            color: {theme["text"]};
        }}
        .gain-pos {{ color: {theme["green"]} !important; }}
        .gain-neg {{ color: {theme["red"]} !important; }}
        .section-header {{
            font-size: 1.1rem;
            font-weight: 600;
            color: {theme["text"]};
            margin: 24px 0 12px 0;
        }}
        .date-badge {{
            display: inline-block;
            background: {theme["border"]};
            color: {theme["muted"]};
            font-size: 0.75rem;
            padding: 2px 10px;
            border-radius: 12px;
        }}
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: {theme["muted"]};
        }}
        .empty-state h3 {{
            color: {theme["text"]};
            margin-bottom: 8px;
        }}
    </style>
    """, unsafe_allow_html=True)


def load_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        return {"stocks": [], "last_updated": None}
    with open(PORTFOLIO_FILE, "r") as f:
        return json.load(f)


def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return {"stocks": [], "last_updated": None}
    with open(WATCHLIST_FILE, "r") as f:
        return json.load(f)


def load_analyses():
    reports = []
    if not os.path.exists(ANALYSIS_DIR):
        return reports
    for filepath in sorted(glob.glob(os.path.join(ANALYSIS_DIR, "*.json")), reverse=True):
        with open(filepath, "r") as f:
            reports.append(json.load(f))
    return reports


def render_metric_card(label, value, delta=None, delta_positive=None):
    delta_html = ""
    if delta is not None:
        cls = "metric-delta-pos" if delta_positive else "metric-delta-neg"
        arrow = "+" if delta_positive else ""
        delta_html = f'<div class="{cls}">{arrow}{delta}</div>'
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """


def render_summary_metrics(portfolio, theme):
    stocks = portfolio.get("stocks", [])
    if not stocks:
        return

    df = pd.DataFrame(stocks)

    total_value = df["total_value"].sum() if "total_value" in df.columns else 0
    total_cost = (df["avg_cost"] * df["shares"]).sum() if "avg_cost" in df.columns and "shares" in df.columns else 0
    total_commission = df["commission"].sum() if "commission" in df.columns else 0
    total_gain = total_value - total_cost
    gain_pct = (total_gain / total_cost * 100) if total_cost > 0 else 0
    net_gain = total_gain - total_commission

    cols = st.columns(5)
    cards = [
        ("Portfolio Value", f"${total_value:,.2f}", None, None),
        ("Total Invested", f"${total_cost:,.2f}", None, None),
        ("Gain / Loss", f"${total_gain:,.2f}", f"{gain_pct:.2f}%", total_gain >= 0),
        ("Commissions", f"${total_commission:,.2f}", None, None),
        ("Net P&L", f"${net_gain:,.2f}", None, net_gain >= 0),
    ]
    for col, (label, value, delta, delta_pos) in zip(cols, cards):
        with col:
            html = render_metric_card(label, value, delta, delta_pos)
            if delta_pos is not None and not delta_pos:
                html = html.replace(f'class="metric-value"', f'class="metric-value gain-neg"')
            st.markdown(html, unsafe_allow_html=True)


def render_stock_row(stock, theme):
    symbol = stock.get("symbol", "???")
    name = stock.get("name", "")
    shares = stock.get("shares", 0)
    avg_cost = stock.get("avg_cost", 0)
    current_price = stock.get("current_price", 0)
    total_value = stock.get("total_value", 0)
    gain_loss = stock.get("gain_loss", 0)
    gain_loss_pct = stock.get("gain_loss_pct", 0)
    commission = stock.get("commission", 0)
    purchase_date = stock.get("purchase_date", "—")

    gain_cls = "gain-pos" if gain_loss >= 0 else "gain-neg"
    gain_sign = "+" if gain_loss >= 0 else ""

    return f"""
    <div class="stock-row">
        <div>
            <div class="stock-symbol">{symbol}</div>
            <div class="stock-name">{name}</div>
        </div>
        <div class="stock-field">
            <div class="stock-field-label">Shares</div>
            <div class="stock-field-value">{shares:,.4f}</div>
        </div>
        <div class="stock-field">
            <div class="stock-field-label">Avg Cost</div>
            <div class="stock-field-value">${avg_cost:,.2f}</div>
        </div>
        <div class="stock-field">
            <div class="stock-field-label">Price</div>
            <div class="stock-field-value">${current_price:,.2f}</div>
        </div>
        <div class="stock-field">
            <div class="stock-field-label">Value</div>
            <div class="stock-field-value">${total_value:,.2f}</div>
        </div>
        <div class="stock-field">
            <div class="stock-field-label">Gain/Loss</div>
            <div class="stock-field-value {gain_cls}">{gain_sign}${gain_loss:,.2f} ({gain_sign}{gain_loss_pct:.2f}%)</div>
        </div>
        <div class="stock-field">
            <div class="stock-field-label">Commission</div>
            <div class="stock-field-value">${commission:,.2f}</div>
        </div>
        <div class="stock-field">
            <div class="stock-field-label">Purchased</div>
            <div class="stock-field-value">{purchase_date}</div>
        </div>
    </div>
    """


def render_portfolio_overview(portfolio, theme):
    stocks = portfolio.get("stocks", [])
    if not stocks:
        st.markdown("""
        <div class="empty-state">
            <h3>No stocks yet</h3>
            <p>Chat with your agent on Telegram to start building your portfolio.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown('<div class="section-header">Holdings</div>', unsafe_allow_html=True)
    for stock in stocks:
        st.markdown(render_stock_row(stock, theme), unsafe_allow_html=True)


def render_portfolio_charts(portfolio, theme):
    stocks = portfolio.get("stocks", [])
    if not stocks:
        return

    df = pd.DataFrame(stocks)
    if "total_value" not in df.columns or "symbol" not in df.columns:
        return

    plot_bg = theme["card"]
    paper_bg = theme["bg"]
    text_color = theme["text"]
    grid_color = theme["border"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Allocation</div>', unsafe_allow_html=True)
        fig = px.pie(df, values="total_value", names="symbol", hole=0.45)
        fig.update_traces(textinfo="label+percent", textfont_size=12)
        fig.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=350,
            paper_bgcolor=paper_bg,
            plot_bgcolor=plot_bg,
            font_color=text_color,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Gain / Loss</div>', unsafe_allow_html=True)
        if "gain_loss" in df.columns:
            colors = [theme["green"] if v >= 0 else theme["red"] for v in df["gain_loss"]]
            fig = go.Figure(go.Bar(
                x=df["symbol"], y=df["gain_loss"],
                marker_color=colors,
                text=[f"${v:,.2f}" for v in df["gain_loss"]],
                textposition="outside",
                textfont=dict(color=text_color, size=11),
            ))
            fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=350,
                paper_bgcolor=paper_bg,
                plot_bgcolor=plot_bg,
                font_color=text_color,
                yaxis=dict(title="$", gridcolor=grid_color, zerolinecolor=grid_color),
                xaxis=dict(gridcolor=grid_color),
            )
            st.plotly_chart(fig, use_container_width=True)


def render_watchlist_row(stock, theme):
    symbol = stock.get("symbol", "???")
    name = stock.get("name", "")
    current_price = stock.get("current_price", 0)
    price_at_add = stock.get("price_at_add", 0)
    change_pct = stock.get("change_pct", 0)
    added_date = stock.get("added_date", "—")
    note = stock.get("note", "")

    change_cls = "gain-pos" if change_pct >= 0 else "gain-neg"
    change_sign = "+" if change_pct >= 0 else ""

    note_html = f'<div style="font-size:0.8rem; color:{theme["muted"]}; margin-top:4px; font-style:italic">{note}</div>' if note else ""

    return f"""
    <div class="stock-row">
        <div style="min-width:160px">
            <div class="stock-symbol">{symbol}</div>
            <div class="stock-name">{name}</div>
            {note_html}
        </div>
        <div class="stock-field">
            <div class="stock-field-label">Price</div>
            <div class="stock-field-value">${current_price:,.2f}</div>
        </div>
        <div class="stock-field">
            <div class="stock-field-label">Price at Add</div>
            <div class="stock-field-value">${price_at_add:,.2f}</div>
        </div>
        <div class="stock-field">
            <div class="stock-field-label">Change</div>
            <div class="stock-field-value {change_cls}">{change_sign}{change_pct:.2f}%</div>
        </div>
        <div class="stock-field">
            <div class="stock-field-label">Tracking Since</div>
            <div class="stock-field-value">{added_date}</div>
        </div>
    </div>
    """


def render_watchlist(watchlist, theme):
    stocks = watchlist.get("stocks", [])
    if not stocks:
        st.markdown("""
        <div class="empty-state">
            <h3>No tracked stocks yet</h3>
            <p>Tell your agent on Telegram to track a stock you're interested in.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown('<div class="section-header">Tracking</div>', unsafe_allow_html=True)
    for stock in stocks:
        st.markdown(render_watchlist_row(stock, theme), unsafe_allow_html=True)


def render_analyses(analyses, theme):
    if not analyses:
        st.markdown("""
        <div class="empty-state">
            <h3>No analysis reports yet</h3>
            <p>Ask your agent to analyze a stock or review your portfolio.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    for i, report in enumerate(analyses):
        title = report.get("title", "Analysis Report")
        date = report.get("date", "")
        content = report.get("content", "")
        report_type = report.get("type", "general")

        header = f"{title}"
        if date:
            header += f"  &nbsp; `{date}`"

        with st.expander(header, expanded=(i == 0)):
            if report_type:
                st.markdown(f'<span class="date-badge">{report_type}</span>', unsafe_allow_html=True)
            st.markdown(content)


def main():
    st.set_page_config(
        page_title="Stock Agent Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Theme toggle — top right, inline with header
    col_title, col_right = st.columns([4, 1])

    with col_right:
        dark_mode = st.toggle("Dark mode", value=True)

    theme = get_theme(dark_mode)
    apply_theme(theme)

    with col_title:
        st.markdown(f'<h1 style="margin-bottom:0; color:{theme["text"]}">Stock Agent</h1>', unsafe_allow_html=True)

    portfolio = load_portfolio()
    last_updated = portfolio.get("last_updated")
    subtitle = "Managed by your AI agent via Telegram"
    if last_updated:
        subtitle += f" &nbsp;·&nbsp; Updated: {last_updated}"
    st.markdown(f'<p style="color:{theme["muted"]}; margin-top:0">{subtitle}</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    render_summary_metrics(portfolio, theme)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Portfolio", "Watchlist", "Analysis Reports"])

    with tab1:
        render_portfolio_overview(portfolio, theme)
        st.markdown("<br>", unsafe_allow_html=True)
        render_portfolio_charts(portfolio, theme)

    with tab2:
        watchlist = load_watchlist()
        render_watchlist(watchlist, theme)

    with tab3:
        analyses = load_analyses()
        render_analyses(analyses, theme)


if __name__ == "__main__":
    main()