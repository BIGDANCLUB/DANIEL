"""
Crypto Trendline Break Scanner — Streamlit App
================================================
6時間以内トレンドラインブレイク検知スキャナー

Phase 1: Binance Futures + DexScreener + 基本条件フィルタ + 詳細ビュー
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
    /* Global dark theme tweaks */
    .stApp {
        background-color: #0e1117;
    }
    .main .block-container {
        padding-top: 1rem;
    }
    /* Score badge colors */
    .score-high { color: #00e676; font-weight: bold; }
    .score-mid  { color: #ffc107; font-weight: bold; }
    .score-low  { color: #ff5252; font-weight: bold; }
    /* Header */
    .scanner-header {
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .scanner-header h1 {
        color: #e0e0e0;
        margin: 0;
        font-size: 1.6rem;
    }
    .scanner-header p {
        color: #9e9e9e;
        margin: 0.3rem 0 0 0;
        font-size: 0.9rem;
    }
    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        padding: 0.8rem;
    }
    /* Table styling */
    .dataframe {
        font-size: 0.85rem;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a2e;
        border-radius: 4px 4px 0 0;
        padding: 0.5rem 1rem;
        color: #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

from scanner_engine import ScannerEngine, ScanResult
from chart_builder import (
    build_candlestick_chart,
    build_order_book_chart,
    build_funding_rate_chart,
    build_long_short_chart,
)
from data_fetcher import CEXFetcher, CoinGlassFetcher, LunarCrushFetcher


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
    show_cex = st.checkbox("CEX (Binance Futures)", value=True)
    show_dex = st.checkbox("DEX (DexScreener)", value=True)

    st.markdown("---")
    st.markdown("**Sort By**")
    sort_col = st.selectbox("Sort Column", ["Score", "Vol Ratio", "24h %", "Price"], index=0)
    sort_asc = st.checkbox("Ascending", value=False)

    st.markdown("---")
    st.markdown("**Auto Refresh**")
    auto_refresh = st.checkbox("Auto refresh (60s)", value=False)

    st.markdown("---")
    st.markdown("**Status**")
    if st.session_state.last_scan_time:
        st.caption(f"Last scan: {st.session_state.last_scan_time.strftime('%H:%M:%S UTC')}")
    else:
        st.caption("No scan yet")

    # API key status
    from config import Config
    st.markdown("**API Keys**")
    st.caption(f"CoinGlass: {'Set' if Config.COINGLASS_API_KEY else 'Not set'}")
    st.caption(f"LunarCrush: {'Set' if Config.LUNARCRUSH_API_KEY else 'Not set'}")


# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="scanner-header">
        <h1>Crypto Trendline Break Scanner</h1>
        <p>6時間以内トレンドラインブレイク検知 — Volume Spike + 200 EMA + Trendline Break + Social Boost</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# Scan button
# ──────────────────────────────────────────────
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
with col_btn1:
    scan_clicked = st.button("Scan Now", type="primary", use_container_width=True)
with col_btn2:
    clear_clicked = st.button("Clear", use_container_width=True)

if clear_clicked:
    st.session_state.results = []
    st.session_state.selected_symbol = None
    st.rerun()

if scan_clicked:
    st.session_state.scan_running = True
    with st.spinner("Scanning markets... (CEX + DEX, this may take 30-90 seconds)"):
        try:
            from config import Config as cfg
            cfg.VOLUME_SPIKE_MULTIPLIER = vol_multiplier

            scanner = st.session_state.scanner
            results = run_async(scanner.run_full_scan())

            # Filter by source preference
            filtered = []
            for r in results:
                if "Binance" in r.source and not show_cex:
                    continue
                if "DEX" in r.source and not show_dex:
                    continue
                if r.score >= min_score:
                    filtered.append(r)

            st.session_state.results = filtered
            st.session_state.last_scan_time = datetime.now(timezone.utc)
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
# Results table
# ──────────────────────────────────────────────
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
        cex_count = sum(1 for r in results if "Binance" in r.source)
        st.metric("CEX Signals", cex_count)
    with mcol5:
        dex_count = sum(1 for r in results if "DEX" in r.source)
        st.metric("DEX Signals", dex_count)

    st.markdown("---")

    # Build dataframe
    rows = [r.to_dict() for r in results]
    df_results = pd.DataFrame(rows)

    # Sort
    if sort_col in df_results.columns:
        df_results = df_results.sort_values(sort_col, ascending=sort_asc)

    # Color-code score column
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

    styled = df_results.style.applymap(color_score, subset=["Score"])
    styled = styled.applymap(color_change, subset=["24h %", "Vol Ratio"])
    styled = styled.applymap(highlight_break, subset=["Trendline Break"])
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

            tab_chart, tab_funding, tab_ls, tab_orderbook = st.tabs(
                ["Chart", "Funding Rate", "Long/Short", "Order Book"]
            )

            # ── Tab: Chart ──
            with tab_chart:
                timeframe = st.radio(
                    "Timeframe", ["1h", "4h"], horizontal=True, key="tf_radio"
                )

                is_cex = "Binance" in sel_result.source

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
                                    ohlcv_df, selected, show_trendlines=True
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

            # ── Tab: Funding Rate ──
            with tab_funding:
                if is_cex:
                    with st.spinner("Loading funding rates..."):
                        fr_data = CoinGlassFetcher.get_funding_rate(selected)
                        fig_fr = build_funding_rate_chart(fr_data, selected)
                        st.plotly_chart(fig_fr, use_container_width=True)

                        if not fr_data:
                            st.info(
                                "No funding rate data. Set COINGLASS_API_KEY in .env "
                                "to enable this feature."
                            )
                else:
                    st.info("Funding rate data is only available for CEX perpetual futures.")

            # ── Tab: Long/Short ──
            with tab_ls:
                if is_cex:
                    with st.spinner("Loading long/short ratio..."):
                        ls_data = CoinGlassFetcher.get_long_short_ratio(selected)
                        fig_ls = build_long_short_chart(ls_data, selected)
                        st.plotly_chart(fig_ls, use_container_width=True)

                        if not ls_data:
                            st.info(
                                "No long/short data. Set COINGLASS_API_KEY in .env "
                                "to enable this feature."
                            )
                else:
                    st.info("Long/Short ratio is only available for CEX perpetual futures.")

            # ── Tab: Order Book ──
            with tab_orderbook:
                if is_cex:
                    with st.spinner("Loading order book..."):
                        try:
                            cex_fetcher = CEXFetcher()
                            ob = run_async(cex_fetcher.fetch_order_book(selected, limit=20))
                            run_async(cex_fetcher.close())

                            bids = ob.get("bids", [])
                            asks = ob.get("asks", [])

                            fig_ob = build_order_book_chart(bids, asks, selected)
                            st.plotly_chart(fig_ob, use_container_width=True)

                            # Whale wall detection
                            st.markdown("**Whale Walls (Top 5 by size)**")
                            all_levels = (
                                [("Bid", b[0], b[1]) for b in bids]
                                + [("Ask", a[0], a[1]) for a in asks]
                            )
                            all_levels.sort(key=lambda x: x[2], reverse=True)
                            whale_df = pd.DataFrame(
                                all_levels[:5], columns=["Side", "Price", "Size"]
                            )
                            whale_df["Value (USD)"] = whale_df["Price"] * whale_df["Size"]
                            st.dataframe(
                                whale_df.style.format({
                                    "Price": "${:,.2f}",
                                    "Size": "{:,.4f}",
                                    "Value (USD)": "${:,.0f}",
                                }),
                                use_container_width=True,
                            )
                        except Exception as e:
                            st.error(f"Order book error: {e}")
                else:
                    st.info("Order book depth is only available for CEX pairs.")

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


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Crypto Trendline Break Scanner v1.0 — Phase 1 "
    "| Data: Binance (CCXT) + DexScreener | "
    "Not financial advice. DYOR."
)
