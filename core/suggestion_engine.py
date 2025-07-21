import pandas as pd
import subprocess
import os
from datetime import datetime, timedelta

BURNOUT_LOG = "burnout_log.csv"
FEEDBACK_FILE = "feedback_log.csv"

def generate_suggestion():
    suggestions = []

    # Check burnout log
    if os.path.exists(BURNOUT_LOG):
        try:
            df_burn = pd.read_csv(BURNOUT_LOG)
            df_burn["timestamp"] = pd.to_datetime(df_burn["timestamp"], errors="coerce")
            recent = df_burn[df_burn["timestamp"] >= datetime.now() - timedelta(days=5)]

            if not recent.empty:
                avg_score = recent["burnout_index"].mean()
                high_burn = (recent["status"] == "🔴 High").sum()

                if avg_score < 60:
                    suggestions.append("🛑 Consider blocking time for focused deep work.")
                if high_burn >= 3:
                    suggestions.append("🚨 You’ve had several high-burnout days. Schedule a break.")
        except Exception as e:
            print("Error reading burnout log:", e)

    # Check subjective feedback
    if os.path.exists(FEEDBACK_FILE):
        try:
            df_feed = pd.read_csv(FEEDBACK_FILE)
            df_feed["timestamp"] = pd.to_datetime(df_feed["timestamp"], errors="coerce")
            recent = df_feed[df_feed["timestamp"] >= datetime.now() - timedelta(days=5)]

            if not recent.empty:
                avg_mental = df_feed["mental_clarity (1-10)"].mean()
                avg_stress = df_feed["stress_level (1-10)"].mean()

                if avg_mental <= 4:
                    suggestions.append("💡 Try a mindfulness or breathing exercise.")
                if avg_stress >= 7:
                    suggestions.append("😵 High stress reported. Step away from screen for 10 min.")
        except Exception as e:
            print("Error reading feedback file:", e)

    # Final output
    if suggestions:
        message = suggestions[0]  # Choose the most critical
        subprocess.run([
            "osascript", "-e",
            f'display notification "{message}" with title \\"LoopBreak Suggestion\\"'
        ])
        print("✅ Suggestion generated:", message)
    else:
        print("📘 No suggestions needed. You're doing fine!")

if __name__ == "__main__":
    generate_suggestion()