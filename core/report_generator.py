import os
import csv
import pandas as pd
import subprocess
from datetime import datetime, timedelta
from fpdf import FPDF

# ---------- Config ----------
LOG_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/app_usage_log.csv"
BURNOUT_LOG = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/burnout_log.csv"
PDF_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/weekly_burnout_behavior_report.pdf"

WORK_APPS = ["Chrome", "VS Code", "Terminal", "Word", "Excel", "PowerPoint"]
DISTRACTION_APPS = ["YouTube", "Netflix", "Spotify", "Discord", "Safari", "Messages", "Photos"]

# ---------- App Classification ----------
def classify_app(app_title):
    for app in WORK_APPS:
        if isinstance(app_title, str) and app.lower() in app_title.lower():
            return "Work"
    for app in DISTRACTION_APPS:
        if isinstance(app_title, str) and app.lower() in app_title.lower():
            return "Distraction"
    return "Neutral"

# ---------- Hourly Summary ----------
def generate_hourly_summary():
    try:
        df = pd.read_csv(LOG_FILE, parse_dates=["timestamp"])
    except Exception as e:
        print(f"❌ Error reading app usage log: {e}")
        return

    one_hour_ago = datetime.now() - timedelta(hours=1)
    df = df[df["timestamp"] >= one_hour_ago]

    if df.empty:
        print("ℹ️ No data available for the last hour.")
        return

    avg_score = df["score"].mean() * 100
    active_time = (df["status"] == "Active").sum() * 5
    idle_time = (df["status"] == "Idle").sum() * 5
    top_category = df["active window"].apply(classify_app).value_counts().idxmax()

    message = (
        f"Productivity: {avg_score:.1f}/100\n"
        f"Active: {active_time} min | Idle: {idle_time} min\n"
        f"Mostly used: {top_category}"
    )
    subprocess.run([
        "osascript", "-e", f'display notification "{message}" with title \\"LoopBreak Hourly Summary\\"'
    ])
    print("✅ Hourly summary notification sent.")

# ---------- Daily Comparison ----------
def compare_scores():
    try:
        df = pd.read_csv(LOG_FILE)
        df.columns = df.columns.str.strip().str.lower()
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
        df = df.dropna(subset=["timestamp"])
    except Exception as e:
        print(f"❌ Error reading app usage log: {e}")
        return

    df["app class"] = df["active window"].apply(classify_app)

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    df_today = df[df["timestamp"] >= today]
    df_past = df[(df["timestamp"] < today) & (df["timestamp"] >= today - timedelta(days=7))]

    def metrics(data):
        total = len(data)
        if total == 0:
            return None
        return {
            "idle": (data["status"] == "Idle").sum() / total,
            "distraction": (data["app class"] == "Distraction").sum() / total,
            "switching": (data["active window"] != data["active window"].shift(1)).sum() / total,
            "score": data["score"].mean()
        }

    t_metrics = metrics(df_today)
    p_metrics = metrics(df_past)

    if not t_metrics or not p_metrics:
        print("⚠️ Not enough data to compare daily scores.")
        return

    msg = []
    if (t_metrics["score"] - p_metrics["score"]) < -0.15 * p_metrics["score"]:
        msg.append("⬇ Productivity score dropped.")
    if (t_metrics["idle"] - p_metrics["idle"]) > 0.2 * p_metrics["idle"]:
        msg.append("⬆ Idle time increased.")
    if (t_metrics["distraction"] - p_metrics["distraction"]) > 0.2 * p_metrics["distraction"]:
        msg.append("⬆ Distraction increased.")
    if (t_metrics["switching"] - p_metrics["switching"]) > 0.2 * p_metrics["switching"]:
        msg.append("⬆ Task switching increased.")

    if msg:
        summary = "\n".join(msg)
        subprocess.run([
            "osascript", "-e", f'display notification "{summary}" with title \\"LoopBreak Daily Report\\"'
        ])
        print("✅ Daily report notification sent.")
    else:
        print("✅ No significant daily changes detected.")

# ---------- Weekly PDF Burnout Report ----------
def generate_weekly_report():
    try:
        df = pd.read_csv(BURNOUT_LOG)
        df.columns = df.columns.str.strip().str.lower()
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df[df["timestamp"] >= datetime.now() - timedelta(days=7)]
    except Exception as e:
        print("❌ Could not load burnout log:", e)
        return

    if df.empty:
        print("⚠️ Not enough data for PDF report.")
        return

    avg_burnout = df["burnout_index"].mean()
    high_days = df["status"].str.contains("High", case=False, na=False).sum()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Weekly Burnout Report", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.ln(5)
    pdf.cell(0, 8, f"Average Burnout Index: {avg_burnout:.1f}", ln=True)
    pdf.cell(0, 8, f"Days with High Burnout: {high_days}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Recent Burnout Logs:", ln=True)
    pdf.set_font("Arial", "", 11)

    for _, row in df.tail(7).iterrows():
        status = row.get("status", "Unknown")
        status_clean = status.replace("🔴", "High").replace("🟡", "Medium").replace("🟢", "Low")
        timestamp = row.get("timestamp", "")
        date_label = timestamp.strftime("%b %d") if isinstance(timestamp, datetime) else "N/A"
        line = f"{date_label}: Index {row['burnout_index']} ({status_clean})"
        pdf.cell(0, 8, line, ln=True)

    try:
        pdf.output(PDF_FILE)
        print(f"📄 Weekly burnout report PDF saved to: {PDF_FILE}")
    except Exception as e:
        print("❌ Failed to save PDF:", e)

# ---------- Entry Point ----------
if __name__ == "__main__":
    print("📦 LoopBreak Report Generator\n")
    generate_hourly_summary()
    compare_scores()
    generate_weekly_report()
    print("✅ All reports executed.")