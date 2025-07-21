import pandas as pd
import subprocess
from datetime import datetime, timedelta
import os

LOG_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/app_usage_log.csv"

THRESHOLDS = {
    "idle": 0.20,        # +20% increase
    "distraction": 0.20, # +20% increase
    "switching": 0.20,   # +20% increase
    "score": 0.15        # -15% drop
}

# App categories
WORK_APPS = ["Chrome", "Visual Studio Code", "VS Code", "Word", "Terminal", "Excel", "PowerPoint"]
DISTRACTION_APPS = ["YouTube", "Netflix", "Spotify", "Discord", "Safari", "Photos", "Messages"]

def classify_app(app_title):
    for app in WORK_APPS:
        if app.lower() in app_title.lower():
            return "Work"
    for app in DISTRACTION_APPS:
        if app.lower() in app_title.lower():
            return "Distraction"
    return "Neutral"

def compute_metrics(df):
    total = len(df)
    if total == 0:
        return None

    idle_ratio = (df["status"] == "Idle").sum() / total
    distraction_ratio = (df["app class"] == "Distraction").sum() / total
    switch_rate = (df["active window"] != df["active window"].shift(1)).sum() / total
    avg_score = df["score"].mean()

    return {
        "idle": idle_ratio,
        "distraction": distraction_ratio,
        "switching": switch_rate,
        "score": avg_score
    }

def show_alert(changes):
    msg = "\n".join(changes)
    subprocess.run([
        "osascript", "-e",
        f'display notification "{msg}" with title \"LoopBreak Daily Shift Detected\"'
    ])
    print("⚠️ Significant change detected:\n" + msg)

def compare_scores(file_path=LOG_FILE):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    df = pd.read_csv(file_path)
    if 'Score' not in df.columns or 'Timestamp' not in df.columns:
        print("Required columns 'Score' or 'Timestamp' not found.")
        return

    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=["Timestamp"])
    df['Date'] = df['Timestamp'].dt.date

    daily_scores = df.groupby('Date')['Score'].mean()

    print("\n📊 Daily Average Productivity Scores:")
    print(daily_scores)

    delta = daily_scores.diff()
    if not delta.empty:
        print("\n🔍 Score Changes Compared to Previous Day:")
        print(delta)

        max_increase = delta.idxmax()
        max_drop = delta.idxmin()
        print(f"\n📈 Highest Increase: {delta[max_increase]:.2f} on {max_increase}")
        print(f"📉 Highest Drop   : {delta[max_drop]:.2f} on {max_drop}")

def run_comparison():
    try:
        df = pd.read_csv(LOG_FILE)
        df.columns = [c.strip().lower() for c in df.columns]
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
        df = df.dropna(subset=["timestamp"])
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    df["app class"] = df["active window"].apply(classify_app)

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    df_today = df[df["timestamp"] >= today]
    df_past = df[df["timestamp"] < today]
    df_past = df_past[df_past["timestamp"] >= today - timedelta(days=7)]

    today_metrics = compute_metrics(df_today)
    past_metrics = compute_metrics(df_past)

    if not today_metrics or not past_metrics:
        print("Not enough data to compare.")
        return

    alerts = []
    for key in today_metrics:
        current = today_metrics[key]
        baseline = past_metrics[key]
        delta = current - baseline

        if key == "score":
            if delta < -THRESHOLDS["score"] * baseline:
                alerts.append(f"⬇ Productivity score dropped {abs(delta):.1%}")
        else:
            if delta > THRESHOLDS[key] * baseline:
                alerts.append(f"⬆ {key.capitalize()} increased by {delta:.1%}")

    if alerts:
        show_alert(alerts)
    else:
        print("✅ No significant behavioral changes detected today.")

    # Add daily score comparison at the end
    compare_scores()

if __name__ == "__main__":
    run_comparison()