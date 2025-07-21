import csv
import time
import threading
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import subprocess
import psutil
import os

# ---------- Config ----------
LOG_DIR = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data"
LOG_FILE = os.path.join(LOG_DIR, "app_usage_log.csv")
TREND_ANALYSIS_INTERVAL = 3600  # Every hour
LOG_INTERVAL = 5               # Every 5 seconds

WORK_APPS = [
    "Chrome", "Visual Studio Code", "VS Code", "Code", "Terminal", "Word",
    "Excel", "PowerPoint", "ChatGPT", "Jupyter", "IntelliJ", "PyCharm", "Sublime", "Notion"
]
DISTRACTION_APPS = [
    "YouTube", "Netflix", "Spotify", "Discord", "Safari", "Photos", "Messages", "Reddit", "Twitter"
]

# ---------- Init ----------
def ensure_log_headers():
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "active window", "status", "cpu_usage", "score"])
        print("📝 Created new log file with headers.")

# ---------- Monitor ----------
def get_active_window_title():
    try:
        from AppKit import NSWorkspace
        app = NSWorkspace.sharedWorkspace().frontmostApplication()
        return app.localizedName()
    except Exception:
        return "Unknown"

def classify_app(title):
    if not isinstance(title, str):
        return "Neutral"
    title_lower = title.lower()
    if any(app.lower() in title_lower for app in WORK_APPS):
        return "Work"
    elif any(app.lower() in title_lower for app in DISTRACTION_APPS):
        return "Distraction"
    return "Neutral"

def get_status(cpu_usage):
    return "Idle" if cpu_usage < 5 else "Active"

def smooth_score(cpu, base_score, low=0.6, high=1.0):
    """ Smooth interpolation between two values """
    return round(low + (high - low) * ((cpu - 15) / (50 - 15)), 2)

def calculate_score(window, status, cpu_usage):
    classification = classify_app(window)

    if status == "Idle":
        return 0.3 if classification == "Work" else 0.1

    if classification == "Work":
        if cpu_usage <= 15:
            return round(0.6 + (cpu_usage / 15) * 0.2, 2)  # 0.6 to 0.8
        elif 15 < cpu_usage < 50:
            return smooth_score(cpu_usage, 1.0, 0.8, 0.95)  # Smooth from 0.8 to 0.95
        else:
            return 1.0

    elif classification == "Distraction":
        return round(0.3 + min(cpu_usage, 50) / 100 * 0.1, 2)  # 0.3 to 0.4 max

    elif classification == "Neutral":
        return round(0.5 + min(cpu_usage, 50) / 100 * 0.2, 2)  # 0.5 to 0.6 max

    return 0.4

# ---------- Logger ----------
def log_usage():
    ensure_log_headers()
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        while True:
            try:
                now = datetime.now()
                window = get_active_window_title()
                cpu_usage = psutil.cpu_percent(interval=1)
                status = get_status(cpu_usage)
                score = calculate_score(window, status, cpu_usage)
                classification = classify_app(window)

                writer.writerow([
                    now.strftime("%Y-%m-%d %H:%M:%S"),
                    window,
                    status,
                    round(cpu_usage, 1),
                    score
                ])
                file.flush()

                print(
                    f"[{now.strftime('%H:%M:%S')}] 🖥 App: {window:<25} | "
                    f"Class: {classification:<11} | Status: {status:<6} | "
                    f"CPU: {cpu_usage:>5.1f}% | Score: {score:.2f}"
                )
                time.sleep(LOG_INTERVAL)

            except KeyboardInterrupt:
                print("🛑 Monitoring stopped by user.")
                break
            except Exception as e:
                print("⚠️ Logging error:", e)
                time.sleep(LOG_INTERVAL)

# ---------- Trend Analyzer ----------
def detect_trend(series):
    if len(series) < 3:
        return "Not enough data"
    x = np.arange(len(series))
    slope = np.polyfit(x, series.values, 1)[0]
    if abs(slope) < 0.001:
        return "Stable"
    elif slope > 0.005:
        return "Upward"
    elif slope < -0.005:
        return "Downward"
    return "Volatile"

def show_popup(message):
    try:
        subprocess.run([
            "osascript", "-e",
            f'display notification "{message}" with title \\"LoopBreak Trend Alert\\"'
        ])
    except Exception as e:
        print("⚠️ Notification error:", e)
    print("🔔", message)

def analyze_trends():
    if not os.path.exists(LOG_FILE):
        print(f"❌ Log file not found: {LOG_FILE}")
        return

    try:
        df = pd.read_csv(LOG_FILE)
        df.columns = [c.strip().lower() for c in df.columns]
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
    except Exception as e:
        print(f"❌ Trend analysis failed: {e}")
        return

    df["app class"] = df["active window"].apply(classify_app)
    df["day"] = df["timestamp"].dt.date
    df = df[df["timestamp"] >= datetime.now() - timedelta(days=14)]

    grouped = df.groupby("day")
    trends_df = pd.DataFrame({
        "Idle Ratio": grouped["status"].apply(lambda x: (x == "Idle").sum() / len(x)),
        "Distraction Ratio": grouped["app class"].apply(lambda x: (x == "Distraction").sum() / len(x)),
        "Switching Rate": grouped["active window"].apply(lambda x: (x != x.shift(1)).sum() / len(x)),
        "Score": grouped["score"].mean()
    }).fillna(0)

    trends = {col: detect_trend(trends_df[col].tail(7)) for col in trends_df.columns}
    alerts = []

    if trends["Score"] == "Downward":
        alerts.append("⬇ Productivity is falling. Risk of burnout.")
    if trends["Idle Ratio"] == "Upward":
        alerts.append("⬆ Idle time rising. Possible disengagement.")
    if trends["Distraction Ratio"] == "Upward":
        alerts.append("⬆ Distractions increasing.")
    if trends["Score"] == "Upward":
        alerts.append("✅ Productivity improving!")
    if trends["Score"] == "Volatile":
        alerts.append("⚠️ Focus inconsistent. Review your routine.")

    show_popup("\n".join(alerts) if alerts else "✅ All behavioral trends are stable. Keep going!")

# ---------- Scheduler ----------
def trend_scheduler():
    while True:
        time.sleep(TREND_ANALYSIS_INTERVAL)
        print("⏳ Trend analysis running...")
        analyze_trends()

# ---------- Main ----------
if __name__ == "__main__":
    threading.Thread(target=trend_scheduler, daemon=True).start()
    log_usage()