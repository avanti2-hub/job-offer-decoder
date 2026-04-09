from openenv.core import EnvClient, SyncEnvClient
from models import JobOfferAction, JobOfferObservation, JobOfferState


class JobOfferDecoderEnv(EnvClient):

    def _step_payload(self, action: JobOfferAction) -> dict:
        return {
            "analysis": action.analysis,
            "task_type": action.task_type,
        }

    def _parse_result(self, payload: dict) -> JobOfferObservation:
        return JobOfferObservation(
            done=payload.get("done", False),
            reward=payload.get("reward"),
            offer_text=payload.get("offer_text", ""),
            task_type=payload.get("task_type", ""),
            instructions=payload.get("instructions", ""),
            difficulty=payload.get("difficulty", ""),
        )

    def _parse_state(self, payload: dict) -> JobOfferState:
        return JobOfferState(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
            task_type=payload.get("task_type", ""),
            difficulty=payload.get("difficulty", ""),
        )