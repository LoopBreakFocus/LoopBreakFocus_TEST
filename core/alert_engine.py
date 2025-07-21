import pandas as pd
import subprocess
import os
from datetime import datetime, timedelta

# ---------- Config ----------
LOG_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/app_usage_log.csv"
ALERT_LOG = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/alert_log.csv"

# ---------- Thresholds ----------
THRESHOLDS = {
    "idle": 0.40,          # More than 40% idle
    "distraction": 0.35,   # More than 35% on distracting apps
    "switching": 0.20,     # More than 20% app switching
    "score": 0.50          # Productivity score below 50
}
COOLDOWN_MINUTES = 60  # Minimum interval between alerts

# ---------- App Classification ----------
DISTRACTION_APPS = ["YouTube", "Netflix", "Spotify", "Discord", "Safari", "Photos", "Messages"]

def classify_app(app_title):
    if isinstance(app_title, str):
        for app in DISTRACTION_APPS:
            if app.lower() in app_title.lower():
                return "Distraction"
    return "Neutral"

# ---------- Alert Display ----------
def send_alert(message):
    subprocess.run([
        "osascript", "-e",
        f'display notification "{message}" with title \\"LoopBreak Alert\\"'
    ])
    print("🚨", message)

# ---------- Alert Cooldown Logic ----------
def can_send_alert():
    if not os.path.exists(ALERT_LOG):
        return True
    try:
        df = pd.read_csv(ALERT_LOG)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        last_alert = df["timestamp"].max()
        return (datetime.now() - last_alert) > timedelta(minutes=COOLDOWN_MINUTES)
    except Exception:
        return True

def log_alert(message):
    os.makedirs(os.path.dirname(ALERT_LOG), exist_ok=True)
    file_exists = os.path.exists(ALERT_LOG)
    with open(ALERT_LOG, "a", newline="", encoding="utf-8") as file:
        pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message]]).to_csv(
            file, header=not file_exists, index=False
        )

# ---------- Alert Engine ----------
def run_alert_engine():
    try:
        df = pd.read_csv(LOG_FILE, usecols=["timestamp", "active window", "status", "cpu_usage", "score"])
        df.columns = [c.strip().lower() for c in df.columns]
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
        df = df.dropna(subset=["timestamp"])
    except Exception as e:
        print(f"Error reading log file: {e}")
        return

    # Focus on last 2 hours
    df = df[df["timestamp"] >= datetime.now() - timedelta(hours=2)]

    if df.empty:
        print("❌ No recent data for alert analysis.")
        return

    df["app class"] = df["active window"].apply(classify_app)

    total = len(df)
    idle_ratio = (df["status"] == "Idle").sum() / total
    distraction_ratio = (df["app class"] == "Distraction").sum() / total
    switching_ratio = (df["active window"] != df["active window"].shift(1)).sum() / total
    avg_score = df["score"].mean() / 100

    alerts = []
    if idle_ratio > THRESHOLDS["idle"]:
        alerts.append("High idle time detected.")
    if distraction_ratio > THRESHOLDS["distraction"]:
        alerts.append("You're spending too much time on distractions.")
    if switching_ratio > THRESHOLDS["switching"]:
        alerts.append("Frequent app switching noted.")
    if avg_score < THRESHOLDS["score"]:
        alerts.append("Your productivity score is low.")

    if alerts and can_send_alert():
        summary = "\n".join(alerts)
        send_alert(summary)
        log_alert(summary)
    else:
        print("✅ No alert triggered or cooldown active.")

# ---------- Run ----------
if __name__ == "__main__":
    run_alert_engine()