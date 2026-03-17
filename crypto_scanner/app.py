"""
Crypto Trendline Break Scanner — Streamlit App
================================================
6時間以内トレンドラインブレイク検知スキャナー
100% 無料API構成: CCXT + Binance Public FAPI + DexScreener + CryptoPanic
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
    /* Fundamental driver window animation */
    @keyframes funda-pulse {
        0%, 100% { border-left-color: #448AFF; }
        50% { border-left-color: #82B1FF; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

from scanner_engine import ScannerEngine, ScanResult
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
)
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
    sort_col = st.selectbox("Sort Column", ["Score", "Vol Ratio", "24h %", "Price", "Break Strength"], index=0)
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

    st.markdown("---")
    st.markdown("**Data Sources** <span class='free-badge'>ALL FREE</span>", unsafe_allow_html=True)
    st.caption("CCXT: OHLCV, Funding Rate, Order Book")
    st.caption("Binance FAPI: Long/Short Ratio")
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
        <span class="free-badge">100% FREE APIs</span></p>
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

            is_cex = "Binance" in sel_result.source

            # ──────────────────────────────────────
            # Fundamental Driver Detection Window
            # ──────────────────────────────────────
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

                    # Category breakdown cards
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

                    # Show matched articles in expander
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

            tab_chart, tab_funding, tab_ls, tab_oi, tab_orderbook, tab_liq, tab_social = st.tabs(
                ["Chart", "Funding Rate", "Long/Short", "Open Interest", "Order Book", "Liquidation", "News/Social"]
            )

            # ── Tab: Chart ──
            with tab_chart:
                timeframe = st.radio(
                    "Timeframe", ["1h", "4h"], horizontal=True, key="tf_radio"
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

            # ── Tab: Funding Rate (CCXT + Binance History) ──
            with tab_funding:
                if is_cex:
                    st.caption("Data source: CCXT + Binance FAPI — All free")
                    with st.spinner("Loading funding rates..."):
                        # Current rates across exchanges
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

                        # Historical funding rate
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

                            # Summary stats
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

            # ── Tab: Long/Short (Binance FAPI — current + history) ──
            with tab_ls:
                if is_cex:
                    st.caption("Data source: Binance Public Futures API — Free")
                    with st.spinner("Loading long/short ratios..."):
                        # Current snapshot
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

                        # Historical timeline
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

            # ── Tab: Open Interest (Binance FAPI — free) ──
            with tab_oi:
                if is_cex:
                    st.caption("Data source: Binance Public Futures API — Free")
                    with st.spinner("Loading open interest..."):
                        # Current OI
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

                        # Historical OI
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

                            # OI change metrics
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

            # ── Tab: Order Book (CCXT — free) ──
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

                            # Depth chart
                            fig_ob = build_order_book_chart(bids, asks, selected)
                            st.plotly_chart(fig_ob, use_container_width=True)

                            # Heatmap
                            st.markdown("---")
                            fig_hm = build_order_book_heatmap(bids, asks, selected)
                            st.plotly_chart(fig_hm, use_container_width=True)

                            # Whale wall detection (improved)
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

                                # Bid/Ask imbalance
                                total_bid = sum(b[1] for b in bids)
                                total_ask = sum(a[1] for a in asks)
                                imbalance = (total_bid - total_ask) / (total_bid + total_ask) * 100 if (total_bid + total_ask) > 0 else 0
                                imcol1, imcol2, imcol3 = st.columns(3)
                                with imcol1:
                                    st.metric("Total Bid Size", f"{total_bid:,.2f}")
                                with imcol2:
                                    st.metric("Total Ask Size", f"{total_ask:,.2f}")
                                with imcol3:
                                    color = "normal" if abs(imbalance) < 10 else ("inverse" if imbalance < 0 else "normal")
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

            # ── Tab: News/Social (CryptoPanic — free) ──
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

                    # Show recent news
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

            # Phase 2 extra details
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


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Crypto Trendline Break Scanner v3.0 — Phase 3 | 100% Free APIs "
    "| FR History + L/S Timeline + Open Interest + Order Book Heatmap + Liquidation "
    "| CCXT + Binance FAPI + DexScreener + CryptoPanic | "
    "Not financial advice. DYOR."
)
