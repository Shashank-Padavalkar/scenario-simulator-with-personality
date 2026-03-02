from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os 

app = FastAPI(title="Scenario Simulator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

from backend.models.schemas import ScenarioRequest, ScenarioResponse
from backend.services.gemini_service import simulate_scenario

@app.post("/simulate", response_model=ScenarioResponse)
def simulate_endpoint(request: ScenarioRequest):
    return simulate_scenario(request.scenario, request.category)

# Mount frontend directory for static serving if it exists
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
