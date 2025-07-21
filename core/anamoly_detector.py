import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# ---------- CONFIG ----------
LOG_FILE = "/Users/VyomeshJoshi/Desktop/LoopBreakFocus/shared_data/app_usage_log.csv"
OUTPUT_CSV = "anomaly_results.csv"
OUTPUT_PLOT = "anomaly_plot.png"

Z_THRESHOLD = 2.0  # Z-score threshold for anomaly detection

# ---------- DETECTION ----------
def detect_anomalies(file_path):
    print("🔍 Starting Z-Score Based Anomaly Detection...")

    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower()
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp", "score"])
    except Exception as e:
        print(f"❌ Failed to read or process file: {e}")
        return

    # Calculate Z-scores
    mean_score = df["score"].mean()
    std_score = df["score"].std()

    if std_score == 0 or np.isnan(std_score):
        print("❌ Not enough variation in scores for anomaly detection.")
        return

    df["z_score"] = (df["score"] - mean_score) / std_score
    df["anomaly"] = df["z_score"].apply(lambda z: -1 if abs(z) > Z_THRESHOLD else 1)

    # Save results
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"[✅] Anomaly detection complete. Results saved to '{OUTPUT_CSV}'.")

    # Show summary
    anomaly_data = df[df["anomaly"] == -1]
    if not anomaly_data.empty:
        print(f"\n⚠️  {len(anomaly_data)} anomalies detected in productivity score.")
        print(anomaly_data[["timestamp", "score", "z_score"]].sort_values(by="score").head(5).to_string(index=False))
        print(f"\n📊 Anomaly Score Range:\nMin: {anomaly_data['score'].min():.2f}, Max: {anomaly_data['score'].max():.2f}")
    else:
        print("✅ No significant anomalies found.")

    # Plot
    try:
        plt.figure(figsize=(12, 6))
        plt.plot(df[df["anomaly"] == 1]["timestamp"], df[df["anomaly"] == 1]["score"], label="Normal", alpha=0.6)
        plt.scatter(anomaly_data["timestamp"], anomaly_data["score"], color="red", label="Anomaly", s=40)
        plt.axhline(y=mean_score, color='gray', linestyle='--', label=f"Mean Score ({mean_score:.2f})")
        plt.title("Z-Score Based Anomaly Detection in Productivity Score")
        plt.xlabel("Timestamp")
        plt.ylabel("Productivity Score")
        plt.legend()
        plt.tight_layout()
        plt.savefig(OUTPUT_PLOT)
        print(f"📈 Plot saved to '{OUTPUT_PLOT}'.")
    except Exception as e:
        print(f"❌ Plotting failed: {e}")

# ---------- RUN ----------
if __name__ == "__main__":
    detect_anomalies(LOG_FILE)