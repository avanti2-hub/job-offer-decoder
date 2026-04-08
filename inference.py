"""
inference.py — Hackathon Submission
Job Offer Decoder — RL Environment
Follows required [START][STEP][END] stdout format
Uses OpenAI Client as required by hackathon rules
"""
import os
import sys

# Fix import paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "server"
))

from openai import OpenAI
from models import JobOfferAction
from job_offer_decoder_environment import JobOfferDecoderEnvironment

# ── Required environment variables ──────────────────
API_BASE_URL = os.environ.get(
    "API_BASE_URL",
    "https://api.openai.com/v1"
)
MODEL_NAME = os.environ.get(
    "MODEL_NAME",
    "gpt-4o-mini"
)
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# ── OpenAI client (required by hackathon) ───────────
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN or "dummy-key"
)


def ask_llm(context: str, instructions: str) -> str:
    """Call LLM using OpenAI client"""
    prompt = f"""You are an expert employment lawyer 
helping a fresher understand a job offer.

CONTEXT (Offer Letter / Current State):
{context}

YOUR CURRENT TASK:
{instructions}

Provide a detailed accurate response based on 
the text provided. Mention exact clause names, 
rupee amounts, durations, and Indian law references 
where applicable."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.0,
    )
    return response.choices[0].message.content


def run_episode(
    env: JobOfferDecoderEnvironment,
    benchmark_name: str,
    difficulty: str
) -> None:
    """Run one complete episode with [START][STEP][END] logging"""

    task_name = f"job_offer_decoder_{difficulty}"
    print(
        f"[START] task={task_name} "
        f"env={benchmark_name} "
        f"model={MODEL_NAME}"
    )

    # Force specific difficulty
    env._next_difficulty = difficulty
    obs = env.reset()

    step_num = 1
    rewards = []
    success = False

    try:
        while not obs.done:
            # Build context for LLM
            context = obs.offer_text if obs.offer_text \
                else "Continue analysis from previous steps."

            # Get LLM analysis
            analysis = ask_llm(context, obs.instructions)

            # Create action
            action = JobOfferAction(
                analysis=analysis,
                task_type=obs.task_type
            )

            # Step environment
            obs = env.step(action)

            reward = obs.reward \
                if obs.reward is not None else 0.0
            done_str = "true" if obs.done else "false"

            print(
                f"[STEP] step={step_num} "
                f"action=analyze_offer_letter "
                f"reward={reward:.2f} "
                f"done={done_str} "
                f"error=null"
            )
            rewards.append(f"{reward:.2f}")
            step_num += 1

        # Episode complete
        final_score = obs.reward \
            if obs.reward is not None else 0.0
        success = final_score > 0.0

    except Exception as e:
        error_msg = str(e).replace('\n', ' ')
        print(
            f"[STEP] step={step_num} "
            f"action=error "
            f"reward=0.00 "
            f"done=true "
            f"error=\"{error_msg}\""
        )
        if not rewards:
            rewards = ["0.00"]
        print(
            f"[END] success=false "
            f"steps={step_num} "
            f"score=0.00 "
            f"rewards={','.join(rewards)}"
        )
        return

    if not rewards:
        rewards = ["0.00"]

    print(
        f"[END] success={str(success).lower()} "
        f"steps={step_num - 1} "
        f"score={final_score:.2f} "
        f"rewards={','.join(rewards)}"
    )


def main():
    env = JobOfferDecoderEnvironment()
    benchmark_name = "job_offer_decoder"
    difficulties = ["easy", "medium", "hard"]

    for difficulty in difficulties:
        run_episode(env, benchmark_name, difficulty)


if __name__ == "__main__":
    main()