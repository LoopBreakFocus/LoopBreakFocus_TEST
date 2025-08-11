from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LoopBreak Central Server")

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "LoopBreak Central Server is running"}

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# TODO:
# - Add authentication (JWT)
# - Connect to DB
# - Add endpoints for Employee & HR frontends
# - Integrate backend processing functions
