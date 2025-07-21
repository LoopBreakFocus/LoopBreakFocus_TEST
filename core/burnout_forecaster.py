import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

LOG_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/app_usage_log.csv"

# ---------- App Classifier ----------
def classify_app(app_title):
    distractions = ["YouTube", "Netflix", "Spotify", "Discord", "Safari", "Photos", "Messages", "Reddit", "Twitter"]
    if isinstance(app_title, str):
        for app in distractions:
            if app.lower() in app_title.lower():
                return "Distraction"
    return "Neutral"

# ---------- Forecast Function ----------
def forecast_burnout():
    if not os.path.exists(LOG_FILE):
        print("❌ Log file not found.")
        return

    try:
        df = pd.read_csv(LOG_FILE)
        df.columns = df.columns.str.strip().str.lower()
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
    except Exception as e:
        print(f"❌ Failed to load log data: {e}")
        return

    if "status" not in df.columns or "active window" not in df.columns:
        print("❌ Required columns missing in log file.")
        return

    df["app class"] = df["active window"].apply(classify_app)
    df["day"] = df["timestamp"].dt.date

    grouped = df.groupby("day")
    summary = pd.DataFrame({
        "idle_ratio": grouped["status"].apply(lambda x: (x == "Idle").sum() / len(x)),
        "distraction_ratio": grouped["app class"].apply(lambda x: (x == "Distraction").sum() / len(x)),
        "switching_rate": grouped["active window"].apply(lambda x: (x != x.shift(1)).sum() / len(x)),
        "score": grouped["score"].mean()
    }).fillna(0)

    if len(summary) < 5:
        print("ℹ️ Not enough data to forecast burnout.")
        return

    recent = summary.tail(7)

    # ---------- Risk Model ----------
    weights = {
        "idle_ratio": 0.3,
        "distraction_ratio": 0.3,
        "switching_rate": 0.2,
        "score": -0.4  # higher score = lower risk
    }

    burnout_risk = (
        weights["idle_ratio"] * recent["idle_ratio"].mean() +
        weights["distraction_ratio"] * recent["distraction_ratio"].mean() +
        weights["switching_rate"] * recent["switching_rate"].mean() +
        weights["score"] * (1 - recent["score"].mean())
    )

    # Normalize between 0–1
    burnout_risk = max(min(burnout_risk, 1.0), 0.0)

    # Estimate days until burnout
    days_until_burnout = int((1.0 - burnout_risk) * 14)

    # ---------- Output ----------
    print(f"\n🧠 Burnout Forecast:")
    print(f"📉 Based on recent behavior, you may hit burnout in ~{days_until_burnout} days.")
    
    if days_until_burnout <= 3:
        print("⚠️  Immediate intervention recommended.")
    elif days_until_burnout <= 7:
        print("🟠 Warning: Trend indicates mid-level burnout approaching.")
    else:
        print("🟢 You're in a stable zone. Keep it up!")

if __name__ == "__main__":
    forecast_burnout()