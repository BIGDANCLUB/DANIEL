"""
Crypto Trendline Break Scanner — Streamlit App (Phase 7)
=========================================================
6時間以内トレンドラインブレイク検知スキャナー
100% 無料API構成: CCXT + Binance Public FAPI + DexScreener + CryptoPanic

Phase 7 additions:
- Fibonacci retracement/extension levels
- Support/Resistance cluster zones
- Position size calculator with risk/reward
- BTC correlation analysis
- CSV export for scan results & backtest
"""

import asyncio
import logging
import sys
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("scanner_app")

# ── Page config ──
st.set_page_config(
    page_title="Crypto Trendline Break Scanner",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS (Dark mode) ──
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    .main .block-container { padding-top: 1rem; }
    .score-high { color: #00e676; font-weight: bold; }
    .score-mid  { color: #ffc107; font-weight: bold; }
    .score-low  { color: #ff5252; font-weight: bold; }
    .scanner-header {
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .scanner-header h1 { color: #e0e0e0; margin: 0; font-size: 1.6rem; }
    .scanner-header p { color: #9e9e9e; margin: 0.3rem 0 0 0; font-size: 0.9rem; }
    div[data-testid="stMetric"] {
        background-color: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        padding: 0.8rem;
    }
    .dataframe { font-size: 0.85rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 2px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a2e;
        border-radius: 4px 4px 0 0;
        padding: 0.5rem 1rem;
        color: #e0e0e0;
    }
    .free-badge {
        display: inline-block;
        background: #1b5e20;
        color: #69f0ae;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .market-ticker {
        background: linear-gradient(90deg, #0d1b2a, #1b2838);
        border: 1px solid #2a3a5a;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin-bottom: 0.8rem;
    }
    .alert-banner {
        background: linear-gradient(135deg, #b71c1c 0%, #880e4f 100%);
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1rem;
        animation: alert-pulse 2s ease-in-out infinite;
    }
    @keyframes alert-pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.85; }
    }
    .watchlist-chip {
        display: inline-block;
        background: #1a237e;
        color: #82b1ff;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 2px;
    }
    .hit-rate-card {
        background: linear-gradient(135deg, #1a1a2e, #1e3a5f);
        border: 1px solid #2a4a7a;
        border-radius: 10px;
        padding: 1rem;
    }
    @keyframes funda-pulse {
        0%, 100% { border-left-color: #448AFF; }
        50% { border-left-color: #82B1FF; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

from scanner_engine import (
    ScannerEngine,
    ScanResult,
    MarketOverview,
    MiniBacktester,
    load_watchlist,
    save_watchlist,
    add_to_watchlist,
    remove_from_watchlist,
    load_signal_history,
    compute_hit_rate_stats,
    update_signal_outcomes,
    load_alerts,
    save_alerts,
    add_alert,
    remove_alert,
)
from chart_builder import (
    build_candlestick_chart,
    build_order_book_chart,
    build_order_book_heatmap,
    build_funding_rate_chart,
    build_funding_rate_history_chart,
    build_long_short_chart,
    build_ls_history_chart,
    build_open_interest_chart,
    build_liquidation_chart,
    build_signal_heatmap,
    build_backtest_chart,
    build_fibonacci_chart,
    build_sr_cluster_chart,
    build_correlation_chart,
)
from technical_analysis import compute_correlation
from data_fetcher import (
    CEXFetcher,
    MultiExchangeFundingFetcher,
    BinanceLongShortFetcher,
    BinanceFundingHistoryFetcher,
    BinanceOpenInterestFetcher,
    CryptoPanicFetcher,
)


# ──────────────────────────────────────────────
# Session state init
# ──────────────────────────────────────────────
if "scanner" not in st.session_state:
    st.session_state.scanner = ScannerEngine()
if "results" not in st.session_state:
    st.session_state.results = []
if "selected_symbol" not in st.session_state:
    st.session_state.selected_symbol = None
if "scan_running" not in st.session_state:
    st.session_state.scan_running = False
if "last_scan_time" not in st.session_state:
    st.session_state.last_scan_time = None
if "market_data" not in st.session_state:
    st.session_state.market_data = None
if "triggered_alerts" not in st.session_state:
    st.session_state.triggered_alerts = []


# ──────────────────────────────────────────────
# Helper: run async in streamlit
# ──────────────────────────────────────────────
def run_async(coro):
    """Run an async coroutine from sync Streamlit context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(asyncio.run, coro).result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Scanner Settings")

    st.markdown("**Filters**")
    min_score = st.slider("Min Score", 0, 100, 20, step=5)
    vol_multiplier = st.slider("Volume Spike Multiplier", 1.5, 10.0, 3.0, step=0.5)

    st.markdown("**Exchanges**")
    show_binance = st.checkbox("Binance Futures", value=True)
    show_bybit = st.checkbox("Bybit Futures", value=True)
    show_dex = st.checkbox("DEX (DexScreener)", value=True)

    st.markdown("---")
    st.markdown("**Sort By**")
    sort_col = st.selectbox("Sort Column", ["Score", "Vol Ratio", "24h %", "Price", "Break Strength"], index=0)
    sort_asc = st.checkbox("Ascending", value=False)

    st.markdown("---")

    # ── Watchlist management in sidebar ──
    st.markdown("### Watchlist")
    watchlist = load_watchlist()
    if watchlist:
        chips_html = " ".join(f'<span class="watchlist-chip">{s}</span>' for s in watchlist)
        st.markdown(chips_html, unsafe_allow_html=True)

        wl_remove = st.selectbox("Remove from watchlist", ["---"] + watchlist, key="wl_remove")
        if wl_remove != "---":
            if st.button("Remove", key="wl_remove_btn"):
                remove_from_watchlist(wl_remove)
                st.rerun()
    else:
        st.caption("Watchlist is empty")

    wl_add = st.text_input("Add symbol (e.g. BTC/USDT:USDT)", key="wl_add")
    if wl_add and st.button("Add to Watchlist", key="wl_add_btn"):
        add_to_watchlist(wl_add.strip().upper())
        st.rerun()

    wl_filter = st.checkbox("Show watchlist only", value=False, key="wl_filter")

    st.markdown("---")
    st.markdown("**Auto Refresh**")
    auto_refresh = st.checkbox("Auto refresh (60s)", value=False)

    st.markdown("---")
    st.markdown("**Status**")
    if st.session_state.last_scan_time:
        st.caption(f"Last scan: {st.session_state.last_scan_time.strftime('%H:%M:%S UTC')}")
    else:
        st.caption("No scan yet")

    st.markdown("---")
    st.markdown("**Data Sources** <span class='free-badge'>ALL FREE</span>", unsafe_allow_html=True)
    st.caption("CCXT: OHLCV, Funding Rate, Order Book")
    st.caption("Binance FAPI: Long/Short, OI, FR History")
    st.caption("DexScreener: DEX pairs")
    st.caption("CryptoPanic: News/Social")


# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="scanner-header">
        <h1>Crypto Trendline Break Scanner</h1>
        <p>6時間以内トレンドラインブレイク検知 — Volume Spike + 200 EMA + Trendline Break + Social
        <span class="free-badge">100% FREE APIs</span>
        <span class="free-badge" style="background:#0d47a1;color:#82b1ff;margin-left:4px;">Phase 7</span></p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# Market Dashboard (Phase 5)
# ──────────────────────────────────────────────
def render_market_dashboard():
    """Render BTC/ETH/Fear&Greed ticker bar."""
    md = st.session_state.market_data
    if md is None:
        try:
            md = MarketOverview.get_btc_dominance_and_fear()
            st.session_state.market_data = md
        except Exception:
            return

    btc_color = "#00e676" if md["btc_change_24h"] >= 0 else "#ff5252"
    eth_color = "#00e676" if md["eth_change_24h"] >= 0 else "#ff5252"

    fg_val = md["fear_greed_value"]
    if fg_val >= 70:
        fg_color = "#00e676"
    elif fg_val >= 40:
        fg_color = "#ffc107"
    else:
        fg_color = "#ff5252"

    st.markdown(
        f"""
        <div class="market-ticker">
            <span style="color:#e0e0e0;font-weight:bold;margin-right:1.5rem;">
                BTC <span style="color:#ffc107;">${md['btc_price']:,.0f}</span>
                <span style="color:{btc_color};font-size:0.85rem;">{md['btc_change_24h']:+.2f}%</span>
            </span>
            <span style="color:#e0e0e0;font-weight:bold;margin-right:1.5rem;">
                ETH <span style="color:#ffc107;">${md['eth_price']:,.0f}</span>
                <span style="color:{eth_color};font-size:0.85rem;">{md['eth_change_24h']:+.2f}%</span>
            </span>
            <span style="color:#e0e0e0;font-weight:bold;">
                Fear & Greed <span style="color:{fg_color};font-size:1rem;">{fg_val}</span>
                <span style="color:#9e9e9e;font-size:0.8rem;">({md['fear_greed_label']})</span>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

render_market_dashboard()


# ──────────────────────────────────────────────
# Triggered Alerts Banner (Phase 5)
# ──────────────────────────────────────────────
if st.session_state.triggered_alerts:
    alerts_html = ""
    for ta in st.session_state.triggered_alerts[:5]:
        alerts_html += (
            f'<div style="margin-bottom:4px;">'
            f'<b>{ta["alert_name"]}</b> — {ta["symbol"]} '
            f'(Score: {ta["score"]:.0f}, {ta.get("breakout_type", "—")}) '
            f'@ ${ta["price"]:,.4f}'
            f'</div>'
        )
    st.markdown(
        f"""
        <div class="alert-banner">
            <div style="color:#FFCDD2;font-weight:bold;font-size:1rem;margin-bottom:4px;">
                Alerts Triggered!
            </div>
            <div style="color:#FFEBEE;font-size:0.85rem;">{alerts_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# Scan button
# ──────────────────────────────────────────────
col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 3])
with col_btn1:
    scan_clicked = st.button("Scan Now", type="primary", use_container_width=True)
with col_btn2:
    clear_clicked = st.button("Clear", use_container_width=True)
with col_btn3:
    refresh_market = st.button("Refresh Market", use_container_width=True)

if refresh_market:
    st.session_state.market_data = None
    st.rerun()

if clear_clicked:
    st.session_state.results = []
    st.session_state.selected_symbol = None
    st.session_state.triggered_alerts = []
    st.rerun()

if scan_clicked:
    st.session_state.scan_running = True
    # Refresh market data on scan
    st.session_state.market_data = None

    with st.spinner("Scanning markets... (Multi-CEX + DEX, 30-90 seconds)"):
        try:
            from config import Config as cfg
            cfg.VOLUME_SPIKE_MULTIPLIER = vol_multiplier

            scanner = st.session_state.scanner

            # Build exchange list based on checkbox
            exchanges = []
            if show_binance:
                exchanges.append("binance")
            if show_bybit:
                exchanges.append("bybit")

            results = run_async(scanner.run_full_scan(
                exchanges=exchanges if exchanges else None,
                include_dex=show_dex,
            ))

            # Filter by source preference + min score + watchlist
            watchlist = load_watchlist()
            filtered = []
            for r in results:
                if r.score < min_score:
                    continue
                if wl_filter and watchlist:
                    if r.symbol not in watchlist:
                        continue
                filtered.append(r)

            st.session_state.results = filtered
            st.session_state.last_scan_time = datetime.now(timezone.utc)
            st.session_state.triggered_alerts = scanner.triggered_alerts
            st.session_state.scan_running = False
            st.rerun()
        except Exception as e:
            st.error(f"Scan failed: {e}")
            logger.exception("Scan failed")
            st.session_state.scan_running = False


# ──────────────────────────────────────────────
# Auto refresh
# ──────────────────────────────────────────────
if auto_refresh:
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=60_000, key="auto_refresh")
    except ImportError:
        st.sidebar.warning("Install streamlit-autorefresh for auto-refresh")


# ──────────────────────────────────────────────
# Main content — tabs: Signals | History | Alerts
# ──────────────────────────────────────────────
main_tab_signals, main_tab_heatmap, main_tab_risk, main_tab_backtest, main_tab_history, main_tab_alerts = st.tabs(
    ["Signals", "Heatmap", "Risk Calculator", "Backtest", "Signal History", "Alert Settings"]
)


# ════════════════════════════════════════════════
# TAB: SIGNALS
# ════════════════════════════════════════════════
with main_tab_signals:
    results: list[ScanResult] = st.session_state.results

    if not results:
        st.info("Click **Scan Now** to scan for trendline breakouts across CEX & DEX markets.")
    else:
        # Summary metrics
        mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)
        with mcol1:
            st.metric("Total Signals", len(results))
        with mcol2:
            bullish = sum(1 for r in results if r.trendline_break.get("breakout_type") == "bullish")
            st.metric("Bullish Breaks", bullish)
        with mcol3:
            avg_score = sum(r.score for r in results) / len(results)
            st.metric("Avg Score", f"{avg_score:.1f}")
        with mcol4:
            cex_count = sum(1 for r in results if "Futures" in r.source)
            st.metric("CEX Signals", cex_count)
        with mcol5:
            dex_count = sum(1 for r in results if "DEX" in r.source)
            st.metric("DEX Signals", dex_count)

        # Scan stats from engine
        scanner = st.session_state.scanner
        if scanner.scan_stats:
            stats_parts = [f"{k}: {v}" for k, v in scanner.scan_stats.items()]
            st.caption(f"Scan breakdown — {' | '.join(stats_parts)}")

        st.markdown("---")

        # Build dataframe
        rows = [r.to_dict() for r in results]
        df_results = pd.DataFrame(rows)

        # Watchlist column
        watchlist = load_watchlist()
        df_results["WL"] = df_results["Symbol"].apply(lambda s: "★" if s in watchlist else "")

        # Sort
        if sort_col in df_results.columns:
            df_results = df_results.sort_values(sort_col, ascending=sort_asc)

        # Color-code
        def color_score(val):
            if val >= 70:
                return "color: #00e676; font-weight: bold"
            elif val >= 40:
                return "color: #ffc107; font-weight: bold"
            else:
                return "color: #ff5252"

        def color_change(val):
            if isinstance(val, (int, float)):
                return "color: #00e676" if val >= 0 else "color: #ff5252"
            return ""

        def highlight_break(val):
            if val == "bullish":
                return "background-color: rgba(0,230,118,0.15); color: #00e676; font-weight: bold"
            elif val == "bearish":
                return "background-color: rgba(255,82,82,0.15); color: #ff5252; font-weight: bold"
            return ""

        def color_pattern(val):
            pattern_colors = {
                "Ascending Triangle": "color: #00e676",
                "Falling Wedge": "color: #00e676",
                "Rising Channel": "color: #66BB6A",
                "Symmetrical Triangle": "color: #FFC107",
                "Descending Triangle": "color: #ff5252",
                "Rising Wedge": "color: #ff5252",
                "Falling Channel": "color: #EF5350",
            }
            return pattern_colors.get(val, "")

        def color_bool(val):
            if val is True:
                return "color: #00e676; font-weight: bold"
            elif val is False:
                return "color: #616161"
            return ""

        styled = df_results.style.applymap(color_score, subset=["Score"])
        styled = styled.applymap(color_change, subset=["24h %", "Vol Ratio"])
        styled = styled.applymap(highlight_break, subset=["Trendline Break"])
        styled = styled.applymap(color_pattern, subset=["Pattern"])
        styled = styled.applymap(color_bool, subset=["Vol Confirm", "Social"])
        styled = styled.format({
            "Price": "${:,.4f}",
            "24h %": "{:+.2f}%",
            "24h Vol": "${:,.0f}",
            "Vol Ratio": "{:.1f}x",
            "Break Strength": "{:.2f}",
            "Score": "{:.1f}",
        })

        st.dataframe(
            styled,
            use_container_width=True,
            height=min(400, 50 + len(df_results) * 35),
        )

        # ── Watchlist quick add buttons ──
        st.markdown("**Quick add to watchlist:**")
        wl_cols = st.columns(min(len(results), 6))
        for i, r in enumerate(results[:6]):
            with wl_cols[i]:
                if r.symbol not in watchlist:
                    if st.button(f"+ {r.symbol.split('/')[0]}", key=f"wl_quick_{i}"):
                        add_to_watchlist(r.symbol)
                        st.rerun()
                else:
                    st.caption(f"★ {r.symbol.split('/')[0]}")

        # ──────────────────────────────────────────
        # Detail view: select a coin
        # ──────────────────────────────────────────
        st.markdown("---")
        st.markdown("### Detail View")

        symbol_options = [r.symbol for r in results]
        selected = st.selectbox(
            "Select coin for detailed analysis",
            options=symbol_options,
            index=0 if symbol_options else None,
        )

        if selected:
            sel_result = next((r for r in results if r.symbol == selected), None)
            if sel_result:
                st.markdown(f"#### {selected} — {sel_result.source}")

                is_cex = "Futures" in sel_result.source

                # ── Fundamental Driver Detection Window ──
                if sel_result.change_pct > 0:
                    with st.spinner("Analyzing price driver..."):
                        funda = CryptoPanicFetcher.analyze_fundamental_driver(selected)

                    if funda["is_funda_driven"]:
                        st.markdown(
                            f"""
                            <div style="
                                background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
                                border-left: 4px solid #448AFF;
                                border-radius: 8px;
                                padding: 1rem 1.2rem;
                                margin-bottom: 1rem;
                            ">
                                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                    <span style="font-size: 1.3rem; margin-right: 0.5rem;">📰</span>
                                    <span style="color: #82B1FF; font-weight: bold; font-size: 1.05rem;">
                                        Fundamental Driver Detected
                                    </span>
                                </div>
                                <p style="color: #E3F2FD; margin: 0.3rem 0; font-size: 0.95rem;">
                                    {funda['summary']}
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        driver_cols = st.columns(min(len(funda["drivers"]), 3))
                        for i, driver in enumerate(funda["drivers"][:3]):
                            with driver_cols[i]:
                                conf_pct = f"{driver['confidence']:.0%}"
                                kw_tags = " ".join(
                                    f'<span style="background:{driver["color"]}33;'
                                    f'color:{driver["color"]};padding:1px 6px;'
                                    f'border-radius:3px;font-size:0.75rem;margin-right:3px;">'
                                    f'{kw}</span>'
                                    for kw in driver["matched_keywords"][:4]
                                )
                                st.markdown(
                                    f"""
                                    <div style="
                                        background-color: #1a1a2e;
                                        border: 1px solid {driver['color']}66;
                                        border-radius: 8px;
                                        padding: 0.8rem;
                                    ">
                                        <div style="color:{driver['color']};font-weight:bold;font-size:0.9rem;">
                                            {driver['label']}
                                        </div>
                                        <div style="color:#9e9e9e;font-size:0.8rem;margin:0.3rem 0;">
                                            {driver['article_count']} articles | Confidence: {conf_pct}
                                        </div>
                                        <div style="margin-top:0.4rem;">{kw_tags}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                        with st.expander("View related articles", expanded=False):
                            for driver in funda["drivers"]:
                                st.markdown(f"**{driver['label']}**")
                                for art in driver["articles"][:3]:
                                    src = art.get("source", "")
                                    pub = art.get("published_at", "")[:16]
                                    st.markdown(f"- {art['title']} — _{src}_ ({pub})")
                                st.markdown("")

                    elif funda["total_articles"] > 0:
                        st.markdown(
                            f"""
                            <div style="
                                background-color: #1a1a2e;
                                border-left: 4px solid #66BB6A;
                                border-radius: 8px;
                                padding: 0.8rem 1.2rem;
                                margin-bottom: 1rem;
                            ">
                                <span style="color: #A5D6A7; font-size: 0.9rem;">
                                    <b>Technical Move</b> — {funda['summary']}
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                tab_chart, tab_ta, tab_fib, tab_sr, tab_corr, tab_funding, tab_ls, tab_oi, tab_orderbook, tab_liq, tab_social = st.tabs(
                    ["Chart", "TA Indicators", "Fibonacci", "S/R Zones", "BTC Corr",
                     "Funding Rate", "Long/Short", "Open Interest", "Order Book", "Liquidation", "News/Social"]
                )

                # ── Tab: Chart ──
                with tab_chart:
                    tc1, tc2 = st.columns([1, 1])
                    with tc1:
                        timeframe = st.radio(
                            "Timeframe", ["1h", "4h"], horizontal=True, key="tf_radio"
                        )
                    with tc2:
                        show_indicators = st.checkbox(
                            "Show RSI / MACD / Bollinger Bands", value=False, key="show_ta"
                        )

                    if is_cex:
                        with st.spinner(f"Loading {timeframe} chart for {selected}..."):
                            try:
                                cex_fetcher = CEXFetcher()
                                ohlcv_df = run_async(
                                    cex_fetcher.fetch_ohlcv(selected, timeframe=timeframe, limit=250)
                                )
                                run_async(cex_fetcher.close())

                                if not ohlcv_df.empty:
                                    fig = build_candlestick_chart(
                                        ohlcv_df, selected,
                                        show_trendlines=True,
                                        show_indicators=show_indicators,
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.warning("No OHLCV data available")
                            except Exception as e:
                                st.error(f"Chart error: {e}")
                    else:
                        st.info(
                            "DEX chart: Full candlestick charts for DEX tokens require "
                            "on-chain OHLCV aggregation. Showing summary data instead."
                        )
                        if sel_result.extra:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("1H Change", f"{sel_result.extra.get('h1_change', 0):+.2f}%")
                            with col2:
                                st.metric("6H Change", f"{sel_result.extra.get('h6_change', 0):+.2f}%")
                            with col3:
                                st.metric(
                                    "Liquidity",
                                    f"${sel_result.extra.get('liquidity_usd', 0):,.0f}",
                                )

                # ── Tab: TA Indicators (Phase 6) ──
                with tab_ta:
                    st.markdown("#### Technical Indicator Summary")
                    rsi_info = sel_result.extra.get("rsi", {})
                    macd_info = sel_result.extra.get("macd", {})
                    bb_info = sel_result.extra.get("bb", {})

                    if rsi_info or macd_info or bb_info:
                        ta_col1, ta_col2, ta_col3 = st.columns(3)

                        # RSI Card
                        with ta_col1:
                            rsi_val = rsi_info.get("value", 0)
                            rsi_sig = rsi_info.get("signal", "neutral")
                            if rsi_val > 70:
                                rsi_color = "#ff5252"
                            elif rsi_val < 30:
                                rsi_color = "#00e676"
                            else:
                                rsi_color = "#ffc107"

                            st.markdown(
                                f"""
                                <div style="background:#1a1a2e;border:1px solid {rsi_color}66;
                                     border-radius:8px;padding:1rem;">
                                    <div style="color:{rsi_color};font-size:2rem;font-weight:bold;">
                                        {rsi_val:.1f}
                                    </div>
                                    <div style="color:#e0e0e0;font-weight:bold;">RSI (14)</div>
                                    <div style="color:#9e9e9e;font-size:0.85rem;margin-top:0.3rem;">
                                        Signal: {rsi_sig.replace('_', ' ').title()}<br>
                                        {'Oversold zone' if rsi_info.get('oversold') else
                                         'Overbought zone' if rsi_info.get('overbought') else
                                         'Bullish zone' if rsi_info.get('bullish_zone') else 'Neutral zone'}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        # MACD Card
                        with ta_col2:
                            macd_trend = macd_info.get("trend", "neutral")
                            macd_color = "#00e676" if macd_trend == "bullish" else (
                                "#ff5252" if macd_trend == "bearish" else "#ffc107"
                            )
                            cross_text = ""
                            if macd_info.get("bullish_cross"):
                                cross_text = "Bullish Cross!"
                            elif macd_info.get("bearish_cross"):
                                cross_text = "Bearish Cross!"

                            st.markdown(
                                f"""
                                <div style="background:#1a1a2e;border:1px solid {macd_color}66;
                                     border-radius:8px;padding:1rem;">
                                    <div style="color:{macd_color};font-size:1.5rem;font-weight:bold;">
                                        {macd_trend.upper()}
                                    </div>
                                    <div style="color:#e0e0e0;font-weight:bold;">MACD (12,26,9)</div>
                                    <div style="color:#9e9e9e;font-size:0.85rem;margin-top:0.3rem;">
                                        MACD: {macd_info.get('macd', 0):.6f}<br>
                                        Signal: {macd_info.get('signal_line', 0):.6f}<br>
                                        Histogram: {macd_info.get('histogram', 0):.6f}
                                        {'<br><b style="color:#ffc107;">' + cross_text + '</b>' if cross_text else ''}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        # BB Card
                        with ta_col3:
                            bb_sig = bb_info.get("signal", "neutral")
                            bb_squeeze = bb_info.get("squeeze", False)
                            bb_color = "#ffc107" if bb_squeeze else (
                                "#00e676" if bb_sig == "above_upper" else
                                "#ff5252" if bb_sig == "below_lower" else "#82b1ff"
                            )

                            st.markdown(
                                f"""
                                <div style="background:#1a1a2e;border:1px solid {bb_color}66;
                                     border-radius:8px;padding:1rem;">
                                    <div style="color:{bb_color};font-size:1.5rem;font-weight:bold;">
                                        {'SQUEEZE' if bb_squeeze else bb_sig.replace('_', ' ').upper()}
                                    </div>
                                    <div style="color:#e0e0e0;font-weight:bold;">Bollinger Bands (20,2)</div>
                                    <div style="color:#9e9e9e;font-size:0.85rem;margin-top:0.3rem;">
                                        Upper: ${bb_info.get('upper', 0):,.4f}<br>
                                        Mid: ${bb_info.get('mid', 0):,.4f}<br>
                                        Lower: ${bb_info.get('lower', 0):,.4f}<br>
                                        %B: {bb_info.get('pct_b', 0):.2f} | BW: {bb_info.get('bandwidth', 0):.4f}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        # Confluence score explanation
                        st.markdown("---")
                        st.markdown("**Indicator Confluence:**")
                        confluence = []
                        if rsi_info.get("bullish_zone") or rsi_info.get("signal") == "bullish_cross":
                            confluence.append(("RSI Bullish", "#00e676"))
                        if rsi_info.get("oversold"):
                            confluence.append(("RSI Oversold (reversal)", "#ffc107"))
                        if macd_info.get("bullish_cross"):
                            confluence.append(("MACD Bullish Cross", "#00e676"))
                        if macd_info.get("trend") == "bullish":
                            confluence.append(("MACD Bullish Trend", "#66BB6A"))
                        if bb_info.get("squeeze"):
                            confluence.append(("BB Squeeze (breakout imminent)", "#ffc107"))
                        if bb_info.get("signal") == "above_upper":
                            confluence.append(("Above BB Upper (strong momentum)", "#00e676"))

                        if confluence:
                            tags_html = " ".join(
                                f'<span style="background:{c}22;color:{c};padding:3px 10px;'
                                f'border-radius:4px;font-size:0.85rem;margin:2px;">{label}</span>'
                                for label, c in confluence
                            )
                            st.markdown(tags_html, unsafe_allow_html=True)
                            st.markdown(f"**Confluence count: {len(confluence)}/6**")
                        else:
                            st.caption("No strong indicator confluence detected.")
                    else:
                        st.info("TA indicator data not available for this signal. Run a new scan to generate.")

                # ── Tab: Fibonacci (Phase 7) ──
                with tab_fib:
                    if is_cex:
                        with st.spinner("Computing Fibonacci levels..."):
                            try:
                                cex_fetcher = CEXFetcher()
                                fib_df = run_async(
                                    cex_fetcher.fetch_ohlcv(selected, timeframe="1h", limit=250)
                                )
                                run_async(cex_fetcher.close())

                                if not fib_df.empty:
                                    fig_fib, fib_data = build_fibonacci_chart(fib_df, selected)
                                    st.plotly_chart(fig_fib, use_container_width=True)

                                    # Fibonacci level table
                                    st.markdown("**Retracement Levels:**")
                                    fib_rows = []
                                    current_p = float(fib_df["close"].iloc[-1])
                                    for lvl in fib_data.get("retracement", []):
                                        dist = (lvl["price"] - current_p) / current_p * 100
                                        fib_rows.append({
                                            "Level": lvl["label"],
                                            "Price": lvl["price"],
                                            "Distance %": f"{dist:+.2f}%",
                                        })
                                    if fib_rows:
                                        st.dataframe(
                                            pd.DataFrame(fib_rows).style.format({"Price": "${:,.4f}"}),
                                            use_container_width=True,
                                        )

                                    if fib_data.get("extension"):
                                        st.markdown("**Extension Levels:**")
                                        ext_rows = []
                                        for lvl in fib_data["extension"]:
                                            dist = (lvl["price"] - current_p) / current_p * 100
                                            ext_rows.append({
                                                "Level": lvl["label"],
                                                "Price": lvl["price"],
                                                "Distance %": f"{dist:+.2f}%",
                                            })
                                        st.dataframe(
                                            pd.DataFrame(ext_rows).style.format({"Price": "${:,.4f}"}),
                                            use_container_width=True,
                                        )
                                else:
                                    st.warning("No OHLCV data available")
                            except Exception as e:
                                st.error(f"Fibonacci error: {e}")
                    else:
                        st.info("Fibonacci analysis requires CEX OHLCV data.")

                # ── Tab: S/R Zones (Phase 7) ──
                with tab_sr:
                    if is_cex:
                        with st.spinner("Finding S/R cluster zones..."):
                            try:
                                cex_fetcher = CEXFetcher()
                                sr_df = run_async(
                                    cex_fetcher.fetch_ohlcv(selected, timeframe="1h", limit=250)
                                )
                                run_async(cex_fetcher.close())

                                if not sr_df.empty:
                                    fig_sr, sr_clusters = build_sr_cluster_chart(sr_df, selected)
                                    st.plotly_chart(fig_sr, use_container_width=True)

                                    if sr_clusters:
                                        st.markdown("**Cluster Zones:**")
                                        sr_rows = []
                                        for z in sr_clusters:
                                            sr_rows.append({
                                                "Type": z["type"].title(),
                                                "Price": z["price"],
                                                "Touches": z["touches"],
                                                "Strength": f"{z['strength']:.0%}",
                                                "Distance %": f"{z['distance_pct']:+.2f}%",
                                            })
                                        sr_df_display = pd.DataFrame(sr_rows)
                                        st.dataframe(
                                            sr_df_display.style.format({"Price": "${:,.4f}"}),
                                            use_container_width=True,
                                        )
                                    else:
                                        st.info("No significant S/R clusters found.")
                                else:
                                    st.warning("No data available")
                            except Exception as e:
                                st.error(f"S/R error: {e}")
                    else:
                        st.info("S/R analysis requires CEX OHLCV data.")

                # ── Tab: BTC Correlation (Phase 7) ──
                with tab_corr:
                    if is_cex and "BTC" not in selected.upper().split("/")[0]:
                        st.caption("Rolling 30-bar correlation with BTC")
                        with st.spinner("Computing BTC correlation..."):
                            try:
                                cex_fetcher = CEXFetcher()
                                coin_df = run_async(
                                    cex_fetcher.fetch_ohlcv(selected, timeframe="1h", limit=200)
                                )
                                btc_df = run_async(
                                    cex_fetcher.fetch_ohlcv("BTC/USDT:USDT", timeframe="1h", limit=200)
                                )
                                run_async(cex_fetcher.close())

                                if not coin_df.empty and not btc_df.empty:
                                    corr_data = compute_correlation(
                                        coin_df["close"], btc_df["close"], window=30
                                    )

                                    # Summary metrics
                                    cc1, cc2, cc3, cc4 = st.columns(4)
                                    with cc1:
                                        cv = corr_data["current_corr"]
                                        c_color = "#00e676" if cv > 0.5 else ("#ff5252" if cv < -0.5 else "#ffc107")
                                        st.metric("Current", f"{cv:.3f}")
                                    with cc2:
                                        st.metric("Average", f"{corr_data['avg_corr']:.3f}")
                                    with cc3:
                                        st.metric("Min", f"{corr_data.get('min_corr', 0):.3f}")
                                    with cc4:
                                        st.metric("Max", f"{corr_data.get('max_corr', 0):.3f}")

                                    fig_corr = build_correlation_chart(
                                        corr_data["rolling"], selected.split("/")[0]
                                    )
                                    st.plotly_chart(fig_corr, use_container_width=True)

                                    # Interpretation
                                    cv = corr_data["current_corr"]
                                    if cv > 0.7:
                                        st.success("Strong positive correlation — coin moves with BTC.")
                                    elif cv > 0.3:
                                        st.info("Moderate positive correlation with BTC.")
                                    elif cv > -0.3:
                                        st.warning("Low/no correlation — independent price action.")
                                    elif cv > -0.7:
                                        st.info("Moderate negative correlation — moves opposite to BTC.")
                                    else:
                                        st.error("Strong negative correlation — inverse to BTC.")
                                else:
                                    st.warning("Insufficient data for correlation analysis.")
                            except Exception as e:
                                st.error(f"Correlation error: {e}")
                    elif "BTC" in selected.upper().split("/")[0]:
                        st.info("This is BTC itself. Select a different coin for correlation analysis.")
                    else:
                        st.info("BTC correlation requires CEX data.")

                # ── Tab: Funding Rate (CCXT + Binance History) ──
                with tab_funding:
                    if is_cex:
                        st.caption("Data source: CCXT + Binance FAPI — All free")
                        with st.spinner("Loading funding rates..."):
                            st.markdown("**Current Funding Rate (Multi-Exchange)**")
                            fr_data = run_async(MultiExchangeFundingFetcher.fetch_all(selected))
                            fig_fr = build_funding_rate_chart(fr_data, selected)
                            st.plotly_chart(fig_fr, use_container_width=True)

                            if fr_data:
                                fr_df = pd.DataFrame(fr_data)
                                fr_df["rate_pct"] = fr_df["rate"].apply(
                                    lambda x: f"{(x or 0) * 100:+.4f}%"
                                )
                                st.dataframe(
                                    fr_df[["exchange", "rate_pct"]].rename(
                                        columns={"exchange": "Exchange", "rate_pct": "Funding Rate"}
                                    ),
                                    use_container_width=True,
                                )

                            st.markdown("---")
                            st.markdown("**Funding Rate History (Binance)**")
                            fr_period = st.radio(
                                "History length", ["50", "100", "200"],
                                horizontal=True, key="fr_hist_len", index=1
                            )
                            fr_hist_df = BinanceFundingHistoryFetcher.get_funding_history(
                                selected, limit=int(fr_period)
                            )
                            if not fr_hist_df.empty:
                                fig_fr_hist = build_funding_rate_history_chart(fr_hist_df, selected)
                                st.plotly_chart(fig_fr_hist, use_container_width=True)

                                hcol1, hcol2, hcol3, hcol4 = st.columns(4)
                                with hcol1:
                                    avg_fr = fr_hist_df["fundingRate"].mean() * 100
                                    st.metric("Avg Rate", f"{avg_fr:+.4f}%")
                                with hcol2:
                                    max_fr = fr_hist_df["fundingRate"].max() * 100
                                    st.metric("Max Rate", f"{max_fr:+.4f}%")
                                with hcol3:
                                    min_fr = fr_hist_df["fundingRate"].min() * 100
                                    st.metric("Min Rate", f"{min_fr:+.4f}%")
                                with hcol4:
                                    pos_pct = (fr_hist_df["fundingRate"] > 0).mean() * 100
                                    st.metric("Positive %", f"{pos_pct:.0f}%")
                            else:
                                st.info("No historical funding rate data available.")
                    else:
                        st.info("Funding rate data is only available for CEX perpetual futures.")

                # ── Tab: Long/Short (Binance FAPI) ──
                with tab_ls:
                    if is_cex:
                        st.caption("Data source: Binance Public Futures API — Free")
                        with st.spinner("Loading long/short ratios..."):
                            st.markdown("**Current L/S Ratio**")
                            ls_data = BinanceLongShortFetcher.get_all_ratios(selected)
                            fig_ls = build_long_short_chart(ls_data, selected)
                            st.plotly_chart(fig_ls, use_container_width=True)

                            if ls_data:
                                ls_df = pd.DataFrame(ls_data)
                                ls_df["Long %"] = ls_df["longRatio"].apply(lambda x: f"{x*100:.1f}%")
                                ls_df["Short %"] = ls_df["shortRatio"].apply(lambda x: f"{x*100:.1f}%")
                                ls_df["L/S Ratio"] = ls_df["longShortRatio"].apply(lambda x: f"{x:.3f}")
                                st.dataframe(
                                    ls_df[["exchange", "Long %", "Short %", "L/S Ratio"]].rename(
                                        columns={"exchange": "Source"}
                                    ),
                                    use_container_width=True,
                                )

                            st.markdown("---")
                            st.markdown("**L/S Ratio History (Global)**")
                            ls_hist_df = BinanceLongShortFetcher.get_global_ls_history(
                                selected, period="1h", limit=48
                            )
                            if not ls_hist_df.empty:
                                fig_ls_hist = build_ls_history_chart(ls_hist_df, selected)
                                st.plotly_chart(fig_ls_hist, use_container_width=True)
                            else:
                                st.info("No historical L/S data available.")
                    else:
                        st.info("Long/Short ratio is only available for CEX perpetual futures.")

                # ── Tab: Open Interest (Binance FAPI) ──
                with tab_oi:
                    if is_cex:
                        st.caption("Data source: Binance Public Futures API — Free")
                        with st.spinner("Loading open interest..."):
                            oi_current = BinanceOpenInterestFetcher.get_current_oi(selected)
                            if oi_current:
                                oicol1, oicol2 = st.columns(2)
                                with oicol1:
                                    st.metric(
                                        "Current OI",
                                        f"{oi_current.get('openInterest', 0):,.2f} contracts",
                                    )
                                with oicol2:
                                    oi_val = oi_current.get("openInterest", 0) * sel_result.price
                                    st.metric("OI Value (est.)", f"${oi_val:,.0f}")

                            st.markdown("---")
                            oi_period = st.radio(
                                "Period", ["5m", "15m", "1h", "4h"],
                                horizontal=True, key="oi_period", index=2
                            )
                            oi_hist = BinanceOpenInterestFetcher.get_oi_history(
                                selected, period=oi_period, limit=48
                            )
                            if not oi_hist.empty:
                                fig_oi = build_open_interest_chart(oi_hist, selected)
                                st.plotly_chart(fig_oi, use_container_width=True)

                                if len(oi_hist) >= 2:
                                    oi_first = float(oi_hist["sumOpenInterestValue"].iloc[0])
                                    oi_last = float(oi_hist["sumOpenInterestValue"].iloc[-1])
                                    oi_change = ((oi_last - oi_first) / oi_first * 100) if oi_first > 0 else 0
                                    chcol1, chcol2, chcol3 = st.columns(3)
                                    with chcol1:
                                        st.metric("OI Start", f"${oi_first:,.0f}")
                                    with chcol2:
                                        st.metric("OI Latest", f"${oi_last:,.0f}")
                                    with chcol3:
                                        st.metric("OI Change", f"{oi_change:+.2f}%")
                            else:
                                st.info("No OI history data available.")
                    else:
                        st.info("Open interest data is only available for CEX perpetual futures.")

                # ── Tab: Order Book ──
                with tab_orderbook:
                    if is_cex:
                        st.caption("Data source: CCXT Order Book — Free")
                        with st.spinner("Loading order book..."):
                            try:
                                cex_fetcher = CEXFetcher()
                                ob = run_async(cex_fetcher.fetch_order_book(selected, limit=20))
                                run_async(cex_fetcher.close())

                                bids = ob.get("bids", [])
                                asks = ob.get("asks", [])

                                fig_ob = build_order_book_chart(bids, asks, selected)
                                st.plotly_chart(fig_ob, use_container_width=True)

                                st.markdown("---")
                                fig_hm = build_order_book_heatmap(bids, asks, selected)
                                st.plotly_chart(fig_hm, use_container_width=True)

                                st.markdown("---")
                                st.markdown("**Whale Walls (Top 5 by size)**")
                                all_levels = (
                                    [("Bid", b[0], b[1]) for b in bids]
                                    + [("Ask", a[0], a[1]) for a in asks]
                                )
                                all_levels.sort(key=lambda x: x[2], reverse=True)

                                if all_levels:
                                    sizes = [l[2] for l in all_levels]
                                    import numpy as np_ob
                                    mean_size = np_ob.mean(sizes)
                                    std_size = np_ob.std(sizes)

                                    whale_rows = []
                                    for side, price, size in all_levels[:10]:
                                        z_score = (size - mean_size) / std_size if std_size > 0 else 0
                                        is_whale = z_score > 2.0
                                        whale_rows.append({
                                            "Side": side,
                                            "Price": price,
                                            "Size": size,
                                            "Value (USD)": price * size,
                                            "Z-Score": round(z_score, 2),
                                            "Whale": "YES" if is_whale else "",
                                        })

                                    whale_df = pd.DataFrame(whale_rows[:5])
                                    st.dataframe(
                                        whale_df.style.format({
                                            "Price": "${:,.2f}",
                                            "Size": "{:,.4f}",
                                            "Value (USD)": "${:,.0f}",
                                            "Z-Score": "{:.2f}",
                                        }),
                                        use_container_width=True,
                                    )

                                    total_bid = sum(b[1] for b in bids)
                                    total_ask = sum(a[1] for a in asks)
                                    imbalance = (total_bid - total_ask) / (total_bid + total_ask) * 100 if (total_bid + total_ask) > 0 else 0
                                    imcol1, imcol2, imcol3 = st.columns(3)
                                    with imcol1:
                                        st.metric("Total Bid Size", f"{total_bid:,.2f}")
                                    with imcol2:
                                        st.metric("Total Ask Size", f"{total_ask:,.2f}")
                                    with imcol3:
                                        st.metric("Bid/Ask Imbalance", f"{imbalance:+.1f}%")

                            except Exception as e:
                                st.error(f"Order book error: {e}")
                    else:
                        st.info("Order book depth is only available for CEX pairs.")

                # ── Tab: Liquidation Levels ──
                with tab_liq:
                    if is_cex:
                        st.caption("Estimated liquidation prices assuming entry at current price")
                        fig_liq = build_liquidation_chart(sel_result.price, selected)
                        st.plotly_chart(fig_liq, use_container_width=True)

                        st.markdown("**Liquidation Price Table**")
                        leverages = [2, 3, 5, 10, 20, 25, 50, 100]
                        liq_rows = []
                        for lev in leverages:
                            long_liq = sel_result.price * (1 - 1 / lev)
                            short_liq = sel_result.price * (1 + 1 / lev)
                            long_dist = (sel_result.price - long_liq) / sel_result.price * 100
                            short_dist = (short_liq - sel_result.price) / sel_result.price * 100
                            liq_rows.append({
                                "Leverage": f"{lev}x",
                                "Long Liq Price": long_liq,
                                "Long Distance %": long_dist,
                                "Short Liq Price": short_liq,
                                "Short Distance %": short_dist,
                            })
                        liq_df = pd.DataFrame(liq_rows)
                        st.dataframe(
                            liq_df.style.format({
                                "Long Liq Price": "${:,.4f}",
                                "Long Distance %": "{:.2f}%",
                                "Short Liq Price": "${:,.4f}",
                                "Short Distance %": "{:.2f}%",
                            }),
                            use_container_width=True,
                        )

                        st.caption(
                            "Note: Actual liquidation depends on margin mode (cross/isolated), "
                            "maintenance margin rate, and unrealized PnL. These are simplified estimates."
                        )
                    else:
                        st.info("Liquidation data is only available for CEX perpetual futures.")

                # ── Tab: News/Social ──
                with tab_social:
                    st.caption("Data source: CryptoPanic — Free tier (no API key required)")
                    with st.spinner("Loading news & social data..."):
                        social_data = CryptoPanicFetcher.detect_social_boost(selected)

                        scol1, scol2, scol3 = st.columns(3)
                        with scol1:
                            boost_text = "Detected" if social_data["boost"] else "None"
                            st.metric("Social Boost", boost_text)
                        with scol2:
                            st.metric("Total Posts", social_data["total_posts"])
                        with scol3:
                            st.metric("Breakout Mentions", social_data["breakout_mentions"])

                        if social_data["matching_titles"]:
                            st.markdown("**Matching Headlines:**")
                            for title in social_data["matching_titles"]:
                                st.markdown(f"- {title}")

                        news = CryptoPanicFetcher.get_news(selected, limit=5)
                        if news:
                            st.markdown("**Recent News:**")
                            for post in news:
                                title = post.get("title", "")
                                source = post.get("source", {}).get("title", "")
                                st.markdown(f"- **{title}** ({source})")

                # ── Signal summary panel ──
                st.markdown("---")
                st.markdown("#### Signal Summary")
                scol1, scol2, scol3, scol4 = st.columns(4)
                with scol1:
                    st.metric("Score", f"{sel_result.score:.1f}/100")
                with scol2:
                    emoji = "Yes" if sel_result.above_ema else "No"
                    st.metric("Above 200 EMA", emoji)
                with scol3:
                    st.metric("Volume Spike", f"{sel_result.volume_ratio:.1f}x")
                with scol4:
                    bt = sel_result.trendline_break.get("breakout_type") or "None"
                    st.metric("Breakout", bt.capitalize())

                scol5, scol6, scol7, scol8 = st.columns(4)
                with scol5:
                    pattern = sel_result.trendline_break.get("pattern_label", "—")
                    st.metric("Pattern", pattern)
                with scol6:
                    vc = "Yes" if sel_result.trendline_break.get("volume_confirmed") else "No"
                    st.metric("Vol Confirmed", vc)
                with scol7:
                    cb = sel_result.trendline_break.get("confirmation_bars", 0)
                    st.metric("Confirm Bars", cb)
                with scol8:
                    mtf = "Yes" if sel_result.trendline_break.get("multi_tf_confirmed") else "No"
                    st.metric("Multi-TF", mtf)


# ════════════════════════════════════════════════
# TAB: HEATMAP (Phase 6)
# ════════════════════════════════════════════════
with main_tab_heatmap:
    st.markdown("### Signal Heatmap")
    st.caption("Treemap visualization — size = 24h volume, color = selected metric")

    results_for_heatmap: list[ScanResult] = st.session_state.results

    if not results_for_heatmap:
        st.info("Run a scan first to see the heatmap.")
    else:
        hm_color = st.radio(
            "Color by", ["score", "change_pct", "volume_ratio"],
            horizontal=True, key="hm_color",
            format_func=lambda x: {"score": "Score", "change_pct": "24h Change %",
                                   "volume_ratio": "Volume Ratio"}[x]
        )
        fig_hm = build_signal_heatmap(results_for_heatmap, color_by=hm_color)
        st.plotly_chart(fig_hm, use_container_width=True)

        # Summary stats below heatmap
        hm_col1, hm_col2, hm_col3, hm_col4 = st.columns(4)
        with hm_col1:
            top_score = max(results_for_heatmap, key=lambda r: r.score)
            st.metric("Top Score", f"{top_score.symbol.split('/')[0]} ({top_score.score:.0f})")
        with hm_col2:
            top_change = max(results_for_heatmap, key=lambda r: r.change_pct)
            st.metric("Top Change", f"{top_change.symbol.split('/')[0]} ({top_change.change_pct:+.1f}%)")
        with hm_col3:
            top_vol = max(results_for_heatmap, key=lambda r: r.volume_ratio)
            st.metric("Top Vol Ratio", f"{top_vol.symbol.split('/')[0]} ({top_vol.volume_ratio:.1f}x)")
        with hm_col4:
            bullish_count = sum(1 for r in results_for_heatmap
                                if r.trendline_break.get("breakout_type") == "bullish")
            st.metric("Bullish / Total", f"{bullish_count} / {len(results_for_heatmap)}")


# ════════════════════════════════════════════════
# TAB: RISK CALCULATOR (Phase 7)
# ════════════════════════════════════════════════
with main_tab_risk:
    st.markdown("### Position Size & Risk/Reward Calculator")
    st.caption("Calculate optimal position size based on your risk tolerance.")

    rk_col1, rk_col2 = st.columns(2)
    with rk_col1:
        account_size = st.number_input("Account Size (USD)", min_value=100.0, value=10000.0, step=500.0, key="rk_acct")
        risk_pct = st.slider("Risk per Trade (%)", 0.5, 5.0, 1.0, step=0.25, key="rk_risk")
        entry_price = st.number_input("Entry Price", min_value=0.0001, value=100.0, step=0.01, key="rk_entry")
    with rk_col2:
        stop_loss_price = st.number_input("Stop Loss Price", min_value=0.0001, value=97.0, step=0.01, key="rk_sl")
        take_profit_price = st.number_input("Take Profit Price", min_value=0.0001, value=106.0, step=0.01, key="rk_tp")
        leverage = st.selectbox("Leverage", [1, 2, 3, 5, 10, 20, 25, 50], index=0, key="rk_lev")

    if entry_price > 0 and stop_loss_price > 0 and stop_loss_price != entry_price:
        risk_amount = account_size * (risk_pct / 100)
        sl_distance = abs(entry_price - stop_loss_price)
        sl_pct = sl_distance / entry_price * 100
        tp_distance = abs(take_profit_price - entry_price)
        tp_pct = tp_distance / entry_price * 100

        # Position size
        position_size_units = risk_amount / sl_distance
        position_value = position_size_units * entry_price
        position_with_leverage = position_value / leverage if leverage > 0 else position_value

        # Risk/Reward ratio
        rr_ratio = tp_distance / sl_distance if sl_distance > 0 else 0

        # P&L at TP and SL
        pnl_at_tp = position_size_units * tp_distance * leverage
        pnl_at_sl = -risk_amount * leverage

        st.markdown("---")
        st.markdown("#### Results")

        r_col1, r_col2, r_col3, r_col4 = st.columns(4)
        with r_col1:
            st.metric("Position Size", f"{position_size_units:,.4f} units")
            st.metric("Position Value", f"${position_value:,.2f}")
        with r_col2:
            st.metric("Margin Required", f"${position_with_leverage:,.2f}")
            st.metric("Leverage", f"{leverage}x")
        with r_col3:
            rr_color = "normal" if rr_ratio >= 2 else "inverse"
            st.metric("Risk:Reward", f"1:{rr_ratio:.2f}")
            st.metric("Risk Amount", f"${risk_amount:,.2f}")
        with r_col4:
            st.metric("Profit at TP", f"${pnl_at_tp:,.2f} (+{tp_pct:.2f}%)")
            st.metric("Loss at SL", f"-${abs(pnl_at_sl):,.2f} (-{sl_pct:.2f}%)")

        # Visual R/R bar
        total_range = tp_distance + sl_distance
        tp_ratio = tp_distance / total_range * 100
        sl_ratio = sl_distance / total_range * 100

        st.markdown(
            f"""
            <div style="margin:1rem 0;">
                <div style="display:flex;height:30px;border-radius:6px;overflow:hidden;">
                    <div style="width:{sl_ratio}%;background:#ef5350;display:flex;
                         align-items:center;justify-content:center;font-size:0.8rem;color:white;
                         font-weight:bold;">SL -{sl_pct:.1f}%</div>
                    <div style="width:{tp_ratio}%;background:#26a69a;display:flex;
                         align-items:center;justify-content:center;font-size:0.8rem;color:white;
                         font-weight:bold;">TP +{tp_pct:.1f}%</div>
                </div>
                <div style="color:#9e9e9e;font-size:0.8rem;margin-top:4px;text-align:center;">
                    R:R = 1:{rr_ratio:.2f} {'(Good)' if rr_ratio >= 2 else '(Consider improving)' if rr_ratio >= 1 else '(Poor — TP < SL)'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Kelly Criterion (simplified)
        if rr_ratio > 0:
            # Assume 50% win rate as default
            assumed_wr = 0.5
            kelly_pct = (assumed_wr * rr_ratio - (1 - assumed_wr)) / rr_ratio
            kelly_pct = max(kelly_pct, 0)
            st.caption(
                f"Kelly Criterion (50% win rate): {kelly_pct:.1%} of account per trade. "
                f"Half-Kelly (safer): {kelly_pct/2:.1%}"
            )

    # CSV Export section
    st.markdown("---")
    st.markdown("### Export Data")
    results_for_export: list[ScanResult] = st.session_state.results
    if results_for_export:
        export_rows = [r.to_dict() for r in results_for_export]
        export_df = pd.DataFrame(export_rows)
        csv_data = export_df.to_csv(index=False)
        st.download_button(
            "Download Scan Results (CSV)",
            csv_data,
            file_name="scan_results.csv",
            mime="text/csv",
            key="csv_export",
        )
    else:
        st.caption("Run a scan first to enable CSV export.")

    history = load_signal_history()
    if history:
        hist_csv = pd.DataFrame(history).to_csv(index=False)
        st.download_button(
            "Download Signal History (CSV)",
            hist_csv,
            file_name="signal_history.csv",
            mime="text/csv",
            key="csv_history_export",
        )


# ════════════════════════════════════════════════
# TAB: BACKTEST (Phase 6)
# ════════════════════════════════════════════════
with main_tab_backtest:
    st.markdown("### Mini Backtester")
    st.caption(
        "Backtest the trendline break strategy on historical data. "
        "Uses the Phase 6 multi-indicator scoring (RSI + MACD + BB + trendline)."
    )

    bt_col1, bt_col2 = st.columns(2)
    with bt_col1:
        bt_symbol = st.text_input("Symbol", value="BTC/USDT:USDT", key="bt_symbol")
        bt_exchange = st.selectbox("Exchange", ["binance", "bybit"], key="bt_exchange")
        bt_timeframe = st.selectbox("Timeframe", ["1h", "4h"], key="bt_tf")
        bt_bars = st.slider("History (bars)", 200, 1000, 500, step=100, key="bt_bars")
    with bt_col2:
        bt_tp = st.slider("Take Profit %", 1.0, 10.0, 3.0, step=0.5, key="bt_tp")
        bt_sl = st.slider("Stop Loss %", 0.5, 5.0, 2.0, step=0.5, key="bt_sl")
        bt_max_hold = st.slider("Max Hold (bars)", 6, 48, 24, step=6, key="bt_hold")
        bt_min_score = st.slider("Min Score to Enter", 20, 80, 40, step=5, key="bt_score")

    if st.button("Run Backtest", type="primary", key="bt_run"):
        with st.spinner(f"Backtesting {bt_symbol} on {bt_exchange} ({bt_bars} bars)..."):
            try:
                backtester = MiniBacktester(
                    take_profit_pct=bt_tp,
                    stop_loss_pct=bt_sl,
                    max_hold_bars=bt_max_hold,
                    min_score=bt_min_score,
                )
                bt_result = run_async(
                    backtester.run_backtest(bt_symbol, bt_exchange, bt_timeframe, bt_bars)
                )

                trades = bt_result["trades"]
                stats = bt_result["stats"]

                if stats.get("error"):
                    st.error(stats["error"])
                elif not trades:
                    st.warning("No trades generated. Try lowering the min score or using more bars.")
                else:
                    # Stats cards
                    st.markdown("#### Backtest Results")
                    bc1, bc2, bc3, bc4, bc5 = st.columns(5)
                    with bc1:
                        st.metric("Total Trades", stats["total"])
                    with bc2:
                        wr_color = "normal" if stats["win_rate"] >= 0.5 else "inverse"
                        st.metric("Win Rate", f"{stats['win_rate']:.1%}")
                    with bc3:
                        st.metric("Total PnL", f"{stats['total_pnl']:+.2f}%")
                    with bc4:
                        st.metric("Profit Factor", f"{stats['profit_factor']:.2f}")
                    with bc5:
                        st.metric("Avg Bars Held", f"{stats['avg_bars']:.0f}")

                    bc6, bc7, bc8, bc9 = st.columns(4)
                    with bc6:
                        st.metric("Wins", stats["wins"])
                    with bc7:
                        st.metric("Losses", stats["losses"])
                    with bc8:
                        st.metric("Max Win", f"{stats['max_win']:+.2f}%")
                    with bc9:
                        st.metric("Max Loss", f"{stats['max_loss']:+.2f}%")

                    # Equity curve chart
                    fig_bt = build_backtest_chart(trades, bt_symbol)
                    st.plotly_chart(fig_bt, use_container_width=True)

                    # Trade log
                    with st.expander("Trade Log", expanded=False):
                        trades_df = pd.DataFrame(trades)
                        st.dataframe(
                            trades_df.style.format({
                                "entry_price": "${:,.4f}",
                                "exit_price": "${:,.4f}",
                                "pnl_pct": "{:+.2f}%",
                            }),
                            use_container_width=True,
                        )

            except Exception as e:
                st.error(f"Backtest failed: {e}")
                logger.exception("Backtest error")


# ════════════════════════════════════════════════
# TAB: SIGNAL HISTORY (Phase 5)
# ════════════════════════════════════════════════
with main_tab_history:
    st.markdown("### Signal History & Hit-Rate Analysis")
    st.caption("Tracks past signals and checks if price rose >2% within 24 hours")

    # Hit rate stats card
    stats = compute_hit_rate_stats()

    st.markdown(
        f"""
        <div class="hit-rate-card">
            <div style="display:flex;gap:2rem;align-items:center;flex-wrap:wrap;">
                <div>
                    <div style="color:#9e9e9e;font-size:0.8rem;">Total Signals</div>
                    <div style="color:#e0e0e0;font-size:1.5rem;font-weight:bold;">{stats['total']}</div>
                </div>
                <div>
                    <div style="color:#9e9e9e;font-size:0.8rem;">Resolved</div>
                    <div style="color:#e0e0e0;font-size:1.5rem;font-weight:bold;">{stats['resolved']}</div>
                </div>
                <div>
                    <div style="color:#9e9e9e;font-size:0.8rem;">Hits (>2%)</div>
                    <div style="color:#00e676;font-size:1.5rem;font-weight:bold;">{stats['hits']}</div>
                </div>
                <div>
                    <div style="color:#9e9e9e;font-size:0.8rem;">Misses</div>
                    <div style="color:#ff5252;font-size:1.5rem;font-weight:bold;">{stats['misses']}</div>
                </div>
                <div>
                    <div style="color:#9e9e9e;font-size:0.8rem;">Hit Rate</div>
                    <div style="color:#ffc107;font-size:1.5rem;font-weight:bold;">{stats['hit_rate']:.1%}</div>
                </div>
                <div>
                    <div style="color:#9e9e9e;font-size:0.8rem;">Avg Max Gain</div>
                    <div style="color:#82b1ff;font-size:1.5rem;font-weight:bold;">{stats['avg_gain']:+.2f}%</div>
                </div>
                <div>
                    <div style="color:#9e9e9e;font-size:0.8rem;">Pending</div>
                    <div style="color:#9e9e9e;font-size:1.5rem;font-weight:bold;">{stats.get('pending', 0)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Update outcomes button
    col_h1, col_h2, col_h3 = st.columns([1, 1, 4])
    with col_h1:
        if st.button("Update Outcomes", key="update_outcomes"):
            with st.spinner("Checking past signal prices..."):
                run_async(update_signal_outcomes())
            st.rerun()
    with col_h2:
        if st.button("Clear History", key="clear_history"):
            from scanner_engine import save_signal_history
            save_signal_history([])
            st.rerun()

    # Show history table
    history = load_signal_history()
    if history:
        hist_df = pd.DataFrame(history[-50:][::-1])  # Latest 50, newest first
        display_cols = [
            "symbol", "score", "breakout_type", "pattern", "price_at_signal",
            "price_after_1h", "price_after_4h", "price_after_24h",
            "hit", "scan_time",
        ]
        available_cols = [c for c in display_cols if c in hist_df.columns]
        hist_display = hist_df[available_cols].copy()

        # Rename for display
        hist_display.columns = [
            c.replace("_", " ").title() for c in hist_display.columns
        ]

        st.dataframe(hist_display, use_container_width=True, height=400)
    else:
        st.info("No signal history yet. Run a scan to start recording signals.")


# ════════════════════════════════════════════════
# TAB: ALERT SETTINGS (Phase 5)
# ════════════════════════════════════════════════
with main_tab_alerts:
    st.markdown("### Alert Configuration")
    st.caption("Configure alert conditions. Matching signals will be highlighted after each scan.")

    # Existing alerts
    alerts = load_alerts()
    if alerts:
        st.markdown("**Active Alerts:**")
        for i, alert in enumerate(alerts):
            enabled_icon = "ON" if alert.get("enabled", True) else "OFF"
            enabled_color = "#00e676" if alert.get("enabled", True) else "#616161"

            acol1, acol2, acol3 = st.columns([3, 1, 1])
            with acol1:
                conditions = []
                conditions.append(f"Score >= {alert.get('min_score', 0)}")
                if alert.get("breakout_type") and alert["breakout_type"] != "any":
                    conditions.append(f"Type: {alert['breakout_type']}")
                if alert.get("patterns"):
                    conditions.append(f"Patterns: {', '.join(alert['patterns'])}")
                if alert.get("min_volume_ratio"):
                    conditions.append(f"Vol >= {alert['min_volume_ratio']}x")
                if alert.get("require_social"):
                    conditions.append("Social required")
                if alert.get("require_multi_tf"):
                    conditions.append("Multi-TF required")
                if alert.get("symbols"):
                    conditions.append(f"Symbols: {', '.join(alert['symbols'][:3])}")

                st.markdown(
                    f"<span style='color:{enabled_color};font-weight:bold;'>[{enabled_icon}]</span> "
                    f"**{alert.get('name', 'Unnamed')}** — {' | '.join(conditions)}",
                    unsafe_allow_html=True,
                )
            with acol2:
                if st.button("Toggle", key=f"alert_toggle_{i}"):
                    alerts[i]["enabled"] = not alerts[i].get("enabled", True)
                    save_alerts(alerts)
                    st.rerun()
            with acol3:
                if st.button("Delete", key=f"alert_del_{i}"):
                    remove_alert(i)
                    st.rerun()
    else:
        st.info("No alerts configured. Create one below.")

    # Create new alert
    st.markdown("---")
    st.markdown("**Create New Alert**")

    with st.form("new_alert_form"):
        a_name = st.text_input("Alert Name", value="High Score Bullish")
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            a_min_score = st.slider("Min Score", 0, 100, 60, step=5, key="alert_score")
            a_breakout = st.selectbox(
                "Breakout Type",
                ["any", "bullish", "bearish"],
                index=0,
                key="alert_breakout",
            )
            a_min_vol = st.number_input(
                "Min Volume Ratio (0 = any)", min_value=0.0, max_value=20.0,
                value=0.0, step=0.5, key="alert_vol"
            )
        with a_col2:
            a_social = st.checkbox("Require Social Boost", key="alert_social")
            a_multi_tf = st.checkbox("Require Multi-TF Confirm", key="alert_mtf")
            a_symbols_str = st.text_input(
                "Symbols (comma-separated, empty = all)",
                value="", key="alert_symbols"
            )

        submitted = st.form_submit_button("Create Alert")
        if submitted:
            new_alert = {
                "name": a_name,
                "min_score": a_min_score,
                "breakout_type": a_breakout,
                "min_volume_ratio": a_min_vol if a_min_vol > 0 else None,
                "require_social": a_social,
                "require_multi_tf": a_multi_tf,
                "symbols": [s.strip().upper() for s in a_symbols_str.split(",") if s.strip()] or None,
                "patterns": None,
            }
            add_alert(new_alert)
            st.success(f"Alert '{a_name}' created!")
            st.rerun()


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Crypto Trendline Break Scanner v7.0 — Phase 7 | 100% Free APIs "
    "| Fibonacci + S/R Clusters + BTC Correlation + Risk Calculator + CSV Export "
    "| RSI + MACD + BB + Heatmap + Backtester "
    "| Market Dashboard + Watchlist + Signal History + Alerts "
    "| Multi-CEX (Binance + Bybit) + DEX "
    "| CCXT + Binance FAPI + DexScreener + CryptoPanic | "
    "Not financial advice. DYOR."
)
