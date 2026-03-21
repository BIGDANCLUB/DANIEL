"""
Phase 8C: AI Prediction Model
==============================
Machine learning model that predicts win probability for scan signals.
Uses historical signal data to train a classifier (RandomForest / GradientBoosting).

Features:
- Automatic feature extraction from signal data
- Train on historical hit/miss outcomes
- Predict win probability for new signals
- Model persistence (save/load)
- Feature importance visualization
"""

import json
import logging
import os
import pickle
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger("ai_predictor")

MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "signal_predictor.pkl"
SCALER_PATH = MODEL_DIR / "signal_scaler.pkl"
METADATA_PATH = MODEL_DIR / "model_metadata.json"


# ──────────────────────────────────────────────
# Feature Engineering
# ──────────────────────────────────────────────
FEATURE_COLUMNS = [
    "score",
    "volume_ratio",
    "change_pct",
    "break_strength",
    "confirmation_bars",
    "is_bullish",
    "is_bearish",
    "volume_confirmed",
    "multi_tf_confirmed",
    "social_boost",
    "above_ema",
    # RSI features
    "rsi_value",
    "rsi_oversold",
    "rsi_overbought",
    "rsi_bullish_zone",
    # MACD features
    "macd_bullish",
    "macd_bearish",
    "macd_bullish_cross",
    # BB features
    "bb_squeeze",
    "bb_above_upper",
    "bb_below_lower",
    "bb_pct_b",
    # Pattern encoding
    "pattern_ascending_triangle",
    "pattern_descending_triangle",
    "pattern_symmetrical_triangle",
    "pattern_rising_wedge",
    "pattern_falling_wedge",
    "pattern_channel_up",
    "pattern_channel_down",
]


def extract_features_from_signal(signal: dict) -> dict:
    """Extract ML features from a single signal dict."""
    features = {}

    # Core metrics
    features["score"] = signal.get("score", 0)
    features["volume_ratio"] = signal.get("volume_ratio", 0)
    features["change_pct"] = signal.get("change_pct", 0)

    # Trendline break features
    features["break_strength"] = signal.get("break_strength", 0)
    features["confirmation_bars"] = signal.get("confirmation_bars", 0)

    bt = signal.get("breakout_type", "")
    features["is_bullish"] = 1 if bt == "bullish" else 0
    features["is_bearish"] = 1 if bt == "bearish" else 0
    features["volume_confirmed"] = 1 if signal.get("volume_confirmed") else 0
    features["multi_tf_confirmed"] = 1 if signal.get("multi_tf_confirmed") else 0
    features["social_boost"] = 1 if signal.get("social_boost") else 0
    features["above_ema"] = 1 if signal.get("above_ema") else 0

    # RSI features
    features["rsi_value"] = signal.get("rsi_value", 50)
    features["rsi_oversold"] = 1 if signal.get("rsi_oversold") else 0
    features["rsi_overbought"] = 1 if signal.get("rsi_overbought") else 0
    features["rsi_bullish_zone"] = 1 if signal.get("rsi_bullish_zone") else 0

    # MACD features
    features["macd_bullish"] = 1 if signal.get("macd_trend") == "bullish" else 0
    features["macd_bearish"] = 1 if signal.get("macd_trend") == "bearish" else 0
    features["macd_bullish_cross"] = 1 if signal.get("macd_bullish_cross") else 0

    # BB features
    features["bb_squeeze"] = 1 if signal.get("bb_squeeze") else 0
    features["bb_above_upper"] = 1 if signal.get("bb_signal") == "above_upper" else 0
    features["bb_below_lower"] = 1 if signal.get("bb_signal") == "below_lower" else 0
    features["bb_pct_b"] = signal.get("bb_pct_b", 0.5)

    # Pattern one-hot encoding
    pattern = signal.get("pattern", "").lower().replace(" ", "_")
    for col in FEATURE_COLUMNS:
        if col.startswith("pattern_"):
            p_name = col.replace("pattern_", "")
            features[col] = 1 if pattern == p_name else 0

    return features


def extract_features_from_history(history: list[dict]) -> pd.DataFrame:
    """Convert signal history list to features DataFrame."""
    rows = []
    for sig in history:
        feat = extract_features_from_signal(sig)
        feat["hit"] = sig.get("hit")
        rows.append(feat)

    df = pd.DataFrame(rows)

    # Ensure all feature columns exist
    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = 0

    # Ensure hit column exists
    if "hit" not in df.columns:
        df["hit"] = None

    return df


def extract_features_from_scan_result(scan_result) -> dict:
    """Extract features from a ScanResult object."""
    tl = scan_result.trendline_break or {}
    extra = scan_result.extra or {}
    rsi = extra.get("rsi", {})
    macd = extra.get("macd", {})
    bb = extra.get("bb", {})

    return extract_features_from_signal({
        "score": scan_result.score,
        "volume_ratio": scan_result.volume_ratio,
        "change_pct": scan_result.change_pct,
        "break_strength": tl.get("break_strength", 0),
        "confirmation_bars": tl.get("confirmation_bars", 0),
        "breakout_type": tl.get("breakout_type", ""),
        "volume_confirmed": tl.get("volume_confirmed", False),
        "multi_tf_confirmed": tl.get("multi_tf_confirmed", False),
        "social_boost": scan_result.social_boost,
        "above_ema": scan_result.above_ema,
        "rsi_value": rsi.get("value", 50),
        "rsi_oversold": rsi.get("oversold", False),
        "rsi_overbought": rsi.get("overbought", False),
        "rsi_bullish_zone": rsi.get("bullish_zone", False),
        "macd_trend": macd.get("trend", "neutral"),
        "macd_bullish_cross": macd.get("bullish_cross", False),
        "bb_squeeze": bb.get("squeeze", False),
        "bb_signal": bb.get("signal", ""),
        "bb_pct_b": bb.get("pct_b", 0.5),
        "pattern": tl.get("pattern_label", ""),
    })


# ──────────────────────────────────────────────
# Model Training & Prediction
# ──────────────────────────────────────────────
class SignalPredictor:
    """ML model for predicting signal win probability."""

    def __init__(self):
        self.model = None
        self.scaler = None
        self.metadata = {}
        self.feature_importance = {}
        self._load_model()

    def _load_model(self):
        """Load saved model if exists."""
        if MODEL_PATH.exists() and SCALER_PATH.exists():
            try:
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
                with open(SCALER_PATH, "rb") as f:
                    self.scaler = pickle.load(f)
                if METADATA_PATH.exists():
                    with open(METADATA_PATH, "r") as f:
                        self.metadata = json.load(f)
                logger.info("Loaded saved model (trained: %s)", self.metadata.get("trained_at"))
            except Exception as e:
                logger.warning("Failed to load model: %s", e)
                self.model = None
                self.scaler = None

    def train(self, history: list[dict], min_samples: int = 30) -> dict:
        """
        Train model on signal history.

        Returns dict with training metrics.
        """
        from sklearn.ensemble import GradientBoostingClassifier
        from sklearn.model_selection import cross_val_score
        from sklearn.preprocessing import StandardScaler

        df = extract_features_from_history(history)

        # Filter only resolved signals
        df_resolved = df[df["hit"].notna()].copy()
        df_resolved["hit"] = df_resolved["hit"].astype(int)

        if len(df_resolved) < min_samples:
            return {
                "error": f"Not enough resolved signals ({len(df_resolved)}/{min_samples}). "
                         "Run more scans and update outcomes first.",
                "samples": len(df_resolved),
                "required": min_samples,
            }

        X = df_resolved[FEATURE_COLUMNS].fillna(0)
        y = df_resolved["hit"]

        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        # Train GradientBoosting
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            min_samples_split=5,
            min_samples_leaf=3,
            subsample=0.8,
            random_state=42,
        )

        # Cross-validation
        cv_scores = cross_val_score(self.model, X_scaled, y, cv=min(5, len(y) // 5 + 1), scoring="accuracy")

        # Full train
        self.model.fit(X_scaled, y)

        # Feature importance
        importances = self.model.feature_importances_
        self.feature_importance = dict(zip(FEATURE_COLUMNS, importances))

        # Save model
        self._save_model(len(df_resolved), float(cv_scores.mean()))

        return {
            "samples": len(df_resolved),
            "hits": int(y.sum()),
            "misses": int(len(y) - y.sum()),
            "cv_accuracy": float(cv_scores.mean()),
            "cv_std": float(cv_scores.std()),
            "feature_importance": dict(sorted(
                self.feature_importance.items(),
                key=lambda x: x[1], reverse=True
            )[:10]),
        }

    def predict(self, signal) -> dict:
        """
        Predict win probability for a signal.

        Parameters
        ----------
        signal : ScanResult object or dict

        Returns
        -------
        dict with 'win_probability', 'confidence', 'prediction'
        """
        if self.model is None or self.scaler is None:
            return {
                "win_probability": None,
                "confidence": "no_model",
                "prediction": "unknown",
                "message": "No trained model. Need 30+ resolved signals.",
            }

        # Extract features
        if hasattr(signal, "score"):  # ScanResult object
            features = extract_features_from_scan_result(signal)
        else:
            features = extract_features_from_signal(signal)

        # Build feature vector
        X = pd.DataFrame([features])[FEATURE_COLUMNS].fillna(0)
        X_scaled = self.scaler.transform(X)

        # Predict probability
        proba = self.model.predict_proba(X_scaled)[0]
        win_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])

        # Classify confidence
        if win_prob >= 0.75:
            confidence = "high"
        elif win_prob >= 0.55:
            confidence = "medium"
        else:
            confidence = "low"

        return {
            "win_probability": round(win_prob, 3),
            "confidence": confidence,
            "prediction": "win" if win_prob >= 0.5 else "loss",
            "model_accuracy": self.metadata.get("cv_accuracy", 0),
        }

    def predict_batch(self, signals: list) -> list[dict]:
        """Predict for multiple signals."""
        return [self.predict(s) for s in signals]

    def get_feature_importance(self) -> list[dict]:
        """Get sorted feature importance for visualization."""
        if not self.feature_importance:
            return []
        sorted_feats = sorted(
            self.feature_importance.items(),
            key=lambda x: x[1], reverse=True
        )
        return [
            {"feature": f, "importance": round(v, 4)}
            for f, v in sorted_feats
        ]

    def _save_model(self, n_samples: int, cv_accuracy: float):
        """Save model to disk."""
        MODEL_DIR.mkdir(exist_ok=True)

        with open(MODEL_PATH, "wb") as f:
            pickle.dump(self.model, f)
        with open(SCALER_PATH, "wb") as f:
            pickle.dump(self.scaler, f)

        self.metadata = {
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "n_samples": n_samples,
            "cv_accuracy": round(cv_accuracy, 4),
            "n_features": len(FEATURE_COLUMNS),
            "model_type": "GradientBoostingClassifier",
        }
        with open(METADATA_PATH, "w") as f:
            json.dump(self.metadata, f, indent=2)

        logger.info("Model saved (samples: %d, CV: %.3f)", n_samples, cv_accuracy)

    @property
    def is_trained(self) -> bool:
        return self.model is not None

    @property
    def model_info(self) -> dict:
        if not self.is_trained:
            return {"status": "not_trained"}
        return {
            "status": "trained",
            **self.metadata,
        }
