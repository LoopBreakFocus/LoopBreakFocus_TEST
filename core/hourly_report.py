import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF
import os

# ---------- Config ----------
LOG_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/app_usage_log.csv"
PDF_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/hourly_summary_report.pdf"

# ---------- App Classifier ----------
def classify_app(app_title):
    work_apps = ["Chrome", "Visual Studio Code", "VS Code", "Word", "Terminal", "Excel", "PowerPoint"]
    distraction_apps = ["YouTube", "Netflix", "Spotify", "Discord", "Safari", "Photos", "Messages"]

    app_title = str(app_title).lower()
    if any(w.lower() in app_title for w in work_apps):
        return "Work"
    elif any(d.lower() in app_title for d in distraction_apps):
        return "Distraction"
    return "Neutral"

# ---------- Hourly Summary ----------
def generate_hourly_summary():
    try:
        df = pd.read_csv(LOG_FILE)
        df.columns = df.columns.str.strip().str.lower()
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
        df = df.dropna(subset=["timestamp"])
    except Exception as e:
        print(f"❌ Error reading log file: {e}")
        return

    one_hour_ago = datetime.now() - timedelta(hours=1)
    recent_df = df[df["timestamp"] >= one_hour_ago]

    if recent_df.empty:
        print("ℹ️ No data available for the last hour.")
        return

    # Calculations
    avg_score = round(recent_df["score"].mean() * 100, 1)  # Convert from 0–1 scale to 0–100
    active_time = (recent_df["status"] == "Active").sum() * 5  # assuming log every 5 seconds
    idle_time = (recent_df["status"] == "Idle").sum() * 5
    app_classes = recent_df["active window"].apply(classify_app)
    top_category = app_classes.value_counts().idxmax()

    # Terminal Summary
    print("\n🕒 Hourly Productivity Summary")
    print(f"🧠 Productivity Score: {avg_score:.1f}/100")
    print(f"💼 Active Time: {active_time} min | 💤 Idle Time: {idle_time} min")
    print(f"📱 Most Used App Category: {top_category}")

    # PDF Report
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "LoopBreak Hourly Summary Report", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"Productivity Score: {avg_score:.1f}/100", ln=True)
    pdf.cell(0, 10, f"Active Time: {active_time} minutes", ln=True)
    pdf.cell(0, 10, f"Idle Time: {idle_time} minutes", ln=True)
    pdf.cell(0, 10, f"Most Used App Category: {top_category}", ln=True)

    try:
        pdf.output(PDF_FILE)
        print(f"📄 PDF generated at: {os.path.abspath(PDF_FILE)}")
    except Exception as e:
        print(f"❌ Failed to generate PDF: {e}")

# ---------- Run ----------
if __name__ == "__main__":
    generate_hourly_summary()