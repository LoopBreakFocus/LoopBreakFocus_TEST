import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import subprocess
from datetime import datetime, timedelta
import os
from logger import log_event  # Adjust path if logger.py is elsewhere

LOG_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/app_usage_log.csv"
BURNOUT_LOG = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/burnout_log.csv"

WEIGHTS = {
    "idle": 0.25,
    "distraction": 0.25,
    "switching": 0.20,
    "score": 0.30
}

# ------------------ Classification ------------------
def classify_app(title):
    work = ["Chrome", "VS Code", "Terminal", "Word", "Excel"]
    distract = ["YouTube", "Netflix", "Spotify", "Discord"]
    if isinstance(title, str):
        if any(app.lower() in title.lower() for app in work):
            return "Work"
        elif any(app.lower() in title.lower() for app in distract):
            return "Distraction"
    return "Neutral"

# ------------------ Metrics ------------------
def normalize(value, ideal, tolerance, reverse=False):
    deviation = abs(value - ideal)
    score = max(0, 1 - deviation / tolerance)
    return 1 - score if reverse else score

def calculate_metrics(df):
    total = len(df)
    if total == 0:
        return None
    idle_ratio = (df["status"].str.lower() == "idle").sum() / total
    distraction_ratio = (df["app class"] == "Distraction").sum() / total
    switch_rate = (df["active window"] != df["active window"].shift(1)).sum() / total
    avg_score = df["score"].mean() / 100 if "score" in df.columns else 0.0
    return idle_ratio, distraction_ratio, switch_rate, avg_score

def calculate_burnout_index(idle, distraction, switch, score):
    norm_idle = normalize(idle, 0.15, 0.20, reverse=True)
    norm_distraction = normalize(distraction, 0.10, 0.15, reverse=True)
    norm_switch = normalize(switch, 0.10, 0.10, reverse=True)
    norm_score = normalize(score, 0.80, 0.25)

    burnout_score = 100 * (
        norm_idle * WEIGHTS["idle"] +
        norm_distraction * WEIGHTS["distraction"] +
        norm_switch * WEIGHTS["switching"] +
        norm_score * WEIGHTS["score"]
    )

    if burnout_score >= 75:
        status = "🟢 Low"
    elif burnout_score >= 50:
        status = "🟡 Medium"
    else:
        status = "🔴 High"

    return round(burnout_score, 1), status

# ------------------ Alert & Report ------------------
def check_alerts(idle, distraction, switch, score):
    alerts = []
    if idle > 0.4:
        alerts.append("⚠️ High idle time")
    if distraction > 0.35:
        alerts.append("⚠️ High distraction")
    if switch > 0.20:
        alerts.append("⚠️ Frequent task switching")
    if score < 0.5:
        alerts.append("⚠️ Low productivity score")
    return alerts

def show_popup(score, status, alerts):
    lines = [f"Burnout Index: {score} ({status})"] + alerts
    message = "\n".join(lines)
    try:
        subprocess.run([
            "osascript", "-e",
            f'display notification "{message}" with title \\"LoopBreak Burnout Report\\"'
        ])
    except Exception as e:
        print(f"Popup failed: {e}")
    print(message)

def log_to_csv(timestamp, idle, distraction, switch, score, burnout_score, status):
    row = [timestamp, round(idle, 3), round(distraction, 3), round(switch, 3), round(score * 100, 1), burnout_score, status]
    headers = ["timestamp", "idle_ratio", "distraction_ratio", "switch_rate", "productivity_score", "burnout_index", "status"]
    file_exists = os.path.isfile(BURNOUT_LOG)
    with open(BURNOUT_LOG, "a", newline="", encoding="utf-8") as f:
        if not file_exists:
            f.write(",".join(headers) + "\n")
        f.write(",".join(map(str, row)) + "\n")

# ------------------ Main Report Generator ------------------
def generate_burnout_report():
    try:
        df = pd.read_csv(LOG_FILE)
        df.columns = [col.strip().lower() for col in df.columns]

        if "timestamp" not in df.columns:
            raise ValueError("CSV is missing 'timestamp' column.")

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
        df["app class"] = df["active window"].apply(classify_app)
    except Exception as e:
        log_event(f"Failed to read log file: {e}", level="error")
        print(f"❌ Failed to read log file: {e}")
        return

    recent_df = df[df["timestamp"] >= datetime.now() - timedelta(hours=6)]
    metrics = calculate_metrics(recent_df)
    if not metrics:
        print("⚠️ Not enough recent data.")
        return

    idle, distraction, switch, avg_score = metrics
    burnout_score, status = calculate_burnout_index(idle, distraction, switch, avg_score)
    alerts = check_alerts(idle, distraction, switch, avg_score)
    show_popup(burnout_score, status, alerts)

    log_to_csv(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), idle, distraction, switch, avg_score, burnout_score, status)
    log_event("Burnout score calculated successfully.")

if __name__ == "__main__":
    generate_burnout_report()