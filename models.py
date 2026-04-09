from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class JobOfferAction(BaseModel):
    analysis: str = ""
    task_type: str = ""


class JobOfferObservation(BaseModel):
    done: bool = False
    reward: Optional[float] = None
    offer_text: str = ""
    task_type: str = ""
    instructions: str = ""
    difficulty: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class JobOfferState(BaseModel):
    episode_id: Optional[str] = None
    step_count: int = 0
    task_type: str = ""
    difficulty: str = ""