"""Chart builder: Plotly candlestick + volume with 200EMA overlay."""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from technical_analysis import compute_ema, get_volume_spike_mask, find_swing_points, fit_trendline


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
    """Add resistance/support trendlines to chart."""
    try:
        df_reset = df.reset_index(drop=True)
        sh_idx, _ = find_swing_points(df_reset["high"], order=5)
        _, sl_idx = find_swing_points(df_reset["low"], order=5)

        # Resistance line
        if len(sh_idx) >= 3:
            res = fit_trendline(sh_idx, df_reset["high"].values, min_points=3)
            if res and res["r_squared"] > 0.5:
                x0 = int(res["indices"][0])
                x1 = len(df_reset) - 1
                y0 = res["slope"] * x0 + res["intercept"]
                y1 = res["slope"] * x1 + res["intercept"]
                fig.add_trace(
                    go.Scatter(
                        x=[plot_df["timestamp"].iloc[x0], plot_df["timestamp"].iloc[x1]],
                        y=[y0, y1],
                        mode="lines",
                        name="Resistance",
                        line=dict(color="#FF5252", width=1.5, dash="dash"),
                    ),
                    row=1,
                    col=1,
                )

        # Support line
        if len(sl_idx) >= 3:
            sup = fit_trendline(sl_idx, df_reset["low"].values, min_points=3)
            if sup and sup["r_squared"] > 0.5:
                x0 = int(sup["indices"][0])
                x1 = len(df_reset) - 1
                y0 = sup["slope"] * x0 + sup["intercept"]
                y1 = sup["slope"] * x1 + sup["intercept"]
                fig.add_trace(
                    go.Scatter(
                        x=[plot_df["timestamp"].iloc[x0], plot_df["timestamp"].iloc[x1]],
                        y=[y0, y1],
                        mode="lines",
                        name="Support",
                        line=dict(color="#4CAF50", width=1.5, dash="dash"),
                    ),
                    row=1,
                    col=1,
                )
    except Exception:
        pass  # Non-critical, skip if trendlines can't be drawn


def build_order_book_chart(bids: list, asks: list, symbol: str) -> go.Figure:
    """Build order book depth chart."""
    fig = go.Figure()

    if bids:
        bid_prices = [b[0] for b in bids]
        bid_cumvol = []
        cumsum = 0
        for b in bids:
            cumsum += b[1]
            bid_cumvol.append(cumsum)
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
        ask_cumvol = []
        cumsum = 0
        for a in asks:
            cumsum += a[1]
            ask_cumvol.append(cumsum)
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


def build_funding_rate_chart(data: list[dict], symbol: str) -> go.Figure:
    """Build funding rate comparison chart across exchanges."""
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
        ex_name = item.get("exchangeName", item.get("exchange", "Unknown"))
        rate = item.get("rate", item.get("currentFundingRate", 0)) or 0
        rate_pct = rate * 100
        exchanges.append(ex_name)
        rates.append(rate_pct)
        colors.append("#26a69a" if rate_pct >= 0 else "#ef5350")

    fig.add_trace(
        go.Bar(
            x=exchanges,
            y=rates,
            marker_color=colors,
            name="Funding Rate %",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        title=f"{symbol} Funding Rate (%)",
        height=300,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        yaxis_title="Rate %",
        font=dict(color="#fafafa"),
    )

    return fig


def build_long_short_chart(data: list[dict], symbol: str) -> go.Figure:
    """Build long/short ratio chart."""
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

    exchanges = []
    long_pcts = []
    short_pcts = []

    for item in data:
        ex_name = item.get("exchangeName", item.get("exchange", "Unknown"))
        long_r = item.get("longRate", item.get("longRatio", 0.5)) or 0.5
        short_r = item.get("shortRate", item.get("shortRatio", 0.5)) or 0.5
        exchanges.append(ex_name)
        long_pcts.append(long_r * 100)
        short_pcts.append(short_r * 100)

    fig.add_trace(go.Bar(x=exchanges, y=long_pcts, name="Long %", marker_color="#26a69a"))
    fig.add_trace(go.Bar(x=exchanges, y=short_pcts, name="Short %", marker_color="#ef5350"))

    fig.update_layout(
        template="plotly_dark",
        title=f"{symbol} Long/Short Ratio",
        barmode="stack",
        height=300,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        yaxis_title="Ratio %",
        font=dict(color="#fafafa"),
    )

    return fig
