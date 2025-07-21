# core/feedback_engine.py

import csv
import subprocess
import os
from datetime import datetime
import random

FEEDBACK_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/feedback_log.csv"

# ---------- Save Daily Feedback ----------
def log_feedback(timestamp, mental_score, productivity_score, stress_level, goal_status, notes):
    file_exists = os.path.exists(FEEDBACK_FILE)
    headers = [
        "timestamp",
        "mental_clarity (1-10)",
        "productivity (1-10)",
        "stress_level (1-10)",
        "goals_completed (yes/no)",
        "notes"
    ]
    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow([timestamp, mental_score, productivity_score, stress_level, goal_status, notes])

# ---------- Nudging System ----------
def send_nudge(mental, productivity, stress, goals):
    messages = []

    if mental <= 4 or stress >= 7:
        messages.append("You seem overwhelmed. Try taking a short break.")
    elif productivity >= 8 and goals == "yes":
        messages.append("Great job today! You're staying focused.")
    elif productivity <= 4 and goals == "no":
        messages.append("Not your best day — tomorrow is a fresh start!")
    else:
        messages.append("Feedback logged. Keep tracking for better self-awareness.")

    for msg in messages:
        subprocess.run([
            "osascript", "-e",
            f'display notification "{msg}" with title \\"LoopBreak Feedback\\"'
        ])
        print("💬", msg)

# ---------- Main Feedback Collector ----------
def run_feedback_engine():
    print("\n🧠 LoopBreak Daily Feedback")

    try:
        mental = int(input("Mental clarity today (1-10): "))
        productivity = int(input("How productive did you feel (1-10): "))
        stress = int(input("Stress level (1-10): "))
        goals = input("Did you complete your planned goals? (yes/no): ").strip().lower()
        notes = input("Any notes you want to add: ").strip()
    except ValueError:
        print("❌ Invalid input. Please enter numbers for scores.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_feedback(timestamp, mental, productivity, stress, goals, notes)
    send_nudge(mental, productivity, stress, goals)
    print("✅ Feedback saved.\n")

# ---------- Productivity & Behavior Feedback ----------
def get_productivity_feedback(score):
    if score >= 85:
        return "🌟 Excellent focus! Keep up the great work!"
    elif score >= 70:
        return "👍 Good productivity. Try to minimize small distractions."
    elif score >= 50:
        return "⚠️ Average focus. Identify what's distracting you."
    else:
        return "❌ Low productivity. Take a break and reset your mind."

def get_behavior_feedback(idle_ratio, distraction_ratio, switch_rate):
    feedback = []
    if idle_ratio > 0.4:
        feedback.append("😴 High idle time. Consider short, scheduled breaks to stay active.")
    if distraction_ratio > 0.3:
        feedback.append("📱 You're spending a lot of time on distracting apps.")
    if switch_rate > 0.2:
        feedback.append("🔁 Frequent context switching detected.")
    if not feedback:
        feedback.append("✅ Great behavioral consistency.")
    return feedback

def generate_feedback_report(score, idle_ratio, distraction_ratio, switch_rate):
    print("\n📊 LoopBreak Feedback Report\n" + "-"*35)
    print(f"🧠 Productivity Score: {score}/100")
    print("🗨️  Overall Feedback:")
    print("  -", get_productivity_feedback(score))
    behavior_feedback = get_behavior_feedback(idle_ratio, distraction_ratio, switch_rate)
    print("🧠 Behavior Feedback:")
    for item in behavior_feedback:
        print("  -", item)
    print("-"*35 + "\n")

def show_popup_summary(score, idle_ratio, distraction_ratio):
    summary = get_productivity_feedback(score)
    if distraction_ratio > 0.4:
        summary += "\n🚫 High distraction time!"
    elif idle_ratio > 0.4:
        summary += "\n🕒 Long idle durations!"
    else:
        summary += "\n✅ You're on track!"
    subprocess.run([
        "osascript", "-e",
        f'display notification "{summary}" with title \\"LoopBreak Feedback\\"'
    ])

# ---------- Manual Test Mode ----------
if __name__ == "__main__":
    run_feedback_engine()
    test_score = random.randint(40, 95)
    generate_feedback_report(score=test_score, idle_ratio=0.32, distraction_ratio=0.21, switch_rate=0.19)
    show_popup_summary(test_score, 0.32, 0.21)