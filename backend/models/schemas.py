from pydantic import BaseModel
from typing import List, Optional

class ScenarioRequest(BaseModel):
    scenario: str
    category: Optional[str] = None

class ScenarioResponse(BaseModel):
    best_case: str
    worst_case: str
    most_likely: str
    risks: List[str]
    recommendations: List[str]
