from flask import Flask, jsonify, request
from anamoly_detector import detect_anomalies
from burnout_score_report import generate_burnout_score_report
from compare import compare_scores
from trend_analyzer import analyze_trends
from hourly_report import generate_hourly_summary
from self_assessment import log_self_assessment
from feedback_engine import collect_feedback
from goal_tracking import add_goal, mark_goal_completed, check_app_alignment
from report_generator import generate_weekly_report
from monitor import log_usage  # ✅ Use new entry point
from alert_engine import send_alert

import threading

app = Flask(__name__)

# ---------- MONITOR ----------
@app.route("/api/monitor", methods=["POST"])
def monitor():
    # Launch monitoring in background thread
    threading.Thread(target=log_usage, daemon=True).start()
    return jsonify({"status": "success", "message": "Monitoring started in background"}), 200

# ---------- BURNOUT ----------
@app.route("/api/burnout_score", methods=["GET"])
def burnout_score():
    generate_burnout_score_report()
    return jsonify({"status": "success", "message": "Burnout score report generated"}), 200

@app.route("/api/compare", methods=["GET"])
def compare_today_vs_past():
    compare_scores()
    return jsonify({"status": "success", "message": "Comparison completed"}), 200

@app.route("/api/trends", methods=["GET"])
def trends():
    analyze_trends()
    return jsonify({"status": "success", "message": "Trend analysis completed"}), 200

@app.route("/api/anomalies", methods=["GET"])
def anomalies():
    result = detect_anomalies("app_usage_log.csv")
    return jsonify({"status": "success", "message": result}), 200

@app.route("/api/hourly_report", methods=["GET"])
def hourly_report():
    generate_hourly_summary("app_usage_log.csv")
    return jsonify({"status": "success", "message": "Hourly report generated"}), 200

# ---------- SELF-ASSESSMENT ----------
@app.route("/api/self_assessment", methods=["POST"])
def self_assessment():
    log_self_assessment()
    return jsonify({"status": "success", "message": "Self-assessment logged"}), 200

# ---------- FEEDBACK ----------
@app.route("/api/feedback", methods=["POST"])
def feedback():
    collect_feedback()
    return jsonify({"status": "success", "message": "Feedback submitted"}), 200

# ---------- WEEKLY REPORT ----------
@app.route("/api/weekly_report", methods=["GET"])
def weekly_report():
    generate_weekly_report()
    return jsonify({"status": "success", "message": "Weekly burnout report PDF generated"}), 200

# ---------- GOALS ----------
@app.route("/api/goal/add", methods=["POST"])
def goal_add():
    add_goal()
    return jsonify({"status": "success", "message": "Goal added"}), 200

@app.route("/api/goal/complete", methods=["POST"])
def goal_complete():
    mark_goal_completed()
    return jsonify({"status": "success", "message": "Goal marked as complete"}), 200

@app.route("/api/goal/alignment", methods=["GET"])
def goal_alignment():
    check_app_alignment()
    return jsonify({"status": "success", "message": "Goal alignment checked"}), 200

# ---------- ALERT ----------
@app.route("/api/alert", methods=["POST"])
def manual_alert():
    send_alert()
    return jsonify({"status": "success", "message": "Alert triggered"}), 200

# ---------- MAIN ----------
if __name__ == "__main__":
    app.run(debug=True)