from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.burnout_score_report import generate_burnout_report
from core.goal_tracking import track_goals
from core.suggestion_engine import generate_suggestion

app = FastAPI()

# Allow frontend to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # replace with ["http://localhost:5173"] in production
    allow_credentials=True,
    allow_methods=["http://localhost:5173"],
    allow_headers=["http://localhost:5173"],
)

@app.get("/api/burnout/{employee_id}")
def burnout(employee_id: str):
    return generate_burnout_report(employee_id)

@app.get("/api/goals/{employee_id}")
def goals(employee_id: str):
    return track_goals(employee_id)

@app.get("/api/suggestions/{employee_id}")
def suggestions(employee_id: str):
    return generate_suggestion(employee_id)