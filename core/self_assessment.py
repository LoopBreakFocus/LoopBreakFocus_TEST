# core/self_assessment.py

import csv
import os
from datetime import datetime
from core.suggestion_engine import generate_suggestion  # ✅ Import Suggestion Engine

SELF_ASSESSMENT_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/self_assessment_log.csv"
GOALS_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/goals_log.csv"

# Ensure CSV has headers
if not os.path.exists(SELF_ASSESSMENT_FILE):
    with open(SELF_ASSESSMENT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Timestamp", "Focus", "Motivation", "Mood", 
            "Energy Drain", "Self-rated Productivity", 
            "User Reported Goal Completion", "Goals Completed (Log)"
        ])

def get_completed_goals_today():
    today = datetime.now().strftime("%Y-%m-%d")
    count = 0
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header if present
            for row in reader:
                if len(row) >= 5:
                    date_str = row[0][:10]
                    if row[4].strip().lower() == "complete" and date_str == today:
                        count += 1
    return count

def run_self_assessment():
    print("\n🧠 Daily Self-Assessment (Rate 1-10)")

    try:
        focus = int(input("Focus: "))
        motivation = int(input("Motivation: "))
        mood = int(input("Mood: "))
        energy = int(input("How mentally drained did you feel today? "))
        productivity = int(input("How productive were you today? "))
        assert all(1 <= val <= 10 for val in [focus, motivation, mood, energy, productivity])
    except:
        print("⚠️ Please enter only numeric values between 1 and 10.")
        return

    goal_completed = input("Did you complete your planned goals? (yes/no): ").strip().lower()
    goals_completed_log = get_completed_goals_today()

    with open(SELF_ASSESSMENT_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            focus, motivation, mood, energy, productivity,
            goal_completed, goals_completed_log
        ])

    print("✅ Self-assessment logged.")

    # ✅ Trigger Suggestion Engine
    print("📡 Generating suggestions based on recent patterns...")
    generate_suggestion()
    print("✅ Suggestion analysis complete.\n")

if __name__ == "__main__":
    run_self_assessment()