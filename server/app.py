import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from models import JobOfferAction, JobOfferObservation
from job_offer_decoder_environment import JobOfferDecoderEnvironment
import uvicorn

app = FastAPI(title="Job Offer Decoder Environment")
env = JobOfferDecoderEnvironment()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "offer_text": obs.offer_text,
        "task_type": obs.task_type,
        "instructions": obs.instructions,
        "difficulty": obs.difficulty,
        "done": obs.done,
        "reward": obs.reward,
    }


@app.post("/step")
def step(action: JobOfferAction):
    obs = env.step(action)
    return {
        "offer_text": obs.offer_text,
        "task_type": obs.task_type,
        "instructions": obs.instructions,
        "difficulty": obs.difficulty,
        "done": obs.done,
        "reward": obs.reward,
    }


@app.get("/state")
def state():
    s = env.state
    return {
        "episode_id": s.episode_id,
        "step_count": s.step_count,
        "task_type": s.task_type,
        "difficulty": s.difficulty,
    }


def main():
    uvicorn.run(
        "server.app:app",
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", 7860)),
        workers=int(os.environ.get("WORKERS", 1)),
    )


if __name__ == "__main__":
    main()