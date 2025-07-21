# athena_server.py
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Flask,request, jsonify, render_template_string
from core.burnout_score_report import generate_burnout_report
from core.trend_analyzer import analyze_trends
from core.burnout_forecaster import forecast_burnout
from core.suggestion_engine import generate_suggestion
from core.feedback_engine import generate_feedback_report
from core.self_assessment import run_self_assessment

app = Flask(__name__)

@app.route("/")
def home():
    with open("athena.html", "r", encoding="utf-8") as file:
        return render_template_string(file.read())

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form.get("query", "").lower()
    
    # === Command Routing ===
    if "burnout report" in query:
        generate_burnout_report()
        return jsonify(response="Burnout report generated.")
    
    elif "forecast" in query:
        forecast_burnout()
        return jsonify(response="Burnout forecast complete.")
    
    elif "trend" in query or "analyze" in query:
        analyze_trends()
        return jsonify(response="Trend analysis complete.")
    
    elif "suggest" in query:
        generate_suggestion()
        return jsonify(response="Suggestion generated.")
    
    elif "feedback" in query:
        generate_feedback_report(score=75, idle_ratio=0.3, distraction_ratio=0.2, switch_rate=0.15)
        return jsonify(response="Feedback summary generated.")

    elif "self assessment" in query:
        run_self_assessment()
        return jsonify(response="Self-assessment interface triggered.")

    else:
        return jsonify(response="Sorry, I didn't understand that. Try asking about 'burnout', 'forecast', or 'trends'.")

if __name__ == "__main__":
    app.run(debug=True, port=5000)