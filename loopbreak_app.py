import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import threading
import time
import subprocess
import os
import sys

sys.path.append('/Users/VyomeshJoshi/Desktop/LoopBreakFocus/core')

# === Import Core Modules ===
from core.monitor import log_usage
from core.alert_engine import run_alert_engine
from core.anamoly_detector import detect_anomalies
from core.burnout_score_report import generate_burnout_report
from core.trend_analyzer import analyze_trends
from core.report_generator import generate_hourly_summary, compare_scores, generate_weekly_report
from core.hourly_report import generate_hourly_summary as hourly_summary
from core.self_assessment import run_self_assessment
from core.goal_tracking import track_goals
from core.suggestion_engine import generate_suggestion
from core.feedback_engine import run_feedback_engine

# === Paths ===
LOG_PATH = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/app_usage_log.csv"

# === Main Scheduler Function ===
def run_background_services():
    threading.Thread(target=log_usage, daemon=True).start()
    threading.Thread(target=analyze_trends, daemon=True).start()
    threading.Thread(target=run_feedback_engine, daemon=True).start()
    threading.Thread(target=track_goals, daemon=True).start()
    threading.Thread(target=run_alert_engine, daemon=True).start()

def run_periodic_tasks():
    while True:
        time.sleep(3600)  # Run every hour
        print("⏳ Hourly tasks triggered...")
        generate_hourly_summary()
        generate_burnout_report()
        run_self_assessment()
        generate_suggestion()
        detect_anomalies(LOG_PATH)
        compare_scores()

def run_weekly_tasks():
    while True:
        time.sleep(86400 * 7)
        print("📅 Weekly summary triggered...")
        generate_weekly_report()

# === Entrypoint ===
if __name__ == "__main__":
    print("🚀 LoopBreak is starting up...\n")

    run_background_services()

    # Periodic reporting
    threading.Thread(target=run_periodic_tasks, daemon=True).start()
    threading.Thread(target=run_weekly_tasks, daemon=True).start()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("🛑 LoopBreak stopped manually.")