import os

SHARED_DIR = "/app/shared_data"  # Inside container
files_to_reset = [
    "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/app_usage_log.csv",
    "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/burnout_log.csv",
    "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/feedback_log.csv",
    "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/self_assessment_log.csv",
    "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/goals_log.csv",
    "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/alert_log.csv"
]

for filename in files_to_reset:
    path = os.path.join(SHARED_DIR, filename)
    try:
        if os.path.exists(path):
            with open(path, "w") as f:
                f.write("")
            print(f"✅ Cleared {filename}")
        else:
            print(f"ℹ️ File not found: {filename}")
    except Exception as e:
        print(f"❌ Error resetting {filename}: {e}")