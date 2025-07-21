# core/goal_tracking.py

import csv
from datetime import datetime
import os

GOALS_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/goals_log.csv"
APP_USAGE_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/app_usage_log.csv"

CATEGORY_KEYWORDS = {
    "work": ["Chrome", "VS Code", "Terminal", "Excel", "PowerPoint"],
    "health": ["Fitbit", "Health", "Workout", "Apple Health"],
    "personal": ["Photos", "Spotify", "Messages", "Notes"]
}

# 🛠 Ensure goals_log.csv exists with headers
if not os.path.exists(GOALS_FILE):
    with open(GOALS_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "title", "category", "deadline", "status"])

def add_goal():
    print("\n🎯 Add New Goal")
    title = input("Goal title: ").strip()
    category = input("Category (e.g., Work, Health, Personal): ").strip().lower()
    deadline = input("Deadline (YYYY-MM-DD): ").strip()

    with open(GOALS_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), title, category, deadline, "incomplete"])

    print("✅ Goal added.\n")

def mark_goal_completed():
    title = input("Enter the title of the goal to mark complete: ").strip()
    updated = False

    rows = []
    with open(GOALS_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            if row and row[1].lower() == title.lower() and row[-1] == "incomplete":
                row[-1] = "complete"
                updated = True
            rows.append(row)

    if updated:
        with open(GOALS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)
        print("✅ Goal marked as complete.")
    else:
        print("⚠️ Goal not found or already completed.")

def get_latest_active_goal():
    if not os.path.exists(GOALS_FILE):
        return None

    with open(GOALS_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        goals = [row for row in reader if row and row[-1].strip().lower() == "incomplete"]

    return goals[-1] if goals else None

def get_app_alignment_status(goal_category):
    if not os.path.exists(APP_USAGE_FILE):
        print("⚠️ App usage log not found.")
        return

    matching_keywords = CATEGORY_KEYWORDS.get(goal_category.lower(), [])
    if not matching_keywords:
        print("⚠️ No defined keywords for this goal category.")
        return

    with open(APP_USAGE_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        total, aligned = 0, 0
        for row in reader:
            app = row.get("Active Window", "")
            if any(keyword.lower() in app.lower() for keyword in matching_keywords):
                aligned += 1
            total += 1

    if total == 0:
        print("📭 No app usage data found.")
        return

    alignment_percent = (aligned / total) * 100
    print(f"\n📊 App Usage Alignment with Goal: {alignment_percent:.2f}%")
    if alignment_percent > 70:
        print("✅ Strong alignment between goal and app usage.")
    elif alignment_percent > 40:
        print("⚠️ Moderate alignment. Some distractions present.")
    else:
        print("❌ Poor alignment. Likely distracted or off-goal.")

def check_app_alignment():
    latest_goal = get_latest_active_goal()
    if not latest_goal:
        print("⚠️ No active goals found.")
        return

    print(f"\n📌 Latest Active Goal: {latest_goal[1]} ({latest_goal[2].capitalize()})")
    get_app_alignment_status(latest_goal[2])

# ✅ Clean entry-point for imports
def track_goals():
    print("\n📋 Goal Tracking Options")
    print("1. Add Goal")
    print("2. Mark Goal as Complete")
    print("3. Check App Alignment")
    choice = input("Choose an option (1/2/3): ").strip()
    if choice == "1":
        add_goal()
    elif choice == "2":
        mark_goal_completed()
    elif choice == "3":
        check_app_alignment()
    else:
        print("❌ Invalid choice.")

# CLI launcher
if __name__ == "__main__":
    track_goals()