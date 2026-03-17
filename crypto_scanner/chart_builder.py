"""Chart builder: Plotly candlestick + volume with 200EMA overlay — Phase 2."""

import logging

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

logger = logging.getLogger(__name__)

from technical_analysis import (
    compute_ema,
    get_volume_spike_mask,
    find_swing_points_adaptive,
    fit_trendline_ransac,
    classify_pattern,
    PATTERN_LABELS,
)


def build_candlestick_chart(
    df: pd.DataFrame,
    symbol: str,
    ema_period: int = 200,
    show_trendlines: bool = True,
    height: int = 700,
) -> go.Figure:
    """
    Build interactive Plotly candlestick chart with:
    - Candlestick (main)
    - Volume bars (subplot) with spike coloring
    - 200 EMA overlay
    - Optional trendlines
    """
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25],
        subplot_titles=[f"{symbol} — Candlestick", "Volume"],
    )

    # Reset index for plotly (need datetime column)
    plot_df = df.reset_index()
    if "timestamp" not in plot_df.columns:
        plot_df["timestamp"] = plot_df.index

    # ── Candlestick ──
    fig.add_trace(
        go.Candlestick(
            x=plot_df["timestamp"],
            open=plot_df["open"],
            high=plot_df["high"],
            low=plot_df["low"],
            close=plot_df["close"],
            name="OHLC",
            increasing_line_color="#26a69a",
            decreasing_line_color="#ef5350",
        ),
        row=1,
        col=1,
    )

    # ── 200 EMA overlay ──
    ema = compute_ema(df, period=ema_period)
    if ema is not None and not ema.dropna().empty:
        ema_reset = ema.reset_index()
        fig.add_trace(
            go.Scatter(
                x=plot_df["timestamp"],
                y=ema.values,
                name=f"EMA {ema_period}",
                line=dict(color="#FFA726", width=1.5, dash="dot"),
            ),
            row=1,
            col=1,
        )

    # ── Trendlines ──
    if show_trendlines and len(df) >= 30:
        _add_trendlines(fig, df, plot_df)

    # ── Volume bars with spike coloring ──
    spike_mask = get_volume_spike_mask(df)
    colors = np.where(
        spike_mask.values,
        "#FF6D00",  # Orange for spike
        np.where(
            plot_df["close"].values >= plot_df["open"].values,
            "rgba(38,166,154,0.5)",   # Green
            "rgba(239,83,80,0.5)",    # Red
        ),
    )

    fig.add_trace(
        go.Bar(
            x=plot_df["timestamp"],
            y=plot_df["volume"],
            name="Volume",
            marker_color=colors,
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    # ── Layout ──
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=50, r=30, t=40, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        xaxis_rangeslider_visible=False,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="#fafafa"),
    )

    fig.update_xaxes(gridcolor="#1e222d", zerolinecolor="#1e222d")
    fig.update_yaxes(gridcolor="#1e222d", zerolinecolor="#1e222d")

    return fig


def _add_trendlines(fig: go.Figure, df: pd.DataFrame, plot_df: pd.DataFrame):
    """Add multiple trendline candidates with pattern label (Phase 2)."""
    try:
        df_reset = df.reset_index(drop=True)
        sh_idx, _ = find_swing_points_adaptive(df_reset["high"])
        _, sl_idx = find_swing_points_adaptive(df_reset["low"])

        # RANSAC resistance candidates (top 3)
        res_colors = ["#FF5252", "#FF8A80", "#FFCDD2"]
        res_candidates = fit_trendline_ransac(
            sh_idx, df_reset["high"].values, line_type="resistance", min_points=3, max_candidates=3
        )
        for i, res in enumerate(res_candidates):
            x0_idx = 0
            x1_idx = len(df_reset) - 1
            y0 = res["slope"] * x0_idx + res["intercept"]
            y1 = res["slope"] * x1_idx + res["intercept"]
            # Clamp start to first data point
            start_x = max(int(res["indices"][0]) if len(res.get("indices", [])) > 0 else 0, 0)
            start_x = min(start_x, len(plot_df) - 1)
            fig.add_trace(
                go.Scatter(
                    x=[plot_df["timestamp"].iloc[start_x], plot_df["timestamp"].iloc[x1_idx]],
                    y=[res["slope"] * start_x + res["intercept"], y1],
                    mode="lines",
                    name=f"Resistance #{i+1}" if i == 0 else f"Res alt #{i+1}",
                    line=dict(
                        color=res_colors[i],
                        width=2.0 if i == 0 else 1.0,
                        dash="dash" if i > 0 else "solid",
                    ),
                    opacity=1.0 if i == 0 else 0.5,
                ),
                row=1, col=1,
            )

        # RANSAC support candidates (top 3)
        sup_colors = ["#4CAF50", "#81C784", "#C8E6C9"]
        sup_candidates = fit_trendline_ransac(
            sl_idx, df_reset["low"].values, line_type="support", min_points=3, max_candidates=3
        )
        for i, sup in enumerate(sup_candidates):
            x0_idx = 0
            x1_idx = len(df_reset) - 1
            y1 = sup["slope"] * x1_idx + sup["intercept"]
            start_x = max(int(sup["indices"][0]) if len(sup.get("indices", [])) > 0 else 0, 0)
            start_x = min(start_x, len(plot_df) - 1)
            fig.add_trace(
                go.Scatter(
                    x=[plot_df["timestamp"].iloc[start_x], plot_df["timestamp"].iloc[x1_idx]],
                    y=[sup["slope"] * start_x + sup["intercept"], y1],
                    mode="lines",
                    name=f"Support #{i+1}" if i == 0 else f"Sup alt #{i+1}",
                    line=dict(
                        color=sup_colors[i],
                        width=2.0 if i == 0 else 1.0,
                        dash="dash" if i > 0 else "solid",
                    ),
                    opacity=1.0 if i == 0 else 0.5,
                ),
                row=1, col=1,
            )

        # Pattern annotation
        best_res = res_candidates[0] if res_candidates else None
        best_sup = sup_candidates[0] if sup_candidates else None
        pattern = classify_pattern(best_res, best_sup)
        label = PATTERN_LABELS.get(pattern, "")
        if label and label != "—":
            fig.add_annotation(
                x=plot_df["timestamp"].iloc[-1],
                y=float(df_reset["high"].max()),
                text=f"Pattern: {label}",
                showarrow=False,
                font=dict(size=11, color="#FFC107"),
                bgcolor="rgba(0,0,0,0.6)",
                bordercolor="#FFC107",
                borderwidth=1,
                borderpad=4,
                xanchor="right",
                yanchor="bottom",
                row=1, col=1,
            )

        # Swing point markers
        if len(sh_idx) > 0:
            fig.add_trace(
                go.Scatter(
                    x=plot_df["timestamp"].iloc[sh_idx],
                    y=df_reset["high"].iloc[sh_idx],
                    mode="markers",
                    name="Swing High",
                    marker=dict(color="#FF5252", size=6, symbol="triangle-down"),
                ),
                row=1, col=1,
            )
        if len(sl_idx) > 0:
            fig.add_trace(
                go.Scatter(
                    x=plot_df["timestamp"].iloc[sl_idx],
                    y=df_reset["low"].iloc[sl_idx],
                    mode="markers",
                    name="Swing Low",
                    marker=dict(color="#4CAF50", size=6, symbol="triangle-up"),
                ),
                row=1, col=1,
            )

    except Exception as e:
        logger.debug("Trendline drawing error: %s", e)


def build_order_book_chart(bids: list, asks: list, symbol: str) -> go.Figure:
    """Build order book depth chart with whale wall annotations."""
    fig = go.Figure()

    if bids:
        bid_prices = [b[0] for b in bids]
        bid_sizes = [b[1] for b in bids]
        bid_cumvol = list(np.cumsum(bid_sizes))
        fig.add_trace(
            go.Scatter(
                x=bid_prices,
                y=bid_cumvol,
                fill="tozeroy",
                name="Bids",
                line=dict(color="#26a69a"),
                fillcolor="rgba(38,166,154,0.3)",
            )
        )

    if asks:
        ask_prices = [a[0] for a in asks]
        ask_sizes = [a[1] for a in asks]
        ask_cumvol = list(np.cumsum(ask_sizes))
        fig.add_trace(
            go.Scatter(
                x=ask_prices,
                y=ask_cumvol,
                fill="tozeroy",
                name="Asks",
                line=dict(color="#ef5350"),
                fillcolor="rgba(239,83,80,0.3)",
            )
        )

    fig.update_layout(
        template="plotly_dark",
        title=f"{symbol} Order Book Depth",
        height=350,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        xaxis_title="Price",
        yaxis_title="Cumulative Volume",
        font=dict(color="#fafafa"),
    )

    return fig


def build_order_book_heatmap(bids: list, asks: list, symbol: str) -> go.Figure:
    """Build order book heatmap showing size at each price level."""
    fig = go.Figure()

    all_prices = []
    all_sizes = []
    all_colors = []
    all_sides = []

    if bids:
        for b in bids:
            all_prices.append(b[0])
            all_sizes.append(b[1])
            all_colors.append("#26a69a")
            all_sides.append("Bid")

    if asks:
        for a in asks:
            all_prices.append(a[0])
            all_sizes.append(a[1])
            all_colors.append("#ef5350")
            all_sides.append("Ask")

    if not all_prices:
        fig.add_annotation(text="No order book data", showarrow=False)
        fig.update_layout(template="plotly_dark", height=300, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117")
        return fig

    # Detect whale walls: levels > mean + 2*std
    sizes_arr = np.array(all_sizes)
    threshold = np.mean(sizes_arr) + 2 * np.std(sizes_arr)
    bar_colors = []
    for i, size in enumerate(all_sizes):
        if size >= threshold:
            bar_colors.append("#FFD600")  # Yellow = whale wall
        else:
            bar_colors.append(all_colors[i])

    fig.add_trace(go.Bar(
        x=all_prices,
        y=all_sizes,
        marker_color=bar_colors,
        text=[f"{s:,.2f}" for s in all_sizes],
        textposition="outside",
        name="Size",
    ))

    # Whale wall annotations
    for i, size in enumerate(all_sizes):
        if size >= threshold:
            fig.add_annotation(
                x=all_prices[i],
                y=size,
                text="WHALE",
                showarrow=True,
                arrowhead=2,
                arrowcolor="#FFD600",
                font=dict(size=9, color="#FFD600"),
                bgcolor="rgba(0,0,0,0.7)",
            )

    fig.update_layout(
        template="plotly_dark",
        title=f"{symbol} Order Book Heatmap (Yellow = Whale Wall)",
        height=400,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        xaxis_title="Price",
        yaxis_title="Size",
        font=dict(color="#fafafa"),
    )

    return fig


def build_funding_rate_chart(data: list[dict], symbol: str) -> go.Figure:
    """Build funding rate comparison chart across exchanges (CCXT format)."""
    fig = go.Figure()

    if not data:
        fig.add_annotation(text="No funding rate data available", showarrow=False)
        fig.update_layout(
            template="plotly_dark",
            height=250,
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
        )
        return fig

    exchanges = []
    rates = []
    colors = []

    for item in data:
        ex_name = item.get("exchange", "Unknown")
        rate = item.get("rate", 0) or 0
        rate_pct = rate * 100
        exchanges.append(ex_name)
        rates.append(rate_pct)
        colors.append("#26a69a" if rate_pct >= 0 else "#ef5350")

    fig.add_trace(
        go.Bar(
            x=exchanges,
            y=rates,
            marker_color=colors,
            text=[f"{r:+.4f}%" for r in rates],
            textposition="outside",
            name="Funding Rate %",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        title=f"{symbol} Funding Rate (%) — via CCXT (free)",
        height=300,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        yaxis_title="Rate %",
        font=dict(color="#fafafa"),
    )

    return fig


def build_long_short_chart(data: list[dict], symbol: str) -> go.Figure:
    """Build long/short ratio chart (Binance public FAPI format)."""
    fig = go.Figure()

    if not data:
        fig.add_annotation(text="No long/short data available", showarrow=False)
        fig.update_layout(
            template="plotly_dark",
            height=250,
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
        )
        return fig

    labels = []
    long_pcts = []
    short_pcts = []

    for item in data:
        label = item.get("exchange", "Unknown")
        long_r = float(item.get("longRatio", 0.5))
        short_r = float(item.get("shortRatio", 0.5))
        labels.append(label)
        long_pcts.append(long_r * 100)
        short_pcts.append(short_r * 100)

    fig.add_trace(go.Bar(
        x=labels, y=long_pcts, name="Long %", marker_color="#26a69a",
        text=[f"{v:.1f}%" for v in long_pcts], textposition="inside",
    ))
    fig.add_trace(go.Bar(
        x=labels, y=short_pcts, name="Short %", marker_color="#ef5350",
        text=[f"{v:.1f}%" for v in short_pcts], textposition="inside",
    ))

    fig.update_layout(
        template="plotly_dark",
        title=f"{symbol} Long/Short Ratio — Binance Public API (free)",
        barmode="stack",
        height=350,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        yaxis_title="Ratio %",
        font=dict(color="#fafafa"),
    )

    return fig


# ──────────────────────────────────────────────
# Phase 3: Historical Funding Rate Chart
# ──────────────────────────────────────────────
def build_funding_rate_history_chart(df: pd.DataFrame, symbol: str) -> go.Figure:
    """Build historical funding rate timeline chart."""
    fig = go.Figure()

    if df.empty:
        fig.add_annotation(text="No historical funding rate data", showarrow=False)
        fig.update_layout(template="plotly_dark", height=300, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117")
        return fig

    colors = ["#26a69a" if r >= 0 else "#ef5350" for r in df["fundingRate"]]

    fig.add_trace(go.Bar(
        x=df["fundingTime"],
        y=df["fundingRate"] * 100,
        marker_color=colors,
        name="Funding Rate %",
    ))

    # Add zero line
    fig.add_hline(y=0, line_dash="dot", line_color="#616161")

    # Average line
    avg_rate = df["fundingRate"].mean() * 100
    fig.add_hline(
        y=avg_rate,
        line_dash="dash",
        line_color="#FFC107",
        annotation_text=f"Avg: {avg_rate:+.4f}%",
        annotation_position="top right",
        annotation_font_color="#FFC107",
    )

    fig.update_layout(
        template="plotly_dark",
        title=f"{symbol} Funding Rate History",
        height=350,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        xaxis_title="Time",
        yaxis_title="Funding Rate %",
        font=dict(color="#fafafa"),
    )

    return fig


# ──────────────────────────────────────────────
# Phase 3: Historical Long/Short Timeline
# ──────────────────────────────────────────────
def build_ls_history_chart(df: pd.DataFrame, symbol: str) -> go.Figure:
    """Build historical long/short ratio timeline."""
    fig = go.Figure()

    if df.empty:
        fig.add_annotation(text="No historical L/S data", showarrow=False)
        fig.update_layout(template="plotly_dark", height=300, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117")
        return fig

    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["longAccount"].astype(float) * 100,
        name="Long %",
        line=dict(color="#26a69a", width=2),
        fill="tonexty" if "shortAccount" in df.columns else None,
    ))

    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["shortAccount"].astype(float) * 100,
        name="Short %",
        line=dict(color="#ef5350", width=2),
    ))

    # 50% line
    fig.add_hline(y=50, line_dash="dot", line_color="#616161", annotation_text="50%")

    fig.update_layout(
        template="plotly_dark",
        title=f"{symbol} Long/Short Ratio History",
        height=350,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        xaxis_title="Time",
        yaxis_title="Ratio %",
        font=dict(color="#fafafa"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig


# ──────────────────────────────────────────────
# Phase 3: Open Interest Chart
# ──────────────────────────────────────────────
def build_open_interest_chart(df: pd.DataFrame, symbol: str) -> go.Figure:
    """Build open interest history chart with value overlay."""
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6, 0.4],
        subplot_titles=[f"{symbol} Open Interest (Contracts)", "OI Value (USD)"],
    )

    if df.empty:
        fig.add_annotation(text="No open interest data", showarrow=False)
        fig.update_layout(template="plotly_dark", height=400, paper_bgcolor="#0e1117", plot_bgcolor="#0e1117")
        return fig

    # OI in contracts
    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["sumOpenInterest"],
        name="OI (contracts)",
        line=dict(color="#42A5F5", width=2),
        fill="tozeroy",
        fillcolor="rgba(66,165,245,0.15)",
    ), row=1, col=1)

    # OI in USD value
    fig.add_trace(go.Bar(
        x=df["timestamp"],
        y=df["sumOpenInterestValue"],
        name="OI Value (USD)",
        marker_color="rgba(171,71,188,0.6)",
    ), row=2, col=1)

    fig.update_layout(
        template="plotly_dark",
        height=450,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="#fafafa"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        showlegend=True,
    )
    fig.update_xaxes(gridcolor="#1e222d")
    fig.update_yaxes(gridcolor="#1e222d")

    return fig


# ──────────────────────────────────────────────
# Phase 3: Liquidation Level Estimation
# ──────────────────────────────────────────────
def build_liquidation_chart(
    current_price: float, symbol: str, leverages: list[int] = None
) -> go.Figure:
    """
    Estimate liquidation price levels for common leverages.
    For longs: liq_price = entry * (1 - 1/leverage)
    For shorts: liq_price = entry * (1 + 1/leverage)
    """
    if leverages is None:
        leverages = [2, 3, 5, 10, 20, 25, 50, 100]

    fig = go.Figure()

    long_liqs = [current_price * (1 - 1 / lev) for lev in leverages]
    short_liqs = [current_price * (1 + 1 / lev) for lev in leverages]
    labels = [f"{lev}x" for lev in leverages]

    fig.add_trace(go.Bar(
        x=labels,
        y=long_liqs,
        name="Long Liq Price",
        marker_color="#ef5350",
        text=[f"${p:,.2f}" for p in long_liqs],
        textposition="outside",
    ))

    fig.add_trace(go.Bar(
        x=labels,
        y=short_liqs,
        name="Short Liq Price",
        marker_color="#26a69a",
        text=[f"${p:,.2f}" for p in short_liqs],
        textposition="outside",
    ))

    # Current price line
    fig.add_hline(
        y=current_price,
        line_dash="dash",
        line_color="#FFC107",
        annotation_text=f"Current: ${current_price:,.2f}",
        annotation_position="top right",
        annotation_font_color="#FFC107",
    )

    fig.update_layout(
        template="plotly_dark",
        title=f"{symbol} Estimated Liquidation Levels by Leverage",
        barmode="group",
        height=400,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        xaxis_title="Leverage",
        yaxis_title="Liquidation Price (USD)",
        font=dict(color="#fafafa"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig
