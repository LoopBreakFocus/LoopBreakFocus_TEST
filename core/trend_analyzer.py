# trend_analyzer.py

import pandas as pd
import subprocess
from datetime import datetime, timedelta
import numpy as np
import os

LOG_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/app_usage_log.csv"

WORK_APPS = ["Chrome", "Visual Studio Code", "VS Code", "Word", "Terminal", "Excel", "PowerPoint"]
DISTRACTION_APPS = ["YouTube", "Netflix", "Spotify", "Discord", "Safari", "Photos", "Messages"]

# ---------- App Classifier ----------
def classify_app(app_title):
    if not isinstance(app_title, str):
        return "Neutral"
    for app in WORK_APPS:
        if app.lower() in app_title.lower():
            return "Work"
    for app in DISTRACTION_APPS:
        if app.lower() in app_title.lower():
            return "Distraction"
    return "Neutral"

# ---------- Trend Detection ----------
def detect_trend(series):
    if len(series) < 3:
        return "Not enough data"
    x = np.arange(len(series))
    y = series.values
    slope = np.polyfit(x, y, 1)[0]
    if abs(slope) < 0.001:
        return "Stable"
    elif slope > 0.005:
        return "Upward"
    elif slope < -0.005:
        return "Downward"
    return "Volatile"

# ---------- Pattern Categorizers ----------
def categorize_patterns(df):
    hour_usage = df['timestamp'].dt.hour
    most_common_hour = hour_usage.mode()[0] if not hour_usage.empty else None

    app_class_counts = df['app class'].value_counts().to_dict()
    total = sum(app_class_counts.values())
    proportions = {k: f"{(v / total) * 100:.1f}%" for k, v in app_class_counts.items()}

    print("\n📊 Usage Pattern Overview:")
    print(f"⏰ Most active hour: {most_common_hour}:00" if most_common_hour is not None else "⏰ No usage hour pattern found.")
    print("🧩 App category distribution:")
    for cls, pct in proportions.items():
        print(f"   - {cls}: {pct}")

# ---------- Notification ----------
def show_popup(message):
    subprocess.run([
        "osascript", "-e",
        f'display notification "{message}" with title \\"LoopBreak Trend Report\\"'
    ])
    print("📢", message)

# ---------- Main Analyzer ----------
def analyze_trends():
    if not os.path.exists(LOG_FILE):
        print("❌ App usage log not found.")
        return

    try:
        df = pd.read_csv(LOG_FILE)
        df.columns = [c.strip().lower() for c in df.columns]
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
    except Exception as e:
        print(f"❌ Error reading data: {e}")
        return

    # Classify app usage
    df["app class"] = df["active window"].apply(classify_app)

    # Last 14 days only
    df = df[df["timestamp"] >= datetime.now() - timedelta(days=14)]

    if df.empty:
        print("⚠️ No data for the last 14 days.")
        return

    df["day"] = df["timestamp"].dt.date
    grouped = df.groupby("day")

    daily_data = pd.DataFrame({
        "Idle Ratio": grouped["status"].apply(lambda x: (x == "Idle").sum() / len(x)),
        "Distraction Ratio": grouped["app class"].apply(lambda x: (x == "Distraction").sum() / len(x)),
        "Switching Rate": grouped["active window"].apply(lambda x: (x != x.shift(1)).sum() / len(x)),
        "Score": grouped["score"].mean()
    }).fillna(0)

    if len(daily_data) < 3:
        print("⚠️ Not enough data to detect trends.")
        return

    print("\n📊 Daily Metrics (Last 7 Days):")
    print(daily_data.tail(7).round(3))

    trends = {col: detect_trend(daily_data[col].tail(7)) for col in daily_data.columns}

    print("\n📈 Detected Trends:")
    for metric, direction in trends.items():
        print(f"🔹 {metric}: {direction}")

    alerts = []
    if trends["Score"] == "Downward":
        alerts.append("⬇ Productivity is falling. Risk of burnout.")
    if trends["Idle Ratio"] == "Upward":
        alerts.append("⬆ Idle time is increasing. Possible disengagement.")
    if trends["Distraction Ratio"] == "Upward":
        alerts.append("⬆ More time on distracting apps.")
    if trends["Score"] == "Upward":
        alerts.append("💪 Productivity improving. Great work!")
    if trends["Score"] == "Volatile":
        alerts.append("⚠️ Focus patterns are irregular. Take care.")

    # Show alert summary
    if alerts:
        show_popup("\n".join(alerts))
    else:
        show_popup("✅ All trends are stable. Keep going!")

    # Print usage pattern insights
    categorize_patterns(df)

if __name__ == "__main__":
    analyze_trends()